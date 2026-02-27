@echo off
:: ============================================================
:: train-hempcrete-sdxl.bat
:: Kohya SS LoRA training — hempcrete material (SDXL)
::
:: Before running:
::   1. Dataset should already be prepared in train_ready\15_hempcrete\
::   2. DELETE any .npz cache files from previous Flux training:
::      del C:\users\adrxi\Earthback\dataset-hempcrete\train_ready\15_hempcrete\*.npz
::   3. Run this bat from any CMD window (no venv activation needed)
::
:: Trigger word: EBHEMPCRETE
:: ============================================================

:: ─── Paths ───────────────────────────────────────────────────
set KOHYA_PATH=D:\AI\kohya_ss
set PYTHON=D:\AI\kohya_ss\venv\Scripts\python.exe
set DATASET=C:\users\adrxi\Earthback\dataset-hempcrete\train_ready
set OUTPUT=C:\users\adrxi\Earthback\lora-output\hempcrete-sdxl
set BASE_MODEL=C:\AI\models\checkpoints\sdXL_v10VAEFix.safetensors

:: ─── Training settings ───────────────────────────────────────
:: RTX 3060 12GB — SDXL fits comfortably with gradient checkpointing
:: Rank 16, alpha 8 (alpha = rank/2 is standard for SDXL LoRA)
:: Expect ~2-5 seconds per step

set STEPS=1500
set RANK=16
set ALPHA=8
set LR=0.0001
set BATCH=1
set SAVE_EVERY=500
set RESOLUTION=1024

echo.
echo ============================================================
echo  Hempcrete SDXL LoRA Training
echo  Steps: %STEPS%  Rank: %RANK%  Alpha: %ALPHA%  LR: %LR%
echo  Resolution: %RESOLUTION%x%RESOLUTION%
echo  GPU: RTX 3060 12GB (gradient checkpointing ON)
echo  Trigger word: EBHEMPCRETE
echo ============================================================
echo.

:: Create output dir
if not exist "%OUTPUT%" mkdir "%OUTPUT%"

:: ─── Clean old Flux cache if present ────────────────────────
echo Checking for old Flux cache files...
if exist "%DATASET%\15_hempcrete\*_flux*.npz" (
    echo  Deleting old Flux .npz cache files...
    del /q "%DATASET%\15_hempcrete\*_flux*.npz"
    del /q "%DATASET%\15_hempcrete\*_flux_te*.npz"
    echo  Done.
) else (
    echo  No old cache files found.
)

:: ─── Force single GPU (bypass distributed) ───────────────────
set CUDA_VISIBLE_DEVICES=0
set ACCELERATE_USE_FSDP=false
set ACCELERATE_MIXED_PRECISION=bf16

:: ─── Run training ────────────────────────────────────────────
cd /d %KOHYA_PATH%\sd-scripts

%PYTHON% sdxl_train_network.py ^
  --pretrained_model_name_or_path="%BASE_MODEL%" ^
  --cache_latents ^
  --cache_latents_to_disk ^
  --cache_text_encoder_outputs ^
  --cache_text_encoder_outputs_to_disk ^
  --gradient_checkpointing ^
  --train_data_dir="%DATASET%" ^
  --output_dir="%OUTPUT%" ^
  --output_name="hempcrete-sdxl-v1" ^
  --caption_extension=".txt" ^
  --resolution="%RESOLUTION%" ^
  --enable_bucket ^
  --min_bucket_reso=512 ^
  --max_bucket_reso=1536 ^
  --train_batch_size=%BATCH% ^
  --max_train_steps=%STEPS% ^
  --save_every_n_steps=%SAVE_EVERY% ^
  --save_model_as=safetensors ^
  --network_train_unet_only ^
  --network_module=networks.lora ^
  --network_dim=%RANK% ^
  --network_alpha=%ALPHA% ^
  --optimizer_type=AdamW8bit ^
  --learning_rate=%LR% ^
  --lr_scheduler=cosine_with_restarts ^
  --lr_warmup_steps=100 ^
  --lr_scheduler_num_cycles=3 ^
  --mixed_precision=bf16 ^
  --loss_type=l2 ^
  --seed=42 ^
  --max_data_loader_n_workers=0 ^
  --logging_dir="%OUTPUT%\logs" ^
  --log_prefix="hempcrete-sdxl"

echo.
echo ============================================================
echo  Training complete!
echo  Output: %OUTPUT%
echo.
echo  Checkpoints saved at steps: 500, 1000, 1500
echo  Final: hempcrete-sdxl-v1.safetensors
echo.
echo  To test in ComfyUI:
echo    1. Copy hempcrete-sdxl-v1.safetensors to D:\AI\ComfyUI\models\loras\
echo    2. Switch checkpoint to sdXL_v10VAEFix.safetensors (NOT Flux!)
echo    3. Add LoRA Loader node, strength 0.7-0.9
echo    4. Use trigger: EBHEMPCRETE
echo.
echo  Test prompts:
echo    EBHEMPCRETE, hempcrete wall, warm golden-buff surface, visible hemp fiber
echo    EBHEMPCRETE, hempcrete construction, timber formwork, workers tamping
echo    EBHEMPCRETE, close-up hempcrete texture, hemp shiv in lime matrix
echo ============================================================

pause
