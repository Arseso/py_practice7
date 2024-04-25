import sys

import numpy as np
import pandas as pd
from pandas import DataFrame as DF
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries, QBarSeries, QPieSeries, QBarSet
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Графики")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)

        self.setCentralWidget(scroll_area)

        # Первое задание sin, cos
        self.plot_task1()

        # Второе задание trees
        self.plot_task2()

        # Третье задание hurricanes
        self.plot_task3()

    def plot_task1(self):
        data = get_data(task=1)
        chart_view1 = self.create_chart_with_series(title="SIN",
                                                    data=zip(data.x.values, data.sin.values),
                                                    mode="scatter")
        chart_view2 = self.create_chart_with_series(title="COS",
                                                    data=zip(data.x.values, data.cos.values),
                                                    mode="scatter")
        self.layout.addWidget(chart_view1)
        self.layout.addWidget(chart_view2)

    def plot_task2(self):
        data = get_data(task=2)
        chart1 = self.create_chart_with_series(title="Girth",
                                               data=zip(data.ID.values, data.Girth.values),
                                               mode="scatter")
        chart2 = self.create_chart_with_series(title="Girth",
                                               data=zip(data.ID.values, data.Girth.values),
                                               mode="bar")
        self.layout.addWidget(chart1)
        self.layout.addWidget(chart2)

        chart3 = self.create_chart_with_series(title="Height",
                                               data=zip(data.ID.values, data.Height.values),
                                               mode="scatter")
        chart4 = self.create_chart_with_series(title="Height",
                                               data=zip(data.ID.values, data.Height.values),
                                               mode="bar")
        self.layout.addWidget(chart3)
        self.layout.addWidget(chart4)

        chart5 = self.create_chart_with_series(title="Volume",
                                               data=zip(data.ID.values, data.Volume.values),
                                               mode="scatter")
        chart6 = self.create_chart_with_series(title="Volume",
                                               data=zip(data.ID.values, data.Volume.values),
                                               mode="bar")
        self.layout.addWidget(chart5)
        self.layout.addWidget(chart6)

    def plot_task3(self):
        data = get_data(task=3)
        chart1 = self.create_chart_with_series(title="Girth",
                                               data=zip(data.Month.values, data["2007"].values),
                                               mode="pie")

        data = DF({
            "Year": data.columns.values[2:],
            "Hurricanes": data.sum(axis=0)[2:],
        })
        chart2 = self.create_chart_with_series(title="Girth",
                                              data=zip(data.Year.values, data.Hurricanes.values),
                                              mode="pie")
        self.layout.addWidget(chart1)
        self.layout.addWidget(chart2)

    def create_chart_with_series(self, title: str, data: zip, mode: str = 'scatter',
                                 size: tuple = (500, 300)) -> QChartView:
        if mode == 'scatter':
            series = QScatterSeries()
            for x, y in data:
                series.append(x, y)
        elif mode == 'bar':
            series = QBarSeries()
            for x, y in data:
                set0 = QBarSet(str(x))
                set0.append(y)
                series.append(set0)

        elif mode == 'pie':
            series = QPieSeries()
            for label, value in data:
                slice_ = series.append(label, value)
                slice_.setLabel(f"{label}: {value}")

        chart = QChart()
        chart.addSeries(series)
        chart.setMinimumSize(size[0], size[1])
        chart.setTitle(title)
        chart.createDefaultAxes()
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view


def get_data(task: int = 0) -> DF:
    data = None
    if task == 1:
        data = DF(data={
            "x": [x / 10 * np.pi for x in range(0, 40, 1)],
            "sin": [np.sin(x / 10 * np.pi) for x in range(0, 40, 1)],
            "cos": [np.cos(x / 10 * np.pi) for x in range(0, 40, 1)]
        })
    if task == 2:
        data = pd.read_csv("./data/trees.csv")
    if task == 3:
        data = pd.read_csv("./data/hurricanes.csv")
    return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

#%%
