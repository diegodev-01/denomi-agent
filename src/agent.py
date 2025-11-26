import argparse
import sys
from pathlib import Path
import cv2

sys.path.append(str(Path(__file__).parent.parent))

from src.inference.predict import BillPredictor
from src.inference.tts import TTSEngine


class BillRecognitionAgent:

    def __init__(self, 
                 model_path='model/mobilenetv2.h5',
                 labels_path='model/labels.json',
                 language='es',
                 confidence_threshold=70.0):

        print("Inicializando Agente de Reconocimiento de Billetes...")
        
        self.predictor = BillPredictor(model_path, labels_path)
        self.tts = TTSEngine(language=language)
        self.confidence_threshold = confidence_threshold
        
        print("Agente listo para operar\n")
    
    def process_image(self, image_path, speak=True, visualize=False):
        print("="*60)
        print("🔍 PROCESANDO IMAGEN")
        print("="*60)
        print(f"Archivo: {image_path}\n")
        
        try:
            print("Analizando imagen...")
            class_name, confidence = self.predictor.predict(image_path)
            
            print(f"Predicción: {class_name}")
            print(f"Confianza: {confidence:.2f}%")
            
            result = {
                'success': True,
                'denomination': class_name,
                'confidence': confidence,
                'status': self._get_confidence_status(confidence)
            }
            
            if speak:
                print("Anunciando resultado...")
                if confidence >= self.confidence_threshold:
                    self.tts.speak_bill_result(class_name, confidence)
                else:
                    self.tts.speak_error("low_confidence")
                    print("Confianza baja - Se recomienda mejor iluminación")

            if visualize:
                print("Generando visualización...")
                _, _, result_image = self.predictor.predict_with_visualization(
                    image_path,
                    save_result=False
                )
                
                import matplotlib.pyplot as plt
                plt.figure(figsize=(10, 8))
                plt.imshow(result_image)
                plt.axis('off')
                plt.title(f"Predicción: {class_name} ({confidence:.1f}%)")
                plt.show()

            print("\n Procesamiento completado")

        except Exception as e:
            print(f"\n Error durante el procesamiento: {str(e)}")
            if speak:
                self.tts.speak_error("general")
            
            result = {
                'success': False,
                'error': str(e)
            }
        
        print("="*60 + "\n")
        return result
    
    def process_from_camera(self, camera_id=0, speak=True):

        print("📷 Accediendo a cámara...")
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print("No se pudo acceder a la cámara")
            if speak:
                self.tts.speak_error("no_camera")
            return {'success': False, 'error': 'No se pudo acceder a la cámara'}
        
        print("Cámara activa")
        print("\nControles:")
        print("  ESPACIO - Capturar imagen")
        print("  ESC     - Salir")
        
        result = None
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error al leer frame")
                break
            
            cv2.imshow('Reconocedor de Billetes - Presione ESPACIO para capturar', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:
                print("Saliendo...")
                break
            
            if key == 32:
                print("\n Capturando imagen...")
                
                temp_path = "temp_capture.jpg"
                cv2.imwrite(temp_path, frame)
                
                result = self.process_image(temp_path, speak=speak, visualize=False)
                
                if result['success']:
                    text = f"{result['denomination']}: {result['confidence']:.1f}%"
                    cv2.putText(frame, text, (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Resultado', frame)
                    cv2.waitKey(2000)  
                
                Path(temp_path).unlink(missing_ok=True)
        
        cap.release()
        cv2.destroyAllWindows()
        
        return result
    
    def _get_confidence_status(self, confidence):
        if confidence >= 90:
            return "high"
        elif confidence >= self.confidence_threshold:
            return "medium"
        else:
            return "low"
    
    def run_interactive(self):
        """Modo interactivo del agente"""
        print("\n" + "="*60)
        print("AGENTE DE RECONOCIMIENTO DE BILLETES")
        print("="*60)
        
        self.tts.speak_welcome()
        
        print("\nOpciones:")
        print("1. Procesar imagen desde archivo")
        print("2. Capturar desde cámara")
        print("3. Salir")
        
        while True:
            choice = input("\nSeleccione opción (1-3): ").strip()
            
            if choice == '1':
                image_path = input("Ruta de la imagen: ").strip()
                self.process_image(image_path, speak=True, visualize=True)
            
            elif choice == '2':
                self.process_from_camera(camera_id=0, speak=True)
            
            elif choice == '3':
                print("👋 ¡Hasta luego!")
                self.tts.speak("Hasta luego")
                break
            
            else:
                print("Opción inválida")


def main():
    parser = argparse.ArgumentParser(
        description='Agente de Reconocimiento de Billetes con IA + TTS'
    )
    parser.add_argument('--image', type=str, help='Ruta de la imagen a procesar')
    parser.add_argument('--camera', action='store_true', help='Usar cámara')
    parser.add_argument('--interactive', action='store_true', help='Modo interactivo')
    parser.add_argument('--model', type=str, default='model/mobilenetv2.h5', 
                       help='Ruta del modelo')
    parser.add_argument('--no-speak', action='store_true', help='No usar TTS')
    parser.add_argument('--visualize', action='store_true', help='Mostrar visualización')
    
    args = parser.parse_args()
    
    agent = BillRecognitionAgent(
        model_path=args.model,
        labels_path='model/labels.json',
        language='es'
    )
    
    if args.interactive:
        agent.run_interactive()
    
    elif args.camera:
        agent.process_from_camera(speak=not args.no_speak)
    
    elif args.image:
        agent.process_image(
            args.image,
            speak=not args.no_speak,
            visualize=args.visualize
        )
    
    else:
        print("Debe especificar --image, --camera o --interactive")
        print("Uso:")
        print("  python src/agent.py --image ruta/imagen.jpg")
        print("  python src/agent.py --camera")
        print("  python src/agent.py --interactive")


if __name__ == "__main__":
    main()