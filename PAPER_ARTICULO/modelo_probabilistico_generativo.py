import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report

def generate_sample_from_nb_with_gen_sub(clf, generico_val, cond_probs):
    # Muestrear subgenerico dado generico
    subgen_candidates = cond_probs[generico_val].index.to_list()
    subgen_probs = cond_probs[generico_val].values
    sampled_subgen = np.random.choice(subgen_candidates, p=subgen_probs)

    class_idx = np.where(clf.classes_ == sampled_subgen)[0][0]

    n_features = clf.feature_log_prob_.shape[1]
    sample_features = []

    for feature_idx in range(n_features):
        log_probs = clf.feature_log_prob_[class_idx, feature_idx]
        probs = np.exp(log_probs)
        probs /= probs.sum()
        sampled_value = np.random.choice(len(probs), p=probs)
        sample_features.append(sampled_value)

    # Forzar que la feature 'generico' tenga el valor que muestreamos (para respetar distribución)
    generico_idx = list(X.columns).index('generico')
    sample_features[generico_idx] = generico_val

    return sampled_subgen, sample_features

# Leer archivo CSV
df = pd.read_csv("denunciados.csv", delimiter=';')

# Gráficos de exploración: género y subgénero
genero_counts = df.groupby("generico")["cantidad"].sum().reset_index().sort_values(by="cantidad", ascending=False)
subgenero_counts = df.groupby("subgenerico")["cantidad"].sum().reset_index().sort_values(by="cantidad", ascending=False)

# Gráfico por género
plt.figure(figsize=(12, 6))
sns.barplot(data=genero_counts, x="generico", y="cantidad", palette="viridis")
plt.title("Cantidad de Delitos por Género")
plt.xticks(rotation=90)
plt.xlabel("Género del Delito")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.show()

# Gráfico por subgénero
plt.figure(figsize=(14, 6))
sns.barplot(data=subgenero_counts, x="subgenerico", y="cantidad", palette="magma")
plt.title("Cantidad de Delitos por Subgénero")
plt.xticks(rotation=90)
plt.xlabel("Subgénero del Delito")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.show()

# -------------------------
# Modelo generativo probabilístico
# -------------------------

# Seleccionar columnas relevantes
cols = ['dpto_pjfs', 'prov_pjfs', 'dist_pjfs', 'especialidad', 'tipo_caso','generico', 'subgenerico']
df_model = df[cols].dropna()

# Codificar categorías en números
label_encoders = {}
for col in df_model.columns:
    le = LabelEncoder()
    df_model[col] = le.fit_transform(df_model[col])
    label_encoders[col] = le

# Matriz de correlación (variables codificadas)
corr_matrix = df_model.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Matriz de Correlación entre Variables Codificadas")
plt.tight_layout()
plt.show()


# Dividir en variables predictoras y objetivo
X = df_model.drop("subgenerico", axis=1)
y = df_model["subgenerico"]

# Separar datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Modelo Naive Bayes (generativo y probabilístico)
modelo = MultinomialNB()
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# Evaluación
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=False, cmap="Blues", fmt="d")
plt.title("Matriz de Confusión - Subgéneros Delictivos")
plt.xlabel("Predicho")
plt.ylabel("Real")
plt.tight_layout()
plt.show()

# Mostrar probabilidades para una muestra del conjunto de prueba
muestra_idx = 0  # puedes cambiar este valor para ver otra muestra
probs = modelo.predict_proba([X_test.iloc[muestra_idx]])[0]

# Decodificar las clases
clases = label_encoders['subgenerico'].inverse_transform(modelo.classes_)

# Mostrar las probabilidades de predicción para esta muestra
df_probs = pd.DataFrame({'Subgénero': clases, 'Probabilidad': probs})
df_probs = df_probs.sort_values(by='Probabilidad', ascending=False)

