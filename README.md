# nmaper
Simple python script that automates Nmap scans: quick port discovery + detailed analysis on open ports.

Goal of this script is to automatize the nmap commands I always use.

## Use Case

**nmaper** is a simple Python script to automate Nmap scans in two steps:

1. Quick scan to detect open ports
```sh
nmap <IP> -Pn --open
```
2. In-depth scan with service, version, and OS detection only on the open ports found:
```sh
nmap <IP> -Pn -p PORT1,PORT2,... -A -oN nmap_<IP>.txt
```

## Usage

```
nmaper.py IP/FILE [OPTIONS]

OPTIONS:
    ALL     : Scan all ports (-p-)
    (all other valid Nmap options are also accepted directly)
```

### Examples

- Scan a single target with the default quick and in-depth scan
```sh
nmaper.py 192.168.1.1
```
- Scan all ports of a target (`-p-`)
```sh
nmaper.py 192.168.1.1 ALL
```
- Use nmaper with custom options (fast UDP scan)
```sh
nmaper.py 192.168.1.1 -sU -T4
```
- Scan multiple targets listed in a file:
```sh
nmaper.py targets.txt
```

## Install

To make `nmaper` accessible globally in your terminal, follow these steps:
1. Copy `nmaper.py` to `/opt` and make it executable:
```sh
sudo cp nmaper.py /opt/
sudo chmod +x /opt/nmaper.py
```
- Create a small wrapper script in `/usr/local/bin/nmaper`:
```sh
#!/bin/bash
/opt/nmaper.py "$@"
```
- Make the wrapper executable:
```sh
sudo chmod +x /usr/local/bin/nmaper
```

## Features
- Accepts a **single IP** or a **file with multiple targets**
- Smart two-step scan:
    - 1st pass: detect open ports (`--open`)
    - 2nd pass: in-depth scan with detection (`-A`) only on detected ports
- Only the `ALL` option is handled internally
- All other valid Nmap options can be passed directly
- Color-coded output for readability
- Automatically saves results to `.txt` files

This script is an improved version inspired by [OlivierProTips/nmaper](https://github.com/OlivierProTips/nmaper):