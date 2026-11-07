# 🔴 VEXLTH TOOL

<p align="center">
  <strong>Advanced Network Analysis, OSINT & Cybersecurity Toolkit</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Interface-Pygame-red" />
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-lightgrey" />
  <img src="https://img.shields.io/badge/Status-Development-orange" />
</p>
---

## Overview

**VEXLTH TOOL** is a Python-based cybersecurity toolkit featuring a custom graphical interface inspired by the Matrix aesthetic.

It combines network analysis, OSINT capabilities, security testing tools and text utilities into a single interactive dashboard.

Designed with a red-on-black interface, keyboard navigation and real network operations, VEXLTH TOOL provides a centralized environment for cybersecurity experimentation and authorized security assessments.

## Features

### 🌐 NETWORK TOOLS

- **Network Scan** – Discover active hosts and accessible ports across a specified subnet.
- **Device Discovery** – Identify devices using ARP, mDNS and SSDP.
- **Traffic Analysis** – Capture and analyze network packets using Scapy.
- **Stress Testing** – Perform controlled HTTP request testing.
- **Netcat / Socat** – TCP connection testing and basic HTTP response inspection.
- **WiFi Security Testing** – WPA capture and wordlist-based password auditing.
- **Vulnerability Scanner** – Probe common network ports and retrieve available service banners.
- **Load Generator** – Multithreaded network load generation.

### 🔎 OSINT TOOLS

- **Domain / DNS / Web Infrastructure** – DNS records, IP resolution, TLS certificates and HTTP headers.
- **People / Username / Social** – Search for public profiles across multiple platforms.
- **Credentials & Breaches** – Check email breach information through Have I Been Pwned.
- **VirusTotal** – IP, domain and URL reputation analysis.
- **Abstract Email** – Email validation and deliverability information.
- **AbuseIPDB** – IP reputation and abuse reports.
- **URLScan** – Submit URLs for security analysis.
- **NumVerify** – Phone number validation and carrier information.

### 🛠️ UTILITIES

- Base64 Encode / Decode
- Base32 Encode / Decode
- Hex Encode / Decode
- URL Encode / Decode
- MD5 Hash
- SHA256 Hash
- ROT13
- Reverse String
- Password Strength Checker
- Character / Word / Line Counter

## Interface

VEXLTH TOOL features:

- Matrix-inspired digital rain boot animation.
- Custom red neon visual theme.
- Interactive HUD dashboard.
- Separate Network and OSINT panels.
- Dedicated Utilities section.
- Keyboard-based navigation.
- Multithreaded execution for selected operations.
- Real-time execution status and results.

## Requirements

- Python 3
- Pygame
- Internet connection for online services and network operations.

### Dependencies

Install the main dependencies:

```bash
pip install pygame requests dnspython
```

If it doesn't work, try:

```bash
python3 -m venv env
```

Then:

```bash
source env/bin/activate
```

After this, retry the main dependencies.

Optional dependency for packet analysis:

```bash
pip install scapy
```

Some tools also require external software:

- **Aircrack-ng** – WiFi security auditing.
- **Hashcat** – Password hash auditing.
- **cap2hccapx** – Optional capture conversion utility.

## Installation

Clone the repository:

```bash
git clone https://github.com
```

Enter the project directory:

```bash
cd VEXLTH-TOOL
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If a requirements file is not provided, install the dependencies manually:

```bash
pip install pygame dnspython
```

Launch the application:

```bash
sudo python3 vexlth_tool.py
```

## API Configuration

Some OSINT integrations require API keys.

VEXLTH TOOL supports the following API services:

| Service | Configuration key |
|---|---|
| VirusTotal | `virustotal` |
| Abstract API | `abstract` |
| AbuseIPDB | `abuseipdb` |
| URLScan | `urlscan` |
| NumVerify | `numverify` |
| Have I Been Pwned | `HIBP_API_KEY` environment variable |

For the first five services, create an `api_keys.json` file in the same directory as the Python script:

```json
{
    "virustotal": "YOUR_API_KEY",
    "abstract": "YOUR_API_KEY",
    "abuseipdb": "YOUR_API_KEY",
    "urlscan": "YOUR_API_KEY",
    "numverify": "YOUR_API_KEY"
}
```

For Have I Been Pwned, configure the `HIBP_API_KEY` environment variable.

**Important:** Never upload API keys, credentials or other sensitive information to a public GitHub repository.

## Controls

| Key | Action |
|---|---|
| ↑ / ↓ | Navigate menus and results |
| TAB | Switch dashboard panels / input fields |
| ENTER | Select and execute tools |
| BACKSPACE | Delete input characters |
| ESC | Go back or exit |
| Q | Quit / return to dashboard |
| SPACE | Skip to the intro credit screen |

## Security & Legal Disclaimer

VEXLTH TOOL is intended exclusively for educational purposes, cybersecurity research and authorized security assessments.

By using this software, you agree to:

- Only scan networks and systems you own or have explicit permission to test.
- Obtain authorization before performing security assessments.
- Never use the software to disrupt services or interfere with third-party infrastructure.
- Respect applicable laws, regulations and privacy requirements.
- Protect API keys, credentials and sensitive information.

Certain features, including WiFi password auditing and multithreaded load generation, can cause unauthorized access attempts or service disruption if misused.

**The author and contributors assume no responsibility for misuse, damage or illegal activities performed with this software.**

## Author

**VEXLTH TECH**

Cybersecurity | Network Analysis | OSINT | Python Development

TikTok: VEXLTH TECH

---

<p align="center">
  <strong>VEXLTH TOOL — Built by VEXLTH TECH</strong>
</p>

<p align="center">
  <i>Explore. Analyze. Understand.</i>
</p>
