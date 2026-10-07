[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$Installation,
 [Parameter(Mandatory=$true)][string]$FirstModelPart,
 [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference='Stop'
$installPath=(Resolve-Path -LiteralPath $Installation).Path
$modelPath=(Resolve-Path -LiteralPath $FirstModelPart).Path
$exePath=Join-Path $installPath 'llama-server.exe'
if (-not (Test-Path -LiteralPath $exePath -PathType Leaf)) { throw 'llama-server.exe missing' }
if ([IO.Path]::GetFileName($modelPath) -ne 'Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf') { throw 'Use the exact first part named in PROFILE-32K.json' }
$modelDirectory=Split-Path -LiteralPath $modelPath
foreach ($part in 1..3) {
 $partPath=Join-Path $modelDirectory ('Qwen3.8-Flash-Next-UD-IQ4_XS-{0:00000}-of-00003.gguf' -f $part)
 if (-not (Test-Path -LiteralPath $partPath -PathType Leaf)) { throw ('Missing model part: '+$partPath) }
}
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Choose a NEW output directory; no overwrite' }
$profile=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'PROFILE-32K.json') -Raw | ConvertFrom-Json
$arguments=@('-m',$modelPath)+@($profile.arguments)
# Quote for PowerShell as literal single-quoted strings; doubling quotes prevents interpolation.
$quoted=@($exePath)+$arguments | ForEach-Object { "'"+$_.Replace("'","''")+"'" }
$command='& '+($quoted -join ' ')
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$encoding=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'STARTBEFEHL.txt'),$command+"`n",$encoding)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'PROFILE.json'),($profile | ConvertTo-Json -Depth 20)+"`n",$encoding)
[IO.File]::WriteAllText((Join-Path $OutputDirectory 'VORBEREITUNG.json'),(@{prepared_only=$true;http_requests=0;server_started=$false;model_loaded=$false;executable=$exePath;executable_sha256=(Get-FileHash -LiteralPath $exePath -Algorithm SHA256).Hash.ToLower();first_model_part=$modelPath} | ConvertTo-Json -Depth 8)+"`n",$encoding)
Write-Output 'Prepared only. Read START.md and check resources/version/model licence before manually using STARTBEFEHL.txt. No HTTP, downloads or execution performed.'
