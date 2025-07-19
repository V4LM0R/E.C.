# Análisis de Correspondencia Multivariado (ACM) - Aplicación Web Educativa

## 📋 Descripción

Aplicación web educativa completa desarrollada con Flask que enseña y permite realizar **Análisis de Correspondencia Multivariado (ACM)**. La aplicación combina contenido educativo interactivo con una herramienta práctica de análisis de datos categóricos.

## 🌟 Características Principales

### 🎓 Contenido Educativo
- **Explicación completa del ACM**: Conceptos fundamentales y aplicaciones prácticas
- **Fundamentos matemáticos**: Descomposición en valores singulares y proyecciones
- **Subtemas especializados**: Interpretación de resultados, métricas de evaluación, ventajas y consideraciones
- **Minijuego interactivo**: Simulador didáctico para entender agrupaciones de datos categóricos

### 🔧 Herramienta de Análisis
- **Carga de datos**: Soporte para archivos CSV y XLSX
- **Validación automática**: Detección de variables categóricas y verificación de requisitos
- **Configuración flexible**: Selección de variables y parámetros de análisis
- **Visualizaciones avanzadas**: Scree plot, biplot y distribuciones de variables
- **Interpretación guiada**: Métricas de calidad y recomendaciones automáticas

### 🎨 Interfaz de Usuario
- **Diseño responsivo**: Compatible con dispositivos móviles y de escritorio
- **Paleta de colores verde**: Tema visual consistente y profesional
- **Interactividad**: Drag & drop, tooltips, animaciones y efectos visuales
- **Navegación intuitiva**: Flujo de trabajo paso a paso

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Instalación Automática (RECOMENDADA)
```bash
# Script automático que instala todo
python install.py

# Ejecutar la aplicación
python app.py
```

### Instalación Manual con Requirements
```bash
# Usar archivo requirements del proyecto
pip install -r requirements_project.txt

# O instalación manual
pip install Flask pandas numpy scikit-learn matplotlib seaborn openpyxl Werkzeug
```

⚠️ **IMPORTANTE**: La dependencia `openpyxl` es ESENCIAL para procesar archivos Excel. Sin ella, la aplicación fallará al analizar archivos .xlsx.

### 🔍 Verificación de Instalación
Antes de ejecutar la aplicación, verifica que todas las dependencias estén instaladas:
```bash
python verificar_instalacion.py
```

Si aparece el error "Missing optional dependency 'openpyxl'", consulta el archivo `INSTRUCCIONES_INSTALACION.md` para una guía detallada de solución.

