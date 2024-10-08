# Copyright (C) 2023 Jaehak Lee
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ...core.abstract_comp import AbstractComp

class LineGraphComp(AbstractComp):
    scrolled = Signal(object)
    mouse_moved = Signal(object)
    mouse_pressed = Signal(object)
    mouse_released = Signal(object)

    def initUI(self):
        self.canvas = FigureCanvasQTAgg(Figure(layout="constrained"))
        self.canvas.mpl_connect('scroll_event', self.scrolled.emit)
        self.canvas.mpl_connect('motion_notify_event', self.mouse_moved.emit)
        self.canvas.mpl_connect('button_press_event', self.mouse_pressed.emit)
        self.canvas.mpl_connect('button_release_event', self.mouse_released.emit)
        self.layout().addWidget(self.canvas)
    
    def updateUI(self):
        data = self.props["data"].get()

        self.canvas.figure.clf()
        plot = self.canvas.figure.add_subplot()
        for side in ['top','bottom','left','right']:
            plot.spines[side].set_linewidth(1.5)
        plot.tick_params(axis='both',direction='in', which='both', top=True, right=True, labelsize=12,
                         width=1.5, length=5, pad=5)

        for data_name in data.keys():
            if type(data[data_name]["y"]) == list:
                y = np.array(data[data_name]["y"])
            elif type(data[data_name]["y"]) in [float, int]:
                y = np.array([data[data_name]["y"]])
            else:
                y = data[data_name]["y"]

            if "x" in data[data_name].keys():
                x = data[data_name]["x"]
            else:                    
                x = np.arange(y.shape[0])

            if len(y) == 1:
                p = plot.scatter(x, y, label=data_name)
                plot.text(x, y, str(y), fontsize=12)
            else:
                p = plot.plot(x, y, label=data_name)

            if "color" in data[data_name].keys():
                p[0].set_color(data[data_name]["color"])
            if "marker" in data[data_name].keys():
                p[0].set_marker(data[data_name]["marker"])
            if "linestyle" in data[data_name].keys():
                p[0].set_linestyle(data[data_name]["linestyle"])
            if "linewidth" in data[data_name].keys():
                p[0].set_linewidth(data[data_name]["linewidth"])
            if "markersize" in data[data_name].keys():
                p[0].set_markersize(data[data_name]["markersize"])

        if "x_label" in self.props.keys():
            plot.set_xlabel(self.props["x_label"].get())
        if "y_label" in self.props.keys():
            plot.set_ylabel(self.props["y_label"].get()) 
        if "x_lim" in self.props.keys():
            plot.set_xlim(self.props["x_lim"].get())
        if "y_lim" in self.props.keys():
            plot.set_ylim(self.props["y_lim"].get())

        if len(plot.lines) > 0:
            plot.legend()
        self.canvas.draw()




