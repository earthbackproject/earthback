# Maintenance Scripts

All scripts live in `C:\Users\adrxi\Earthback\maint-scripts\`.

---

## Reset-GPU.ps1

Power-cycles one or both RTX 3060 GPUs without rebooting. Useful when a GPU gets stuck, shows driver errors, or ComfyUI/Flux stops recognizing it.

**Requires:** Administrator PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\adrxi\Earthback\maint-scripts\Reset-GPU.ps1"
```

You'll get a menu to pick GPU 1, GPU 2, or both. Close any GPU-heavy apps (ComfyUI, games, renders) on the target GPU first.

---

## fix-cowork-vm.ps1

Restarts the CoworkVMService when Claude's Cowork mode shows "VM service not running" or the VM hangs.

**Requires:** Administrator PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\adrxi\Earthback\maint-scripts\fix-cowork-vm.ps1"
```

Self-elevates to admin if needed. Stops the service (if stuck), restarts it, and confirms the fix. Reopen Claude afterward.

---

## fix-cowork-vm.bat

Same as above but as a `.bat` you can double-click from Explorer. It will prompt for admin privileges automatically.

---

## eb-git.ps1

Git wrapper that cleans stale `.lock` files before running any git command. The Cowork VM's virtiofs mount leaves orphan lock files that block future git operations — this script removes them first, then passes your command through to git.

**Usage (direct):**

```powershell
& "C:\Users\adrxi\Earthback\maint-scripts\eb-git.ps1" status
& "C:\Users\adrxi\Earthback\maint-scripts\eb-git.ps1" add -A
& "C:\Users\adrxi\Earthback\maint-scripts\eb-git.ps1" commit -m "your message"
& "C:\Users\adrxi\Earthback\maint-scripts\eb-git.ps1" push
```

**Usage (with `g` alias — recommended):**

Run this once to set up the alias:

```powershell
Add-Content $PROFILE 'function g { & "$env:USERPROFILE\Earthback\maint-scripts\eb-git.ps1" @args }'
. $PROFILE
```

Then just use `g` like git:

```powershell
g status
g add -A
g commit -m "describe what changed"
g push
```

---

## cache-offline-install.ps1

Builds a complete offline cache of everything needed to rebuild the workstation from scratch: software installers, git repos, AI models, pip wheels, project scripts/configs/datasets.

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\adrxi\Earthback\maint-scripts\cache-offline-install.ps1"
```

Default output: `D:\earthback-cache\`. Override with `-CachePath "E:\my-cache"`. Use `-SkipInstallers`, `-SkipModels`, or `-SkipWheels` to skip sections. Total cache size: ~30-50 GB.

To copy to an external drive:

```powershell
robocopy D:\earthback-cache E:\earthback-cache /MIR
```

---

## install-from-cache.ps1

Rebuilds the full workstation from an offline cache. Run on the new machine after installing base software (Git, Python 3.11, Node.js, CUDA, NVIDIA drivers).

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\adrxi\Earthback\maint-scripts\install-from-cache.ps1" -CachePath "E:\earthback-cache"
```

Deploys: AI repos, model files, Python venvs (from cached wheels), project files, PowerShell profile, and comfy-run.bat.

---

## Earthback-Rebuild-Guide.docx

Comprehensive 12-section document covering the full workstation setup: hardware specs, software install order, cloud services, Python environments, AI pipeline, LoRA training, folder structure, site architecture, characters, startup sequence, and known quirks. Generated from 33 sessions of accumulated configuration.
