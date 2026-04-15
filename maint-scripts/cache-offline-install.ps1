<#
.SYNOPSIS
    Build an offline install cache for a full Earthback workstation rebuild.

.DESCRIPTION
    Gathers everything needed to rebuild the complete dev + AI environment
    without internet access. Run this on the CURRENT working machine.
    Output goes to D:\earthback-cache\ (or specify -CachePath).

    Caches: software installers, git repos, AI models, pip wheels,
    project scripts/configs/datasets, maintenance scripts.

    Total size: ~30-50 GB depending on models.

.PARAMETER CachePath
    Where to build the cache. Default: D:\earthback-cache

.PARAMETER SkipInstallers
    Skip downloading software installers (if you already have them).

.PARAMETER SkipModels
    Skip copying AI model files (largest part of the cache).

.PARAMETER SkipWheels
    Skip exporting pip wheel caches from venvs.

.NOTES
    Author : Claude (for Nicco)
    Date   : 2026-03-10
    Run from: PowerShell (no admin required)
    Time   : 30-90 minutes depending on model sizes and internet speed
#>

param(
    [string]$CachePath = "D:\earthback-cache",
    [switch]$SkipInstallers,
    [switch]$SkipModels,
    [switch]$SkipWheels
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Helpers ──────────────────────────────────────────────────────────
function Write-Step($msg) { Write-Host "`n  [$script:stepNum] $msg" -ForegroundColor Cyan; $script:stepNum++ }
function Write-Ok($msg) { Write-Host "      $msg" -ForegroundColor Green }
function Write-Skip($msg) { Write-Host "      SKIP: $msg" -ForegroundColor Yellow }
function Write-Warn($msg) { Write-Host "      WARN: $msg" -ForegroundColor Red }
function Ensure-Dir($path) { if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null } }

$script:stepNum = 1
$EB = "C:\users\adrxi\Earthback"

Write-Host ""
Write-Host "  ┌────────────────────────────────────────────────┐" -ForegroundColor Cyan
Write-Host "  │   Earthback Offline Cache Builder                │" -ForegroundColor Cyan
Write-Host "  │   Target: $CachePath" -ForegroundColor Cyan
Write-Host "  └────────────────────────────────────────────────┘" -ForegroundColor Cyan
Write-Host ""

# ── Create directory structure ───────────────────────────────────────
Write-Step "Creating directory structure"
$dirs = @(
    "$CachePath\installers",
    "$CachePath\repos\ComfyUI",
    "$CachePath\repos\kohya_ss",
    "$CachePath\repos\ai-toolkit",
    "$CachePath\models\diffusion_models",
    "$CachePath\models\clip",
    "$CachePath\models\vae",
    "$CachePath\models\checkpoints",
    "$CachePath\models\loras",
    "$CachePath\models\pulid",
    "$CachePath\wheels\comfy-env",
    "$CachePath\wheels\kohya",
    "$CachePath\wheels\ai-toolkit",
    "$CachePath\project\local",
    "$CachePath\project\maint-scripts",
    "$CachePath\project\docs"
)
foreach ($d in $dirs) { Ensure-Dir $d }
Write-Ok "Directory tree created"

