#!/usr/bin/env python3
# ===================== AIBrainstorming =====================
# Este script permite simular un brainstorming entre varios modelos de IA usando Ollama.
# - Solo se mantienen instalados los modelos especificados por el usuario, los demás se eliminan para optimizar recursos.
# - Si un modelo ya está instalado, no se vuelve a descargar.
# - Cada modelo responde como un especialista humano en el tema, nunca como IA.
# - El turno inicial es aleatorio y la conversación alterna entre todos los modelos.
# - El contexto y tópico se pasan como argumentos y se incluyen en cada turno.
# - El usuario puede detener la discusión en cualquier momento con Ctrl+C.
# ===========================================================

import argparse
import requests
import json
import time
import os
import subprocess
import random

# -----------------------------------------------------------
# Función para eliminar modelos no usados
# Elimina de Ollama todos los modelos que no estén en la lista de modelos_usados
# para liberar memoria y espacio, pero solo si no están en la lista de modelos requeridos.
# -----------------------------------------------------------
def eliminar_modelos_no_usados(modelos_usados):
    """
    Elimina de Ollama todos los modelos que no estén en la lista de modelos_usados para liberar memoria y espacio,
    pero solo si no están en la lista de modelos requeridos por el usuario.
    Usa regex para coincidencia exacta de nombre base y versión/tag si corresponde.
    """
    import re
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        modelos_actuales = [line.split()[0] for line in result.stdout.strip().split('\n')[1:] if line]
        # Construir patrones regex para todos los modelos requeridos (nombre y opcionalmente tag)
        patrones = []
        for m in modelos_usados:
            if ':' in m:
                nombre, tag = m.split(':', 1)
                patrones.append(re.compile(rf'^{re.escape(nombre)}(:{re.escape(tag)})?$'))
            else:
                patrones.append(re.compile(rf'^{re.escape(m)}(:[\w\.-]+)?$'))
        for modelo in modelos_actuales:
            keep = any(pat.match(modelo) for pat in patrones)
            if not keep:
                print(f"Eliminando modelo no usado: {modelo}")
                subprocess.run(['ollama', 'rm', modelo])
            else:
                print(f"Modelo requerido '{modelo}' ya está instalado y se mantiene.")
    except Exception as e:
        print(f"Advertencia: No se pudieron eliminar modelos no usados: {e}")

# -----------------------------------------------------------
# Función para instalar modelos requeridos
# Instala solo los modelos que no están ya instalados en Ollama.
# -----------------------------------------------------------
def instalar_modelos(modelos):
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        modelos_actuales = [line.split()[0] for line in result.stdout.strip().split('\n')[1:] if line]
        for modelo in modelos:
            nombre_base = modelo.split(":")[0]
            if nombre_base not in modelos_actuales:
                print(f"Instalando modelo '{modelo}'...")
                subprocess.run(['ollama', 'pull', modelo])
            else:
                print(f"Modelo '{modelo}' ya está instalado.")
    except Exception as e:
        print(f"Advertencia: No se pudo verificar/instalar modelos: {e}")

# -----------------------------------------------------------
# Función para consultar Ollama (stream)
# Procesa la respuesta en modo stream para evitar errores de JSON extra data.
# -----------------------------------------------------------
def consultar_ollama(modelo, mensajes):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": modelo,
        "messages": mensajes,
        "stream": True
    }
    respuesta = ""
    try:
        with requests.post(url, json=data, stream=True) as r:
            for linea in r.iter_lines():
                if linea:
                    obj = json.loads(linea.decode("utf-8"))
                    if "message" in obj and "content" in obj["message"]:
                        respuesta += obj["message"]["content"]
        return respuesta.strip()
    except Exception as e:
        print(f"Error al consultar Ollama: {e}")
        return None

# -----------------------------------------------------------
# Función para liberar modelo tras cada turno
# Llama al endpoint /api/stop de Ollama para intentar liberar el modelo activo de memoria.
# -----------------------------------------------------------
def liberar_modelo():
    try:
        requests.post("http://localhost:11434/api/stop")
    except Exception as e:
        print(f"Advertencia: No se pudo liberar el modelo: {e}")

