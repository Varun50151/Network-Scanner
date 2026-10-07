# Network Security Scanner

A multithreaded network scanner I built in Python. It finds live hosts, scans ports, grabs banners, fingerprints operating systems, runs Nmap's vulnerability scripts, and emails you the results when it's done.

I started this to get hands-on with how scanners like Nmap work under the hood, then kept adding to it. Running 100 threads through `ThreadPoolExecutor` made port scans about 50x faster than my first sequential version.

## What it does

- **Host discovery:** sends ARP requests with Scapy to find live hosts on a network range
- **Port scanning:** scans any TCP port range concurrently
- **Banner grabbing:** connects to open ports and reads the service banner to see what's running
- **Vulnerability scanning:** uses Nmap (`-O -sV --script=vuln`) for OS detection, service versions and known CVEs
- **Email reports:** sends the results to your inbox over Gmail SMTP
- **CLI menu:** a simple colour-coded terminal menu (colorama)

A full scan report includes open ports and their services, banners, hostnames, the detected OS (with Nmap's confidence percentage), any vulnerabilities found, and the scan time and duration.

## Project structure

```
network-scanner/
├── scanner.py          # main CLI and scanning logic
├── Email_sender.py     # sends the report over SMTP
├── Host_scanner.py     # ARP host discovery
├── message.txt         # default email message template
├── password.txt        # not included, see setup below
├── .gitignore
└── README.md
```

## Getting started

Install the Python dependencies:

```bash
pip install python-nmap scapy colorama
```

You'll also need Nmap installed on your machine (https://nmap.org/download.html). The vulnerability scan needs root/admin privileges, so run it with `sudo` on Linux or macOS, or from an admin terminal on Windows.

### Email setup

1. Create a `password.txt` file in the project root with your Gmail app password in it. It's already gitignored, so it won't get committed.
2. Generate the app password at https://myaccount.google.com/apppasswords
3. Change the sender address in `Email_sender.py` to your own.

### Running it

```bash
python scanner.py
```

It asks for your email address first, then shows the menu:

```
1. Host Discovery
2. Port Scan
3. Full Network Scan
4. Exit
```

## How it works

### Port scanning

Every port in the range gets submitted to a thread pool as its own task:

```python
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(single_port_scan, target, port)
               for port in range(start_port, end_port + 1)]
```

Most of the time in a port scan is spent waiting on connections to time out, so doing them in parallel instead of one after another is where the speedup comes from.

### Vulnerability detection

The full scan hands the target to Nmap with `-O -sV --script=vuln`. That gives me the OS guess and accuracy, service versions, and any CVEs Nmap's scripts match against them.

## Libraries used

| Library | Used for |
|---|---|
| `python-nmap` | port scanning, OS detection, vuln scripts |
| `scapy` | ARP host discovery |
| `socket` | TCP connections and banner grabbing |
| `concurrent.futures` | the thread pool |
| `smtplib` | sending the email report |
| `colorama` | terminal colours |
| `datetime` | timestamps and scan duration |

## Disclaimer

This is for learning and for testing networks you own or have written permission to test. Scanning anything else is illegal, so please don't.

## Author

Varun Ramesh
- GitHub: [@Varun50151](https://github.com/Varun50151)
- LinkedIn: [linkedin.com/in/varun-ramesh-8b4314290](https://linkedin.com/in/varun-ramesh-8b4314290)
