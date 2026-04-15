#Requires -RunAsAdministrator

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$pattern = "RTX\s*3060"

# -- Query GPUs via nvidia-smi ---------------------------------------------
$csv = nvidia-smi --query-gpu=index,name,pci.bus_id,utilization.gpu,memory.used,memory.total --format=csv,noheader
$gpuList = @()
foreach ($line in $csv) {
    $fields = $line -split ', '
    $gpuList += [PSCustomObject]@{
        Index   = $fields[0].Trim()
        Name    = $fields[1].Trim()
        BusId   = $fields[2].Trim()
        GpuUtil = $fields[3].Trim()
        MemUsed = $fields[4].Trim()
        MemTotal= $fields[5].Trim()
    }
}

if ($gpuList.Count -eq 0) {
    Write-Host ""
    Write-Host "  No NVIDIA GPUs found." -ForegroundColor Red
    exit 1
}

# -- Display menu ----------------------------------------------------------
Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host "       NVIDIA GPU Reset (nvidia-smi)        " -ForegroundColor Cyan
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($gpu in $gpuList) {
    # Check for processes on this GPU
    $procs = nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader -i $gpu.Index 2>$null
    $procList = @()
    if ($procs) {
        foreach ($p in $procs) {
            if ($p.Trim() -ne "") {
                $procList += $p.Trim()
            }
        }
    }

    Write-Host "  [$($gpu.Index)]  $($gpu.Name)"
    Write-Host "        Bus ID   : $($gpu.BusId)" -ForegroundColor DarkGray
    Write-Host "        GPU Load : $($gpu.GpuUtil)" -ForegroundColor DarkGray
    Write-Host "        VRAM     : $($gpu.MemUsed) / $($gpu.MemTotal)" -ForegroundColor DarkGray
    if ($procList.Count -gt 0) {
        Write-Host "        Processes:" -ForegroundColor Yellow
        foreach ($p in $procList) {
            Write-Host "          $p" -ForegroundColor Yellow
        }
    } else {
        Write-Host "        Processes: none" -ForegroundColor DarkGray
    }
    Write-Host ""
}

Write-Host "  [A]  Reset ALL GPUs"
Write-Host "  [Q]  Quit"
Write-Host ""

$choice = Read-Host "  Select GPU index (or A/Q)"

if ($choice -eq 'Q' -or $choice -eq 'q') {
    Write-Host "  Cancelled." -ForegroundColor Yellow
    exit 0
}

# -- Build list of GPU indices to reset ------------------------------------
if ($choice -eq 'A' -or $choice -eq 'a') {
    $targets = $gpuList | ForEach-Object { $_.Index }
} else {
    $match = $gpuList | Where-Object { $_.Index -eq $choice }
    if (-not $match) {
        Write-Host "  Invalid selection." -ForegroundColor Red
        exit 1
    }
    $targets = @($choice)
}

# -- Reset each GPU --------------------------------------------------------
foreach ($idx in $targets) {
    $gpu = $gpuList | Where-Object { $_.Index -eq $idx }
    Write-Host ""

    # Check for blocking processes
    $procs = nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader -i $idx 2>$null
    $pidList = @()
    if ($procs) {
        foreach ($p in $procs) {
            if ($p.Trim() -ne "") {
                $fields = $p -split ', '
                $pidList += [PSCustomObject]@{
                    PID  = $fields[0].Trim()
                    Name = $fields[1].Trim()
                }
            }
        }
    }

    if ($pidList.Count -gt 0) {
        Write-Host "  GPU $idx has running processes:" -ForegroundColor Yellow
        foreach ($proc in $pidList) {
            Write-Host "    PID $($proc.PID) - $($proc.Name)" -ForegroundColor Yellow
        }
        Write-Host ""
        $kill = Read-Host "  Kill these processes and reset? (y/n)"
        if ($kill -ne 'y' -and $kill -ne 'Y') {
            Write-Host "  Skipping GPU $idx." -ForegroundColor Yellow
            continue
        }

        foreach ($proc in $pidList) {
            Write-Host "  Killing PID $($proc.PID) ($($proc.Name)) ..." -ForegroundColor Yellow
            Stop-Process -Id $proc.PID -Force -ErrorAction SilentlyContinue
        }
        Start-Sleep -Seconds 2
    }

    Write-Host "  Resetting GPU $idx ($($gpu.Name)) ..." -ForegroundColor Yellow

    $result = nvidia-smi --gpu-reset -i $idx 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "  [OK] GPU $idx reset complete." -ForegroundColor Green
    } else {
        Write-Host "  [WARN] nvidia-smi returned exit code $exitCode" -ForegroundColor Red
        Write-Host "  $result" -ForegroundColor Red
    }
}

# -- Post-reset status -----------------------------------------------------
Write-Host ""
Write-Host "  -- Post-reset status --" -ForegroundColor Cyan
Start-Sleep -Seconds 2
nvidia-smi
Write-Host ""
Write-Host "  Done." -ForegroundColor Green
Write-Host ""
