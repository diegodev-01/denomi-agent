# 🌐 Guía de Uso - Interfaz Web con Gradio

Esta guía te ayudará a usar la aplicación web del reconocedor de billetes.

---

## 🚀 Inicio Rápido

### Ejecutar la aplicación

```bash
python app_gradio.py
```

O usando main.py:

```bash
python main.py --gradio
```

La aplicación se abrirá automáticamente en tu navegador en: **http://localhost:7860**

---

## 📱 Usando la Interfaz

### Pestaña 1: 📷 Captura desde Cámara

**Para personas con discapacidad visual:**
1. Al abrir esta pestaña, tu navegador pedirá permiso para usar la cámara
2. **Acepta el permiso**
3. Coloca el billete frente a la cámara
4. El lector de pantalla anunciará: "Cámara Web"
5. Presiona **Tab** hasta llegar al botón "Reconocer Billete"
6. Presiona **Enter** o **Espacio**
7. Espera unos segundos
8. El resultado se **reproducirá automáticamente por audio** 🔊
9. También aparecerá como texto que tu lector de pantalla puede leer

**Consejos:**
- ✅ Asegúrate de tener buena iluminación
- ✅ Mantén el billete a unos 30cm de la cámara
- ✅ Usa un fondo contrastante (ej: mesa oscura)
- ✅ El billete debe estar completamente visible

### Pestaña 2: 📁 Subir Imagen

**Para usuarios que ya tienen una foto:**
1. Navega a la pestaña "Subir Imagen"
2. Presiona Tab hasta "Seleccionar Imagen"
3. Presiona Enter para abrir el selector de archivos
4. Selecciona la foto del billete
5. Presiona Tab hasta "Reconocer Billete"
6. Presiona Enter
7. Escucha el resultado por audio automáticamente 🔊

### Pestaña 3: ℹ️ Información

Contiene información sobre el sistema, consejos de uso y tecnología.

---

## 🔊 Audio (Texto-a-Voz)

### ¿Cómo funciona?

El sistema tiene una casilla **"Habilitar retroalimentación de voz"** que está **activada por defecto**.

Cuando reconoce un billete:
- ✅ **Alta confianza (>90%)**: "Billete de X bolivianos"
- ⚠️ **Confianza media (70-90%)**: "Posible billete de X bolivianos, con Y por ciento de confianza"
- ❌ **Baja confianza (<70%)**: "No estoy seguro, intente con mejor iluminación"

El audio se **reproduce automáticamente** después de la predicción.

### Desactivar audio

Si prefieres solo ver el resultado (sin audio):
1. Desmarca la casilla "🔊 Habilitar retroalimentación de voz"
2. El sistema solo mostrará texto

---

## ⌨️ Atajos de Teclado

- **Tab**: Navegar entre elementos
- **Shift + Tab**: Navegar hacia atrás
- **Enter** o **Espacio**: Activar botones
- **Ctrl + C**: Cerrar la aplicación (en la terminal)

---

## 🌍 Compartir la Aplicación

### Opción 1: Uso Local (por defecto)
- Solo tú puedes acceder: `http://localhost:7860`
- Ideal para uso personal

### Opción 2: Red Local
La aplicación ya está configurada para ser accesible desde otros dispositivos en tu red:
- Otros dispositivos en tu WiFi pueden acceder usando tu IP
- Ejemplo: `http://192.168.1.100:7860`

Para ver tu IP:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

### Opción 3: Link Público Temporal

Si quieres que alguien fuera de tu red use la aplicación:

1. Edita `app_gradio.py`
2. Busca la línea:
   ```python
   app.launch(share=False)
   ```
3. Cámbiala a:
   ```python
   app.launch(share=True)
   ```
4. Guarda y ejecuta: `python app_gradio.py`
5. Verás un link público: `https://xxxxx.gradio.live`
6. **Este link es temporal** (72 horas máximo)
7. Compártelo con quien quieras

