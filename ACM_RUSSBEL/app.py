from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import io
import base64
import os
from werkzeug.utils import secure_filename

# Configure matplotlib backend first
import matplotlib
matplotlib.use('Agg')

# Check for openpyxl dependency
try:
    import openpyxl
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False

app = Flask(__name__)
app.secret_key = 'acm_secret_key_2025'

# Configuración para uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear directorio uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acm_tool')
def acm_tool():
    return render_template('acm_tool.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se seleccionó archivo')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No se seleccionó archivo')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Procesar archivo
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                # Verificar si openpyxl está disponible para archivos Excel
                try:
                    df = pd.read_excel(filepath, engine='openpyxl')
                except ImportError:
                    flash('Error: Para procesar archivos Excel (.xlsx) necesitas instalar openpyxl. Ejecuta: pip install openpyxl')
                    return redirect(url_for('acm_tool'))
                except Exception as e:
                    # Intentar sin especificar engine como fallback
                    try:
                        df = pd.read_excel(filepath)
                    except ImportError:
                        flash('Error: Para procesar archivos Excel (.xlsx) necesitas instalar openpyxl. Ejecuta: pip install openpyxl')
                        return redirect(url_for('acm_tool'))
            
            # Validar datos
            if len(df) < 50:
                flash('Advertencia: Se recomiendan al menos 50 observaciones para mejores resultados')
            
            # Identificar variables categóricas
            categorical_columns = []
            for col in df.columns:
                if df[col].dtype == 'object' or df[col].nunique() < 20:
                    categorical_columns.append(col)
            
            if len(categorical_columns) < 3:
                flash('Error: Se necesitan al menos 3 variables categóricas')
                return redirect(url_for('acm_tool'))
            
            # Guardar información del dataset
            app.config['current_data'] = {
                'dataframe': df,
                'categorical_columns': categorical_columns,
                'filename': filename
            }
            
            return redirect(url_for('configure_acm'))
            
        except Exception as e:
            flash(f'Error al procesar archivo: {str(e)}')
            return redirect(url_for('acm_tool'))
    
    flash('Formato de archivo no válido')
    return redirect(url_for('acm_tool'))

@app.route('/configure_acm')
def configure_acm():
    if 'current_data' not in app.config:
        flash('Primero debe cargar un archivo')
        return redirect(url_for('acm_tool'))
    
    data_info = app.config['current_data']
    return render_template('configure_acm.html', 
                         columns=data_info['categorical_columns'],
                         filename=data_info['filename'],
                         num_rows=len(data_info['dataframe']))

@app.route('/analyze_acm', methods=['POST'])
def analyze_acm():
    if 'current_data' not in app.config:
        return redirect(url_for('acm_tool'))
    
    # Obtener configuración
    selected_columns = request.form.getlist('columns')
    n_components = int(request.form.get('n_components', 2))
    
    if len(selected_columns) < 3:
        flash('Seleccione al menos 3 variables')
        return redirect(url_for('configure_acm'))
    
    try:
        df = app.config['current_data']['dataframe']
        
        # Preparar datos para ACM
        df_selected = df[selected_columns].copy()
        df_selected = df_selected.dropna()  # Eliminar valores faltantes
        
        # Crear matriz indicadora (dummy variables)
        df_encoded = pd.get_dummies(df_selected, prefix=selected_columns)
        
        # Aplicar PCA (aproximación al ACM)
        pca = PCA(n_components=n_components)
        transformed_data = pca.fit_transform(df_encoded)
        
        # Generar visualizaciones
        plots = generate_acm_plots(transformed_data, pca, df_selected, selected_columns)
        
        # Calcular métricas
        explained_variance = pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)
        
        results = {
            'transformed_data': transformed_data,
            'explained_variance': explained_variance,
            'cumulative_variance': cumulative_variance,
            'n_observations': len(df_selected),
            'n_variables': len(selected_columns),
            'plots': plots,
            'selected_columns': selected_columns
        }
        
        app.config['acm_results'] = results
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        flash(f'Error en el análisis: {str(e)}')
        return redirect(url_for('configure_acm'))

def generate_acm_plots(transformed_data, pca, df_original, columns):
    plots = {}
    
    # Configurar estilo
    plt.style.use('default')
    sns.set_palette("Greens_r")
    
    # Plot 1: Scree plot (varianza explicada)
    fig, ax = plt.subplots(figsize=(10, 6))
    components = range(1, len(pca.explained_variance_ratio_) + 1)
    ax.bar(components, pca.explained_variance_ratio_ * 100, color='#2E8B57')
    ax.set_xlabel('Componentes')
    ax.set_ylabel('Varianza Explicada (%)')
    ax.set_title('Varianza Explicada por Componente')
    ax.grid(True, alpha=0.3)
    
    plots['scree'] = plot_to_base64(fig)
    plt.close(fig)
    
    # Plot 2: Biplot (primeras dos componentes)
    if transformed_data.shape[1] >= 2:
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(transformed_data[:, 0], transformed_data[:, 1], 
                           alpha=0.6, c='#228B22', s=50)
        ax.set_xlabel(f'Componente 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
        ax.set_ylabel(f'Componente 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
        ax.set_title('Biplot - Primeras Dos Componentes')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)
        
        plots['biplot'] = plot_to_base64(fig)
        plt.close(fig)
    
    # Plot 3: Distribución de categorías
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, col in enumerate(columns[:4]):  # Máximo 4 variables
        if i < len(axes):
            df_original[col].value_counts().plot(kind='bar', ax=axes[i], color='#32CD32')
            axes[i].set_title(f'Distribución de {col}')
            axes[i].set_xlabel('')
            axes[i].tick_params(axis='x', rotation=45)
    
    # Ocultar axes no utilizados
    for i in range(len(columns), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plots['distribution'] = plot_to_base64(fig)
    plt.close(fig)
    
    return plots

def plot_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)