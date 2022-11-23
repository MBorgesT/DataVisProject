from shiny import App, render, ui
from metrica import MetricasPlot


metricaPlot = MetricasPlot()


app_ui = ui.page_fluid(
    ui.h2("Hello Shiny!"),
    ui.input_numeric("vline", "VLine", value=0),
    ui.output_plot("scatter1")
)


def server(input, output, session):
    @output
    @render.text
    def scatter1():
        return metricaPlot.get_scatter_1(1000)


app = App(app_ui, server)
