# Flash Next: prepare your own experiment and understand its limits

This new learning kit documents our historical Windows/Strix Halo experiment. It is not a fresh installation or model test and does not certify every64GB system. New MOSS films are still pending. No model weights, runtime, drivers or private photos are included.

1. Extract the complete ZIP into a new folder. Read BUILD-SOURCE.json, PROFILE-32K.json and the official model licence first.
2. The archived device was a Windows GMKtec EVO-X2 with Ryzen AI Max+395, Radeon8060S,64GB shared memory and NVMe storage. Record your own hardware, driver, available RAM and SSD space. Other Radeon PCs and Macs were not verified with this setup.
3. Open the official release page from BUILD-SOURCE.json. b10867 is a pinned prerelease. For this specific historical path use its Windows Vulkan asset, not an unrelated latest CUDA,CPU or Linux package. Downloading it is your own deliberate step.
4. Check a downloaded ZIP with Get-FileHash -Algorithm SHA256. Expected: bd9a55f96bbfa0241b6321bd0ba8a62bf48f3a80b32c182977a143e4e65131da. Only after a match, extract the complete archive into a new runtime folder. Our existing ZIP and all52 contained files were compared and match byte for byte.
5. Read the official Qwen model terms and the selected quantization before downloading any weights. Put all three UD-IQ4_XS GGUF parts in the same models folder. Historically their total size was about93.7GB. Disk size is neither total RAM usage nor proof of stability. Check changes in the provider inventory.
6. The model card distinguishes125B language-model parameters,6B active parameters,51B N-gram embedding and4B MTP. The rounded177B historical main-model figure is not180B including all components. Active parameters do not mean only6B need to be stored.
7. In your own runtime folder inspect .\llama-server.exe --version and --help. The saved --load-mode and --lazy-mode flags must be supported. --n-cpu-moe16 means CPU computation for16MoE layers, not16individual experts. KV-cache quantization and GGUF weight quantization are separate settings.
8. VORBEREITEN-FLASH.ps1 only writes a copyable command, the chosen profile and the hash of your existing executable. It performs no download, execution or HTTP request. Example from the companion folder:

```powershell
.\VORBEREITEN-FLASH.ps1 -Installation "C:\your\flash-runtime" -FirstModelPart "C:\your\flash-runtime\models\Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf" -OutputDirectory "C:\your\Flash-Preparation-1"
```

9. Open STARTBEFEHL.txt as text. Check every path, flash-next-32k alias,32768context and8091port. Input, conversation and output all use context. The100K archive profile is not a faster default. Change only one setting at a time.
10. Coordinate conflicting model jobs before starting your own experiment. Never stop someone else's processes. Check current identity, ports,GPU, free RAM,SSD space and queues. Some historical tasks passed with less than1MB of free physical RAM. That is not a healthy general memory reserve. Merely starting a model does not establish a useful application.
11. Only then manually run the prepared command in your own terminal. Keep it open, preserve actual errors and monitor memory. Under severe memory pressure stop your own experiment in a controlled way. This kit does not claim any fresh BIOS or driver changes.
12. PRUEFE-EIGENEN-SERVER.ps1 sends two read-only GETs to localhost8091 and saves HEALTH.json and MODELS.json in a new folder. It sends no model query. If the server is not ready, inspect the error and terminal instead of starting another instance automatically.
13. Open http://127.0.0.1:8091 in your browser. For an OpenAI-compatible client use http://127.0.0.1:8091/v1 and the actual model ID from MODELS.json. An API connection does not itself grant file or tool access. Our Vulkan/client tutorial explains that separate stage.
14. Start with a short question. EIGENE-FRAGE-EN.txt provides a fictional source-selection and arithmetic exercise. Preserve your actual answer unchanged, then compare with SOLL-DE-EN.md and fill in DEIN-TEST.csv. This new exercise was not run with Flash Next here.
15. ARCHIVE-METRICS.json preserves all six historical rows. Four selected32K tasks recorded10.22/11.33/9.40/11.73output tokens per second; a separate wiki task is also retained. Those rates are not time to first visible answer or total waiting time. The long test recorded86,135input tokens,7/7checks,6.48output tokens per second and8952.5seconds total time. Nearly two and a half hours are a central part of the result.
16. Report hardware,version,profile,waiting time,errors and your actual answer. Someone else's128GB Linux measurements or closed unmerged optimisation proposals do not establish new performance on our64GB Windows device. This kit provides a verifiable personal learning path. Complete listening to the new films and fresh practical testing remain pending.
