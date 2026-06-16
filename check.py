import requests
import json

worldstate = requests.get("https://api.warframestat.us/pc").json()

print("=== TODAS LAS FISSURES HARD MODE ===")

for fissure in worldstate.get("fissures", []):
    if fissure.get("isHard"):
        print(json.dumps(fissure, indent=2))
        print("-" * 50)
