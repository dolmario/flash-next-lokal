param([Parameter(Mandatory=$true)][string]$Destination)
$ErrorActionPreference='Stop'
$target=[IO.Path]::GetFullPath($Destination)
if(Test-Path -LiteralPath $target){throw 'Choose a new empty installation path.'}
New-Item -ItemType Directory -Path $target | Out-Null
$archive=Join-Path $target 'llama-b10867-bin-win-vulkan-x64.zip'
$url='https://github.com/ggml-org/llama.cpp/releases/download/b10867/llama-b10867-bin-win-vulkan-x64.zip'
Invoke-WebRequest -Uri $url -OutFile $archive
$expected='bd9a55f96bbfa0241b6321bd0ba8a62bf48f3a80b32c182977a143e4e65131da'
if((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Runtime checksum mismatch.'}
$runtime=Join-Path $target 'runtime'
Expand-Archive -LiteralPath $archive -DestinationPath $runtime
$server=Join-Path $runtime 'llama-server.exe'
& $server --version
if($LASTEXITCODE -ne0){throw 'Runtime version command failed.'}
Write-Output "Runtime ready: $runtime"
