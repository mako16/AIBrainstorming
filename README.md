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
- Exportar la conversación a PDF con un solo clic (solo la conversación, formato bonito).
- Botón para detener la discusión y pedir a cada modelo un resumen final desde su punto de vista.
- Ahora el sistema utiliza RAG: antes de cada turno de modelo, busca información relevante en internet usando DuckDuckGo, extrae el texto de las páginas encontradas y lo resume con el propio modelo Ollama. Ese resumen se inyecta como contexto adicional para el debate.

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

## Instrucciones para Windows 11

1. Instala [Ollama para Windows](https://ollama.com/download) y asegúrate de que el comando `ollama` funcione en tu terminal.
2. Instala Python 3.11 desde [python.org](https://www.python.org/downloads/).
3. Abre una terminal (CMD o PowerShell) y navega a la carpeta del proyecto.
4. Instala las dependencias:
   ```bat
   pip install -r requirements.txt
   ```
5. Ejecuta el script con doble clic en `start_windows.bat` o desde la terminal:
   ```bat
   python AIBrainstorming_gradio.py
   ```

**Notas:**
- Si usas Anaconda, puedes crear un entorno con `conda create -n brainstorming python=3.11` y activarlo con `conda activate brainstorming`.
- Todos los comandos de descarga de modelos y scraping funcionan igual en Windows.
- Si tienes problemas con permisos, ejecuta la terminal como administrador.

# AI Brainstorming - Documentación de Ejecución y Seguridad

## Requisitos
- Python 3.8+
- Instalar dependencias:
  ```sh
  pip install -r requirements.txt
  ```
- Tener permisos de administrador/root para lanzar el sistema (solo el canary y el gestor, no Ollama).

## Ejecución

### macOS / Linux
1. Ejecuta el script principal como root o usando sudo:
   ```sh
   sudo python3 AIBrainstorming_gradio.py
   ```
   - El script:
     - Mata cualquier Ollama corriendo como root/servicio.
     - Lanza Ollama como usuario normal (el usuario original de la sesión).
     - Lanza el canary como root para monitoreo y control de recursos.
     - Lanza la interfaz Gradio para el usuario.

### Windows
1. Ejecuta el script principal como Administrador (clic derecho → “Ejecutar como administrador” o desde terminal elevada):
   ```sh
   python AIBrainstorming_gradio.py
   ```
   - El script:
     - Mata cualquier Ollama corriendo como SYSTEM/Administrador.
     - Lanza Ollama como usuario normal usando `runas`.
     - Lanza el canary como Administrador para monitoreo y control de recursos.
     - Lanza la interfaz Gradio para el usuario.

## Flujo de uso
- Selecciona los modelos y parámetros en la interfaz.
- Al iniciar el debate:
  - El selector de modelos desaparece.
  - El debate alterna entre modelos y permite intervención humana en cualquier momento tras cada respuesta de modelo.
- El canary monitorea y controla el uso de recursos de Ollama en segundo plano.

## Seguridad
- **Nunca ejecutes Ollama como root/Administrador**: el sistema lo previene automáticamente.
- **El canary debe correr con privilegios elevados** para poder pausar, renicear y matar procesos de otros usuarios.
- Si quieres reiniciar el sistema, simplemente vuelve a ejecutar el script principal como se indica arriba.

## Personalización
- Puedes ajustar los límites de CPU/RAM del canary editando las variables `CPU_WARN`, `CPU_CRIT`, `RAM_WARN`, `RAM_CRIT` en `canary_ollama.py`.

## Monitoreo de GPU (NVIDIA) y reinicio automático

- El canary ahora monitorea el uso de GPU (requiere tarjeta NVIDIA y la librería `nvidia-ml-py3`).
- Si la GPU supera el 90% de uso, el canary mata Ollama y lo relanza forzando el uso de CPU (variable de entorno `OLLAMA_NO_GPU=1`).
- Puedes ajustar los umbrales de GPU con las variables `GPU_WARN` y `GPU_CRIT` en `canary_ollama.py`.
- Si no tienes GPU NVIDIA, el monitoreo de GPU se ignora automáticamente.

### Instalar dependencias extra para GPU:
```sh
pip install nvidia-ml-py3
```

### Notas:
- El cambio de GPU a CPU requiere reiniciar Ollama, no es posible cambiarlo en caliente.
- El monitoreo de GPU solo funciona con NVIDIA y drivers compatibles.

## Notas
- Si tienes problemas de permisos, asegúrate de ejecutar el script principal con los privilegios adecuados.
- El sistema está diseñado para máxima seguridad y robustez en entornos multiusuario.

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
