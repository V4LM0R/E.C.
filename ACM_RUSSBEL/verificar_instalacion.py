#!/usr/bin/env python3
"""
Script para verificar que todas las dependencias necesarias estén instaladas correctamente.
Ejecuta este script antes de correr la aplicación ACM.
"""

def verificar_dependencias():
    dependencias = [
        ('Flask', 'flask'),
        ('Pandas', 'pandas'),
        ('NumPy', 'numpy'),
        ('Scikit-learn', 'sklearn'),
        ('Matplotlib', 'matplotlib'),
        ('Seaborn', 'seaborn'),
        ('OpenPyXL', 'openpyxl'),
        ('Werkzeug', 'werkzeug')
    ]
    
    print("=== VERIFICACIÓN DE DEPENDENCIAS ACM ===\n")
    
    todas_instaladas = True
    faltantes = []
    
    for nombre, modulo in dependencias:
        try:
            __import__(modulo)
            print(f"✓ {nombre} - INSTALADO")
        except ImportError:
            print(f"✗ {nombre} - NO ENCONTRADO")
            todas_instaladas = False
            faltantes.append(modulo)
    
    print("\n" + "="*50)
    
    if todas_instaladas:
        print("🎉 ¡EXCELENTE! Todas las dependencias están instaladas.")
        print("Puedes ejecutar la aplicación con: python app.py")
    else:
        print("❌ FALTAN DEPENDENCIAS")
        print("\nPara instalar las dependencias faltantes, ejecuta:")
        print(f"pip install {' '.join(faltantes)}")
        print("\nO instala todas las dependencias con:")
        print("pip install Flask pandas numpy scikit-learn matplotlib seaborn openpyxl Werkzeug")
    
    print("\n" + "="*50)
    return todas_instaladas

if __name__ == "__main__":
    verificar_dependencias()