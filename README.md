# AIBrainstorming

![placeholder](docs/brainstorming_placeholder.png)

Brainstorming automatizado entre varios modelos de IA de Ollama.

## Descripción
Este proyecto permite simular una discusión entre varios modelos de inteligencia artificial usando Ollama. El usuario define el tópico y puede pasar un contexto diferente para cada modelo desde la línea de comandos. Además, puedes participar como humano en el debate.

## Características principales
- Solo se mantienen instalados los modelos especificados en `--instalar-modelos`.
- Si un modelo ya está instalado, no se vuelve a descargar.
- Cada modelo puede tener su propio contexto, pasado por línea de comandos.
- El prompt (tópico y reglas) es igual para todos.
- Puedes participar como humano en el debate usando la opción `--humano`.
- El turno inicial es aleatorio y la conversación alterna entre todos los participantes.
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
   python AIBrainstorming.py --contextos "Contexto para modelo1" "Contexto para modelo2" --topico "Tópico del brainstorming" --instalar-modelos modelo1 modelo2 [--humano] [--nombre-humano "TuNombre"]
   ```
   > **Importante:** El orden de los contextos debe coincidir exactamente con el orden de los modelos en `--instalar-modelos`. Antes de iniciar el debate, el script mostrará la correspondencia entre cada modelo y su contexto para que puedas verificarlo.
   Puedes usar la opción `--auto` para avanzar automáticamente y `--pausa` para definir la pausa entre mensajes.

## Ejemplo
```sh
python AIBrainstorming.py --contextos "Contexto físico" "Contexto matemático" --topico "¿Qué interpretación es más útil para la enseñanza?" --instalar-modelos deepseek-llm:7b-chat llama3.2 --humano --nombre-humano "Fenix"
```

## Requisitos
- Python 3.11
- Conda
- Ollama instalado y modelos configurados localmente
- requests

## Notas
- Solo se mantienen instalados los modelos especificados en `--instalar-modelos`.
- Si un modelo ya está instalado, no se vuelve a descargar.
- Cada modelo puede tener su propio contexto.
- Puedes participar como humano en el debate.
- El debate finaliza automáticamente cuando todos los modelos responden exactamente con la frase: `estoy definitivamente de acuerdo`.
- Puedes detener la discusión en cualquier momento con Ctrl+C.

## Disclaimer

Las pruebas de este proyecto se realizaron en una laptop con Linux. No se pudo testear el funcionamiento con más de dos modelos simultáneos debido a limitaciones de hardware. El rendimiento y la estabilidad pueden variar según los recursos disponibles en tu equipo.

## Autor
- mako16

## Licencia
MIT
