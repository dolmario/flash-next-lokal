# Flash Next locally: a 177B model on a 64 GB AMD mini PC

How we ran the ~177B Flash Next model with llama.cpp and Vulkan on a GMKtec EVO-X2 (AMD Strix Halo, 64 GB shared memory), and how you can prepare the same setup.

| Language | Download | Read first |
|---|---|---|
| English | [FLASH-NEXT-EN.zip](https://raw.githubusercontent.com/dolmario/flash-next-lokal/main/FLASH-NEXT-EN.zip) | [EN/START.md](EN/START.md) |
| Deutsch | [FLASH-NEXT-DE.zip](https://raw.githubusercontent.com/dolmario/flash-next-lokal/main/FLASH-NEXT-DE.zip) | [DE/START.md](DE/START.md) |

**Measured on the EVO-X2** ([ARCHIVE-METRICS.json](ARCHIVE-METRICS.json)): 9.4–11.7 output tokens per second on four 32K tasks. A long run with 86,135 input tokens took about 8,952 seconds (almost 2.5 hours). Some tasks ran with less than 1 MB of free physical RAM, so this works, but right at the limit.

What you learn:
- which pinned llama.cpp build (b10867) and SHA256 to use,
- how the three GGUF parts, SSD space, shared memory and context size fit together,
- how to prepare the documented 32K profile (`VORBEREITEN-FLASH.ps1` writes the start command, it does not start a server) and check your own server (`PRUEFE-EIGENEN-SERVER.ps1`).

`--n-cpu-moe 16` means 16 MoE layers on the CPU, not 16 experts. Runtime, model weights and drivers are not included; official sources are in [QUELLEN.md](QUELLEN.md). Qwen's model licence applies.

## Deutsch

So lief das rund 177B große Flash-Next-Modell mit llama.cpp und Vulkan auf einem GMKtec EVO-X2 (AMD Strix Halo, 64 GB), und so bereitest du denselben Aufbau vor. Gemessen: 9,4–11,7 Ausgabetoken pro Sekunde bei vier 32K-Aufgaben; ein langer Lauf mit 86.135 Eingabetoken dauerte etwa 8.952 Sekunden (fast 2,5 Stunden); teils weniger als 1 MB freier physischer RAM. ZIP vollständig entpacken und [DE/START.md](DE/START.md) lesen. Runtime, Modellgewichte und Treiber sind nicht enthalten.
