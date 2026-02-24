@echo off
echo.
echo === Cowork VM Fix ===
echo.
echo Requesting admin privileges...
powershell -Command "Start-Process cmd -ArgumentList '/c powershell -ExecutionPolicy Bypass -Command \"$svc = Get-Service -Name CoworkVMService -ErrorAction SilentlyContinue; if (-not $svc) { Write-Host CoworkVMService not found -ForegroundColor Red } else { Write-Host Status: $($svc.Status) -ForegroundColor Yellow; if ($svc.Status -eq ''Running'') { net stop CoworkVMService; timeout /t 3 >nul }; net start CoworkVMService; Start-Sleep 2; $svc.Refresh(); if ($svc.Status -eq ''Running'') { Write-Host FIXED! Open Claude now. -ForegroundColor Green } else { Write-Host Service did not start. Try rebooting. -ForegroundColor Red } }; pause\"' -Verb RunAs"
