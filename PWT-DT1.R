# 1. Calcular el promedio de tatuajes por grupo
jovenes <- c(0,0,1,0,0,4,2,2,1,6,0,3,1,0,2)
adultos <- c(0,6,2,0,0,0,0,0,1,0,0,0,0,0,4)

mean(jovenes)   # Promedio de tatuajes en jóvenes
mean(adultos)   # Promedio de tatuajes en adultos

# 2. Calcular la desviación estándar
sd(jovenes)     # Medida de dispersión para jóvenes
sd(adultos)     # Medida de dispersión para adultos

# 3. Calcular el coeficiente de variación en jóvenes
cv <- sd(jovenes)/mean(jovenes)
cv * 100        # Variabilidad relativa en porcentaje

# 4. Prueba t de Student (asumiendo varianzas iguales)
t.test(jovenes, adultos, var.equal = TRUE)

# 5. Prueba t de Welch (sin asumir varianzas iguales)
t.test(jovenes, adultos)

# 6. Coeficiente de variación en adultos
cv_adultos <- sd(adultos)/mean(adultos)
cv_adultos * 100

# 7. Probabilidad de tener al menos un tatuaje
sum(jovenes > 0) / length(jovenes)  # Proporción en jóvenes
sum(adultos > 0) / length(adultos)  # Proporción en adultos

# 8. Preparación de promedios para los gráficos
mean_j <- mean(jovenes)
mean_a <- mean(adultos)

# 9. Gráfico de barras: comparación de promedios
barplot(c(mean_j, mean_a),
        names.arg = c("Jóvenes", "Adultos"),
        col = c("skyblue", "orange"),
        main = "Promedio de tatuajes por grupo",
        ylab = "Promedio de tatuajes")

# 10. Gráfico de personas con y sin tatuajes
sin_tatuajes <- c(sum(jovenes == 0), sum(adultos == 0))
con_tatuajes <- c(sum(jovenes > 0), sum(adultos > 0))

barplot(rbind(con_tatuajes, sin_tatuajes),
        beside = TRUE,
        col = c("green", "red"),
        names.arg = c("Jóvenes", "Adultos"),
        legend.text = c("Con tatuajes", "Sin tatuajes"),
        main = "Personas con y sin tatuajes",
        ylab = "Cantidad de personas")

# 11. Boxplot para comparar la distribución de tatuajes
boxplot(jovenes, adultos,
        names = c("Jóvenes", "Adultos"),
        col = c("skyblue", "orange"),
        main = "Distribución de tatuajes por grupo",
        ylab = "Cantidad de tatuajes")

# 12. Gráfico ajustado: promedio con límites definidos
barplot(c(mean_j, mean_a),
        names.arg = c("Jóvenes", "Adultos"),
        col = c("skyblue", "orange"),
        ylim = c(0, max(mean_j, mean_a) + 1),
        main = "Promedio de tatuajes",
        ylab = "Número promedio")

# 13. Gráfico de proporción de personas con tatuajes
prop_j <- sum(jovenes > 0) / length(jovenes)
prop_a <- sum(adultos > 0) / length(adultos)

barplot(c(prop_j, prop_a),
        names.arg = c("Jóvenes", "Adultos"),
        col = c("green", "red"),
        ylim = c(0, 1),
        main = "Proporción de personas con al menos un tatuaje",
        ylab = "Proporción (0 a 1)")

# 14. Comparación de frecuencia con/sin tatuajes
labels <- c("Con tatuajes", "Sin tatuajes")
jov_cont <- c(sum(jovenes > 0), sum(jovenes == 0))
adu_cont <- c(sum(adultos > 0), sum(adultos == 0))

barplot(rbind(jov_cont, adu_cont),
        beside = TRUE,
        col = c("blue", "gray"),
        names.arg = labels,
        legend.text = c("Jóvenes", "Adultos"),
        main = "Cantidad de personas con y sin tatuajes",
        ylab = "Cantidad de personas")

# 15. Tablas de frecuencia del número de tatuajes (0 a 6)
tatuajes <- 0:6
freq_jovenes <- table(factor(jovenes, levels = tatuajes))
freq_adultos <- table(factor(adultos, levels = tatuajes))

# 16. Gráfico de distribución exacta de tatuajes
datos <- rbind(Jóvenes = freq_jovenes, Adultos = freq_adultos)

barplot(datos,
        beside = TRUE,
        col = c("skyblue", "orange"),
        main = "Distribución de número de tatuajes por grupo",
        xlab = "Número de tatuajes",
        ylab = "Cantidad de personas",
        legend.text = TRUE,
        args.legend = list(x = "topright"))

