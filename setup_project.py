from pathlib import Path


def create_directory_structure():
    """Crear todas las carpetas necesarias del proyecto"""
    
    directories = [
        # Datos
        "data/raw",
        "data/processed",
        "data/samples",
        
        # Notebooks
        "notebooks",
        
        # Código fuente
        "src/data",
        "src/models",
        "src/inference",
        
        # Modelos
        "model",
        
        # Scripts
        "scripts",
        
        # Logs
        "logs/tensorboard",
    ]
    
    print("📁 Creando estructura de directorios...\n")
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        gitkeep = dir_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        
        print(f"   ✓ {directory}")
    
    print("\n Estructura de directorios creada exitosamente!")


def create_init_files():
    """Crear archivos __init__.py necesarios"""
    
    init_files = [
        "src/__init__.py",
        "src/data/__init__.py",
        "src/models/__init__.py",
        "src/inference/__init__.py",
    ]
    
    print("\n Creando archivos __init__.py...\n")
    
    for init_file in init_files:
        init_path = Path(init_file)
        init_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not init_path.exists():
            init_path.touch()
            print(f"   ✓ {init_file}")
    
    print("\n Archivos __init__.py creados!")


def create_readme_for_data():
    """Crear README en carpeta data explicando estructura"""
    
    readme_content = """# Directorio de Datos

Este directorio contiene el dataset del proyecto.

## Estructura

- `raw/` - Dataset original sin procesar
  - Organizar por carpetas según clase
  - Ejemplo: `raw/10_bolivianos/`, `raw/20_bolivianos/`, etc.

- `processed/` - Imágenes preprocesadas (generadas automáticamente)
  - Redimensionadas a 224x224
  - Normalizadas
  - Mejoradas (contraste, brillo)

- `samples/` - Subset reducido para pruebas rápidas
  - Generado automáticamente
  - ~50 imágenes por clase

## Uso

1. Coloca tus imágenes originales en `raw/<nombre_clase>/`
2. Ejecuta: `python src/data/preprocess.py`
3. Las imágenes procesadas aparecerán en `processed/`

##  Importante

**Los datos NO se suben a GitHub** (están en .gitignore)
"""
    
    readme_path = Path("data/README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("\n README.md creado en data/")


def print_next_steps():
    """Imprimir los próximos pasos"""
    
    next_steps = """
╔══════════════════════════════════════════════════════════════╗
║                       CONFIGURACIÓN COMPLETA                 ║
╚══════════════════════════════════════════════════════════════╝

 Próximos pasos:

  Instalar dependencias:
   pip install -r requirements.txt

  Organizar dataset:
   - Coloca imágenes en data/raw/<clase>/
   - Estructura: data/raw/10_bolivianos/, data/raw/20_bolivianos/, etc.

  Preprocesar datos:
   python src/data/preprocess.py

  Entrenar modelo:
   bash scripts/train.sh

  Evaluar modelo:
   bash scripts/evaluate.sh

  Ejecutar agente:
   python main.py --interactive

 Más información: README.md
 Problemas: Consulta la sección de solución de problemas

¡Listo para comenzar! 
"""
    
    print(next_steps)


def main():
    
    print("="*60)
    print("  CONFIGURACIÓN INICIAL DEL PROYECTO")
    print("="*60)
    print()
    
    create_directory_structure()
    create_init_files()
    create_readme_for_data()
    
    print_next_steps()


if __name__ == "__main__":
    main()