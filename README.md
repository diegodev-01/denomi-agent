# 🧠 Clasificador de Billetes con IA + TTS

**Agente de Inteligencia Artificial** basado en Visión por Computadora y Aprendizaje Supervisado para clasificar denominaciones de billetes y comunicar el resultado mediante texto-a-voz, contribuyendo a la autonomía de personas con discapacidad visual.

---

## 📌 Objetivo del Proyecto

Desarrollar un sistema capaz de:

1. **Capturar o recibir** una imagen de un billete
2. **Clasificar automáticamente** su denominación utilizando Transfer Learning (MobileNetV2/ResNet50)
3. **Generar una respuesta audible** con un motor de Texto-a-Voz (TTS)
4. **Integrarse en un agente simple** que ejecute todo el flujo: `imagen → predicción → voz`

---

## 🏗️ Estructura del Proyecto

```
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
│   │   └── tts.py                  # Texto-a-voz (gTTS)
│   │
│   └── agent.py                    # Pipeline completo (imagen → predicción → audio)
│
├── model/
│   ├── mobilenetv2.h5              # Modelo entrenado
│   ├── labels.json                 # Mapeo de clases
│   └── evaluation_results.json     # Resultados de evaluación
│
├── scripts/
│   ├── train.sh                    # Entrenamiento desde terminal
│   └── evaluate.sh                 # Evaluación del modelo
│
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── .gitignore                      # Archivos a ignorar
└── main.py                         # Punto de entrada principal
```

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repo>
cd denomi-agent
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📊 Preparación del Dataset

### 1. Organizar el dataset

Coloca tus imágenes en `data/raw/` organizadas por carpetas según la denominación:

```
data/raw/
├── 10_bolivianos/
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ...
├── 20_bolivianos/
├── 50_bolivianos/
├── 100_bolivianos/
└── 200_bolivianos/
```

### 2. Preprocesar imágenes

```bash
python src/data/preprocess.py
```

Esto creará:
- `data/processed/` - Imágenes redimensionadas y mejoradas
- `data/samples/` - Subset reducido para pruebas rápidas

---

## 🏋️ Entrenamiento del Modelo

### Opción 1: Usando script de shell (Recomendado)

```bash
bash scripts/train.sh
```

### Opción 2: Usando Python directamente

```python
python -c "
from src.data.dataloader import create_data_loaders
from src.models.mobilenetv2 import create_mobilenetv2_model, compile_model, get_callbacks, train_model

# Cargar datos
loader, train_gen, val_gen = create_data_loaders('data/processed')

# Crear modelo
model, base_model = create_mobilenetv2_model(num_classes=5)
compile_model(model)

# Entrenar
callbacks = get_callbacks()
history = train_model(model, train_gen, val_gen, epochs=50, callbacks=callbacks)
"
```

### Opción 3: Usando Jupyter Notebook

Abre `notebooks/02_entrenamiento_mobilenetv2.ipynb`

### Monitorear entrenamiento con TensorBoard

```bash
tensorboard --logdir=logs/tensorboard
```

---

## 📊 Evaluación del Modelo

```bash
bash scripts/evaluate.sh
```

Esto generará:
- Reporte de clasificación (precision, recall, f1-score)
- Matriz de confusión
- Precisión por clase
- Archivo `model/evaluation_results.json` con todos los resultados

---

## 🔍 Inferencia (Predicción)

### Predecir una imagen

```bash
python src/inference/predict.py --image ruta/imagen.jpg
```

### Predecir con visualización

```bash
python src/inference/predict.py --image ruta/imagen.jpg --visualize
```

### Ver top-3 predicciones

```bash
python src/inference/predict.py --image ruta/imagen.jpg --top-k 3
```

---

## 🔊 Generación de Voz (TTS)

### Probar el motor TTS

```bash
python src/inference/tts.py --text "Billete de cien bolivianos"
```

### Ejecutar pruebas

```bash
python src/inference/tts.py --test
```

---

## 🤖 Ejecución del Agente Completo

### Modo 1: Procesar imagen desde archivo

```bash
python src/agent.py --image ruta/imagen.jpg
```

### Modo 2: Capturar desde cámara

```bash
python src/agent.py --camera
```

Controles:
- **ESPACIO**: Capturar imagen
- **ESC**: Salir

### Modo 3: Modo interactivo (Menú)

```bash
python src/agent.py --interactive
```

### Opciones adicionales

```bash
# Sin voz (solo predicción visual)
python src/agent.py --image test.jpg --no-speak

# Con visualización
python src/agent.py --image test.jpg --visualize

# Usando modelo específico
python src/agent.py --image test.jpg --model model/resnet50.h5
```

---

## 🎯 Flujo de Trabajo Completo

```bash
# 1. Preprocesar datos
python src/data/preprocess.py

# 2. Entrenar modelo
bash scripts/train.sh

# 3. Evaluar modelo
bash scripts/evaluate.sh

# 4. Ejecutar agente
python src/agent.py --interactive
```

---

## 📌 Tecnologías Utilizadas

- **TensorFlow / Keras** - Framework de Deep Learning
- **MobileNetV2** - Transfer Learning para clasificación eficiente
- **OpenCV** - Procesamiento de imágenes
- **gTTS** - Google Text-to-Speech
- **NumPy** - Computación numérica
- **Matplotlib** - Visualización
- **scikit-learn** - Métricas de evaluación
- **Python 3.10+** - Lenguaje de programación

---

## 🔒 Sobre el Dataset

⚠️ **IMPORTANTE**: El dataset **NO debe subirse a GitHub**

Está configurado automáticamente en `.gitignore`:
- `data/raw/*`
- `data/processed/*`
- `data/samples/*`
- `model/*.h5`

Solo se versiona:
- ✅ Código fuente
- ✅ Notebooks
- ✅ Scripts
- ✅ Configuraciones
- ✅ Documentación

---

## 📈 Métricas Esperadas

- **Precisión objetivo**: > 95%
- **Tiempo de inferencia**: < 1 segundo
- **Confianza mínima aceptable**: 70%
- **Soporte**: Billetes de 10, 20, 50, 100, 200 bolivianos

---

## 🐛 Solución de Problemas

### Error: "No se encontró el modelo"
```bash
# Entrenar el modelo primero
bash scripts/train.sh
```

### Error: "No se pudo acceder a la cámara"
```bash
# Verificar permisos de cámara en tu sistema
# En Linux, puede ser necesario:
sudo usermod -a -G video $USER
```

### Baja precisión del modelo
- Aumentar número de épocas: Editar `scripts/train.sh` → `EPOCHS=100`
- Recolectar más datos de entrenamiento
- Aplicar más data augmentation en `src/data/preprocess.py`

---

## 📚 Documentación Adicional

- Ver notebooks en `notebooks/` para análisis exploratorio
- Revisar comentarios en el código para detalles de implementación
- Consultar logs de TensorBoard para análisis de entrenamiento

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto tiene fines educativos y de investigación.


