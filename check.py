import os
import json
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

STATE_FILE = "state.json"

# Cargar estado previo
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {
        "sent_ids": []
    }

sent_ids = set(state.get("sent_ids", []))

worldstate = requests.get(
    "https://api.warframestat.us/pc",
    timeout=30
).json()

messages = []

for fissure in worldstate.get("fissures", []):

    fissure_id = fissure.get("id")

    node = fissure.get("node", "")
    mission = fissure.get("missionType", "")
    tier = fissure.get("tier", "")
    hard = fissure.get("isHard", False)
    expiry = fissure.get("expiry", "")

    # Ignorar si ya fue notificada
    if fissure_id in sent_ids:
        continue

    # Helene Steel Path
    if hard and "Helene" in node:
        messages.append(
            f"🚨 HELENE STEEL PATH FISSURE\n"
            f"📍 {node}\n"
            f"🎯 {mission}\n"
            f"🔮 {tier}\n"
            f"⏰ Expira: {expiry}"
        )
        sent_ids.add(fissure_id)

    # Omnia Steel Path
    elif hard and tier == "Omnia":
        messages.append(
            f"🔮 OMNIA DETECTADA\n"
            f"📍 {node}\n"
            f"🎯 {mission}\n"
            f"⏰ Expira: {expiry}"
        )
        sent_ids.add(fissure_id)

# Enviar alertas
for msg in messages:

    response = requests.post(
        WEBHOOK_URL,
        json={"content": msg},
        timeout=30
    )

    print(
        f"Enviada alerta: {response.status_code}"
    )

# Guardar estado
with open(STATE_FILE, "w") as f:
    json.dump(
        {
            "sent_ids": list(sent_ids)
        },
        f,
        indent=2
    )

print("Revision completada")
