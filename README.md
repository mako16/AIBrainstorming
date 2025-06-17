# AIBrainstorming

Brainstorming automatizado entre dos modelos de IA de Ollama.

## Descripción
Este proyecto permite simular una discusión creativa y crítica entre dos modelos de inteligencia artificial usando Ollama. El usuario puede definir el contexto y el tópico del brainstorming desde la línea de comandos. Al finalizar, ambos modelos buscan un consenso sobre el tema propuesto.

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
   python AIBrainstorming.py --contexto "Contexto general" --topico "Tópico del brainstorming"
   ```

## Ejemplo
```sh
python AIBrainstorming.py --contexto "Educación en la era digital" --topico "¿Cómo reinventar la educación para niños usando IA?"
```

## Requisitos
- Python 3.11
- Conda
- Ollama instalado y modelos configurados localmente

## Autor
- mako16

## Licencia
MIT
