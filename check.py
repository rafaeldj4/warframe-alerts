import os
import json
import requests
from datetime import datetime

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
STATE_FILE = "state.json"

# Cargar estado
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {"sent_ids": []}

sent_ids = set(state.get("sent_ids", []))

# Obtener datos de Warframe
worldstate = requests.get(
    "https://api.warframestat.us/pc",
    timeout=30
).json()

messages = []

for fissure in worldstate.get("fissures", []):

    fissure_id = fissure.get("id")

    # Evitar alertas duplicadas
    if fissure_id in sent_ids:
        continue

    node = fissure.get("node", "")
    mission = fissure.get("missionType", "")
    tier = fissure.get("tier", "")
    hard = fissure.get("isHard", False)
    expiry_str = fissure.get("expiry", "")

    try:
        expiry = datetime.fromisoformat(
            expiry_str.replace("Z", "+00:00")
        )

        expiry_unix = int(expiry.timestamp())

    except Exception:
        continue

    # HELENE STEEL PATH
    print(
    f"Nodo={node} | Tipo={mission} | Tier={tier} | Hard={hard}"
)
    if hard and node == "Helene (Saturn)":

        messages.append(
            f"🚨 HELENE STEEL PATH DISPONIBLE\n"
            f"📍 Nodo: {node}\n"
            f"🎯 Tipo: {mission}\n"
            f"🔮 Reliquia: {tier}\n"
            f"⏰ Finaliza: <t:{expiry_unix}:F>\n"
            f"⏳ Restante: <t:{expiry_unix}:R>"
        )

        sent_ids.add(fissure_id)

    # OMNIA VOID CASCADE
    elif (
        hard
        and tier == "Omnia"
        and mission == "Void Cascade"
    ):

        messages.append(
            f"🔥 OMNIA VOID CASCADE DISPONIBLE\n"
            f"📍 Nodo: {node}\n"
            f"⏰ Finaliza: <t:{expiry_unix}:F>\n"
            f"⏳ Restante: <t:{expiry_unix}:R>"
        )

        sent_ids.add(fissure_id)

# Enviar alertas
print(f"Cantidad de alertas encontradas: {len(messages)}")

for msg in messages:

    print("=== ALERTA ===")
    print(msg)

    response = requests.post(
        WEBHOOK_URL,
        json={"content": msg},
        timeout=30
    )

    print(f"Discord status: {response.status_code}")
    print(response.text)

# Mantener historial limitado
sent_ids = list(sent_ids)[-500:]

# Guardar estado
with open(STATE_FILE, "w") as f:
    json.dump(
        {
            "sent_ids": sent_ids
        },
        f,
        indent=2
    )

print("Revision completada")
