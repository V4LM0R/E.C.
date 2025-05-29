# ===============================
# Comparación de Generadores Aleatorios: LCG vs Mersenne Twister
# ===============================

# ---------- CONFIGURACIÓN ----------
# Cambia esta variable para elegir cuántos números aleatorios generar
n <- 1000  # Por ejemplo, 1 millón

# ---------- MÉTODO 1: LCG ----------
lcg_generator <- function(n, seed = 12345, a = 1664525, c = 1013904223, m = 2^32) {
  x <- numeric(n)
  x[1] <- seed
  for (i in 2:n) {
    x[i] <- (a * x[i - 1] + c) %% m
  }
  return(x / m)  # Normalizar a [0,1]
}

# ---------- MÉTODO 2: Mersenne Twister ----------
mersenne_twister_generator <- function(n) {
  runif(n)  # Usa Mersenne Twister (por defecto en R)
}

# ---------- GENERACIÓN Y MEDICIÓN DE TIEMPOS ----------
cat("Generando", n, "números con LCG...\n")
time_lcg <- system.time({
  lcg_numbers <- lcg_generator(n)
})

cat("Generando", n, "números con Mersenne Twister...\n")
time_mt <- system.time({
  mt_numbers <- mersenne_twister_generator(n)
})

# ---------- COMPARACIÓN DE TIEMPOS ----------
cat("\n--- Comparación de tiempos (en segundos) ---\n")
cat("LCG:             ", time_lcg["elapsed"], "segundos\n")
cat("Mersenne Twister:", time_mt["elapsed"], "segundos\n")

# ---------- PRUEBAS ESTADÍSTICAS ----------
cat("\n--- Prueba de Uniformidad (Kolmogorov-Smirnov) ---\n")
ks_lcg <- ks.test(lcg_numbers, "punif")
ks_mt  <- ks.test(mt_numbers, "punif")

cat("\nResultados para LCG:\n")
print(ks_lcg)

cat("\nResultados para Mersenne Twister:\n")
print(ks_mt)

# ---------- VISUALIZACIÓN ----------
par(mfrow = c(1, 2))  # Mostrar dos histogramas lado a lado
hist(lcg_numbers, main = "Histograma - LCG", col = "skyblue", breaks = 50,
     xlab = "Valor", probability = TRUE)
hist(mt_numbers, main = "Histograma - Mersenne Twister", col = "orange", breaks = 50,
     xlab = "Valor", probability = TRUE)

