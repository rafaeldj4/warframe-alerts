import requests
import json

worldstate = requests.get("https://api.warframestat.us/pc").json()

print("=== STEEL PATH ===")
print(json.dumps(worldstate.get("steelPath", {}), indent=2))

print("\n=== ZARIMAN CYCLE ===")
print(json.dumps(worldstate.get("zarimanCycle", {}), indent=2))

print("\n=== ARBITRATION ===")
print(json.dumps(worldstate.get("arbitration", {}), indent=2))

print("\n=== FISSURES (PRIMERAS 5) ===")
print(json.dumps(worldstate.get("fissures", [])[:5], indent=2))
