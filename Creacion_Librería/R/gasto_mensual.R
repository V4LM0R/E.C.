#' Generar gasto mensual en soles
#'
#' Esta función genera valores aleatorios simulando el gasto mensual de personas en soles.
#'
#' @param n Número de datos de gasto a generar.
#' @return Vector de gastos mensuales aleatorios entre 200 y 3000 soles.
#' @examples
#' generar_gasto_mensual(10)
generar_gasto_mensual <- function(n) {
  round(runif(n, min = 200, max = 3000), 2)
}
