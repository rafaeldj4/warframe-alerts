import os
import json
import requests
from datetime import datetime, timezone

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

worldstate = requests.get(
    "https://api.warframestat.us/pc",
    timeout=30
).json()

messages = []

for fissure in worldstate.get("fissures", []):

    node = fissure.get("node", "")
    mission = fissure.get("missionType", "")
    tier = fissure.get("tier", "")
    hard = fissure.get("isHard", False)

    expiry_str = fissure.get("expiry", "")

    try:
        expiry = datetime.fromisoformat(
            expiry_str.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        remaining_seconds = int(
            (expiry - now).total_seconds()
        )

        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60

        remaining_text = f"{hours}h {minutes}m"

    except Exception:
        remaining_text = "Desconocido"

    # Helene Steel Path
    if hard and "Helene" in node:
        messages.append(
            f"🚨 HELENE STEEL PATH FISSURE\n"
            f"📍 {node}\n"
            f"🎯 {mission}\n"
            f"🔮 {tier}\n"
            f"⏳ Restante: {remaining_text}"
        )

    # Omnia Steel Path
    elif hard and tier == "Omnia":
        messages.append(
            f"🔮 OMNIA DETECTADA\n"
            f"📍 {node}\n"
            f"🎯 {mission}\n"
            f"⏳ Restante: {remaining_text}"
        )

# Enviar alertas
for msg in messages:
    requests.post(
        WEBHOOK_URL,
        json={"content": msg},
        timeout=30
    )

print("Revision completada")
