
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from pathlib import Path
import json


def create_mobilenetv2_model(num_classes, input_shape=(224, 224, 3), trainable_base=False):
    print(" Construyendo MobileNetV2...")
    
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = trainable_base
    
    inputs = keras.Input(shape=input_shape)
    x = base_model(inputs, training=False)
    
    x = layers.GlobalAveragePooling2D(name='global_avg_pool')(x)
    x = layers.BatchNormalization(name='bn_1')(x)
    x = layers.Dense(256, activation='relu', name='dense_256')(x)
    x = layers.Dropout(0.5, name='dropout_1')(x)
    x = layers.Dense(128, activation='relu', name='dense_128')(x)
    x = layers.Dropout(0.3, name='dropout_2')(x)
    outputs = layers.Dense(num_classes, activation='softmax', name='output')(x)
    
    model = Model(inputs, outputs, name='MobileNetV2_BillClassifier')
    
    print(f" Modelo creado:")
    print(f" Capas totales: {len(model.layers)}")
    print(f" Parámetros totales: {model.count_params():,}")
    
    return model, base_model


def compile_model(model, learning_rate=0.001):
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    print(f" Modelo compilado (lr={learning_rate})")


def get_callbacks(model_save_path='model/mobilenetv2.h5'):
    Path(model_save_path).parent.mkdir(parents=True, exist_ok=True)
    
    callbacks = [
        ModelCheckpoint(
            filepath=model_save_path,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    return callbacks


def train_model(model, train_generator, validation_generator, epochs=50, callbacks=None):
    print("\n  INICIANDO ENTRENAMIENTO")
    
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\n Entrenamiento completado!")
    return history

def evaluate_model(model, test_generator):
    print("\n" + "="*60)
    print(" EVALUANDO MODELO")
    print("="*60)
    
    results = model.evaluate(test_generator, verbose=1)
    
    metrics = {}
    for i, metric_name in enumerate(model.metrics_names):
        metrics[metric_name] = results[i]
    
    print("\n Resultados:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.4f}")
    
    return metrics

if __name__ == "__main__":
    print("Modelo MobileNetV2 listo para usar")