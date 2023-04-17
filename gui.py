import sys
import matplotlib
matplotlib.use('QtAgg')
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
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
        self.setWindowTitle('Distribution Generator')
        layout = QHBoxLayout()

        ## Clear folder
        shutil.rmtree('./results')
        os.mkdir('./results')

        ## Canvas
        self.sc = MplCanvas(self)
        self.dist = 'normal'
        self.mean = 30
        self.std_dev = 5
        self.redraw()
        layout.addWidget(self.sc)

        ## Controls
        controls = QWidget()
        v_layout = QVBoxLayout()

        # Number of distributions
        self.countInput = QSpinBox()
        self.countInput.setRange(1, 10)
        self.countInput.setValue(1)
        v_layout.addWidget(QLabel('Distribution Number:'))
        v_layout.addWidget(self.countInput)

        # Button
        self.saveBtn = QPushButton("Save")
        self.saveBtn.clicked.connect(self.save)
        v_layout.addWidget(self.saveBtn)

        # Combobox
        v_layout.addWidget(QLabel('Distribution:'))
        self.cb = QComboBox()
        self.cb.addItems(['normal', 'chi-square', 'triangular', 'uniform', 'rayleigh'])
        self.cb.currentIndexChanged.connect(self.change_dist)
        v_layout.addWidget(self.cb)

        # Slider
        v_layout.addWidget(QLabel('Mean:'))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 60)
        self.slider.setValue(30)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.change_mean)
        v_layout.addWidget(self.slider)

        # Slider 2
        v_layout.addWidget(QLabel('Std dev:'))
        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        self.slider2.setRange(1, 30)
        self.slider2.setValue(5)
        self.slider2.setSingleStep(0.5)
        self.slider2.valueChanged.connect(self.change_std)
        v_layout.addWidget(self.slider2)

        controls.setLayout(v_layout)
        layout.addWidget(controls)

        main = QWidget()
        main.setLayout(layout)
        self.setCentralWidget(main)
        self.show()
    
    def redraw(self):
        self.sc.axes.clear()
        self.sc.axes.set_title(self.dist + ' distribution')
        self.results = self.calc_values(self.dist, self.mean, self.std_dev)
        self.sc.axes.plot(self.results)
        self.sc.draw()

    def change_dist(self, i):
        self.dist = self.cb.currentText()
        self.slider.setEnabled(self.dist != 'uniform')
        self.slider2.setEnabled(self.dist == 'normal')
        self.redraw()

    def change_mean(self, m):
        self.mean = m
        self.redraw()

    def change_std(self, s):
        self.std_dev = s
        self.redraw()
    
    def save(self):
        count = self.countInput.value()

        np.savetxt('results/dist'+str(count)+'.csv', self.results, delimiter=',')
        self.sc.axes.get_figure().savefig('results/dist'+str(count)+'.png')
        
        # dlg = QDialog(self)
        # message = QLabel('Results are saved to \'results/dist'+str(count)+'.csv\'')
        # dlg_layout = QVBoxLayout()
        # dlg_layout.addWidget(message)
        # dlg.setLayout(dlg_layout)
        # dlg.show()

    def calc_values(self, dist, mean, std):
        samples = 10000 

        if dist == 'normal':
            values = np.random.normal(mean, std, samples)
        elif dist == 'chi-square':
            values = np.random.chisquare(mean, samples)
        elif dist == 'triangular':
            values = np.random.triangular(0, mean, 60, samples)
        elif dist == 'uniform':
            values = np.random.uniform(0, 60, samples)
        elif dist == 'rayleigh':
            values = np.random.rayleigh(mean, samples)
        
        values = values[(values >= 0) & (values <= 60)]

        results,_ = np.histogram(values, bins=60)

        # Smooth the data
        w = 3
        results = np.convolve(results, np.ones(w), 'valid') / w
        results = np.interp(results, (results.min(), results.max()), (0, 100))

        return results


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()