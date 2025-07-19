#!/usr/bin/env python3
"""
Script automático de instalación para la aplicación ACM.
Instala todas las dependencias necesarias y verifica la instalación.
"""

import subprocess
import sys

def instalar_dependencia(paquete):
    """Instala una dependencia usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    dependencias = [
        "Flask==3.0.0",
        "pandas==2.1.4",
        "numpy==1.25.2",
        "scikit-learn==1.3.2",
        "matplotlib==3.8.2",
        "seaborn==0.13.0",
        "openpyxl==3.1.2",
        "Werkzeug==3.0.1"
    ]
    
    print("=== INSTALADOR AUTOMÁTICO ACM ===\n")
    print("Instalando dependencias necesarias...\n")
    
    errores = []
    
    for dependencia in dependencias:
        nombre = dependencia.split("==")[0]
        print(f"Instalando {nombre}...", end=" ")
        
        if instalar_dependencia(dependencia):
            print("✓ INSTALADO")
        else:
            print("✗ ERROR")
            errores.append(dependencia)
    
    print("\n" + "="*50)
    
    if not errores:
        print("🎉 ¡INSTALACIÓN COMPLETADA!")
        print("Ejecuta 'python app.py' para iniciar la aplicación.")
    else:
        print("❌ ERRORES EN LA INSTALACIÓN:")
        for error in errores:
            print(f"  - {error}")
        print("\nIntenta instalar manualmente:")
        print(f"pip install {' '.join(errores)}")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()