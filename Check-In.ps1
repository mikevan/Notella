[CmdletBinding()]
param(
    [switch]$Execute,
    [switch]$Push,
    [switch]$CreateRemote
)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\')
$remoteUrl = 'https://github.com/mikevan/Notella.git'
$manifestPath = Join-Path $taskRoot 'checkpoint\baseline-manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if (($Push -or $CreateRemote) -and -not $Execute) { throw '-Push and -CreateRemote require -Execute. Preview alone makes no changes.' }
if ($CreateRemote -and -not $Push) { throw '-CreateRemote requires -Push so remote creation is an explicit publishing action.' }
$paths = @()
foreach ($item in $manifest.files) {
    $fullPath = [IO.Path]::GetFullPath((Join-Path $taskRoot $item.path))
    if (-not $fullPath.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Manifest path escapes the project.' }
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) { throw "Missing checkpoint file: $($item.path)" }
    $actual = (Get-FileHash -LiteralPath $fullPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $item.sha256) { throw "File changed since checkpoint preparation: $($item.path). Preserve the change and regenerate/review the checkpoint; do not weaken the check." }
    $paths += $item.path
}
$paths += 'checkpoint/baseline-manifest.json'
Write-Host "Notella baseline: $($paths.Count) explicit files, target $remoteUrl"
Write-Host 'Includes source, tutorials, examples, check-in tools, and selected development evidence.'
Write-Host 'Model weights, runtime folders, environments, caches and subsequent experiment files are excluded.'
$paths | ForEach-Object { Write-Host "  $_" }
if (-not $Execute) {
    Write-Host "Preview only. Local commit: .\Check-In.ps1 -Execute"
    Write-Host "Commit and push existing repo: .\Check-In.ps1 -Execute -Push"
    Write-Host "Create a private repo if absent, commit and push: .\Check-In.ps1 -Execute -Push -CreateRemote"
    return
}
function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$GitArguments)
    & git -C $taskRoot @GitArguments
    if ($LASTEXITCODE -ne 0) { throw "Git failed: $($GitArguments -join ' ')" }
}
function Invoke-ReadOnlyProbe {
    param([string]$Executable,[string[]]$NativeArguments)
    # Windows PowerShell 5.1 turns redirected native stderr into error records.
    # A nonzero result is expected for these existence checks; inspect the exit code.
    $ErrorActionPreference = 'Continue'
    $PSNativeCommandUseErrorActionPreference = $false
    $probeOutput = @(& $Executable @NativeArguments 2>$null)
    $probeExitCode = $LASTEXITCODE
    [pscustomobject]@{ Output=$probeOutput; ExitCode=$probeExitCode }
}
Get-Command git -ErrorAction Stop | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $taskRoot '.git'))) {
    $ancestor = Invoke-ReadOnlyProbe -Executable git -NativeArguments @('-C',$taskRoot,'rev-parse','--show-toplevel')
    if ($ancestor.ExitCode -eq 0) { throw "This folder is inside another repository: $($ancestor.Output). No nested repository was created." }
    Invoke-Git init -b main
}
$actualRoot = & git -C $taskRoot rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0 -or [IO.Path]::GetFullPath($actualRoot).TrimEnd('\') -ne $taskRoot) { throw 'Repository root does not match Notella.' }
$staged = & git -C $taskRoot diff --cached --name-only
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect existing staged files.' }
if ($staged) { throw 'Existing staged files found. Inspect them yourself before rerunning; this script will not clear your staging area.' }
$identityName = & git -C $taskRoot config user.name
$identityEmail = & git -C $taskRoot config user.email
if (-not $identityName -or -not $identityEmail) { throw 'Configure your Git author name and email, inspect them, then rerun.' }
if ($Push) {
    Get-Command gh -ErrorAction Stop | Out-Null
    $remoteProbe = Invoke-ReadOnlyProbe -Executable gh -NativeArguments @('repo','view','mikevan/Notella','--json','nameWithOwner')
    if ($remoteProbe.ExitCode -ne 0) {
        if (-not $CreateRemote) { throw 'Cannot access mikevan/Notella. Create it yourself, fix authentication, or explicitly add -CreateRemote to create it privately.' }
        & gh repo create mikevan/Notella --private --description 'Ontology-guided semantic LoRA training by Project Revive Solutions'
        if ($LASTEXITCODE -ne 0) { throw 'Private repository creation failed; no push attempted.' }
    }
    $heads = & git ls-remote --heads $remoteUrl
    if ($LASTEXITCODE -ne 0) { throw 'Could not read remote branches; no push attempted.' }
    $headProbe = Invoke-ReadOnlyProbe -Executable git -NativeArguments @('-C',$taskRoot,'rev-parse','--verify','HEAD')
    $localHasHead = $headProbe.ExitCode -eq 0
    if ($heads -and -not $localHasHead) { throw 'Remote already has history. Clone/reconcile that history before an initial push; this script will not force or replace it.' }
    $originProbe = Invoke-ReadOnlyProbe -Executable git -NativeArguments @('-C',$taskRoot,'remote','get-url','origin')
    $origin = $originProbe.Output -join "`n"
    if ($originProbe.ExitCode -eq 0) {
        if ($origin -notin @($remoteUrl,'https://github.com/mikevan/Notella','git@github.com:mikevan/Notella.git')) { throw "Existing origin differs: $origin. Inspect it yourself; this script will not change it." }
    } else { Invoke-Git remote add origin $remoteUrl }
}
# Explicit allowlist only. Never use git add . or force-add ignored files.
Invoke-Git add -- @paths
Invoke-Git diff --cached --check
$stagedPaths = @(& git -C $taskRoot diff --cached --name-only)
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the prepared index.' }
if (-not $stagedPaths.Count) { Write-Host 'No new checkpoint changes to commit.' }
else {
    foreach ($path in $stagedPaths) { if ($path -notin $paths) { throw "Unexpected staged path: $path" } }
    Invoke-Git diff --cached --stat
    Invoke-Git commit -F (Join-Path $taskRoot 'checkpoint\CHECKIN.md')
}
if ($Push) {
    $branch = & git -C $taskRoot branch --show-current
    if (-not $branch) { throw 'Detached HEAD: choose a branch yourself before publishing.' }
    Invoke-Git push --set-upstream origin $branch
    $localSha = & git -C $taskRoot rev-parse HEAD
    $remoteHead = & git ls-remote origin "refs/heads/$branch"
    if ($LASTEXITCODE -ne 0 -or -not $remoteHead.StartsWith($localSha + "`t")) { throw 'Remote verification failed; inspect the remote before retrying.' }
    Write-Host "Verified $localSha on origin/$branch."
}
Write-Host 'Checkpoint handled. Unlisted files remain outside this commit.'
