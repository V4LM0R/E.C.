#' Generar notas aleatorias de estudiantes
#'
#' Esta función genera un vector de notas aleatorias enteras entre 0 y 20.
#'
#' @param n Número de notas a generar.
#' @return Vector con notas aleatorias.
#' @examples
#' generar_notas(10)
generar_notas <- function(n) {
  sample(0:20, n, replace = TRUE)
}
