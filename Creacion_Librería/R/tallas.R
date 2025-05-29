#' Generar tallas aleatorias
#'
#' Esta función genera un vector de tallas aleatorias entre 0.5 y 1.99.
#'
#' @param n Número de tallas a generar.
#' @return Vector de tallas aleatorias.
#' @examples
#' generar_tallas(10)
generar_tallas <- function(n) {
  round(runif(n, min = 0.5, max = 1.99), 2)
}
