import requests
import json

worldstate = requests.get(
    "https://api.warframestat.us/pc",
    timeout=30
).json()

for fissure in worldstate.get("fissures", []):

    if fissure.get("tier") == "Omnia":
        print(json.dumps(fissure, indent=2))
        print("=" * 80)
