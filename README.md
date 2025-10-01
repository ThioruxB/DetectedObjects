# Proyecto de Detección y Análisis de Perfiles

Este proyecto es un sistema integral para detectar personas en un video, analizar sus características demográficas y de estilo, y visualizar los perfiles resultantes en una interfaz web interactiva.

## Flujo de Trabajo del Proyecto

El proyecto se divide en tres fases principales:

1.  **Detección de Personas**: Un script de Python utiliza el modelo YOLOv8 para procesar un archivo de video. Detecta y rastrea a cada persona, guardando una imagen recortada y de alta calidad de cada individuo único en la carpeta `cropped_persons/`.
2.  **Análisis y Descripción**: Otro script procesa las imágenes recortadas, utilizando un modelo de lenguaje visual (a través de una API que requiere una clave) para generar una descripción detallada de cada persona. Esta descripción incluye el rango de edad, el género y un perfil de consumidor basado en su vestimenta y estilo. Los resultados se guardan en `results.json`.
3.  **Visualización de Datos**: Una aplicación web (HTML, CSS y JavaScript) presenta los perfiles de los consumidores. Muestra un panel con gráficos agregados (distribución de género, histograma de edades) y un carrusel para explorar los perfiles individuales en detalle, incluyendo un gráfico de radar con atributos del consumidor.

## Componentes del Proyecto

### 1. Detección de Objetos (`detect.py`)

-   **Función**: Procesa un video para detectar y recortar imágenes de personas.
-   **Entrada**: Un archivo de video (ej. `video.mp4`).
-   **Salida**: Imágenes JPG de personas únicas en el directorio `cropped_persons/`.
-   **Tecnología**: Python, OpenCV, Ultralytics YOLOv8.
-   **Uso**:
    ```bash
    python detect.py <ruta_del_video>
    ```
    Por ejemplo:
    ```bash
    python detect.py video.mp4
    ```
-   **Nota**: Si deseas ver un ejemplo de los resultados de la detección directamente, puedes revisar el archivo `yolotrol.mp4` que muestra el video procesado con los cuadros delimitadores y los IDs de seguimiento.

### 2. Generación de Descripciones (`describe_and_save.py`)

-   **Función**: Toma las imágenes recortadas y genera descripciones en formato JSON.
-   **Entrada**: Las imágenes en la carpeta `cropped_persons/`.
-   **Salida**: Un archivo `results.json` con las descripciones detalladas y un `results.csv` con un resumen.
-   **Dependencias**: Requiere una clave de API para el modelo de análisis de imágenes, que se pasa como argumento.
-   **Uso**:
    ```bash
    python describe_and_save.py <TU_API_KEY>
    ```

### 3. Visualizador de Perfiles (Interfaz Web)

-   **Función**: Muestra los perfiles de consumidor de forma interactiva.
-   **Archivos**: `index.html`, `style.css`, `script.js`.
-   **Uso**: Abre el archivo `index.html` en un navegador web.
-   **Nota Importante**: Actualmente, la página web utiliza datos de ejemplo que están incrustados directamente en el archivo `script.js`. Para visualizar los resultados generados por tus propios análisis, necesitarías reemplazar manualmente los datos en `script.js` con el contenido de `results.json`.

### 4. Como Instalar e Implementar YOLOv8x

-   **Función**: YOLOv8x es el modelo más preciso de la familia YOLOv8, ideal para obtener la máxima calidad en la detección de objetos, aunque requiere más recursos computacionales.
-   **Uso**: Este modelo se puede integrar en el script `detect.py` para mejorar la precisión de la detección de personas.

#### Instalación

1.  **Descargar el Modelo**:
    El modelo `yolov8x.pt` ya se encuentra en el repositorio. Si necesitas descargarlo manualmente, puedes hacerlo desde la página oficial de [Ultralytics](https://ultralytics.com/yolo) o usando el siguiente comando:
    ```bash
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
    ```

2.  **Instalar Dependencias**:
    Asegúrate de tener todas las dependencias del proyecto instaladas. Si ya has seguido los pasos de la sección "Cómo Empezar", no necesitas hacer nada más. De lo contrario, ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

#### Implementación

Para utilizar el modelo `yolov8x.pt` en lugar del `yolov8m.pt` que viene por defecto, solo necesitas modificar una línea en el script `detect.py`.

1.  **Abrir `detect.py`**:
    Abre el archivo `detect.py` en tu editor de código.

2.  **Modificar el Modelo**:
    Busca la siguiente línea en la función `object_detector`:
    ```python
    model = YOLO('yolov8m.pt')
    ```
    Y reemplázala por:
    ```python
    model = YOLO('yolov8x.pt')
    ```

3.  **Ejecutar el Script**:
    Ahora puedes ejecutar el script de detección como de costumbre, y utilizará el modelo `yolov8x.pt` para el análisis.
    ```bash
    python detect.py tu_video.mp4
    ```

-   **Nota**: El uso de `yolov8x.pt` puede ser más lento y consumir más memoria RAM y VRAM en comparación con `yolov8m.pt`. Asegúrate de que tu hardware es capaz de soportarlo, especialmente si trabajas con videos de alta resolución o de larga duración.

## Estructura de Archivos

```
.
├── cropped_persons/      # Directorio para las imágenes recortadas de personas.
├── venv/                 # Entorno virtual de Python.
├── detect.py             # Script para la detección de personas en video.
├── describe_person.py    # Script auxiliar para describir una sola imagen (llamado por el principal).
├── describe_and_save.py  # Script principal para generar descripciones de todas las imágenes.
├── index.html            # Estructura de la página web.
├── script.js             # Lógica de la aplicación web y datos de visualización.
├── style.css             # Estilos para la página web.
├── video.mp4             # Video de ejemplo para el análisis.
├── yolov8m.pt            # Modelo de YOLO utilizado para la detección.
├── results.json          # Archivo JSON con los datos generados de los perfiles.
└── README.md             # Este archivo.
```

## Cómo Empezar

1.  **Clonar el Repositorio**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```

2.  **Configurar el Entorno Virtual**
    Asegúrate de tener Python 3.10 o superior instalado.

    *   **Crear el entorno virtual:**
        ```bash
        python -m venv venv
        ```

    *   **Activar el entorno virtual:**
        *   En Windows:
            ```bash
            .\venv\Scripts\activate
            ```
        *   En macOS/Linux:
            ```bash
            source venv/bin/activate
            ```

3.  **Instalar Dependencias**
    Con el entorno virtual activado, instala todas las dependencias necesarias desde el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar Detección**
    Coloca tu video en la raíz del proyecto y ejecuta el script `detect.py`.
    ```bash
    python detect.py tu_video.mp4
    ```

5.  **Generar Descripciones**
    Una vez que tengas las imágenes en `cropped_persons/`, ejecuta el script de descripción con tu clave de API.
    ```bash
    python describe_and_save.py <TU_API_KEY>
    ```

6.  **Ver Resultados**
    Abre `index.html` en tu navegador para ver el panel de visualización. (Recuerda que por defecto muestra datos de ejemplo).

Si desean ver la pagina web desde cualquier dispositivo le den clik a este link https://thioruxb.github.io/DetectedObjects