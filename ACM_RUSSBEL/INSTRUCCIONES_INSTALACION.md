# 🚀 GUÍA DE INSTALACIÓN PASO A PASO

## PROBLEMA COMÚN: Error "Missing optional dependency 'openpyxl'"

Si estás viendo este error, significa que necesitas instalar las dependencias de Python en tu entorno local.

## SOLUCIÓN RÁPIDA (RECOMENDADA):

### 1. Abre una terminal en la carpeta del proyecto

### 2. Ejecuta el script de verificación:
```bash
python verificar_instalacion.py
```

### 3. Si faltan dependencias, instálalas:
```bash
pip install Flask pandas numpy scikit-learn matplotlib seaborn openpyxl Werkzeug
```

### 4. Verifica nuevamente:
```bash
python verificar_instalacion.py
```

### 5. Ejecuta la aplicación:
```bash
python app.py
```

## INSTALACIÓN ALTERNATIVA:

### Opción 1 - Script automático (MÁS FÁCIL):
```bash
python install.py
```

### Opción 2 - Archivo requirements:
```bash
pip install -r requirements_project.txt
```

### Opción 3 - Install requirements antiguo:
```bash
pip install -r install_requirements.txt
```

## VERIFICACIÓN MANUAL:

Para verificar específicamente openpyxl:
```bash
python -c "import openpyxl; print('✓ openpyxl funciona correctamente')"
```

## SOLUCIÓN DE PROBLEMAS:

### Si usas un entorno virtual:
1. Asegúrate de que esté activado
2. Instala las dependencias en el entorno virtual

### Si el error persiste:
```bash
pip uninstall openpyxl
pip install openpyxl
```

### Para entornos conda:
```bash
conda install openpyxl
```

## ESTRUCTURA DE CARPETAS NECESARIA:

Tu proyecto debe tener:
```
acm-analyzer/
├── app.py
├── templates/
├── static/
├── uploads/ (se creará automáticamente)
└── (estos archivos de instalación)
```

## PRUEBA FINAL:

1. Ejecuta: `python verificar_instalacion.py`
2. Si todo está ✓, ejecuta: `python app.py`
3. Abre http://localhost:5000
4. ¡Prueba cargar un archivo Excel!