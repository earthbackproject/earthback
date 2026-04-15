# eb-git.ps1 — Git wrapper that cleans stale lock files before running
#
# WHY THIS EXISTS:
# Claude's Cowork VM accesses this repo through a virtiofs FUSE mount.
# Git creates .lock files during operations, but the VM can't always
# unlink them afterward (cross-filesystem permission issue). They pile
# up and block future git operations.
#
# This wrapper removes any stale lock files before passing your command
# through to git. Use it exactly like git:
#
#   .\maint` scripts\eb-git.ps1 status
#   .\maint` scripts\eb-git.ps1 add -A
#   .\maint` scripts\eb-git.ps1 commit -m "your message"
#   .\maint` scripts\eb-git.ps1 push
#
# Or set up an alias (see below) so you can just type: g status
#
# TO SET UP THE ALIAS (run once in PowerShell):
#   Add-Content $PROFILE 'function g { & "$env:USERPROFILE\Earthback\maint scripts\eb-git.ps1" @args }'
#   . $PROFILE
#
# Then just use:  g status / g add -A / g commit -m "msg" / g push
#

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$gitDir = Join-Path $repoRoot ".git"

# Clean stale lock files
$lockFiles = @(
    (Join-Path $gitDir "index.lock"),
    (Join-Path $gitDir "HEAD.lock"),
    (Join-Path $gitDir "refs\heads\main.lock"),
    (Join-Path $gitDir "COMMIT_EDITMSG.lock")
)

$cleaned = 0
foreach ($lock in $lockFiles) {
    if (Test-Path $lock) {
        try {
            Remove-Item $lock -Force -ErrorAction Stop
            $cleaned++
            Write-Host "  cleaned: $($lock | Split-Path -Leaf)" -ForegroundColor DarkYellow
        } catch {
            Write-Host "  WARN: could not remove $($lock | Split-Path -Leaf) - is another git process running?" -ForegroundColor Red
        }
    }
}

if ($cleaned -gt 0) {
    Write-Host ('  {0} stale lock file(s) removed' -f $cleaned) -ForegroundColor DarkYellow
    Write-Host ""
}

# Pass through to git
Set-Location $repoRoot
& git @args
