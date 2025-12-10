#!/bin/bash

echo "=========================================="
echo "EVALUACIÓN DEL MODELO"
echo "=========================================="

MODEL_PATH="model/mobilenetv2.h5"
TEST_DIR="data/processed"  
BATCH_SIZE=32

if [ ! -f "$MODEL_PATH" ]; then
    echo " Error: No se encontró el modelo: $MODEL_PATH"
    echo " Entrena primero el modelo: bash scripts/train.sh"
    exit 1
fi

echo ""
echo " Modelo: $MODEL_PATH"
echo " Datos: $TEST_DIR"
echo ""

python -c "
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from tensorflow import keras
from src.data.dataloader import BillDataLoader
from src.models.mobilenetv2 import evaluate_model
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import json

print(' Cargando modelo...')
model = keras.models.load_model('$MODEL_PATH')

print(' Cargando datos de test...')
loader = BillDataLoader(
    data_dir='$TEST_DIR',
    batch_size=$BATCH_SIZE
)

# Crear generador de validación (como test)
_, test_gen = loader.create_train_generator(validation_split=0.2, augment=False)

print('\n Evaluando modelo...')
metrics = evaluate_model(model, test_gen)

print('\n Generando reporte de clasificación...')

# Predicciones
test_gen.reset()
predictions = model.predict(test_gen, verbose=1)
predicted_classes = np.argmax(predictions, axis=1)

# Clases verdaderas
true_classes = test_gen.classes

# Nombres de clases
class_names = list(test_gen.class_indices.keys())

# Reporte de clasificación
print('\n' + '='*60)
print('REPORTE DE CLASIFICACIÓN')
print('='*60)
print(classification_report(
    true_classes,
    predicted_classes,
    target_names=class_names,
    digits=4
))

# Matriz de confusión
print('\n' + '='*60)
print('MATRIZ DE CONFUSIÓN')
print('='*60)
cm = confusion_matrix(true_classes, predicted_classes)
print('Clases:', class_names)
print(cm)

# Calcular precisión por clase
print('\n' + '='*60)
print('PRECISIÓN POR CLASE')
print('='*60)
for i, class_name in enumerate(class_names):
    class_accuracy = cm[i, i] / cm[i, :].sum() * 100
    print(f'{class_name:20s}: {class_accuracy:6.2f}%')

# Guardar resultados
results = {
    'metrics': {k: float(v) for k, v in metrics.items()},
    'classification_report': classification_report(
        true_classes,
        predicted_classes,
        target_names=class_names,
        output_dict=True
    ),
    'confusion_matrix': cm.tolist()
}

with open('model/evaluation_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print('\n Resultados guardados en: model/evaluation_results.json')
"

echo ""
echo "=========================================="
echo "EVALUACIÓN COMPLETADA"
echo "=========================================="
echo ""