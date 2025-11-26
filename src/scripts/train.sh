#!/bin/bash
echo "=========================================="
echo "🏋️  ENTRENAMIENTO DE MODELO"
echo "=========================================="

DATA_DIR="data/processed"
MODEL_TYPE="mobilenetv2" 
EPOCHS=50
BATCH_SIZE=32
LEARNING_RATE=0.001
VALIDATION_SPLIT=0.2

if [ ! -d "$DATA_DIR" ]; then
    echo "Error: No se encontró el directorio de datos: $DATA_DIR"
    echo "Ejecuta primero: python src/data/preprocess.py"
    exit 1
fi

mkdir -p model
mkdir -p logs/tensorboard

echo ""
echo "   Configuración:"
echo "   Datos: $DATA_DIR"
echo "   Modelo: $MODEL_TYPE"
echo "   Épocas: $EPOCHS"
echo "   Batch size: $BATCH_SIZE"
echo "   Learning rate: $LEARNING_RATE"
echo "   Validación: ${VALIDATION_SPLIT}%"
echo ""

python -c "
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

from src.data.dataloader import create_data_loaders
from src.models.mobilenetv2 import (
    create_mobilenetv2_model,
    compile_model,
    get_callbacks,
    train_model
)

print('Cargando datos...')
loader, train_gen, val_gen = create_data_loaders(
    data_dir='$DATA_DIR',
    batch_size=$BATCH_SIZE,
    validation_split=$VALIDATION_SPLIT
)

print('\n Creando modelo...')
model, base_model = create_mobilenetv2_model(
    num_classes=loader.num_classes,
    input_shape=(224, 224, 3)
)

print('\n Compilando modelo...')
compile_model(model, learning_rate=$LEARNING_RATE)

print('\n Callbacks configurados')
callbacks = get_callbacks(model_save_path='model/mobilenetv2.h5')

print('\n Iniciando entrenamiento...')
history = train_model(
    model=model,
    train_generator=train_gen,
    validation_generator=val_gen,
    epochs=$EPOCHS,
    callbacks=callbacks
)

print('\n Entrenamiento completado!')
print('Modelo guardado en: model/mobilenetv2.h5')
print('Logs de TensorBoard en: logs/tensorboard/')
print('')
print('Para ver los logs de entrenamiento:')
print('  tensorboard --logdir=logs/tensorboard')
"

echo ""
echo "=========================================="
echo "PROCESO COMPLETADO"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "  1. Evaluar modelo: bash scripts/evaluate.sh"
echo "  2. Probar predicción: python src/inference/predict.py --image test.jpg"
echo "  3. Ejecutar agente: python src/agent.py --interactive"
echo ""