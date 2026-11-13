# 🔴 VEXTH TOOL

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

**VEXTH TOOL** is a Python-based cybersecurity toolkit featuring a custom graphical interface inspired by the Matrix aesthetic.

It combines network analysis, OSINT capabilities, security testing tools and text utilities into a single interactive dashboard.

Designed with a red-on-black interface, keyboard navigation and real network operations, VEXTH TOOL provides a centralized environment for cybersecurity experimentation and authorized security assessments.

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

VEXTH TOOL features:

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

