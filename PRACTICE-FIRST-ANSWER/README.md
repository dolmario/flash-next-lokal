# Flash Next on a Strix Halo mini PC

Use a local model to turn three source notes into a short card or tutorial description. This practice folder supplies a pinned Windows runtime installer, model-file manifest, compact startup profile and an executable API example. The model files stay separate.

## Install the runtime

Open PowerShell in this extracted folder. Python3.12 must already be available (`py -3.12 -V`). The launcher uses the standard library.

```powershell
.\INSTALL-RUNTIME.ps1 -Destination .\my-flash-runtime
```

The installer downloads the official pinned Vulkan archive, checks itsSHA256 and retains the matching libraries. It leaves your working directory unchanged.

## Select the model files

This example uses the three UD-IQ4_XS parts, approximately94GB on disk. Keep all three in one folder. MODELS.json links a pinned revision and gives every complete file hash. Existing verified model files can be reused. To download into a new folder:

```powershell
.\DOWNLOAD-MODELS.ps1 -Destination .\models
```

The model uses Qwen's own conditions; follow the model links before downloading. Runtime/model weights are not included in this kit.

## Start your local chat

```powershell
py -3.12 run_flash.py --runtime .\my-flash-runtime\runtime --models C:\Models\Flash-Next-IQ4_XS --output my-first-chat
```

Open http://127.0.0.1:18194. In Settings > Tools, disable the optional Browser tools for a short question using only the supplied notes, save settings and start a new chat. Paste the content from EXAMPLE-REQUEST.json, then Send. Ask for one natural description sentence as a follow-up. Stop the server with Ctrl+C in its starting window when finished.

The compact profile uses4K context,32CPU MoE layers, file mapping,64/32batch sizes, disabled weight repacking and disabled extra prompt-state cache/checkpoints. PROFILE.json contains the exact command arguments.16/32here count MoE layers, not individual experts.

## Run the source example from an application

```powershell
py -3.12 run_flash.py --runtime .\my-flash-runtime\runtime --models C:\Models\Flash-Next-IQ4_XS --output my-source-test --test-and-exit
```

This checks every runtime/model file, starts its own loopback server, submits the source example, saves request/response/timings and stops that exact child. It refuses an occupied local model port and requires a new output directory. It never stops another process or edits system settings. Startup requires12GiB available Windows RAM; the SSD profile monitors physical memory and commit reserve separately while mapped files are in use.

## Earlier tests

ARCHIVE-METRICS.json and both earlier profile files keep the dated historical short and long tasks. These are different configurations. Output-token speed, loading time and the wait to process a long source are separate measurements. The recorded64GBWindows setup does not establish the same behaviour on every system.

Official runtime: https://github.com/ggml-org/llama.cpp/releases/tag/b10867
Model: https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF

## Deutsch

Dieses Praxispaket verbindet die Einrichtung mit einer konkreten Quellenfrage und dem API-Beispiel. Runtime und dreiModelldateien bleiben getrennt. INSTALL-RUNTIME.ps1 lädt das festgelegte offizielle Archiv. Verwende vorhandene geprüfte GGUF-Dateien oder lade die dreiTeile mit DOWNLOAD-MODELS.ps1. run_flash.py startet den eigenen lokalen Server; --test-and-exit schreibt Anfrage/Antwort/Zeiten und beendet genau diesen Prozess. Die historischen Tests verwenden andereProfile und behalten ihreDatierung.
