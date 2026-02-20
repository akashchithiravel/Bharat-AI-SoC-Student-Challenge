# 🇮🇳 Offline, Privacy-Preserving Hindi Voice Assistant  
## Bharat AI-SoC Student Challenge  
### Problem Statement 1 – Embedded Offline Hindi Voice Assistant on Raspberry Pi

---

##  Project Overview

This project implements a fully offline Hindi Voice Assistant running on a **Raspberry Pi 4 (2GB RAM)**. The assistant processes Hindi voice commands locally using on-device Automatic Speech Recognition (ASR) and Text-to-Speech (TTS) without any cloud dependency.

The system performs:

-  Speech-to-Text using Vosk Hindi Model  
-  Intent Recognition using custom Python logic  
-  Text-to-Speech using eSpeak-NG  
-  Website launching  
-  Application launching  
-  Time and Date queries  
-  100% Offline processing  

All inference runs entirely on the Raspberry Pi CPU.

---

##  System Architecture

USB Microphone  
→ Audio Capture (sounddevice)  
→ Vosk Hindi ASR (Offline Speech Recognition)  
→ Intent Matching & Command Parsing  
→ Command Execution  
→ eSpeak-NG TTS  
→ 3.5mm Speaker Output  

---

##  Hardware Configuration

| Component | Specification |
|------------|---------------|
| SBC | Raspberry Pi 4 (2GB RAM) |
| OS | Raspberry Pi OS 64-bit |
| Microphone | USB Microphone |
| Audio Output | 3.5mm Jack Speaker |
| Processing | CPU Only |

---

##  Software Stack

| Component | Technology Used |
|------------|----------------|
| Language | Python 3 |
| Audio Input | sounddevice |
| ASR Engine | Vosk Hindi Model |
| TTS Engine | espeak-ng |
| Intent Logic | Custom Python |
| Fuzzy Matching | difflib.SequenceMatcher |


---

##  Project Folder Structure
```
project_root/
│
├── dev/
├── files/
├── hindi_model/ # Vosk Hindi ASR Model
├── venvc2s/ # Python Virtual Environment
├── voice_assistant/
│
├── ref.py # Main Assistant Script
└── README.md
```
---

##  Conclusion

This project demonstrates a fully functional, privacy-preserving Hindi Voice Assistant optimized for Raspberry Pi 4 (2GB RAM). The solution runs entirely offline and meets the performance and design goals of the Bharat AI-SoC Student Challenge.

