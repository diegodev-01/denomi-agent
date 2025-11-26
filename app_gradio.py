
import gradio as gr
import sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

sys.path.append(str(Path(__file__).parent))

from src.inference.predict import BillPredictor
from src.inference.tts import TTSEngine
from src.data.preprocess import BillPreprocessor


class GradioBillRecognizer:
    
    def __init__(self, model_path='model/mobilenetv2.h5', labels_path='model/labels.json'):
        print(" Inicializando aplicación Gradio...")
        
        try:
            self.predictor = BillPredictor(model_path, labels_path)
            self.tts = TTSEngine(language='es')
            self.preprocessor = BillPreprocessor(target_size=(224, 224))
            print(" Componentes cargados exitosamente")
        except Exception as e:
            print(f" Error al cargar componentes: {str(e)}")
            raise
    
    def predict_and_speak(self, image, enable_tts=True):
        if image is None:
            return " No se proporcionó ninguna imagen", None, None
        
        try:
            if isinstance(image, np.ndarray):
                temp_path = "temp_gradio_image.jpg"
                cv2.imwrite(temp_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            else:
                temp_path = "temp_gradio_image.jpg"
                image.save(temp_path)
            
            class_name, confidence = self.predictor.predict(temp_path)
            
            if confidence >= 90:
                result_text = f" **{class_name}**\n\n Confianza: **{confidence:.1f}%**\n\n Alta confianza"
                emoji = "✅"
            elif confidence >= 70:
                result_text = f" **{class_name}**\n\n Confianza: **{confidence:.1f}%**\n\n Confianza moderada"
                emoji = "⚠️"
            else:
                result_text = f" **{class_name}**\n\n Confianza: **{confidence:.1f}%**\n\n Baja confianza - Intente con mejor iluminación"
                emoji = "❌"
            
            annotated_image = self._create_annotated_image(
                temp_path, class_name, confidence
            )
            
            audio_path = None
            if enable_tts:
                audio_path = self._generate_audio(class_name, confidence)
            
            Path(temp_path).unlink(missing_ok=True)
            
            return result_text, annotated_image, audio_path
            
        except Exception as e:
            error_msg = f" Error: {str(e)}"
            print(error_msg)
            return error_msg, None, None
    
    def _create_annotated_image(self, image_path, class_name, confidence):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        h, w = image.shape[:2]
        if w > 800:
            scale = 800 / w
            new_w, new_h = int(w * scale), int(h * scale)
            image = cv2.resize(image, (new_w, new_h))
        
        text = f"{class_name}"
        conf_text = f"{confidence:.1f}%"
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 3
        
        if confidence >= 90:
            color = (0, 255, 0)  
        elif confidence >= 70:
            color = (255, 200, 0)  
        else:
            color = (255, 0, 0)  
        
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        (conf_w, conf_h), _ = cv2.getTextSize(conf_text, font, font_scale, thickness)
        
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (max(text_w, conf_w) + 30, text_h + conf_h + 50), (0, 0, 0), -1)
        image = cv2.addWeighted(overlay, 0.7, image, 0.3, 0)
        
        cv2.putText(image, text, (20, 40), font, font_scale, color, thickness)
        cv2.putText(image, conf_text, (20, 40 + text_h + 20), font, font_scale, color, thickness)
        
        return image
    
    def _generate_audio(self, class_name, confidence):
        """Generar audio con TTS"""
        audio_path = "temp_audio_gradio.mp3"
        
        if confidence >= 95:
            text = f"Billete de {class_name}"
        elif confidence >= 70:
            text = f"Posible billete de {class_name}, con {int(confidence)} por ciento de confianza"
        else:
            text = "No estoy seguro, intente con mejor iluminación"
        
        self.tts.speak(text, save_path=audio_path, play=False)
        
        return audio_path


