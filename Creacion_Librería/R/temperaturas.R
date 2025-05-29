#' Generar temperaturas ambientales aleatorias
#'
#' Esta función genera temperaturas aleatorias entre -10°C y 40°C, simulando datos ambientales.
#'
#' @param n Número de temperaturas a generar.
#' @return Vector de temperaturas aleatorias con una precisión de una decimal.
#' @examples
#' generar_temperaturas(10)
generar_temperaturas <- function(n) {
  round(runif(n, min = -10, max = 40), 1)
}
