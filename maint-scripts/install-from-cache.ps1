<#
.SYNOPSIS
    Rebuild an Earthback workstation from an offline cache.

.DESCRIPTION
    Deploys everything from a cache built by cache-offline-install.ps1.
    Run this on the NEW machine after copying the cache folder over.

    Handles: repos, models, venvs (from cached wheels), project files,
    maintenance scripts, and PowerShell profile setup.

    Software installers (Python, Git, Node, CUDA) must be run manually
    first — this script tells you which ones and checks for them.

.PARAMETER CachePath
    Path to the offline cache folder. Default: D:\earthback-cache

.PARAMETER AIPath
    Where to install AI tools. Default: D:\AI

.PARAMETER ProjectPath
    Where to clone the Earthback repo. Default: C:\users\adrxi\Earthback

.NOTES
    Author : Claude (for Nicco)
    Date   : 2026-03-10
    Run from: Administrator PowerShell (needed for some installs)
#>

param(
    [string]$CachePath = "D:\earthback-cache",
    [string]$AIPath = "D:\AI",
    [string]$ProjectPath = "C:\users\adrxi\Earthback"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Step($msg) { Write-Host "`n  [$script:stepNum] $msg" -ForegroundColor Cyan; $script:stepNum++ }
function Write-Ok($msg) { Write-Host "      $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "      WARN: $msg" -ForegroundColor Red }
function Ensure-Dir($path) { if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null } }

$script:stepNum = 1

Write-Host ""
Write-Host "  ┌────────────────────────────────────────────────┐" -ForegroundColor Cyan
Write-Host "  │   Earthback Workstation Installer (from cache)  │" -ForegroundColor Cyan
Write-Host "  │   Cache: $CachePath" -ForegroundColor Cyan
Write-Host "  │   AI:    $AIPath" -ForegroundColor Cyan
Write-Host "  │   Repo:  $ProjectPath" -ForegroundColor Cyan
Write-Host "  └────────────────────────────────────────────────┘" -ForegroundColor Cyan
Write-Host ""

# ── Verify cache exists ──────────────────────────────────────────────
if (-not (Test-Path "$CachePath\MANIFEST.md")) {
    Write-Host "  ERROR: Cache not found at $CachePath" -ForegroundColor Red
    Write-Host "  Make sure the earthback-cache folder is accessible." -ForegroundColor Red
    exit 1
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 1: PRE-FLIGHT — Check base software
# ═══════════════════════════════════════════════════════════════════
Write-Step "Pre-flight checks — base software"

$missing = @()

# Git
$gitOk = Get-Command git -ErrorAction SilentlyContinue
if ($gitOk) { Write-Ok "Git found: $(git --version)" }
else { $missing += "Git"; Write-Warn "Git not found — install from: $CachePath\installers\Git-*.exe" }

# Python 3.11
$py311 = $null
# Check common paths
$py311Paths = @(
    "C:\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "C:\Program Files\Python311\python.exe"
)
foreach ($pp in $py311Paths) {
    if (Test-Path $pp) { $py311 = $pp; break }
}
# Also try py launcher
if (-not $py311) {
    try {
        $pyVer = & py -3.11 --version 2>&1
        if ($pyVer -match "3\.11") { $py311 = "py -3.11" }
    } catch {}
}
if ($py311) { Write-Ok "Python 3.11 found: $py311" }
else { $missing += "Python 3.11"; Write-Warn "Python 3.11 not found — install from: $CachePath\installers\python-3.11*.exe (check 'Add to PATH')" }

# Node
$nodeOk = Get-Command node -ErrorAction SilentlyContinue
if ($nodeOk) { Write-Ok "Node.js found: $(node --version)" }
else { $missing += "Node.js"; Write-Warn "Node.js not found — install from: $CachePath\installers\node-*.msi" }

# NVIDIA / CUDA
$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaSmi) {
    $gpuInfo = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>$null
    Write-Ok "NVIDIA GPU(s): $gpuInfo"
} else {
    $missing += "NVIDIA drivers"
    Write-Warn "nvidia-smi not found — install GPU drivers + CUDA from: $CachePath\installers\"
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "  STOP: Install these first, then re-run this script:" -ForegroundColor Red
    foreach ($m in $missing) { Write-Host "    - $m" -ForegroundColor Red }
    Write-Host ""
    $cont = Read-Host "  Continue anyway? (y/n)"
    if ($cont -ne 'y') { exit 0 }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 2: CLONE PROJECT REPO
# ═══════════════════════════════════════════════════════════════════
Write-Step "Setting up project repository"

if (Test-Path "$ProjectPath\.git") {
    Write-Ok "Repo already exists at $ProjectPath"
} else {
    Write-Host "      Cloning from GitHub..." -ForegroundColor White
    Ensure-Dir (Split-Path $ProjectPath)
    try {
        git clone https://github.com/earthbackproject/earthback.git $ProjectPath
        Write-Ok "Repo cloned"
    } catch {
        Write-Warn "GitHub clone failed (no internet?). Copying project docs from cache instead."
        Ensure-Dir $ProjectPath
    }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 3: DEPLOY AI REPOS
# ═══════════════════════════════════════════════════════════════════
Write-Step "Deploying AI tool repositories"
Ensure-Dir $AIPath

$repos = @(
    @{ Name = "ComfyUI"; Src = "$CachePath\repos\ComfyUI"; Dest = "$AIPath\ComfyUI" },
    @{ Name = "kohya_ss"; Src = "$CachePath\repos\kohya_ss"; Dest = "$AIPath\kohya_ss" },
    @{ Name = "ai-toolkit"; Src = "$CachePath\repos\ai-toolkit"; Dest = "$AIPath\ai-toolkit" }
)

foreach ($repo in $repos) {
    if (Test-Path "$($repo.Dest)\.git") {
        Write-Ok "$($repo.Name) already deployed"
    } elseif (Test-Path "$($repo.Src)\.git") {
        Write-Host "      Deploying $($repo.Name)..." -ForegroundColor White
        robocopy $repo.Src $repo.Dest /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
        Write-Ok "$($repo.Name) deployed"
    } else {
        Write-Warn "$($repo.Name) not in cache — clone manually"
    }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 4: DEPLOY MODELS
# ═══════════════════════════════════════════════════════════════════
Write-Step "Deploying AI model files"

$modelMaps = @(
    @{ Src = "$CachePath\models\diffusion_models"; Dest = "$AIPath\ComfyUI\models\diffusion_models" },
    @{ Src = "$CachePath\models\diffusion_models"; Dest = "$AIPath\ComfyUI\models\unet" },
    @{ Src = "$CachePath\models\clip"; Dest = "$AIPath\ComfyUI\models\clip" },
    @{ Src = "$CachePath\models\vae"; Dest = "$AIPath\ComfyUI\models\vae" },
    @{ Src = "$CachePath\models\checkpoints"; Dest = "$AIPath\ComfyUI\models\checkpoints" },
    @{ Src = "$CachePath\models\loras"; Dest = "$AIPath\ComfyUI\models\loras" },
    @{ Src = "$CachePath\models\pulid"; Dest = "$AIPath\ComfyUI\models\pulid" }
)

foreach ($mm in $modelMaps) {
    if (Test-Path $mm.Src) {
        $files = Get-ChildItem $mm.Src -Filter "*.safetensors" -ErrorAction SilentlyContinue
        if ($files.Count -gt 0) {
            Ensure-Dir $mm.Dest
            foreach ($f in $files) {
                $destFile = Join-Path $mm.Dest $f.Name
                if (Test-Path $destFile) {
                    Write-Ok "$($f.Name) already in place"
                } else {
                    $sizeGB = '{0:N1} GB' -f ($f.Length / 1GB)
                    Write-Host "      Copying $($f.Name) ($sizeGB)..." -ForegroundColor White
                    Copy-Item $f.FullName $destFile -Force
                    Write-Ok "$($f.Name) deployed"
                }
            }
        }
    }
}

# Restore local LoRA checkpoints
if (Test-Path "$CachePath\models\lora-output") {
    Ensure-Dir "$ProjectPath\local\lora-output"
    robocopy "$CachePath\models\lora-output" "$ProjectPath\local\lora-output" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "Local LoRA checkpoints restored"
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 5: CREATE VENVS + INSTALL FROM WHEELS
# ═══════════════════════════════════════════════════════════════════
Write-Step "Creating Python virtual environments"

# Find Python 3.11
$py311Exe = $null
foreach ($pp in $py311Paths) {
    if (Test-Path $pp) { $py311Exe = $pp; break }
}
if (-not $py311Exe) {
    try { & py -3.11 --version 2>$null; $py311Exe = "py" } catch {}
}

if (-not $py311Exe) {
    Write-Warn "Python 3.11 not found — skipping venv creation. Install Python 3.11 first."
} else {
    # ── comfy-env ──
    $comfyVenv = "$AIPath\comfy-env"
    if (-not (Test-Path "$comfyVenv\Scripts\python.exe")) {
        Write-Host "      Creating comfy-env venv..." -ForegroundColor White
        if ($py311Exe -eq "py") { & py -3.11 -m venv $comfyVenv }
        else { & $py311Exe -m venv $comfyVenv }

        $comfyPip = "$comfyVenv\Scripts\pip.exe"
        $comfyWheels = "$CachePath\wheels\comfy-env"
        if (Test-Path "$comfyWheels\requirements.txt") {
            Write-Host "      Installing comfy-env packages from cached wheels..." -ForegroundColor White
            & $comfyPip install --no-index --find-links $comfyWheels -r "$comfyWheels\requirements.txt" 2>$null
            Write-Ok "comfy-env created and packages installed"
        } else {
            Write-Warn "No cached wheels for comfy-env — install manually with internet"
        }
    } else {
        Write-Ok "comfy-env already exists"
    }

    # ── kohya venv ──
    $kohyaVenv = "$AIPath\kohya_ss\venv"
    if (-not (Test-Path "$kohyaVenv\Scripts\python.exe")) {
        Write-Host "      Creating kohya venv..." -ForegroundColor White
        if ($py311Exe -eq "py") { & py -3.11 -m venv $kohyaVenv }
        else { & $py311Exe -m venv $kohyaVenv }

        $kohyaPip = "$kohyaVenv\Scripts\pip.exe"
        $kohyaWheels = "$CachePath\wheels\kohya"
        if (Test-Path "$kohyaWheels\requirements.txt") {
            Write-Host "      Installing kohya packages from cached wheels..." -ForegroundColor White
            & $kohyaPip install --no-index --find-links $kohyaWheels -r "$kohyaWheels\requirements.txt" 2>$null
            Write-Ok "kohya venv created and packages installed"
        } else {
            Write-Warn "No cached wheels for kohya — run setup.bat in kohya_ss directory"
        }
    } else {
        Write-Ok "kohya venv already exists"
    }

    # ── ai-toolkit venv ──
    $aitkVenv = "$AIPath\ai-toolkit\venv"
    if (-not (Test-Path "$aitkVenv\Scripts\python.exe")) {
        Write-Host "      Creating ai-toolkit venv..." -ForegroundColor White
        if ($py311Exe -eq "py") { & py -3.11 -m venv $aitkVenv }
        else { & $py311Exe -m venv $aitkVenv }

        $aitkPip = "$aitkVenv\Scripts\pip.exe"
        $aitkWheels = "$CachePath\wheels\ai-toolkit"
        if (Test-Path "$aitkWheels\requirements.txt") {
            Write-Host "      Installing ai-toolkit packages from cached wheels..." -ForegroundColor White
            # CRITICAL: torch must be 2.4.1+cu121
            & $aitkPip install --no-index --find-links $aitkWheels -r "$aitkWheels\requirements.txt" 2>$null
            Write-Ok "ai-toolkit venv created and packages installed"
            Write-Host "      VERIFY: torch version must be 2.4.1+cu121" -ForegroundColor Yellow
            & "$aitkVenv\Scripts\python.exe" -c "import torch; print(f'      torch {torch.__version__}  CUDA: {torch.cuda.is_available()}')"
        } else {
            Write-Warn "No cached wheels for ai-toolkit — run install-ai-toolkit.ps1"
        }
    } else {
        Write-Ok "ai-toolkit venv already exists"
    }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 6: DEPLOY PROJECT FILES
# ═══════════════════════════════════════════════════════════════════
Write-Step "Restoring project files (local/, maint-scripts/, docs/)"

# local/ (scripts, datasets, faces, workflows)
$localSrc = "$CachePath\project\local"
if (Test-Path $localSrc) {
    Ensure-Dir "$ProjectPath\local"
    robocopy $localSrc "$ProjectPath\local" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "local/ restored"
}

# maint-scripts/
$maintSrc = "$CachePath\project\maint-scripts"
if (Test-Path $maintSrc) {
    Ensure-Dir "$ProjectPath\maint-scripts"
    robocopy $maintSrc "$ProjectPath\maint-scripts" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "maint-scripts/ restored"
}

# docs/
$docsSrc = "$CachePath\project\docs"
if (Test-Path $docsSrc) {
    Ensure-Dir "$ProjectPath\docs"
    robocopy $docsSrc "$ProjectPath\docs" /MIR /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
    Write-Ok "docs/ restored"
}

# Key root docs (only if not already in git clone)
foreach ($doc in @("CLAUDE.md", "SESSION_NOTES.md", "TRACKER.md", "QUICKSTART.md", "command-center.html")) {
    $src = Join-Path "$CachePath\project" $doc
    $dest = Join-Path $ProjectPath $doc
    if ((Test-Path $src) -and (-not (Test-Path $dest))) {
        Copy-Item $src $dest -Force
        Write-Ok "$doc restored"
    }
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 7: POWERSHELL PROFILE
# ═══════════════════════════════════════════════════════════════════
Write-Step "Setting up PowerShell profile"

$aliasLine = "function g { & `"$ProjectPath\maint-scripts\eb-git.ps1`" @args }"
$profileContent = ""
if (Test-Path $PROFILE) { $profileContent = Get-Content $PROFILE -Raw }

if ($profileContent -match "function g \{") {
    Write-Ok "g alias already in profile"
} else {
    Add-Content $PROFILE "`n$aliasLine"
    Write-Ok "g alias added to PowerShell profile"
    Write-Host "      Run '. `$PROFILE' to load it now." -ForegroundColor DarkGray
}

# ═══════════════════════════════════════════════════════════════════
# SECTION 8: CREATE comfy-run.bat
# ═══════════════════════════════════════════════════════════════════
Write-Step "Creating comfy-run.bat"

$comfyBat = @"
@echo off
cd /d $AIPath\ComfyUI
$AIPath\comfy-env\Scripts\python.exe main.py --normalvram --port 8188 --output-directory $ProjectPath\comfyui-output
"@

$comfyBatPath = "$ProjectPath\local\scripts\comfy-run.bat"
Ensure-Dir (Split-Path $comfyBatPath)
$comfyBat | Out-File $comfyBatPath -Encoding ascii
Ensure-Dir "$ProjectPath\comfyui-output"
Write-Ok "comfy-run.bat created"

# ═══════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "  ┌────────────────────────────────────────────────┐" -ForegroundColor Green
Write-Host "  │   Installation complete!                        │" -ForegroundColor Green
Write-Host "  └────────────────────────────────────────────────┘" -ForegroundColor Green
Write-Host ""
Write-Host "  Project: $ProjectPath" -ForegroundColor White
Write-Host "  AI tools: $AIPath" -ForegroundColor White
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor Cyan
Write-Host "    1. Install ComfyUI custom nodes via Manager:" -ForegroundColor White
$cnList = "$CachePath\repos\comfyui-custom-nodes.txt"
if (Test-Path $cnList) {
    Get-Content $cnList | ForEach-Object { Write-Host "       - $_" -ForegroundColor DarkGray }
}
Write-Host "    2. Run comfy-run.bat and verify http://127.0.0.1:8188" -ForegroundColor White
Write-Host "    3. Open Claude Desktop (Cowork mode)" -ForegroundColor White
Write-Host "    4. Recreate command-center.html with your API keys" -ForegroundColor White
Write-Host "    5. Set up Supabase credentials" -ForegroundColor White
Write-Host ""
Write-Host "  If ComfyUI won't start, run:" -ForegroundColor DarkGray
Write-Host "    .\maint-scripts\Reset-GPU.ps1" -ForegroundColor DarkGray
Write-Host ""

pause