def create_gradio_interface(): 
    try:
        recognizer = GradioBillRecognizer()
    except Exception as e:
        print(f" Error al inicializar: {str(e)}")
        print("\n Asegúrate de que el modelo esté entrenado:")
        print("   bash scripts/train.sh")
        return None
    
    with gr.Blocks(
        title="Reconocedor de Billetes Bolivianos"
    ) as app:

        gr.HTML("""
            <style>
                .gradio-container {font-family: 'Arial', sans-serif;}
                .output-text {font-size: 1.2em; font-weight: bold;}
            </style>
        """)

        
        # Header
        gr.Markdown(
            """
            #  Reconocedor de Billetes Bolivianos 
            
            ### Sistema de IA con Retroalimentación Auditiva para Personas con Discapacidad Visual
            
            **Instrucciones:**
            1. Capture o suba una imagen de un billete
            2. El sistema identificará la denominación automáticamente
            3. Escuche el resultado mediante audio (si está habilitado)
            
            ---
            """
        )
        
        with gr.Tabs():
            with gr.TabItem(" Captura desde Cámara"):
                gr.Markdown("### Capture un billete con su cámara")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        camera_input = gr.Image(
                            sources=["webcam"],
                            streaming=True,
                            label="Cámara"
                        )

                        
                        camera_tts_checkbox = gr.Checkbox(
                            label=" Habilitar retroalimentación de voz",
                            value=True
                        )
                        
                        camera_button = gr.Button(
                            " Reconocer Billete",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column(scale=1):
                        camera_result = gr.Markdown(
                            label="Resultado",
                            elem_classes="output-text"
                        )
                        camera_annotated = gr.Image(
                            label="Imagen Anotada",
                            type="numpy"
                        )
                        camera_audio = gr.Audio(
                            label=" Resultado Audible",
                            autoplay=True
                        )
                
                camera_button.click(
                    fn=recognizer.predict_and_speak,
                    inputs=[camera_input, camera_tts_checkbox],
                    outputs=[camera_result, camera_annotated, camera_audio]
                )
            
            with gr.TabItem(" Subir Imagen"):
                gr.Markdown("### Suba una imagen de un billete desde su dispositivo")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        file_input = gr.Image(
                            type="numpy",
                            label="Seleccionar Imagen"
                        )
                        
                        file_tts_checkbox = gr.Checkbox(
                            label=" Habilitar retroalimentación de voz",
                            value=True
                        )
                        
                        file_button = gr.Button(
                            " Reconocer Billete",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column(scale=1):
                        file_result = gr.Markdown(
                            label="Resultado",
                            elem_classes="output-text"
                        )
                        file_annotated = gr.Image(
                            label="Imagen Anotada",
                            type="numpy"
                        )
                        file_audio = gr.Audio(
                            label=" Resultado Audible",
                            autoplay=True
                        )
                
                file_button.click(
                    fn=recognizer.predict_and_speak,
                    inputs=[file_input, file_tts_checkbox],
                    outputs=[file_result, file_annotated, file_audio]
                )
            
            with gr.TabItem(" Información"):
                gr.Markdown(
                    """
                    ## Acerca del Sistema
                    
                    Este sistema utiliza **Inteligencia Artificial** y **Visión por Computadora** 
                    para reconocer automáticamente las denominaciones de billetes bolivianos.
                    
                    ###  Características
                    
                    -  Reconocimiento en tiempo real
                    -  Retroalimentación auditiva (Texto-a-Voz)
                    -  Funciona con diferentes condiciones de iluminación
                    -  Interfaz accesible para personas con discapacidad visual
                    -  Compatible con lectores de pantalla
                    
                    ###  Tecnología
                    
                    - **Modelo**: MobileNetV2 con Transfer Learning
                    - **Framework**: TensorFlow/Keras
                    - **Precisión**: >95% en condiciones óptimas
                    - **TTS**: Google Text-to-Speech (gTTS)
                    
                    ###  Denominaciones Soportadas
                    
                    - 10 Bolivianos
                    - 20 Bolivianos
                    - 50 Bolivianos
                    - 100 Bolivianos
                    - 200 Bolivianos
                    
                    ###  Consejos para Mejor Reconocimiento
                    
                    1. **Iluminación**: Asegure buena iluminación sobre el billete
                    2. **Enfoque**: Mantenga la cámara enfocada y estable
                    3. **Distancia**: Coloque el billete a ~30cm de la cámara
                    4. **Fondo**: Use un fondo uniforme y contrastante
                    5. **Estado del billete**: Billetes muy desgastados pueden tener menor precisión
                    
                    ###  Privacidad
                    
                    - Las imágenes se procesan localmente
                    - No se almacenan imágenes de billetes
                    - Los archivos temporales se eliminan automáticamente
                    
                    ###  Desarrollado con  para la Accesibilidad
                    
                    ---
                    
                    **Versión**: 1.0.0  
                    **Última actualización**: 2025
                    """
                )
        
        gr.Markdown(
            """
            ---
            
            ### 🆘 ¿Necesitas ayuda?
            
            Si el sistema no funciona correctamente, verifica:
            - ✅ La cámara está habilitada en tu navegador
            - ✅ La imagen del billete es clara y bien iluminada
            - ✅ El billete está completamente visible en el cuadro
            
            ---
            
            **© 2025 | Proyecto de Accesibilidad con IA**
            """
        )
    
    return app


def main():
    print("="*60)
    print(" INICIANDO APLICACIÓN GRADIO")
    print("="*60)
    
    model_path = Path("model/mobilenetv2.h5")
    if not model_path.exists():
        print("\n ERROR: No se encontró el modelo entrenado")
        print(f"   Esperado en: {model_path}")
        print("\n Entrena el modelo primero:")
        print("   bash scripts/train.sh")
        return
    
    app = create_gradio_interface()
    
    if app is None:
        print("\n No se pudo crear la interfaz")
        return
    
    print("\n Aplicación lista!")
    print("\n Opciones de lanzamiento:")
    print("   - Local: http://localhost:7860")
    print("   - Share: Usa share=True para link público")
    print("\n  Presiona CTRL+C para detener\n")
    
    app.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False, 
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    main()