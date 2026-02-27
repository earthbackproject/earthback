# Test a REAL Flux training step - loads model to GPU and does forward+backward
# This tests whether the actual training step fits in 12GB VRAM
# Run from: D:\AI\kohya_ss
# Usage: .\venv\Scripts\python.exe C:\users\adrxi\Earthback\test-real-step.py
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import sys
sys.path.insert(0, r"D:\AI\kohya_ss\sd-scripts")
sys.path.insert(0, r"D:\AI\kohya_ss\sd-scripts\library")

import torch
import time
import traceback
from pathlib import Path
from safetensors.torch import load_file

LOG = Path(r"C:\users\adrxi\Earthback\real-step-diagnostic.log")

def log(msg):
    print(msg, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def vram():
    free, total = torch.cuda.mem_get_info()
    return f"{round(free/1024**3,1)}/{round(total/1024**3,1)} GB"

log("=" * 60)
log("REAL FLUX TRAINING STEP TEST")
log("=" * 60)

try:
    log(f"GPU: {torch.cuda.get_device_name(0)}")
    log(f"VRAM: {vram()}")

    # Load Flux model using Kohya's loader
    log("\n[1/6] Loading Flux model via Kohya...")
    from library.utils import setup_logging
    setup_logging()
    from library import flux_utils

    t0 = time.time()
    ckpt_path = r"C:\AI\models\checkpoints\flux1-dev-fp8.safetensors"
    # Check actual function signature
    import inspect
    sig = inspect.signature(flux_utils.load_flow_model)
    log(f"  load_flow_model signature: {sig}")
    # Try passing just the path
    result = flux_utils.load_flow_model(ckpt_path, torch.bfloat16, "cpu")
    if isinstance(result, tuple):
        log(f"  Got tuple with {len(result)} elements: {[type(x).__name__ for x in result]}")
        model = result[1]
    else:
        model = result
    log(f"  Model type: {type(model).__name__}")
    log(f"  Loaded in {time.time()-t0:.0f}s, VRAM: {vram()}")

    # Move to GPU
    log("\n[2/6] Moving model to GPU...")
    model.to("cuda", dtype=torch.bfloat16)
    log(f"  On GPU, VRAM: {vram()}")

    # Enable gradient checkpointing
    log("\n[3/6] Enabling gradient checkpointing...")
    model.enable_gradient_checkpointing()
    log(f"  Enabled, VRAM: {vram()}")

    # Create fake latent input (512x512 to be safe)
    log("\n[4/6] Creating test inputs (512x512)...")
    batch_size = 1
    latent_h, latent_w = 64, 64  # 512x512 in latent space (8x downscale)
    channels = 16  # Flux uses 16 latent channels

    # Pack latents like Flux expects
    noisy_latents = torch.randn(batch_size, channels, latent_h, latent_w,
                                 device="cuda", dtype=torch.bfloat16)

    # Fake text embeddings
    text_embed = torch.randn(batch_size, 512, 4096, device="cuda", dtype=torch.bfloat16)  # T5
    pooled = torch.randn(batch_size, 768, device="cuda", dtype=torch.bfloat16)  # CLIP-L

    # Timestep
    timesteps = torch.tensor([0.5], device="cuda", dtype=torch.bfloat16)

    log(f"  Inputs created, VRAM: {vram()}")

    # Forward pass
    log("\n[5/6] Forward pass...")
    t0 = time.time()
    model.train()
    try:
        # Try the simplest possible forward call
        # Flux models take: img, img_ids, txt, txt_ids, timesteps, y (pooled), guidance
        from library.flux_models import get_packed_latent_ids
        import torch.nn.functional as F

        # Reshape for Flux (pack into sequence)
        h_tokens = latent_h // 2
        w_tokens = latent_w // 2
        img = noisy_latents.reshape(batch_size, channels, h_tokens, 2, w_tokens, 2)
        img = img.permute(0, 2, 4, 3, 5, 1).reshape(batch_size, h_tokens * w_tokens, channels * 4)

        img_ids = torch.zeros(h_tokens, w_tokens, 3, device="cuda")
        for i in range(h_tokens):
            for j in range(w_tokens):
                img_ids[i, j] = torch.tensor([0, i, j])
        img_ids = img_ids.reshape(1, h_tokens * w_tokens, 3).expand(batch_size, -1, -1)

        txt_ids = torch.zeros(batch_size, 512, 3, device="cuda")

        guidance_vec = torch.full((batch_size,), 1.0, device="cuda", dtype=torch.bfloat16)

        log(f"  Shapes: img={img.shape}, txt={text_embed.shape}, t={timesteps.shape}")
        log(f"  Pre-forward VRAM: {vram()}")

        with torch.cuda.amp.autocast(dtype=torch.bfloat16):
            output = model(
                img=img,
                img_ids=img_ids,
                txt=text_embed,
                txt_ids=txt_ids,
                timesteps=timesteps,
                y=pooled,
                guidance=guidance_vec,
            )
        log(f"  Forward OK in {time.time()-t0:.1f}s! Output: {output.shape}")
        log(f"  Post-forward VRAM: {vram()}")

    except Exception as e:
        log(f"  Forward pass failed: {e}")
        log(traceback.format_exc())
        log(f"  VRAM at failure: {vram()}")
        raise

    # Backward pass
    log("\n[6/6] Backward pass...")
    t0 = time.time()
    try:
        loss = output.sum()
        loss.backward()
        log(f"  Backward OK in {time.time()-t0:.1f}s! Loss: {loss.item():.4f}")
        log(f"  Post-backward VRAM: {vram()}")
    except Exception as e:
        log(f"  Backward pass failed: {e}")
        log(traceback.format_exc())
        log(f"  VRAM at failure: {vram()}")
        raise

    log("\n" + "=" * 60)
    log("REAL TRAINING STEP TEST PASSED!")
    log("The model CAN do forward+backward on your GPU.")
    log("=" * 60)

except torch.cuda.OutOfMemoryError as e:
    log(f"\n!!! OUT OF MEMORY !!!")
    log(f"VRAM: {vram()}")
    log(f"The model does NOT fit in 12GB at this resolution.")
    log(f"Options: use fp8 throughout, reduce resolution, or use CPU offloading.")

except Exception as e:
    log(f"\n!!! FAILED !!!")
    log(f"Error type: {type(e).__name__}")
    log(f"Error: {e}")
    log(traceback.format_exc())

log(f"\nLog saved to: {LOG}")
input("Press Enter to exit...")