**⚠️ Importante:**
- El link público expone tu aplicación a internet
- Solo úsalo si es necesario
- El link expira después de 72 horas

---

## 🎯 Mejores Prácticas

### Para mejores resultados:

#### Iluminación ✨
- ✅ Usa luz natural o luz blanca
- ✅ Evita sombras sobre el billete
- ❌ No uses flash directo
- ❌ Evita luz muy amarilla o tenue

#### Posición 📐
- ✅ Billete completamente visible
- ✅ Paralelo a la cámara
- ✅ A unos 30cm de distancia
- ❌ No inclinado o doblado

#### Fondo 🖼️
- ✅ Fondo uniforme y contrastante
- ✅ Mesa oscura ideal para billetes claros
- ✅ Mesa clara ideal para billetes oscuros
- ❌ Evita fondos con patrones

#### Estado del Billete 💵
- ✅ Billetes en buen estado: 95-99% precisión
- ⚠️ Billetes desgastados: 85-95% precisión
- ❌ Billetes muy dañados: puede fallar

---

## 🐛 Solución de Problemas

### La cámara no funciona
1. Verifica permisos en tu navegador
2. Chrome → Configuración → Privacidad → Configuración de sitios → Cámara
3. Asegúrate de que `localhost` tenga permiso

### El audio no se reproduce
1. Verifica que tu navegador no esté en silencio
2. Verifica el volumen del sistema
3. Algunos navegadores bloquean autoplay de audio
4. Solución: Haz clic en la página primero, luego captura

### La aplicación no se abre
```bash
# Verifica que Gradio esté instalado
pip install gradio==4.44.0

# Verifica que no haya otro proceso usando el puerto 7860
# Windows: netstat -ano | findstr 7860
# Linux/Mac: lsof -i :7860
```

### Error: "No se encontró el modelo"
```bash
# Entrenar el modelo primero
bash scripts/train.sh
```

### Predicciones incorrectas
- Mejora la iluminación
- Asegúrate de que el billete esté completamente visible
- Intenta con un fondo más contrastante
- Si el billete está muy desgastado, la precisión baja

---

## 📊 Interpretando los Resultados

### Niveles de Confianza

| Confianza | Significado | Recomendación |
|-----------|-------------|---------------|
| 90-100% ✅ | **Alta confianza** | El sistema está muy seguro |
| 70-89% ⚠️ | **Confianza media** | Probablemente correcto, pero verifica |
| 0-69% ❌ | **Baja confianza** | Intenta con mejor iluminación |

### Imagen Anotada

El sistema muestra la imagen con:
- **Texto verde** = Alta confianza (>90%)
- **Texto amarillo** = Confianza media (70-90%)
- **Texto rojo** = Baja confianza (<70%)
- **Porcentaje** = Nivel de confianza exacto

---

## 🔒 Privacidad y Seguridad

### ✅ Lo que hace el sistema:
- Procesa imágenes **localmente** en tu computadora
- **NO guarda** ni **NO sube** ninguna imagen a internet
- Los archivos temporales se **eliminan automáticamente**
- El audio se genera **localmente**

### ❌ Lo que NO hace:
- No guarda historial de billetes
- No envía datos a servidores externos
- No almacena información personal

---

## 💡 Consejos Avanzados

### Para Desarrolladores

#### Personalizar el puerto
```python
# En app_gradio.py
app.launch(server_port=8080)  # Cambia 7860 por tu puerto
```

#### Modo debug
```python
app.launch(debug=True)  # Ver logs detallados
```

#### Cambiar tema
```python
# En create_gradio_interface()
with gr.Blocks(theme=gr.themes.Glass()):  # Prueba: Glass, Monochrome, Soft
```

#### Desactivar autoplay de audio
```python
# En la definición de audio
gr.Audio(autoplay=False)  # El usuario debe dar play manualmente
```