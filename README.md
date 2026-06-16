# PA-5260 Automation

Python scripts to automate operational tasks on a Palo Alto Networks PA-5260 firewall via the PAN-OS REST API.

## Overview

This repo replaces manual GUI and CLI tasks with repeatable, version-controlled Python scripts. All scripts connect to the firewall over HTTPS using the PAN-OS XML API and display output in a clean, readable format.

## Scripts

| Script | What it does |
|---|---|
| `get_firewall_info.py` | System info — hostname, model, PAN-OS version, uptime |
| `get_security_rules.py` | List all security policies |
| `get_interfaces.py` | List all interfaces and their status |
| `get_ha_status.py` | Check HA enabled/disabled and state |
| `get_active_sessions.py` | Session table — active, TCP, UDP, max capacity |
| `get_routing_table.py` | Full routing table across all virtual routers |
| `pa5260_status.py` | All of the above in one clean dashboard |

## Requirements

- Python 3.x
- `requests` library
- `python-dotenv` library

Install dependencies:

```bash
pip install requests python-dotenv
```

## Setup

1. Clone the repo:

```bash
git clone https://github.com/bhavikajmera-tomtom/pa5260-automation.git
cd pa5260-automation
```

2. Create a `.env` file in the root folder:

```
PANOS_HOSTNAME=<your-firewall-ip>
PANOS_API_KEY=<your-api-key>
```

3. Generate your API key from the firewall:

```bash
curl -k "https://<firewall-ip>/api/?type=keygen&user=<username>&password=<password>"
```

Copy the value between `<key>...</key>` in the response.

> **Note:** The `.env` file is listed in `.gitignore` and will never be committed to GitHub.

## Usage

Run the full status dashboard:

```bash
python pa5260_status.py
```

Run individual scripts:

```bash
python get_firewall_info.py
python get_interfaces.py
python get_security_rules.py
python get_ha_status.py
python get_active_sessions.py
python get_routing_table.py
```

## Example Output

```
==================================================
  SYSTEM INFO
==================================================
  Hostname   : nl-ams-fwl-test
  Model      : PA-5260
  PAN-OS     : 11.1.2-h3
  Serial     : 012501002600
  Uptime     : 337 days, 4:09:46
  IP Address : 10.21.129.28

==================================================
  INTERFACES (logical, with IP)
==================================================
  Name            Zone         IP Address             State
  --------------- ------------ ---------------------- --------
  vlan.51         Lab          192.168.51.1/24        vr:VR_01
  vlan.2008       Untrust      192.168.200.22/29      vr:VR_01
  vlan.2009       Untrust      192.168.200.30/29      vr:VR_02

==================================================
  SESSION TABLE
==================================================
  Active sessions  : 5
  TCP sessions     : 2
  UDP sessions     : 0
  Total installed  : 2,038,870
  Max capacity     : 33,000,000
```

## Security

- Credentials are stored in `.env` — never hardcoded in scripts
- `.env` is excluded from Git via `.gitignore`
- Scripts use `verify=False` for self-signed firewall certificates (acceptable for management network use)

## Roadmap

- [ ] Ansible playbooks for config changes (address objects, security rules, NAT)
- [ ] GitHub Actions — scheduled daily health check
- [ ] Terraform provider for infrastructure-as-code firewall management
- [ ] Output to Slack / email alerts

## Author

Bhavik Ajmera — Network & Security Engineer, TomTom