# 🛡️ Network Security Scanner

A high-performance, multithreaded network security tool built in Python — capable of host discovery, port scanning, banner grabbing, OS fingerprinting, vulnerability detection, and automated email reporting.

---

## ⚡ Performance Highlight

> Achieved a **50x performance improvement** over sequential scanning through concurrent execution using `ThreadPoolExecutor` with 100 workers — designed with low-latency and high-throughput principles in mind.

---

## 🔧 Features

- **Host Discovery** — ARP-based live host detection across a network range using Scapy
- **Multithreaded Port Scanning** — Concurrent TCP port scanning across any port range
- **Banner Grabbing** — Retrieves service banners from open ports to identify running services
- **Vulnerability Scanning** — OS fingerprinting and CVE detection via Nmap scripting engine (`--script=vuln`)
- **Automated Email Reporting** — Sends structured scan reports directly to your inbox via SMTP (Gmail)
- **CLI Menu Interface** — Clean, colorama-enhanced terminal UI with modular architecture

---

## 📋 Scan Report Output

Each full network scan generates a structured report including:

- Open ports with service identification
- Banner information per port
- Detected hostnames
- OS name, family, and detection accuracy
- Vulnerability findings
- Scan duration and timestamp

---

## 🗂️ Project Structure

```
network-scanner/
│
├── scanner.py          # Main CLI application & core scanning logic
├── Email_sender.py     # SMTP email reporting module
├── Host_scanner.py     # ARP-based host discovery module
├── message.txt         # Default email message template
├── password.txt        # ⚠️ NOT included — see setup instructions
├── .gitignore          # Excludes sensitive files from version control
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install python-nmap scapy colorama
```

> **Note:** Nmap must be installed on your system: https://nmap.org/download.html
> Running vulnerability scans (`-sV --script=vuln`) requires **root/admin privileges**.

### Setup — Email Reporting

1. Create a `password.txt` file in the project root (this file is gitignored):
```
your_gmail_app_password_here
```
2. Generate a Gmail App Password at: https://myaccount.google.com/apppasswords
3. Update the sender email in `Email_sender.py` if needed

### Run

```bash
python scanner.py
```

You will be prompted to enter your email, then choose from:

```
1. Host Discovery
2. Port Scan
3. Full Network Scan
4. Exit
```

---

## 🧠 How It Works

### Multithreaded Port Scanner

```python
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(single_port_scan, target, port)
               for port in range(start_port, end_port + 1)]
```

All ports are submitted as concurrent tasks to a thread pool. Results are collected as futures, eliminating the sequential wait time of traditional single-threaded scanners.

### Vulnerability Detection

Uses Nmap's `-O -sV --script=vuln` arguments to perform:
- OS detection with accuracy percentage
- Service version identification
- Known CVE vulnerability matching

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes and authorised network testing only**. Scanning networks or systems without explicit permission is illegal and unethical. Always ensure you have written authorisation before scanning any target.

---

## 🛠️ Technologies Used

| Library | Purpose |
|---|---|
| `python-nmap` | Port scanning, OS detection, vulnerability scripts |
| `scapy` | ARP-based host discovery |
| `socket` | Raw TCP connection and banner grabbing |
| `concurrent.futures` | Multithreaded execution (ThreadPoolExecutor) |
| `smtplib` | SMTP email delivery |
| `colorama` | Terminal colour formatting |
| `datetime` | Scan timestamps and duration tracking |

---

## 👤 Author

**Varun Ramesh**
- GitHub: [@Varun50151](https://github.com/Varun50151)
- LinkedIn: [linkedin.com/in/varun-ramesh-8b4314290](https://linkedin.com/in/varun-ramesh-8b4314290)
