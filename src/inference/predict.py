import numpy as np
import cv2
from tensorflow import keras
from pathlib import Path
import json
import argparse
import sys

# Agregar path del proyecto
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.data.preprocess import BillPreprocessor


class BillPredictor:    
    def __init__(self, model_path='model/mobilenetv2.h5', labels_path='model/labels.json'):
        self.model_path = Path(model_path)
        self.labels_path = Path(labels_path)
        self.model = None
        self.labels = None
        self.preprocessor = BillPreprocessor(target_size=(224, 224))
        
        self._load_model()
        self._load_labels()
        
        print(f"Predictor inicializado")
        print(f"Modelo: {self.model_path.name}")
        print(f"Clases: {len(self.labels)}")
    
    def _load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {self.model_path}")
        
        print(f"Cargando modelo desde: {self.model_path}")
        self.model = keras.models.load_model(self.model_path)
        print(f"Modelo cargado exitosamente")
    
    def _load_labels(self):
        if not self.labels_path.exists():
            raise FileNotFoundError(f"Archivo de etiquetas no encontrado: {self.labels_path}")
        
        with open(self.labels_path, 'r', encoding='utf-8') as f:
            self.labels = json.load(f)
        
        print(f"Etiquetas cargadas: {list(self.labels.values())}")
    
    def predict(self, image_path, return_confidence=True):
        image = self.preprocessor.preprocess_for_model(image_path, enhance=True)
        
        predictions = self.model.predict(image, verbose=0)
        
        class_idx = np.argmax(predictions[0])
        confidence = predictions[0][class_idx] * 100
        
        class_name = self.labels[str(class_idx)]
        
        if return_confidence:
            return class_name, confidence
        else:
            return class_name
    
    def predict_top_k(self, image_path, k=3):
        image = self.preprocessor.preprocess_for_model(image_path, enhance=True)
        
        predictions = self.model.predict(image, verbose=0)[0]
        
        top_k_indices = np.argsort(predictions)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            class_name = self.labels[str(idx)]
            confidence = predictions[idx] * 100
            results.append((class_name, confidence))
        
        return results
    
    def predict_with_visualization(self, image_path, save_result=False, output_path=None):
        class_name, confidence = self.predict(image_path)
        
        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        text = f"{class_name}: {confidence:.1f}%"
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        cv2.rectangle(image, (10, 10), (text_width + 20, text_height + 30), (0, 0, 0), -1)
        
        color = (0, 255, 0) if confidence > 90 else (255, 255, 0) if confidence > 70 else (255, 0, 0)
        cv2.putText(image, text, (15, text_height + 20), font, font_scale, color, thickness)
        
        if save_result:
            if output_path is None:
                output_path = Path(image_path).parent / f"result_{Path(image_path).name}"
            
            cv2.imwrite(str(output_path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            print(f"Resultado guardado en: {output_path}")
        
        return class_name, confidence, image
    
    def predict_batch(self, image_paths):
        results = []
        
        for img_path in image_paths:
            try:
                class_name, confidence = self.predict(img_path)
                results.append((img_path, class_name, confidence))
            except Exception as e:
                print(f"Error procesando {img_path}: {str(e)}")
                results.append((img_path, "ERROR", 0.0))
        
        return results


def main():
    """Función principal para uso desde línea de comandos"""
    parser = argparse.ArgumentParser(description='Predictor de Billetes')
    parser.add_argument('--image', type=str, required=True, help='Ruta de la imagen')
    parser.add_argument('--model', type=str, default='model/mobilenetv2.h5', help='Ruta del modelo')
    parser.add_argument('--labels', type=str, default='model/labels.json', help='Ruta de etiquetas')
    parser.add_argument('--top-k', type=int, default=1, help='Mostrar top-k predicciones')
    parser.add_argument('--visualize', action='store_true', help='Visualizar resultado')
    parser.add_argument('--save', action='store_true', help='Guardar resultado')
    
    args = parser.parse_args()
    
    predictor = BillPredictor(
        model_path=args.model,
        labels_path=args.labels
    )
    
    print("\n" + "="*60)
    print("PREDICCIÓN")
    print("="*60)
    print(f"Imagen: {args.image}")
    
    if args.top_k > 1:
        results = predictor.predict_top_k(args.image, k=args.top_k)
        print(f"\nTop-{args.top_k} predicciones:")
        for i, (class_name, conf) in enumerate(results, 1):
            print(f"  {i}. {class_name}: {conf:.2f}%")
    else:
        class_name, confidence = predictor.predict(args.image)
        print(f"\nPredicción: {class_name}")
        print(f"Confianza: {confidence:.2f}%")
        
        if confidence < 70:
            print("Baja confianza - Intente con mejor iluminación")
        elif confidence < 90:
            print("Confianza moderada")
        else:
            print("Alta confianza")
    
    if args.visualize or args.save:
        class_name, confidence, result_image = predictor.predict_with_visualization(
            args.image,
            save_result=args.save
        )
        
        if args.visualize:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 8))
            plt.imshow(result_image)
            plt.axis('off')
            plt.title(f"Predicción: {class_name} ({confidence:.1f}%)")
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    main()