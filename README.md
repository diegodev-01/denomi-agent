# 🧠 Clasificador de Billetes con IA + TTS

Agente de Inteligencia Artificial basado en Visión por Computadora y Aprendizaje Supervisado para clasificar denominaciones de billetes y comunicar el resultado mediante texto a voz, contribuyendo a la autonomía de personas con discapacidad visual.

---

## 📌 Objetivo del Proyecto

Desarrollar un sistema capaz de:

1. Capturar o recibir una imagen de un billete.  
2. Clasificar automáticamente su denominación utilizando Transfer Learning.  
3. Generar una respuesta audible con un motor de Texto-a-Voz (TTS).  
4. Integrarse en un agente simple que ejecute todo el flujo: imagen → predicción → voz.

---

## 📁 Estructura del Repositorio

Se tienen sugerencias de nomenclatura de archivos con sus funcionalidades

``` bash
denomi-agent/
│
├── data/
│   ├── raw/                # Dataset original (no se versiona)
│   ├── processed/          # Imágenes preprocesadas
│   └── samples/            # Subconjunto reducido para pruebas
│
├── notebooks/
│   ├── 01_exploracion_dataset.ipynb
│   ├── 02_entrenamiento_mobilenetv2.ipynb
│   └── 03_evaluacion_modelo.ipynb
│
├── src/
│   ├── data/
│   │   ├── preprocess.py           # Resizing, normalización, augmentations
│   │   └── dataloader.py           # Generadores de datos para Keras
│   │
│   ├── models/
│   │   ├── mobilenetv2.py          # Modelo principal con Transfer Learning
│   │   ├── resnet50.py             # Alternativa más pesada
│   │   └── utils.py                # Funciones auxiliares
│   │
│   ├── inference/
│   │   ├── predict.py              # Carga modelo y predice billete
│   │   └── tts.py                  # Texto-a-voz (gTTS / pyttsx3)
│   │
│   └── agent.py                    # Pipeline completo (imagen → predicción → audio)
│
├── model/
│   ├── mobilenetv2.h5              # Modelo entrenado (no subir si pesa >100MB)
│   └── labels.json                 # Mapeo de clases
│
├── scripts/
│   ├── train.sh                    # Entrenamiento desde terminal
│   └── evaluate.sh                 # Evaluación del modelo
│
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Documentación del repositorio
└── .gitignore                      # Archivos a ignorar (datasets, modelos pesados, etc.)

```

---

## ⚙️ Instalación

1. Crear entorno virtual

    ``` bash
    Windows (PowerShell):
    python -m venv .venv
    .venv\Scripts\activate
    ```

    ``` bash
    Linux / macOS:
    python3 -m venv .venv
    source .venv/bin/activate
    
    ```

2. Instalar dependencias

    pip install --upgrade pip
    pip install -r requirements.txt

---

## 🏋️‍♂️ Entrenamiento del Modelo

El dataset debe ubicarse en:

data/raw/<carpetas_por_clase>

Ejecutar desde terminal:

bash scripts/train.sh

o desde el notebook:

notebooks/02_entrenamiento_mobilenetv2.ipynb

---

## 🔍 Inferencia (Predicción)

python src/inference/predict.py --image ruta/imagen.jpg

Salida esperada:
Predicción: Billete de 100 pesos

---

## 🔊 Generación de Voz (TTS)

python src/inference/tts.py --text "Billete de cien pesos"

---

## 🤖 Ejecución del Agente Completo

python src/agent.py --image ruta/imagen.jpg

---

## 🚫 Sobre el Dataset

El dataset NO debe subirse a GitHub.  
Aunque ya es ignorado automáticamente mediante .gitignore, tengan cuidado.

Solo se versiona:
    - código  
    - notebooks  
    - scripts  
    - archivos de configuración  

---

## 📌 Tecnologías Utilizadas

- TensorFlow / Keras  
- MobileNetV2 (Transfer Learning)  
- OpenCV  
- Python 3.10+  
- gTTS / pyttsx3  
- Jupyter Notebooks  
- Streamlit (para front-end)

---