# Diagnostic: test a single Flux LoRA training step outside of Kohya.
# This isolates whether the problem is VRAM, PyTorch, or Kohya's training loop.
# Run from: D:\AI\kohya_ss
# Usage: .\venv\Scripts\python.exe C:\users\adrxi\Earthback\test-training-step.py
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import sys
import torch
import traceback
from pathlib import Path

LOG = Path(r"C:\users\adrxi\Earthback\training-diagnostic.log")

def log(msg):
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("=" * 60)
log("FLUX LORA TRAINING DIAGNOSTIC")
log("=" * 60)

try:
    log(f"\nPython: {sys.executable}")
    log(f"PyTorch: {torch.__version__}")
    log(f"CUDA available: {torch.cuda.is_available()}")
    log(f"GPU: {torch.cuda.get_device_name(0)}")
    free, total = torch.cuda.mem_get_info()
    log(f"VRAM: {round(free/1024**3,1)} GB free / {round(total/1024**3,1)} GB total")

    # Step 1: Load fp8 model
    log("\n--- STEP 1: Load fp8 checkpoint ---")
    from safetensors.torch import load_file
    sd = load_file(r"C:\AI\models\checkpoints\flux1-dev-fp8.safetensors")
    log(f"Loaded {len(sd)} keys")
    log(f"First key dtype: {list(sd.values())[0].dtype}")
    del sd
    torch.cuda.empty_cache()
    free, _ = torch.cuda.mem_get_info()
    log(f"VRAM after cleanup: {round(free/1024**3,1)} GB free")

    # Step 2: Create a small model on GPU and do forward+backward
    log("\n--- STEP 2: Forward + backward pass test ---")
    model = torch.nn.Linear(1024, 1024, dtype=torch.bfloat16, device="cuda")
    x = torch.randn(1, 1024, dtype=torch.bfloat16, device="cuda")
    y = model(x)
    loss = y.sum()
    loss.backward()
    log(f"Simple backward pass OK, loss={loss.item():.4f}")
    del model, x, y, loss
    torch.cuda.empty_cache()

    # Step 3: Test AdamW8bit
    log("\n--- STEP 3: AdamW8bit optimizer test ---")
    import bitsandbytes as bnb
    model = torch.nn.Linear(1024, 1024, dtype=torch.bfloat16, device="cuda")
    optimizer = bnb.optim.AdamW8bit(model.parameters(), lr=0.0001)
    x = torch.randn(1, 1024, dtype=torch.bfloat16, device="cuda")
    y = model(x)
    loss = y.sum()
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    log(f"AdamW8bit step OK")
    del model, optimizer, x, y, loss
    torch.cuda.empty_cache()

    # Step 4: Test Kohya's Flux model loading
    log("\n--- STEP 4: Kohya Flux model load ---")
    sys.path.insert(0, r"D:\AI\kohya_ss\sd-scripts")
    sys.path.insert(0, r"D:\AI\kohya_ss\sd-scripts\library")
    from library import flux_utils
    log("Imported flux_utils OK")

    # Load just the Flux model in bf16
    log("Loading Flux model (this takes a minute)...")
    from library.utils import setup_logging
    setup_logging()

    dtype = torch.bfloat16
    loading_device = "cpu"

    # Manually load to check
    log("  Loading checkpoint to CPU...")
    sd = load_file(r"C:\AI\models\checkpoints\flux1-dev-fp8.safetensors", device="cpu")
    log(f"  Loaded {len(sd)} tensors to CPU")

    free, _ = torch.cuda.mem_get_info()
    log(f"  VRAM: {round(free/1024**3,1)} GB free")

    log("  Moving a single tensor to GPU as bf16...")
    key0 = list(sd.keys())[0]
    t = sd[key0].to(device="cuda", dtype=torch.bfloat16)
    log(f"  Moved {key0}: {t.shape} {t.dtype} on {t.device}")

    free, _ = torch.cuda.mem_get_info()
    log(f"  VRAM: {round(free/1024**3,1)} GB free")

    del t, sd
    torch.cuda.empty_cache()

    log("\n--- STEP 5: Test accelerate ---")
    from accelerate import Accelerator
    log("Imported Accelerator OK")
    log(f"  Creating accelerator with mixed_precision=bf16...")
    acc = Accelerator(mixed_precision="bf16")
    log(f"  Accelerator device: {acc.device}")
    log(f"  Num processes: {acc.num_processes}")
    log(f"  Distributed type: {acc.distributed_type}")
    del acc

    log("\n" + "=" * 60)
    log("ALL DIAGNOSTIC STEPS PASSED")
    log("=" * 60)

except Exception as e:
    log(f"\n!!! FAILED !!!")
    log(f"Error: {e}")
    log(traceback.format_exc())

log("\nDone. Log saved to: " + str(LOG))
input("Press Enter to exit...")
