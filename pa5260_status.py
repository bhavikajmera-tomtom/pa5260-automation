import requests
import urllib3
import xml.etree.ElementTree as ET
urllib3.disable_warnings()

HOSTNAME = "10.21.129.28"
API_KEY = "LUFRPT1Sczg3V3IzdmF3U0JtME1hbWQvanhuaUxaU0E9ZlJjZG5SUitSWnU1M1A5ejRvVG5SUWFPSDJhMDdiWWgwSktKRzA2WDJHSGx5bmpiSEU5dnBUWXM1bmoxaW50aXdnMVBjUlNsazJDVXpQN282WGo4SVE9PQ=="

def query(cmd):
    r = requests.get(f"https://{HOSTNAME}/api/",
        params={"type": "op", "cmd": cmd, "key": API_KEY}, verify=False)
    return ET.fromstring(r.text)

def query_config(xpath):
    r = requests.get(f"https://{HOSTNAME}/api/",
        params={"type": "config", "action": "get", "xpath": xpath, "key": API_KEY}, verify=False)
    return ET.fromstring(r.text)

def val(tree, path, default="N/A"):
    node = tree.find(path)
    return node.text if node is not None and node.text else default

# ── System Info ─────────────────────────────────────────────
print("=" * 50)
print("  SYSTEM INFO")
print("=" * 50)
tree = query("<show><system><info></info></system></show>")
s = tree.find("result/system")
print(f"  Hostname   : {val(s, 'hostname')}")
print(f"  Model      : {val(s, 'model')}")
print(f"  PAN-OS     : {val(s, 'sw-version')}")
print(f"  Serial     : {val(s, 'serial')}")
print(f"  Uptime     : {val(s, 'uptime')}")
print(f"  IP Address : {val(s, 'ip-address')}")

# ── HA Status ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("  HA STATUS")
print("=" * 50)
tree = query("<show><high-availability><state></state></high-availability></show>")
enabled = val(tree, "result/enabled")
print(f"  HA Enabled : {enabled}")

# ── Interfaces ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("  INTERFACES (logical, with IP)")
print("=" * 50)
tree = query("<show><interface>all</interface></show>")
print(f"  {'Name':<15} {'Zone':<12} {'IP Address':<22} {'State'}")
print(f"  {'-'*15} {'-'*12} {'-'*22} {'-'*8}")
for entry in tree.findall("result/ifnet/entry"):
    name  = val(entry, "name")
    zone  = val(entry, "zone", "-")
    ip    = val(entry, "ip", "-")
    state = val(entry, "fwd", "-")
    if ip != "N/A" and ip != "-":
        print(f"  {name:<15} {zone:<12} {ip:<22} {state}")

# ── Sessions ────────────────────────────────────────────────
print("\n" + "=" * 50)
print("  SESSION TABLE")
print("=" * 50)
tree = query("<show><session><info></info></session></show>")
r = tree.find("result")
print(f"  Active sessions  : {val(r, 'num-active')}")
print(f"  TCP sessions     : {val(r, 'num-tcp')}")
print(f"  UDP sessions     : {val(r, 'num-udp')}")
print(f"  Total installed  : {val(r, 'num-installed')}")
print(f"  Max capacity     : {val(r, 'num-max')}")

# ── Routing Table ───────────────────────────────────────────
print("\n" + "=" * 50)
print("  ROUTING TABLE")
print("=" * 50)
tree = query("<show><routing><route></route></routing></show>")
print(f"  {'VR':<8} {'Destination':<20} {'Next Hop':<18} {'Interface':<15} {'Flags'}")
print(f"  {'-'*8} {'-'*20} {'-'*18} {'-'*15} {'-'*8}")
for entry in tree.findall("result/entry"):
    vr   = val(entry, "virtual-router")
    dest = val(entry, "destination")
    nh   = val(entry, "nexthop")
    intf = val(entry, "interface", "-")
    flags= val(entry, "flags","").strip()
    print(f"  {vr:<8} {dest:<20} {nh:<18} {intf:<15} {flags}")

print("\n" + "=" * 50)