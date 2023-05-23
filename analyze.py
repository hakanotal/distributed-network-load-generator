import sys
import matplotlib
matplotlib.use('QtAgg')
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import shutil
import os


class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Distribution Analysis')
        layout = QHBoxLayout()

        ## Load Data
        self.real, self.target = self.load_data()

        ## Canvas
        self.sc = MplCanvas(self)
        self.redraw()
        layout.addWidget(self.sc)

        ## Controls
        controls = QWidget()
        v_layout = QVBoxLayout()

        controls.setLayout(v_layout)
        layout.addWidget(controls)

        main = QWidget()
        main.setLayout(layout)
        self.setCentralWidget(main)
        self.show()

    def load_data(self):
        # Real Load Data
        df = pd.read_csv('loadresults/load_stats_history.csv')
        df.dropna(subset=['Type'], inplace=True)
        start_timestamp = df['Timestamp'].iloc[0]
        df['Timestamp'] = df['Timestamp'].apply(lambda x: x - start_timestamp)
        real = df[['User Count']].to_numpy()
        if real.shape[0] < 60:
            real = np.append(np.zeros(60-real.shape[0]), real)

        # Target Load Data
        target = np.genfromtxt('results/dist.csv', delimiter=',')

        return real, target
   
    def redraw(self):
        self.sc.axes.clear()
        self.sc.axes.set_title('Custom Distribution Analysis')
        self.sc.axes.plot(self.real)
        self.sc.axes.plot(self.target)
        self.sc.axes.legend(['Real', 'Target'])
        self.sc.draw()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()