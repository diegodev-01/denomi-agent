
import sys
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.agent import BillRecognitionAgent


def print_banner():
    """Mostrar banner de bienvenida"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    DENOMI-AGENT                              ║
    ║                                                              ║
    ║        Sistema de Reconocimiento de Billetes con IA          ║
    ║           Visión por Computadora + Texto-a-Voz               ║
    ║                                                              ║
    ║              Contribuyendo a la Accesibilidad                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_requirements():
    """Verificar que existen los archivos necesarios"""
    model_path = Path("model/mobilenetv2.h5")
    labels_path = Path("model/labels.json")
    
    if not model_path.exists():
        print(" ERROR: No se encontró el modelo entrenado")
        print(f"   Esperado en: {model_path}")
        print("\n Solución:")
        print("   1. Entrenar el modelo: bash scripts/train.sh")
        print("   2. O usar un notebook: notebooks/02_entrenamiento_mobilenetv2.ipynb")
        return False
    
    if not labels_path.exists():
        print("  ADVERTENCIA: No se encontró el archivo de etiquetas")
        print(f"   Esperado en: {labels_path}")
        print("\n Se intentará crear automáticamente durante la carga de datos")
    
    return True


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='DENOMI-AGENT: Reconocimiento de Billetes con IA + TTS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Interfaz web con Gradio (RECOMENDADO)
  python main.py --gradio
  
  # Modo interactivo CLI
  python main.py --interactive
  
  # Procesar imagen específica
  python main.py --image ruta/imagen.jpg
  
  # Capturar desde cámara
  python main.py --camera
  
  # Sin retroalimentación de voz
  python main.py --image test.jpg --no-speak
  
  # Con visualización
  python main.py --image test.jpg --visualize
        """
    )
    
    parser.add_argument(
        '--gradio',
        action='store_true',
        help='Lanzar interfaz web con Gradio (recomendado)'
    )
    
    parser.add_argument(
        '--image',
        type=str,
        help='Ruta de la imagen a procesar'
    )
    
    parser.add_argument(
        '--camera',
        action='store_true',
        help='Capturar desde cámara web'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Modo interactivo (menú de opciones)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='model/mobilenetv2.h5',
        help='Ruta del modelo a usar (default: model/mobilenetv2.h5)'
    )
    
    parser.add_argument(
        '--no-speak',
        action='store_true',
        help='Desactivar texto-a-voz'
    )
    
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Mostrar resultado visual'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Verificar requisitos del sistema'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.check:
        print("🔍 Verificando requisitos del sistema...\n")
        if check_requirements():
            print("\n Todos los requisitos están cumplidos")
            print(" Puedes ejecutar el agente con: python main.py --interactive")
        else:
            print("\n Faltan algunos requisitos")
            print(" Consulta el README.md para más información")
        return
    
    if not check_requirements():
        print("\n No se puede iniciar el agente sin el modelo entrenado")
        return
    
    try:
        if args.gradio:
            print("\n Lanzando interfaz web con Gradio...")
            print("   La aplicación se abrirá en tu navegador\n")
            
            import subprocess
            subprocess.run(["python", "app_gradio.py"])
            return
        
        agent = BillRecognitionAgent(
            model_path=args.model,
            labels_path='model/labels.json',
            language='es',
            confidence_threshold=70.0
        )
        
        if args.interactive or (not args.image and not args.camera):
            agent.run_interactive()
        
        elif args.camera:
            print("\n Modo Cámara")
            print("   Controles: ESPACIO=capturar, ESC=salir\n")
            agent.process_from_camera(speak=not args.no_speak)
        
        elif args.image:
            agent.process_image(
                image_path=args.image,
                speak=not args.no_speak,
                visualize=args.visualize
            )
        
    except KeyboardInterrupt:
        print("\n\n Interrupción del usuario. ¡Hasta luego!")
    
    except Exception as e:
        print(f"\n Error crítico: {str(e)}")
        print("\n Intenta:")
        print("   1. Verificar que el modelo existe: python main.py --check")
        print("   2. Revisar logs de error arriba")
        print("   3. Consultar README.md para solución de problemas")


if __name__ == "__main__":
    main()