### Acceso
La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
acm-analyzer/
├── app.py                 # Servidor Flask principal
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
├── replit.md             # Documentación del proyecto
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal educativa
│   ├── acm_tool.html     # Interfaz de carga de datos
│   ├── configure_acm.html # Configuración de análisis
│   └── results.html      # Resultados y visualizaciones
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos personalizados
│   └── data/
│       └── ejemplo_acm.csv # Datos de ejemplo
└── uploads/              # Directorio para archivos subidos
```

## 🎮 Cómo Usar la Aplicación

### 1. Aprendizaje Interactivo
1. **Visita la página principal** para aprender sobre ACM
2. **Juega el minijuego** para entender cómo funciona la agrupación de datos
3. **Lee las explicaciones** de fundamentos matemáticos y conceptos clave

### 2. Análisis de Datos
1. **Carga tu archivo** CSV o XLSX con datos categóricos
2. **Configura el análisis** seleccionando variables y parámetros
3. **Revisa los resultados** con gráficos interactivos y métricas
4. **Interpreta los hallazgos** usando las guías proporcionadas

### 3. Simulador Interactivo de ACM
- **Objetivo**: Identificar grupos de personas con características similares
- **Características del simulador**:
  - **Tutorial paso a paso**: 4 pasos claros para aprender
  - **Leyenda visual**: Códigos de colores para edad, ciudad y hobby
  - **Tarjetas de personas**: Información visual clara con avatares
  - **Grupos objetivo**: Ejemplos de agrupaciones correctas
  - **Sistema de pistas**: 3 niveles de ayuda progresiva
  - **Contadores dinámicos**: Seguimiento de personas seleccionadas
  - **Feedback detallado**: Explicaciones sobre los resultados

- **Instrucciones**: 
  1. Observa las características de cada persona en su tarjeta
  2. Identifica patrones entre personas similares
  3. Haz clic en las tarjetas para seleccionar personas del mismo grupo
  4. Usa el botón "Pista" si necesitas ayuda
  5. Verifica tu agrupación y aprende de los resultados
  6. Reinicia para practicar más veces

## 📊 Especificaciones Técnicas

### Formato de Datos Requerido
- **Tipo de archivo**: CSV o XLSX
- **Estructura**: Matriz individuos × variables categóricas
- **Variables**: Mínimo 3 variables categóricas
- **Observaciones**: Mínimo 50 individuos (recomendado)
- **Codificación**: UTF-8 para archivos CSV
- **Valores faltantes**: Se eliminan automáticamente

### Ejemplo de Datos Válidos
```csv
ID,Edad_Grupo,Ciudad,Educacion,Ocupacion,Hobby_Principal
001,Joven,Madrid,Universitaria,Ingeniero,Tecnología
002,Adulto,Barcelona,Secundaria,Comerciante,Deportes
003,Senior,Valencia,Universitaria,Profesor,Lectura
```

## 🔧 Dependencias Tecnológicas

### Backend
- **Flask**: Framework web principal
- **Pandas**: Análisis y manipulación de datos
- **NumPy**: Computación numérica
- **Scikit-learn**: Algoritmos de machine learning (PCA para ACM)
- **Matplotlib**: Generación de gráficos
- **Seaborn**: Visualizaciones estadísticas
- **Openpyxl**: Lectura de archivos Excel

### Frontend
- **Bootstrap 5**: Framework CSS responsivo
- **Font Awesome**: Iconos
- **JavaScript**: Interactividad y efectos

## 🎯 Funcionalidades del Simulador

### Mecánica de Juego
- **Datos de ejemplo**: 8 personas con diferentes características
- **Interacción**: Clic para seleccionar/deseleccionar tarjetas
- **Contador dinámico**: Personas seleccionadas y grupos encontrados
- **Sistema de pistas**: 3 niveles de ayuda progresiva
- **Retroalimentación**: Análisis detallado de la agrupación

### Grupos Objetivo
- **Grupo A**: Jóvenes de Madrid con intereses tecnológicos (Ana, Carlos)
- **Grupo B**: Adultos de Barcelona con intereses culturales (Beatriz, David)
- **Grupo C**: Jóvenes de Valencia con intereses deportivos (Elena, Francisco)
- **Casos únicos**: Personas con combinaciones específicas (Gloria, Héctor)

### Efectos Visuales
- **Hover**: Efecto de escala y sombra
- **Selección**: Animación de pulso y brillo
- **Tarjetas**: Diseño atractivo con avatares coloridos
- **Animaciones**: Transiciones suaves CSS
- **Scroll automático**: Navegación hacia resultados

## 🚀 Características Avanzadas

### Análisis ACM
- **Aproximación PCA**: Implementación usando descomposición en componentes principales
- **Múltiples visualizaciones**: Scree plot, biplot, distribuciones
- **Métricas de calidad**: Evaluación automática de resultados
- **Interpretación guiada**: Recomendaciones basadas en los datos

### Validación de Datos
- **Detección automática**: Identificación de variables categóricas
- **Verificación de requisitos**: Mínimo de variables y observaciones
- **Manejo de errores**: Mensajes informativos y sugerencias
- **Limpieza de datos**: Eliminación de valores faltantes

### Experiencia de Usuario
- **Diseño responsivo**: Adaptable a diferentes tamaños de pantalla
- **Navegación fluida**: Transiciones entre páginas
- **Feedback visual**: Indicadores de progreso y estado
- **Accesibilidad**: Uso de colores contrastantes y elementos semánticos

## 🎨 Paleta de Colores

- **Verde primario**: `#2E8B57` (SeaGreen)
- **Verde claro**: `#90EE90` (LightGreen)
- **Verde oscuro**: `#006400` (DarkGreen)
- **Verde acento**: `#32CD32` (LimeGreen)
- **Verde suave**: `#F0FFF0` (Honeydew)
- **Verde medio**: `#228B22` (ForestGreen)

