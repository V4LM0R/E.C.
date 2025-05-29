library(shiny)
library(GNCL)     # Tu paquete personalizado
library(writexl)  # Para exportar a Excel

ui <- fluidPage(
  titlePanel("Generador de Datos Aleatorios - GNCL"),

  sidebarLayout(
    sidebarPanel(
      selectInput("tipo_dato", "Selecciona tipo de dato a generar:",
                  choices = c("Notas" = "notas",
                              "Tallas" = "tallas",
                              "Temperaturas" = "temperaturas",
                              "Gasto mensual" = "gasto")),
      numericInput("cantidad", "Cantidad de datos a generar:", value = 10, min = 1),
      actionButton("generar", "Generar"),
      br(),
      downloadButton("descargar_excel", "Descargar Excel")
    ),

    mainPanel(
      h3("Datos generados:"),
      tableOutput("tabla_resultados")
    )
  )
)

server <- function(input, output) {

  datos_generados <- eventReactive(input$generar, {
    n <- input$cantidad
    switch(input$tipo_dato,
           notas = generar_notas(n),
           tallas = generar_tallas(n),
           temperaturas = generar_temperaturas(n),
           gasto = generar_gasto_mensual(n))
  })

  output$tabla_resultados <- renderTable({
    data.frame(Valores = datos_generados())
  })

  # Descargar Excel
  output$descargar_excel <- downloadHandler(
    filename = function() {
      paste0("datos_generados_", input$tipo_dato, ".xlsx")
    },
    content = function(file) {
      write_xlsx(data.frame(Valores = datos_generados()), path = file)
    }
  )
}

shinyApp(ui = ui, server = server)
