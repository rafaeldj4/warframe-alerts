import os
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

worldstate = requests.get(
    "https://api.warframestat.us/pc"
).json()

messages = []

for fissure in worldstate.get("fissures", []):

    node = fissure.get("node", "")
    mission = fissure.get("missionType", "")
    tier = fissure.get("tier", "")
    hard = fissure.get("isHard", False)

    # Helene Steel Path Fissure
    if hard and "Helene" in node:
        messages.append(
            f"🚨 HELENE STEEL PATH FISSURE\n"
            f"📍 {node}\n"
            f"🎯 {mission}\n"
            f"🔮 {tier}"
        )

    # Mostrar Omnia para depuración
    if hard and tier == "Omnia":
    messages.append(
        f"🔮 OMNIA DETECTADA\n"
        f"📍 {node}\n"
        f"🎯 {mission}"
    )

for msg in messages:
    requests.post(
        WEBHOOK_URL,
        json={"content": msg}
    )

print("Revision completada")
