[CmdletBinding()]
param([switch]$Execute,[switch]$Push)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
function Invoke-CheckpointGit {
 param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
 & git.exe -C $root @Arguments
 if ($LASTEXITCODE -ne 0) { throw "Git failed: $($Arguments -join ' ')" }
}
if ($Push -and -not $Execute) { throw '-Push requires -Execute.' }
$manifest = Get-Content (Join-Path $root 'checkpoint/semantic-v6-manifest.json') -Raw | ConvertFrom-Json
$head = Invoke-CheckpointGit rev-parse HEAD
if ($head -ne $manifest.parent) { throw 'HEAD differs from checkpoint parent. Review before regenerating.' }
$staged = @(Invoke-CheckpointGit diff --cached --name-only)
if ($staged.Count) { throw 'Existing staged changes: inspect them before proceeding.' }
foreach ($file in $manifest.files) {
 $full = [IO.Path]::GetFullPath((Join-Path $root $file.path))
 if (-not $full.StartsWith([IO.Path]::GetFullPath($root).TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid manifest path.' }
 if ((Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) { throw "Changed since preparation: $($file.path)" }
}
$paths = @($manifest.files | ForEach-Object { $_.path }) + 'checkpoint/semantic-v6-manifest.json'
Write-Host "Checkpoint: $($paths.Count) explicit files. Runtime and weights excluded."
$paths | ForEach-Object { Write-Host "  $_" }
Invoke-CheckpointGit diff --check
if (-not $Execute) { Write-Host 'Preview only. Publish with: .\Check-In-SemanticV6.ps1 -Execute -Push'; return }
if ($Push) {
 $origin = Invoke-CheckpointGit remote get-url origin
 if ($origin -notin @('https://github.com/mikevan/Notella.git','git@github.com:mikevan/Notella.git')) { throw 'Unexpected origin.' }
 $branch = Invoke-CheckpointGit branch --show-current
 if ($branch -ne 'main') { throw 'Expected main. Review the branch before publishing.' }
}
Invoke-CheckpointGit add -- @paths
Invoke-CheckpointGit diff --cached --check
$actual = @(Invoke-CheckpointGit diff --cached --name-only)
foreach ($path in $actual) { if ($path -notin $paths) { throw "Unexpected staged path: $path" } }
Invoke-CheckpointGit --no-pager diff --cached --stat
Invoke-CheckpointGit commit -F (Join-Path $root 'checkpoint/SEMANTIC-V6.md')
if ($Push) {
 Invoke-CheckpointGit push origin main
 $sha = Invoke-CheckpointGit rev-parse HEAD
 $remote = Invoke-CheckpointGit ls-remote origin refs/heads/main
 if (-not $remote.StartsWith($sha+"`t")) { throw 'Remote verification failed.' }
 Write-Host "Verified $sha on mikevan/Notella main."
}