import requests
import json

worldstate = requests.get(
    "https://api.warframestat.us/pc"
).json()

print("=== CLAVES PRINCIPALES ===")
print(worldstate.keys())

print("\n=== STEEL PATH ===")
print(json.dumps(worldstate.get("steelPath", {}), indent=2)[:5000])

print("\n=== MISIONES ===")
print(json.dumps(worldstate.get("missions", []), indent=2)[:5000])
