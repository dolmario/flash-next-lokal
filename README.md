# Flash Next lokal: 177B auf 64 GB verstehen

Ein Lernpaket zum dokumentierten Windows-Vulkan-Versuch auf unserem GMKtec EVO-X2 mit Strix Halo. Du erhältst einen kontrollierbaren Weg vom passenden Runtime-Paket bis zur eigenen Quellenfrage, mit getrennten deutschen und englischen Anleitungen.

## Download und Einstieg

| Sprache | Download | Zuerst lesen |
|---|---|---|
| Deutsch | [FLASH-NEXT-DE.zip](https://raw.githubusercontent.com/dolmario/flash-next-lokal/main/FLASH-NEXT-DE.zip) | [DE/START.md](DE/START.md) |
| English | [FLASH-NEXT-EN.zip](https://raw.githubusercontent.com/dolmario/flash-next-lokal/main/FLASH-NEXT-EN.zip) | [EN/START.md](EN/START.md) |

ZIP komplett in einen neuen Ordner entpacken. `VORBEREITEN-FLASH.ps1` schreibt einen Startbefehl für deine vorhandenen Dateien und startet dabei keinen Server. `PRUEFE-EIGENEN-SERVER.ps1` prüft ausschließlich Health und Modellliste deines eigenen lokalen Servers. Beide Skripte wurden syntaxgeprüft; die Vorbereitung wurde mit absichtlich nicht ausführbarer EXE und leeren Modell-Sentineldateien getestet, einschließlich Schutz vor Überschreiben. Ein neuer Modelllauf oder Live-HTTP-Test wurde damit nicht ausgeführt.

## Was du hier lernst

- Die genaue b10867-Prerelease-Version und ihren öffentlichen SHA256 identifizieren. Unsere bestehende ZIP und alle 52 enthaltenen Dateien stimmen mit diesem Archiv überein.
- Drei GGUF-Teile, SSD-Bedarf, gemeinsam genutzten Speicher und Kontext auseinanderhalten.
- Ein dokumentiertes 32K-Profil vorbereiten und anschließend die eigene tatsächliche Antwort bewerten.
- Ausgabetoken pro Sekunde, gesamte Wartezeit und freien physischen RAM getrennt beurteilen.

## Das dokumentierte Ergebnis hat Grenzen

Die sechs archivierten Testzeilen sind in [ARCHIVE-METRICS.json](ARCHIVE-METRICS.json) erhalten. Vier ausgewählte 32K-Aufgaben ergaben 10,22 / 11,33 / 9,40 / 11,73 Ausgabetoken pro Sekunde. Der lange Versuch mit 86.135 Eingabetoken benötigte etwa 8.952,5 Sekunden insgesamt, also fast zweieinhalb Stunden. Einige Aufgaben bestanden bei weniger als 1 MB freiem physischem RAM. Das begründet keine allgemeine Betriebsfreigabe für 64-GB-Systeme.

`--n-cpu-moe 16` bezeichnet 16 MoE-Schichten auf der CPU, nicht 16 einzelne Experten. Rund 177B im historischen Hauptmodell sind von den 180B einschließlich MTP in der offiziellen Modellkarte zu unterscheiden. Die neue Quellenübung ist fiktiv und wurde hier nicht frisch mit Flash Next ausgeführt. Andere Radeon-PCs und Macs wurden nicht getestet.

Runtime, Modellgewichte und Treiber sind nicht im ZIP enthalten. Für einen eigenen Download gelten die Bedingungen der jeweiligen Anbieter; Qwen verwendet seine eigene Modelllizenz. [QUELLEN.md](QUELLEN.md) enthält die offiziellen Quellen und den festgehaltenen Versionsstand. Die neuen MOSS-Videos werden separat produziert; vollständiges Endhören bleibt offen.

## English

This kit teaches the documented Windows Vulkan experiment, from a pinned runtime and split GGUF files to your own source-selection exercise. Read [EN/START.md](EN/START.md) and extract the English ZIP completely. Preparation does not run a model. The archived long test took almost 2.5 hours, and some tasks left less than 1 MB of free physical RAM. Neither a successful start nor output-token speed proves general stability. No fresh model test, macOS verification, runtime or model weights are included. New MOSS videos are being produced separately.
