import os
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

# Obtener estado de Warframe
worldstate = requests.get(
    "https://api.warframestat.us/pc"
).json()

messages = []

# Buscar Steel Path Incursions
incursions = worldstate.get("steelPath", {}).get("currentReward", {})
missions = worldstate.get("steelPath", {}).get("rotation", [])

for mission in missions:
    node = mission.get("node", "")

    if "Helene" in node:
        messages.append(
            f"🚨 HELENE EN STEEL PATH DISPONIBLE\n{node}"
        )

# Buscar Void Cascade
for mission in worldstate.get("missions", []):
    mission_type = mission.get("type", "")
    node = mission.get("node", "")

    if "Cascade" in mission_type:
        messages.append(
            f"🚨 VOID CASCADE DISPONIBLE\n{node}"
        )

# Enviar mensajes a Discord
for msg in messages:
    requests.post(
        WEBHOOK_URL,
        json={"content": msg}
    )

print("Revisión completada")
