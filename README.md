# AIBrainstorming

![placeholder](docs/brainstorming_placeholder.png)

Brainstorming automatizado entre varios modelos de IA de Ollama.

## Descripción
Este proyecto permite simular una discusión entre varios modelos de inteligencia artificial usando Ollama. El usuario define el contexto, el tópico y los modelos participantes desde la línea de comandos. Al iniciar, solo se mantienen instalados los modelos requeridos y se eliminan los demás para optimizar recursos. Cada modelo responde como un especialista humano en el tema, sin mencionar que es IA.

## Características principales
- Solo se mantienen instalados los modelos especificados en `--instalar-modelos`.
- Si un modelo ya está instalado, no se vuelve a descargar.
- Cada modelo responde como un especialista humano, nunca como IA.
- El turno inicial es aleatorio y la conversación alterna entre todos los modelos.
- El contexto y tópico se pasan como argumentos y se incluyen en cada turno.
- El usuario puede detener la discusión en cualquier momento con Ctrl+C.
- **El debate finaliza automáticamente cuando todos los modelos responden exactamente con la frase:**

  `estoy definitivamente de acuerdo`

## Uso
1. Clona el repositorio y entra al directorio:
   ```sh
   git clone https://github.com/mako16/AIBrainstorming.git
   cd AIBrainstorming
   ```
2. Crea y activa el entorno conda:
   ```sh
   conda create -n brainstorming python=3.11
   conda activate brainstorming
   ```
3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Ejecuta el script con tus propios argumentos:
   ```sh
   python AIBrainstorming.py --contexto "Contexto general" --topico "Tópico del brainstorming" --instalar-modelos modelo1 modelo2 ...
   ```
   Puedes usar la opción `--auto` para avanzar automáticamente y `--pausa` para definir la pausa entre mensajes.

## Ejemplo
```sh
python AIBrainstorming.py --contexto "Física cuántica y computación" --topico "¿Cómo podría la computación cuántica revolucionar la inteligencia artificial?" --instalar-modelos deepseek-llm:7b-chat llama3.2 mixtral --auto --pausa 2
```

## Requisitos
- Python 3.11
- Conda
- Ollama instalado y modelos configurados localmente
- requests

## Notas
- Solo se mantienen instalados los modelos especificados en `--instalar-modelos`.
- Si un modelo ya está instalado, no se vuelve a descargar.
- Cada modelo responde como un especialista humano, nunca como IA.
- El debate finaliza automáticamente cuando todos los modelos responden exactamente con la frase: `estoy definitivamente de acuerdo`.
- Puedes detener la discusión en cualquier momento con Ctrl+C.

## Disclaimer

Las pruebas de este proyecto se realizaron en una laptop con Linux. No se pudo testear el funcionamiento con más de dos modelos simultáneos debido a limitaciones de hardware. El rendimiento y la estabilidad pueden variar según los recursos disponibles en tu equipo.

## Autor
- mako16

## Licencia
MIT