# Gráfico de barras de probabilidades
plt.figure(figsize=(12, 6))
sns.barplot(data=df_probs.head(10), x="Subgénero", y="Probabilidad", palette="coolwarm")
plt.title(f"Probabilidades Predichas para la Muestra {muestra_idx}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Visualización de la distribución de predicciones generadas
subgenero_predicho = label_encoders['subgenerico'].inverse_transform(y_pred)
df_resultados = pd.DataFrame({'Subgénero_Predicho': subgenero_predicho})


plt.figure(figsize=(14, 6))
sns.countplot(data=df_resultados, x='Subgénero_Predicho', order=df_resultados['Subgénero_Predicho'].value_counts().index, palette="Set2")
plt.title("Distribución de Subgéneros Delictivos Predichos")
plt.xticks(rotation=90)
plt.xlabel("Subgénero del Delito (Predicho)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.show()

# Filtrar las 5 clases más frecuentes
top_subs = df_model['subgenerico'].value_counts().nlargest(5).index
df_small = df_model[df_model['subgenerico'].isin(top_subs)].copy()

# Reetiquetar de nuevo
df_small['subgenerico_label'] = label_encoders['subgenerico'].inverse_transform(df_small['subgenerico'])

# Generar registros con la probabilidad de ocurrencia por muestra
probs_all = modelo.predict_proba(X_test)
pred_clase_cod = modelo.predict(X_test)

# Decodificar clases reales y predichas
clases_subgenerico = label_encoders['subgenerico'].inverse_transform(modelo.classes_)
subgenero_real = label_encoders['subgenerico'].inverse_transform(y_test)
subgenero_predicho = label_encoders['subgenerico'].inverse_transform(pred_clase_cod)

print(f"\nCantidad de subgéneros posibles: {len(clases_subgenerico)}")
print("Subgéneros reconocidos por el modelo:")
print(clases_subgenerico)

# Tomemos una variable codificada
df_model["subgenerico_label"] = label_encoders['subgenerico'].inverse_transform(df_model["subgenerico"])

plt.figure(figsize=(12, 6))
sns.boxplot(data=df_model, x='subgenerico_label', y='generico')  # tipo_caso es numérico aquí
plt.xticks(rotation=90)
plt.title("Distribución de Tipo de Caso por Subgénero")
plt.tight_layout()
plt.show()


# Construir DataFrame con predicciones y probabilidades
resultados_prob = pd.DataFrame(X_test.reset_index(drop=True))
resultados_prob['Subgénero_Real'] = subgenero_real
resultados_prob['Subgénero_Predicho'] = subgenero_predicho

# Agregar la probabilidad más alta para cada predicción (con 3 decimales)
resultados_prob['Probabilidad_Predicha'] = probs_all.max(axis=1).round(3)

# También puedes agregar la probabilidad completa por clase si quieres más detalle (con 3 decimales)
for i, clase in enumerate(clases_subgenerico):
    resultados_prob[f'P({clase})'] = probs_all[:, i].round(3)

# Cantidad predicha por subgénero (frecuencia en predicciones)
cantidad_por_subgenero_predicho = resultados_prob['Subgénero_Predicho'].value_counts().to_dict()

# Agregar columna con cantidad predicha para el subgénero predicho
resultados_prob['Cantidad_Predicha_Subgénero'] = resultados_prob['Subgénero_Predicho'].map(cantidad_por_subgenero_predicho)

# Convertir códigos numéricos a etiquetas originales en columnas dpto_pjfs, prov_pjfs, dist_pjfs
# Primero obtener un valor para todas las filas (por ejemplo, la etiqueta para el código 0)
val_dpto = label_encoders['dpto_pjfs'].inverse_transform([0])[0]
val_prov = label_encoders['prov_pjfs'].inverse_transform([0])[0]
val_dist = label_encoders['dist_pjfs'].inverse_transform([0])[0]
val_esp= label_encoders['especialidad'].inverse_transform([0])[0]
val_tipo_caso = label_encoders['tipo_caso'].inverse_transform([0])[0]

# Asignar el mismo valor no numérico a todas las filas
resultados_prob['dpto_pjfs'] = val_dpto
resultados_prob['prov_pjfs'] = val_prov
resultados_prob['dist_pjfs'] = val_dist
resultados_prob['especialidad'] = val_esp
resultados_prob['tipo_caso'] = val_tipo_caso

# (Opcional) Si quieres conservar otras columnas igual que antes, déjalas igual

# Guardar en CSV con la nueva información
resultados_prob.to_csv("predicciones_modificadas.csv", index=False, encoding='utf-8-sig')
print("Archivo 'predicciones_modificadas.csv' guardado con cantidad predicha y etiquetas no numéricas.")


# Resumen por subgénero predicho
resumen_tabla = resultados_prob.groupby('Subgénero_Predicho').agg({
    'Probabilidad_Predicha': 'mean',
    'Cantidad_Predicha_Subgénero': 'first'
}).reset_index().sort_values(by='Cantidad_Predicha_Subgénero', ascending=False)

print("Resumen de Subgéneros Predichos:")
print(resumen_tabla)

# Probabilidad promedio por subgénero
probs_prom = pd.DataFrame(probs_all, columns=clases_subgenerico).mean()

# Suponiendo que esperas 1000 nuevos casos, puedes estimar:
nuevos_casos = 1000
estimacion_subgeneros = (probs_prom * nuevos_casos).round(0).astype(int)

print("Estimación de nuevos casos por subgénero (usando promedios de probabilidad):")
print(estimacion_subgeneros)

plt.figure(figsize=(10,6))
sns.scatterplot(data=resumen_tabla,
                x='Cantidad_Predicha_Subgénero',
                y='Probabilidad_Predicha',
                hue='Subgénero_Predicho', 
                palette='tab10',
                s=100)
plt.title("Dispersión: Frecuencia vs. Probabilidad Promedio de Subgéneros Predichos")
plt.xlabel("Cantidad Predicha del Subgénero")
plt.ylabel("Probabilidad Promedio")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Crear tabla de estimación
tabla_estimacion = pd.DataFrame({
    'Subgénero': probs_prom.index,
    'Estimación Casos Nuevos': estimacion_subgeneros.values
}).sort_values(by='Estimación Casos Nuevos', ascending=False)

# Guardar en un nuevo CSV
tabla_estimacion.to_csv("estimacion_subgeneros.csv", index=False, encoding='utf-8-sig')
print("Archivo 'estimacion_subgeneros.csv' guardado con estimación de casos nuevos por subgénero.")

# Mostrar tabla
print(tabla_estimacion)

# Gráfico de barras
tabla_estimacion.plot(
    x='Subgénero',
    y='Estimación Casos Nuevos',
    kind='bar',
    legend=False,
    figsize=(10, 5),
    color='skyblue'
)

plt.title('Estimación de Nuevos Casos por Subgénero')
plt.xlabel('Subgénero')
plt.ylabel('Casos Estimados')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Crear gráfico de dispersión
plt.figure(figsize=(10, 5))
plt.scatter(
    tabla_estimacion['Subgénero'],
    tabla_estimacion['Estimación Casos Nuevos'],
    color='orange',
    s=100,  # tamaño de los puntos
    edgecolors='black'
)

plt.title('Estimación de Nuevos Casos por Subgénero (Dispersión)')
plt.xlabel('Subgénero')
plt.ylabel('Casos Estimados')
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