## 📱 Compatibilidad

### Navegadores Soportados
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Dispositivos
- **Desktop**: Resoluciones 1024px y superiores
- **Tablet**: Resoluciones 768px - 1024px
- **Mobile**: Resoluciones 320px - 768px

## 🔄 Flujo de Trabajo

### Proceso de Análisis
1. **Educación** → Página principal con conceptos y minijuego
2. **Carga** → Upload de archivo con validación
3. **Configuración** → Selección de variables y parámetros
4. **Procesamiento** → Análisis ACM con generación de gráficos
5. **Resultados** → Visualización e interpretación

### Estados de la Aplicación
- **Inicial**: Página educativa
- **Carga**: Validación de archivos
- **Configuración**: Selección de parámetros
- **Procesamiento**: Análisis en curso
- **Resultados**: Visualización completa

## 🛠️ Desarrollo y Mantenimiento

### Estructura del Código
- **Modular**: Separación clara entre frontend y backend
- **Escalable**: Fácil añadir nuevas funcionalidades
- **Mantenible**: Código comentado y documentado
- **Testeable**: Funciones independientes y reutilizables

### Configuración de Desarrollo
```bash
# Modo desarrollo
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Archivos de Configuración
- **app.py**: Configuración principal del servidor
- **style.css**: Estilos y tema visual
- **replit.md**: Documentación técnica del proyecto

## 📈 Métricas y Evaluación

### Calidad del Análisis
- **Varianza explicada**: Porcentaje de información capturada
- **Inercia total**: Variabilidad en los datos
- **Calidad de representación**: Precisión de la proyección
- **Eigenvalues**: Importancia de cada componente

### Evaluación Automática
- **Excelente**: >70% varianza explicada en 2 componentes
- **Buena**: 50-70% varianza explicada
- **Regular**: <50% varianza explicada

## 🎯 Casos de Uso

### Educativo
- **Cursos universitarios**: Estadística multivariada
- **Investigación**: Análisis de encuestas y cuestionarios
- **Tesis**: Estudios de comportamiento y preferencias

### Profesional
- **Marketing**: Segmentación de clientes
- **Recursos Humanos**: Análisis de perfiles laborales
- **Investigación Social**: Estudios de opinión pública

## 💡 Consejos de Uso

### Mejores Prácticas
1. **Prepara tus datos** en formato CSV con encabezados claros
2. **Usa variables categóricas** con 2-20 categorías cada una
3. **Incluye suficientes observaciones** (mínimo 50, ideal 200+)
4. **Selecciona variables relevantes** para tu análisis
5. **Interpreta los resultados** usando las guías proporcionadas

### Solución de Problemas
- **Error de formato**: Verifica que sea CSV o XLSX válido
- **Pocas variables**: Necesitas al menos 3 variables categóricas
- **Muestra pequeña**: Considera recopilar más datos
- **Resultados pobres**: Revisa la calidad de las variables

## 🔗 Enlaces Útiles

- **Documentación ACM**: Recursos teóricos sobre análisis de correspondencia
- **Ejemplos de datos**: Casos de uso reales y plantillas
- **Guías de interpretación**: Cómo leer y entender los resultados

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una branch para tu feature
3. Commit tus cambios
4. Push a la branch
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas sobre el ACM:
- Abre un issue en el repositorio
- Consulta la documentación en `replit.md`
- Revisa los ejemplos incluidos

---

**Desarrollado con ❤️ para hacer el Análisis de Correspondencia Multivariado accesible y comprensible para todos.**