import ollama
import time
import argparse

# Argumentos de línea de comandos
parser = argparse.ArgumentParser(description="Brainstorming entre dos modelos de IA de Ollama")
parser.add_argument('--contexto', type=str, required=True, help='Contexto general para ambos modelos')
parser.add_argument('--topico', type=str, required=True, help='Tópico o pregunta central del brainstorming')
parser.add_argument('--turnos', type=int, default=6, help='Cantidad de turnos de discusión (debe ser par)')
args = parser.parse_args()

model_a = "llama3.2"       # Creativa
model_b = "mixtral"        # Crítica / técnica
num_turnos = args.turnos if args.turnos % 2 == 0 else 6

# Roles
sistema_a = f"Eres una IA muy creativa y entusiasta enfocada en ideas disruptivas para el futuro. Contexto: {args.contexto}"
sistema_b = f"Eres una IA crítica y realista que analiza ideas desde la viabilidad y el impacto a largo plazo. Contexto: {args.contexto}"

conversacion = []

print("🔄 Iniciando brainstorming entre dos IAs...\n")
print("🎯 Tópico:", args.topico, "\n")
print("📚 Contexto:", args.contexto, "\n")

# Turnos alternos de discusión
for i in range(num_turnos):
    es_turno_a = (i % 2 == 0)
    model = model_a if es_turno_a else model_b
    sistema = sistema_a if es_turno_a else sistema_b
    nombre = "IA Creativa" if es_turno_a else "IA Crítica"

    if i == 0:
        mensajes = [
            {"role": "system", "content": sistema},
            {"role": "user", "content": args.topico}
        ]
    else:
        mensajes = [
            {"role": "system", "content": sistema},
            {"role": "user", "content": conversacion[-1]["respuesta"]}
        ]

    respuesta = ollama.chat(model=model, messages=mensajes)

    conversacion.append({
        "turno": i + 1,
        "ia": nombre,
        "modelo": model,
        "respuesta": respuesta["message"]["content"]
    })

    print(f"🧠 {nombre} ({model}):\n{respuesta['message']['content']}\n")
    time.sleep(1)

# Ronda final: buscar consenso
print("🤝 Ronda final: Consenso entre IAs\n")
consenso_prompt = (
    f"Ambas IAs han discutido el siguiente tópico: '{args.topico}'. "
    f"Contexto: {args.contexto}. "
    "A continuación se muestran los últimos argumentos de cada IA. "
    "Como IA colaborativa, resume los puntos en común y propone una conclusión o acuerdo final." 
    f"\n\nÚltima respuesta IA Creativa: {conversacion[-2]['respuesta']}\n"
    f"Última respuesta IA Crítica: {conversacion[-1]['respuesta']}\n"
)

mensajes_consenso = [
    {"role": "system", "content": "Eres una IA mediadora experta en encontrar acuerdos y conclusiones colaborativas."},
    {"role": "user", "content": consenso_prompt}
]
consenso = ollama.chat(model=model_a, messages=mensajes_consenso)
print(f"🤖 Consenso final:\n{consenso['message']['content']}\n")

print("✅ Brainstorming finalizado.")