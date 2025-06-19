# AIBrainstorming

![placeholder](docs/brainstorming_placeholder.png)

Brainstorming automatizado entre varios modelos de IA de Ollama, con interfaz visual Gradio.

## Descripción
Este proyecto permite simular una discusión entre varios modelos de inteligencia artificial usando Ollama, todo desde una interfaz web moderna y visual (Gradio). El usuario define el tópico y puede pasar un contexto diferente para cada modelo. Además, puedes participar como humano en el debate.

## Características principales
- Interfaz web moderna y fácil de usar (Gradio).
- Selección dinámica de modelos Ollama desde la web oficial.
- Cada modelo puede tener su propio contexto.
- Participación opcional de un humano en el debate.
- Visualización clara y colorida de la discusión y los logs.
- Solo se mantienen instalados los modelos seleccionados; los demás se liberan de memoria (RAM) automáticamente.
- Solo un modelo IA está cargado en memoria a la vez, optimizando recursos.
- El debate avanza automáticamente entre los modelos IA hasta que sea necesario esperar al humano o se alcance consenso.
- Límite de iteraciones configurable en `.env` (por defecto 10).
- Logs detallados y visualización de la conversación en HTML.

## Instalación y uso
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
4. (Opcional) Configura el límite de iteraciones en un archivo `.env`:
   ```sh
   echo "MAX_ITERACIONES=10" > .env
   ```
5. Ejecuta la interfaz Gradio:
   ```sh
   python AIBrainstorming_gradio.py
   ```
6. Abre el enlace local que te muestra Gradio en tu navegador y configura el brainstorming a tu gusto.

## Requisitos
- Python 3.11
- Conda
- Ollama instalado y modelos configurados localmente
- requests, gradio, beautifulsoup4, python-dotenv

## Gestión de modelos y memoria (importante)
- **Instalación y limpieza de modelos:**
  - Al iniciar un debate, solo se instalan los modelos seleccionados si no están presentes localmente (`ollama pull`).
  - Los modelos que no están seleccionados se liberan de la memoria RAM usando `ollama stop`, pero **no se borran del disco**. Así, solo el modelo en turno está cargado en RAM, optimizando recursos y evitando tener que volver a descargar modelos.
- **Diferencia entre `ollama stop` y `ollama rm`:**
  - `ollama stop <modelo>`: Libera el modelo de la memoria RAM, pero lo mantiene instalado localmente. Es rápido volver a cargarlo.
  - `ollama rm <modelo>`: Borra el modelo completamente del disco. Si luego lo necesitas, tendrás que volver a descargarlo.

## Optimización de recursos
- Solo un modelo IA está cargado en memoria a la vez durante el debate. Esto permite usar varios modelos en equipos con poca RAM.
- El cambio de modelo en memoria es automático y transparente para el usuario.
- Si se alcanza el límite de iteraciones sin consenso, la conversación se muestra hasta ese punto.

## Disclaimer

Las pruebas de este proyecto se realizaron en una laptop con Linux. El rendimiento y la estabilidad pueden variar según los recursos disponibles en tu equipo.

## Autor
- mako16

## Licencia
MIT
