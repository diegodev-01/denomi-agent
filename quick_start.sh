#!/bin/bash

clear

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║               DENOMI-AGENT - INICIO RÁPIDO                   ║"
echo "║                                                              ║"
echo "║         Sistema de Reconocimiento de Billetes con IA         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

ask_yes_no() {
    while true; do
        read -p "$1 (s/n): " yn
        case $yn in
            [Ss]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Por favor responde s o n.";;
        esac
    done
}

echo " Paso 1: Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "    Python encontrado: $PYTHON_VERSION"
else
    echo "    Python 3 no encontrado. Por favor instálalo primero."
    exit 1
fi

echo ""
echo " Paso 2: Entorno Virtual"
if [ -d "venv" ]; then
    echo "    Entorno virtual ya existe"
else
    if ask_yes_no "   ¿Crear entorno virtual?"; then
        echo "   Creando entorno virtual..."
        python3 -m venv venv
        echo "    Entorno virtual creado"
    fi
fi

if [ -d "venv" ]; then
    echo "   Activando entorno virtual..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    echo "    Entorno virtual activado"
fi

echo ""
echo " Paso 3: Instalando Dependencias"
if ask_yes_no "   ¿Instalar/actualizar dependencias?"; then
    echo "   Instalando paquetes..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "    Dependencias instaladas"
fi

echo ""
echo " Paso 4: Estructura del Proyecto"
if [ ! -d "data/raw" ] || [ ! -d "model" ]; then
    if ask_yes_no "   ¿Crear estructura de directorios?"; then
        echo "   Creando directorios..."
        python setup_project.py
        echo "    Estructura creada"
    fi
fi

echo ""
echo " Paso 5: Dataset"
if [ -z "$(ls -A data/raw 2>/dev/null)" ]; then
    echo "      No se encontraron datos en data/raw/"
    echo ""
    echo "      Organiza tus imágenes así:"
    echo "      data/raw/10_bolivianos/"
    echo "      data/raw/20_bolivianos/"
    echo "      data/raw/50_bolivianos/"
    echo "      data/raw/100_bolivianos/"
    echo "      data/raw/200_bolivianos/"
    echo ""
    
    if ask_yes_no "   ¿Ya organizaste tus imágenes?"; then
        if ask_yes_no "   ¿Preprocesar dataset ahora?"; then
            echo "   Preprocesando imágenes..."
            python src/data/preprocess.py
            echo "    Dataset preprocesado"
        fi
    else
        echo "    Organiza las imágenes y ejecuta: python src/data/preprocess.py"
    fi
else
    echo "    Dataset encontrado en data/raw/"
fi

echo ""
echo " Paso 6: Modelo de IA"
if [ -f "model/mobilenetv2.h5" ]; then
    echo "    Modelo encontrado: model/mobilenetv2.h5"
else
    echo "     No se encontró modelo entrenado"
    
    if ask_yes_no "   ¿Entrenar modelo ahora? (puede tomar 30-60 min)"; then
        echo "   🏋️  Iniciando entrenamiento..."
        bash scripts/train.sh
        echo "    Modelo entrenado"
    else
        echo "    Entrena el modelo después con: bash scripts/train.sh"
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                     CONFIGURACIÓN COMPLETA                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo " ¡Todo listo para usar!"
echo ""
echo "Elige cómo quieres ejecutar la aplicación:"
echo ""
echo " Interfaz Web (Gradio) - RECOMENDADO "
echo "   → python app_gradio.py"
echo "   → Se abrirá en tu navegador"
echo "   → Fácil de usar con cámara"
echo ""
echo "  Línea de comandos (CLI) "
echo "   → python main.py --interactive"
echo "   → Menú interactivo en terminal"
echo ""
echo " Procesar una imagen "
echo "   → python main.py --image ruta/imagen.jpg"
echo ""

if [ -f "model/mobilenetv2.h5" ]; then
    echo ""
    if ask_yes_no "¿Ejecutar interfaz web ahora?"; then
        echo ""
        echo "🌐 Iniciando aplicación web Gradio..."
        echo "   Se abrirá en: http://localhost:7860"
        echo ""
        echo "⌨️  Presiona Ctrl+C para detener"
        echo ""
        python app_gradio.py
    fi
else
    echo ""
    echo "  Primero necesitas entrenar el modelo:"
    echo "   bash scripts/train.sh"
fi

echo ""
echo " ¡Hasta luego!"