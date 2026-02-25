@echo off
:: ============================================================
:: train-hempcrete-lora.bat
:: Kohya SS LoRA training — Hempcrete material + construction
::
:: Before running:
::   1. python collect-hempcrete-images.py --source wikimedia
::      python collect-hempcrete-images.py --pexels-key KEY --pixabay-key KEY
::   2. python curate-hempcrete-images.py --review
::      (manually reject off-target images — important for this dataset)
::   3. python caption-hempcrete-images.py
::   4. Run this bat
::
:: Trigger word: EBHEMPCRETE
::   Use in Flux prompts as: "EBHEMPCRETE hempcrete wall construction..."
::   Activate with low weight (0.7-1.0) for blended results
::   Activate with higher weight (1.2-1.5) for strong hempcrete material rendering
::
:: Evaluate at steps: 500, 1000, 1500
::   Look for: pale grey-green surface, visible hemp fibers in lime matrix,
::             rough porous texture, warm-cool color of cured lime, correct
::             formwork and construction process rendering
:: ============================================================

:: ─── Paths ──────────────────────────────────────────────────
set KOHYA_PATH=D:\AI\kohya_ss
set PYTHON=D:\AI\comfy-env\Scripts\python.exe
set DATASET=C:\users\adrxi\Earthback\dataset-hempcrete\curated
set OUTPUT=C:\users\adrxi\Earthback\lora-output\hempcrete
set BASE_MODEL=D:\AI\ComfyUI\models\checkpoints\flux1-dev.safetensors
set CLIP_L=D:\AI\ComfyUI\models\clip\clip_l.safetensors
set T5=D:\AI\ComfyUI\models\clip\t5xxl_fp16.safetensors
set VAE=D:\AI\ComfyUI\models\vae\ae.safetensors

:: ─── Training settings ──────────────────────────────────────
:: Material/texture LoRA — hempcrete is visually subtle
:: Lower rank than 3D printer (less structural complexity, more texture)
:: Steps: 1000-1500 depending on dataset size
:: If dataset < 80 images, reduce steps to 1000 to avoid overfitting

set STEPS=1500
set RANK=16
set ALPHA=8
set LR=0.00008
set BATCH=1
set SAVE_EVERY=500

:: ─── Dataset structure ──────────────────────────────────────
set TRAIN_DIR=C:\users\adrxi\Earthback\dataset-hempcrete\train_ready

echo.
echo ============================================================
echo  Hempcrete LoRA Training
echo  Steps: %STEPS%  Rank: %RANK%  Alpha: %ALPHA%  LR: %LR%
echo  Trigger word: EBHEMPCRETE
echo ============================================================
echo.

:: Create output dirs
if not exist "%OUTPUT%" mkdir "%OUTPUT%"
if not exist "%TRAIN_DIR%\10_hempcrete" mkdir "%TRAIN_DIR%\10_hempcrete"

:: Copy curated images + captions to train_ready structure
echo Preparing dataset structure...
xcopy /Y /Q "%DATASET%\curated_*.jpg" "%TRAIN_DIR%\10_hempcrete\"
xcopy /Y /Q "%DATASET%\curated_*.txt" "%TRAIN_DIR%\10_hempcrete\"
echo Done.
echo.

:: ─── Run training ───────────────────────────────────────────
cd /d %KOHYA_PATH%

%PYTHON% flux_train_network.py ^
  --pretrained_model_name_or_path="%BASE_MODEL%" ^
  --clip_l="%CLIP_L%" ^
  --t5xxl="%T5%" ^
  --ae="%VAE%" ^
  --train_data_dir="%TRAIN_DIR%" ^
  --output_dir="%OUTPUT%" ^
  --output_name="hempcrete-lora-v1" ^
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
  --log_prefix="hempcrete"

echo.
echo ============================================================
echo  Training complete.
echo  Output: %OUTPUT%
echo.
echo  Drop hempcrete-lora-v1.safetensors into:
echo    D:\AI\ComfyUI\models\loras\
echo.
echo  Test prompts (use LoRA weight 0.8-1.2):
echo    EBHEMPCRETE, hempcrete wall construction, timber formwork,
echo      hemp hurds visible in pale lime matrix, natural light
echo    EBHEMPCRETE, close-up hempcrete texture, rough grey-green
echo      surface, hemp fibers in cured lime binder, sidelight
echo    EBHEMPCRETE, hempcrete being mixed in barrel mixer, hemp
echo      hurd and hydraulic lime, construction site, afternoon
echo.
echo  Evaluate checkpoints at: 500, 1000, 1500
echo  Good signs: pale grey-green color, visible fiber texture,
echo              porous surface, correct mixing/formwork scenes
echo  Bad signs:  smooth white walls, generic concrete, clay color
echo ============================================================

pause
