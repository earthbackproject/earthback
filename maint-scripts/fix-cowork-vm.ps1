# Fix Claude Cowork "VM service not running" error
# Double-click this file to run. It will request admin privileges automatically.

# --- Self-elevate to admin if not already ---
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host ""
Write-Host "=== Cowork VM Fix ===" -ForegroundColor Cyan
Write-Host ""

$svc = Get-Service -Name CoworkVMService -ErrorAction SilentlyContinue
if (-not $svc) {
    Write-Host "CoworkVMService not found. Is Claude Cowork installed?" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host "CoworkVMService status: $($svc.Status)" -ForegroundColor Yellow

if ($svc.Status -eq "Running") {
    Write-Host "Service is running but stuck - stopping it..." -ForegroundColor Yellow
    net stop CoworkVMService | Out-Null
    Start-Sleep -Seconds 3
}

Write-Host "Starting CoworkVMService..." -ForegroundColor Yellow
net start CoworkVMService | Out-Null
Start-Sleep -Seconds 2

$svc.Refresh()
if ($svc.Status -eq "Running") {
    Write-Host ""
    Write-Host "FIXED! Open Claude now." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Service didn't start. You may need to reboot." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to close"
