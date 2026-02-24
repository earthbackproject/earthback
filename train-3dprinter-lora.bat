@echo off
:: ============================================================
:: train-3dprinter-lora.bat
:: Kohya SS LoRA training — 3D printer hardware (object LoRA)
::
:: Before running:
::   1. python collect-3dprinter-images.py  (need API keys)
::   2. python curate-3dprinter-images.py --review
::   3. python caption-3dprinter-images.py
::   4. Edit KOHYA_PATH below if needed
::   5. Run this bat
:: ============================================================

:: ─── Paths (edit if yours differ) ──────────────────────────
set KOHYA_PATH=D:\AI\kohya_ss
set PYTHON=D:\AI\comfy-env\Scripts\python.exe
set DATASET=C:\users\adrxi\Earthback\dataset-3dprinter\curated
set OUTPUT=C:\users\adrxi\Earthback\lora-output\3dprinter
set BASE_MODEL=D:\AI\ComfyUI\models\checkpoints\flux1-dev.safetensors
set CLIP_L=D:\AI\ComfyUI\models\clip\clip_l.safetensors
set T5=D:\AI\ComfyUI\models\clip\t5xxl_fp16.safetensors
set VAE=D:\AI\ComfyUI\models\vae\ae.safetensors

:: ─── Training settings ─────────────────────────────────────
:: Object LoRA — no trigger word (teach the category, not a specific switch)
:: If you want a trigger word, add --caption_extension .txt is already set
:: and prepend EB3DPRINTER to captions via:
::   python caption-3dprinter-images.py --trigger EB3DPRINTER --overwrite

set STEPS=1500
set RANK=16
set ALPHA=16
set LR=0.0001
set BATCH=1
set SAVE_EVERY=500

:: ─── Dataset repeat ────────────────────────────────────────
:: Kohya expects: dataset/<N>_<caption_text>/images
:: OR: use metadata json approach.
:: Simpler: put all curated images in a single repeats folder.
:: We create the expected structure here.

set TRAIN_DIR=C:\users\adrxi\Earthback\dataset-3dprinter\train_ready

echo.
echo ============================================================
echo  3D Printer LoRA Training
echo  Steps: %STEPS%  Rank: %RANK%  LR: %LR%
echo ============================================================
echo.

:: Create output dirs
if not exist "%OUTPUT%" mkdir "%OUTPUT%"
if not exist "%TRAIN_DIR%\10_3dprinter" mkdir "%TRAIN_DIR%\10_3dprinter"

:: Copy curated images + captions to train_ready structure
echo Preparing dataset structure...
xcopy /Y /Q "%DATASET%\curated_*.jpg" "%TRAIN_DIR%\10_3dprinter\"
xcopy /Y /Q "%DATASET%\curated_*.txt" "%TRAIN_DIR%\10_3dprinter\"
echo Done.
echo.

:: ─── Run training ──────────────────────────────────────────
cd /d %KOHYA_PATH%

%PYTHON% flux_train_network.py ^
  --pretrained_model_name_or_path="%BASE_MODEL%" ^
  --clip_l="%CLIP_L%" ^
  --t5xxl="%T5%" ^
  --ae="%VAE%" ^
  --train_data_dir="%TRAIN_DIR%" ^
  --output_dir="%OUTPUT%" ^
  --output_name="3dprinter-lora-v1" ^
  --caption_extension=".txt" ^
  --resolution="1024,1024" ^
  --train_batch_size=%BATCH% ^
  --max_train_steps=%STEPS% ^
  --save_every_n_steps=%SAVE_EVERY% ^
  --save_model_as=safetensors ^
  --network_module=networks.lora_flux ^
  --network_dim=%RANK% ^
  --network_alpha=%ALPHA% ^
  --optimizer_type=AdamW8bit ^
  --learning_rate=%LR% ^
  --lr_scheduler=cosine_with_restarts ^
  --lr_warmup_steps=100 ^
  --mixed_precision=bf16 ^
  --guidance_scale=1.0 ^
  --timestep_sampling=shift ^
  --discrete_flow_shift=3.1582 ^
  --model_prediction_type=raw ^
  --loss_type=l2 ^
  --seed=42 ^
  --logging_dir="%OUTPUT%\logs" ^
  --log_prefix="3dprinter"

echo.
echo ============================================================
echo  Training complete.
echo  Output: %OUTPUT%
echo.
echo  Test in ComfyUI with prompts like:
echo    a desktop FDM 3D printer, actively printing, warm workshop lighting
echo    a desktop FDM Cartesian 3D printer, idle, studio lighting
echo.
echo  Evaluate at step checkpoints: 500, 1000, 1500
echo  Look for: correct gantry shape, extruder position, filament path
echo ============================================================

pause