# -----------------------------------------------------------
# Función para mostrar la interacción de cada ronda
# -----------------------------------------------------------
def mostrar_discusion(historial, ronda, pausa, auto, modelos=None):
    print(f"\n{'='*20} RONDA {ronda} {'='*20}")
    ronda_historial = historial[-1:]
    for h in ronda_historial:
        print(f"Modelo: {h['modelo']}\nRespuesta: {h['content']}\n{'-'*40}")
        if not auto:
            input("Presiona Enter para continuar...")
        else:
            time.sleep(pausa)
    # Mostrar consenso si todos respondieron
    if modelos is not None and len(historial) >= len(modelos):
        frases_consenso = [h['content'].strip().lower() for h in historial[-len(modelos):]]
        if all(fc == "estoy definitivamente de acuerdo" for fc in frases_consenso):
            print("\n¡Todos los especialistas han llegado a un consenso!")
            for idx, h in enumerate(historial[-len(modelos):]):
                print(f"{h['modelo']}: {h['content']}")
            exit(0)

# -----------------------------------------------------------
# Función para verificar si hay consenso
# -----------------------------------------------------------
def hay_consenso(historial, modelos):
    """
    Devuelve True si todos los modelos incluyen la frase de consenso (ignorando mayúsculas y si está dentro de otra frase) en la última ronda.
    """
    frase_consenso = "estoy definitivamente de acuerdo"
    if len(historial) < len(modelos):
        return False
    ultimas_respuestas = [h['content'].strip().lower() for h in historial[-len(modelos):]]
    return all(frase_consenso in r for r in ultimas_respuestas)

# -----------------------------------------------------------
# Lógica principal de la discusión entre especialistas
# -----------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brainstorming multi-modelo con Ollama")
    parser.add_argument("--contexto", required=True, help="Contexto general del brainstorming")
    parser.add_argument("--topico", required=True, help="Tópico específico a discutir")
    parser.add_argument("--instalar-modelos", nargs='+', required=True, help="Lista de modelos Ollama a usar")
    parser.add_argument("--pausa", type=float, default=1.5, help="Segundos de pausa entre turnos (solo con --auto)")
    parser.add_argument("--auto", action="store_true", help="Avanza automáticamente entre rondas")
    args = parser.parse_args()

    modelos = args.instalar_modelos
    instalar_modelos(modelos)            # Primero instala los modelos requeridos si falta alguno
    eliminar_modelos_no_usados(modelos)  # Luego elimina solo los modelos que no están en la lista de requeridos (nombre y tag exactos)

    # Instrucción para todos los modelos: deben debatir como especialistas humanos y usar la frase de consenso
    contexto_modelo = (
        f"{args.contexto}\n"
        "Debes debatir como un especialista humano en el tema, sin mencionar que eres un modelo de IA. "
        'Cuando estés totalmente de acuerdo con la propuesta del otro especialista, responde exactamente con la frase: "estoy definitivamente de acuerdo".'
    )
    participantes = modelos.copy()
    nombres = [f"Especialista {i+1}" for i in range(len(participantes))]
    # Mensaje inicial para el primer modelo
    mensaje_inicial = f"Contexto: {args.contexto}\nTópico: {args.topico}\nPor favor, propón tu mejor idea inicial."
    primer_modelo = participantes[0]
    historial = [{
        "role": "assistant",
        "modelo": primer_modelo,
        "content": consultar_ollama(primer_modelo, [
            {"role": "system", "content": contexto_modelo},
            {"role": "user", "content": mensaje_inicial}
        ])
    }]
    ronda = 1
    mostrar_discusion(historial, ronda, args.pausa, args.auto, participantes)

    orden = list(participantes)  # Copia del orden original de participantes
    while True:
        ronda += 1
        for i in range(1, len(orden)):
            modelo = orden[i]
            anterior = historial[-1]
            prompt = (
                f"Esta es la última propuesta del especialista anterior ({anterior['modelo']}):\n"
                f"{anterior['content']}\n"
                "Responde como un especialista humano, debatiendo el tema. "
                'Si estás totalmente de acuerdo, responde exactamente con la frase: "estoy definitivamente de acuerdo".'
            )
            mensajes = [
                {"role": "system", "content": contexto_modelo},
                {"role": "user", "content": prompt}
            ]
            respuesta = consultar_ollama(modelo, mensajes)
            historial.append({
                "role": "assistant",
                "modelo": modelo,
                "content": respuesta
            })
            mostrar_discusion(historial, ronda, args.pausa, args.auto, participantes)
            # Chequeo de consenso tras cada ronda completa
            if hay_consenso(historial, participantes):
                print("\n¡Todos los especialistas han llegado a un consenso!")
                for idx, h in enumerate(historial[-len(participantes):]):
                    print(f"{h['modelo']}: {h['content']}")
                exit(0)
        # Alterna el orden para la siguiente ronda
        orden = orden[1:] + orden[:1]