# ═══════════════════════════════════════════════════════════════════
# SECTION 1: SOFTWARE INSTALLERS
# ═══════════════════════════════════════════════════════════════════
if ($SkipInstallers) {
    Write-Step "Software installers — SKIPPED"
} else {
    Write-Step "Downloading software installers"

    $downloads = @(
        @{ Name = "Python 3.11"; Url = "https://www.python.org/ftp/python/3.11.11/python-3.11.11-amd64.exe"; File = "python-3.11.11-amd64.exe" },
        @{ Name = "Git for Windows"; Url = "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.2/Git-2.47.1.2-64-bit.exe"; File = "Git-2.47.1.2-64-bit.exe" },
        @{ Name = "Node.js LTS"; Url = "https://nodejs.org/dist/v22.14.0/node-v22.14.0-x64.msi"; File = "node-v22.14.0-x64.msi" },
        @{ Name = "CUDA Toolkit 12.1"; Url = "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_531.14_windows.exe"; File = "cuda_12.1.0_531.14_windows.exe" }
    )

    foreach ($dl in $downloads) {
        $dest = Join-Path "$CachePath\installers" $dl.File
        if (Test-Path $dest) {
            Write-Ok "$($dl.Name) already cached"
        } else {
            Write-Host "      Downloading $($dl.Name)..." -ForegroundColor White
            try {
                Invoke-WebRequest -Uri $dl.Url -OutFile $dest -UseBasicParsing
                Write-Ok "$($dl.Name) downloaded"
            } catch {
                Write-Warn "Failed to download $($dl.Name): $_"
                Write-Host "      Download manually from: $($dl.Url)" -ForegroundColor DarkGray
            }
        }
    }

    Write-Host ""
    Write-Host "      NOTE: Download your NVIDIA GPU driver manually from:" -ForegroundColor Yellow
    Write-Host "      https://www.nvidia.com/download/" -ForegroundColor DarkGray
    Write-Host "      Save it to: $CachePath\installers\" -ForegroundColor DarkGray
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 2: GIT REPOS (full clone with submodules)
# ═══════════════════════════════════════════════════════════════════
Write-Step "Caching git repositories"

$repos = @(
    @{ Name = "ComfyUI"; Src = "D:\AI\ComfyUI"; Dest = "$CachePath\repos\ComfyUI"; Url = "https://github.com/comfyanonymous/ComfyUI.git" },
    @{ Name = "kohya_ss"; Src = "D:\AI\kohya_ss"; Dest = "$CachePath\repos\kohya_ss"; Url = "https://github.com/bmaltais/kohya_ss.git" },
    @{ Name = "ai-toolkit"; Src = "D:\AI\ai-toolkit"; Dest = "$CachePath\repos\ai-toolkit"; Url = "https://github.com/ostris/ai-toolkit.git" }
)

foreach ($repo in $repos) {
    if (Test-Path "$($repo.Dest)\.git") {
        Write-Host "      $($repo.Name) — pulling latest..." -ForegroundColor White
        Push-Location $repo.Dest
        git pull 2>$null
        git submodule update --init --recursive 2>$null
        Pop-Location
        Write-Ok "$($repo.Name) updated"
    } elseif (Test-Path "$($repo.Src)\.git") {
        Write-Host "      $($repo.Name) — copying local repo..." -ForegroundColor White
        # Use robocopy for speed (mirrors the .git dir too)
        robocopy $repo.Src $repo.Dest /MIR /NFL /NDL /NJH /NJS /NC /NS /NP /XD __pycache__ .venv venv node_modules | Out-Null
        Write-Ok "$($repo.Name) copied from local"
    } else {
        Write-Host "      $($repo.Name) — cloning from GitHub..." -ForegroundColor White
        git clone $repo.Url $repo.Dest
        Push-Location $repo.Dest
        git submodule update --init --recursive 2>$null
        Pop-Location
        Write-Ok "$($repo.Name) cloned"
    }
}

# Also cache custom nodes list
Write-Step "Caching ComfyUI custom nodes list"
$cnDir = "D:\AI\ComfyUI\custom_nodes"
if (Test-Path $cnDir) {
    $customNodes = Get-ChildItem $cnDir -Directory | Select-Object -ExpandProperty Name
    $customNodes | Out-File "$CachePath\repos\comfyui-custom-nodes.txt" -Encoding utf8
    Write-Ok "Custom nodes list saved ($($customNodes.Count) nodes)"
    foreach ($cn in $customNodes) {
        Write-Host "        - $cn" -ForegroundColor DarkGray
    }
} else {
    Write-Skip "No custom nodes directory found"
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 3: AI MODELS
# ═══════════════════════════════════════════════════════════════════
if ($SkipModels) {
    Write-Step "AI model files — SKIPPED"
} else {
    Write-Step "Copying AI model files (this may take a while)"

    $models = @(
        # Flux models
        @{ Src = "D:\AI\ComfyUI\models\diffusion_models"; Dest = "$CachePath\models\diffusion_models"; Pattern = "*.safetensors" },
        @{ Src = "D:\AI\ComfyUI\models\unet"; Dest = "$CachePath\models\diffusion_models"; Pattern = "*.safetensors" },
        # CLIP + T5
        @{ Src = "D:\AI\ComfyUI\models\clip"; Dest = "$CachePath\models\clip"; Pattern = "*.safetensors" },
        # VAE
        @{ Src = "D:\AI\ComfyUI\models\vae"; Dest = "$CachePath\models\vae"; Pattern = "*.safetensors" },
        # Checkpoints (SDXL etc)
        @{ Src = "D:\AI\ComfyUI\models\checkpoints"; Dest = "$CachePath\models\checkpoints"; Pattern = "*.safetensors" },
        # Also check C:\AI for SDXL checkpoint
        @{ Src = "C:\AI\models\checkpoints"; Dest = "$CachePath\models\checkpoints"; Pattern = "*.safetensors" },
        # Trained LoRAs
        @{ Src = "D:\AI\ComfyUI\models\loras"; Dest = "$CachePath\models\loras"; Pattern = "*.safetensors" },
        # PuLID models
        @{ Src = "D:\AI\ComfyUI\models\pulid"; Dest = "$CachePath\models\pulid"; Pattern = "*.safetensors" }
    )

    foreach ($m in $models) {
        if (Test-Path $m.Src) {
            $files = Get-ChildItem $m.Src -Filter $m.Pattern -ErrorAction SilentlyContinue
            foreach ($f in $files) {
                $destFile = Join-Path $m.Dest $f.Name
                if (Test-Path $destFile) {
                    $srcSize = $f.Length
                    $dstSize = (Get-Item $destFile).Length
                    if ($srcSize -eq $dstSize) {
                        Write-Ok "$($f.Name) already cached ($('{0:N1} GB' -f ($srcSize/1GB)))"
                        continue
                    }
                }
                Ensure-Dir $m.Dest
                $sizeGB = '{0:N1} GB' -f ($f.Length / 1GB)
                Write-Host "      Copying $($f.Name) ($sizeGB)..." -ForegroundColor White
                Copy-Item $f.FullName $destFile -Force
                Write-Ok "$($f.Name) cached"
            }
        }
    }

    # Copy any LoRA output from local/lora-output/
    $loraLocal = "$EB\local\lora-output"
    if (Test-Path $loraLocal) {
        Write-Host "      Copying trained LoRA checkpoints..." -ForegroundColor White
        Ensure-Dir "$CachePath\models\lora-output"
        robocopy $loraLocal "$CachePath\models\lora-output" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
        Write-Ok "Local LoRA checkpoints cached"
    }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 4: PIP WHEEL CACHES
# ═══════════════════════════════════════════════════════════════════
if ($SkipWheels) {
    Write-Step "Pip wheel caches — SKIPPED"
} else {
    Write-Step "Exporting pip wheels for offline install"

    $venvs = @(
        @{ Name = "comfy-env"; Python = "D:\AI\comfy-env\Scripts\python.exe"; WheelDir = "$CachePath\wheels\comfy-env" },
        @{ Name = "kohya"; Python = "D:\AI\kohya_ss\venv\Scripts\python.exe"; WheelDir = "$CachePath\wheels\kohya" },
        @{ Name = "ai-toolkit"; Python = "D:\AI\ai-toolkit\venv\Scripts\python.exe"; WheelDir = "$CachePath\wheels\ai-toolkit" }
    )

    foreach ($v in $venvs) {
        if (Test-Path $v.Python) {
            Write-Host "      $($v.Name) — freezing requirements..." -ForegroundColor White
            $reqFile = Join-Path $v.WheelDir "requirements.txt"
            & $v.Python -m pip freeze | Out-File $reqFile -Encoding utf8
            Write-Host "      $($v.Name) — downloading wheels (may take a few minutes)..." -ForegroundColor White
            try {
                & $v.Python -m pip download -r $reqFile -d $v.WheelDir --no-deps 2>$null
                Write-Ok "$($v.Name) wheels cached"
            } catch {
                Write-Warn "$($v.Name) wheel download had errors (some platform-specific wheels may need re-download)"
            }
        } else {
            Write-Skip "$($v.Name) — venv not found at $($v.Python)"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 5: PROJECT FILES
# ═══════════════════════════════════════════════════════════════════
Write-Step "Copying project scripts, configs, and datasets"

# local/scripts/ (all Python/bat scripts + configs)
$localScripts = "$EB\local\scripts"
if (Test-Path $localScripts) {
    robocopy $localScripts "$CachePath\project\local\scripts" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP /XD __pycache__ | Out-Null
    Write-Ok "local/scripts/ cached"
}

# local/datasets/ (training images + captions)
$localDatasets = "$EB\local\datasets"
if (Test-Path $localDatasets) {
    Write-Host "      Copying datasets (may be large)..." -ForegroundColor White
    robocopy $localDatasets "$CachePath\project\local\datasets" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "local/datasets/ cached"
}

# local/faces-reference/ (PuLID reference images)
$facesRef = "$EB\local\faces-reference"
if (Test-Path $facesRef) {
    robocopy $facesRef "$CachePath\project\local\faces-reference" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "local/faces-reference/ cached"
}

# local/lora-reference/workflows/ (ComfyUI workflow JSONs)
$workflows = "$EB\local\lora-reference"
if (Test-Path $workflows) {
    robocopy $workflows "$CachePath\project\local\lora-reference" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "local/lora-reference/ cached"
}

# maint-scripts/
robocopy "$EB\maint-scripts" "$CachePath\project\maint-scripts" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
Write-Ok "maint-scripts/ cached"

# Key docs
$keyDocs = @("CLAUDE.md", "SESSION_NOTES.md", "TRACKER.md", "QUICKSTART.md", "command-center.html")
foreach ($doc in $keyDocs) {
    $src = Join-Path $EB $doc
    if (Test-Path $src) {
        Copy-Item $src "$CachePath\project\" -Force
    }
}
# docs/ folder
if (Test-Path "$EB\docs") {
    robocopy "$EB\docs" "$CachePath\project\docs" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
}
Write-Ok "Key docs cached"

# ═══════════════════════════════════════════════════════════════════
# SECTION 6: MANIFEST
# ═══════════════════════════════════════════════════════════════════
Write-Step "Generating cache manifest"

$manifest = @"
# Earthback Offline Cache Manifest
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm")
# Machine: $env:COMPUTERNAME
# Cache path: $CachePath

## Contents

### installers/
Software installers for base system setup.
NOTE: Download NVIDIA GPU driver separately from https://www.nvidia.com/download/

### repos/
Full git clones (with .git history) of:
- ComfyUI (image generation engine)
- kohya_ss (SDXL LoRA training)
- ai-toolkit (Flux LoRA training)
- comfyui-custom-nodes.txt (list of installed custom nodes)

### models/
All AI model files (.safetensors):
- diffusion_models/ — Flux dev weights
- clip/ — CLIP-L + T5XXL text encoders
- vae/ — Flux VAE (ae.safetensors)
- checkpoints/ — SDXL checkpoint
- loras/ — Trained LoRA files deployed to ComfyUI
- lora-output/ — All local training checkpoints
- pulid/ — PuLID face-lock models

### wheels/
Pip wheel caches + frozen requirements.txt for each venv:
- comfy-env/ — ComfyUI dependencies
- kohya/ — Kohya SS dependencies
- ai-toolkit/ — ai-toolkit dependencies (torch 2.4.1+cu121!)

### project/
Project files that aren't in git:
- local/scripts/ — All queue/training/caption scripts + configs
- local/datasets/ — Training image datasets with captions
- local/faces-reference/ — PuLID reference face images
- local/lora-reference/ — ComfyUI workflow JSONs
- maint-scripts/ — GPU reset, VM fix, git wrapper, rebuild guide
- docs/ — Character bibles, circle prompts, handoff docs
- Key project docs: CLAUDE.md, SESSION_NOTES.md, TRACKER.md, etc.

## To Install on New Machine

Run: install-from-cache.ps1 -CachePath "path\to\this\folder"
See: Earthback-Rebuild-Guide.docx in maint-scripts/ for full details.
"@

$manifest | Out-File "$CachePath\MANIFEST.md" -Encoding utf8
Write-Ok "Manifest written"

# ═══════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "  ┌────────────────────────────────────────────────┐" -ForegroundColor Green
Write-Host "  │   Cache build complete!                         │" -ForegroundColor Green
Write-Host "  └────────────────────────────────────────────────┘" -ForegroundColor Green
Write-Host ""

# Calculate total size
$totalBytes = (Get-ChildItem $CachePath -Recurse -File | Measure-Object -Property Length -Sum).Sum
$totalGB = '{0:N1}' -f ($totalBytes / 1GB)
Write-Host "  Total cache size: $totalGB GB" -ForegroundColor White
Write-Host "  Location: $CachePath" -ForegroundColor White
Write-Host ""
Write-Host "  To move to external drive:" -ForegroundColor DarkGray
Write-Host "    robocopy $CachePath E:\earthback-cache /MIR" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  To install on new machine:" -ForegroundColor DarkGray
Write-Host "    .\install-from-cache.ps1 -CachePath E:\earthback-cache" -ForegroundColor DarkGray
Write-Host ""

# Reminder about manual items
Write-Host "  Manual items NOT in cache:" -ForegroundColor Yellow
Write-Host "    - NVIDIA GPU driver (download for your specific GPU)" -ForegroundColor Yellow
Write-Host "    - Supabase credentials (get from dashboard)" -ForegroundColor Yellow
Write-Host "    - command-center.html (recreate with credentials)" -ForegroundColor Yellow
Write-Host "    - PowerShell profile (re-run g alias one-liner)" -ForegroundColor Yellow
Write-Host ""
