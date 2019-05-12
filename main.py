# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from training import *
from test import *
#from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("window.ui", self)

        self.setWindowTitle("C4.5 con atributos continuos")

        self.crear_modelo.clicked.connect(self.procesar_dataset) #boton para disparar el training
        self.examinar.clicked.connect(self.buscar_archivo) #boton para buscar el dataset de training
        self.examinar_test.clicked.connect(self.buscar_archivo_test) #boton para buscar el dataset de test
        self.testear.clicked.connect(self.test)  # boton para disparar el testeo

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def update_graph(self, dataset):

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.clear()

        ax = plt.gca()
        for line in ax.lines:
            self.MplWidget.canvas.axes.plot(line.get_xdata(), line.get_ydata())

        colors = np.where(dataset['clase'] == 1, 'b', 'k')  # clase 1 = azul // clase0 = negro

        x = dataset['x'].to_numpy()
        y = dataset['y'].to_numpy()
        self.MplWidget.canvas.axes.scatter(x=x,y=y, c=colors, s=25)

        self.MplWidget.canvas.axes.set_title('C4.5 con atributos continuos')

        self.MplWidget.canvas.draw()
        plt.close()

    # buscar archivo para training
    def buscar_archivo(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Seleccione CSV", "", "CSV Files (*.csv );;All Files (*)")

        if fileName:
            self.input_file.setText(fileName)

    # disparar el proceso de entrenamiento
    def procesar_dataset(self):
        if self.input_file.text():
            dataset_path = self.input_file.text()
            dataset = train(dataset_path)
            self.update_graph(dataset)
            window.tabWidget.setCurrentIndex(1)


    # buscar archivo para testing
    def buscar_archivo_test(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Seleccione CSV", "", "CSV Files (*.csv );;All Files (*)")

        if fileName:
            self.input_file_test.setText(fileName)


    # disparar el proceso de testing y devuelve una lista con datos de las 3 tablas (incorrectas, correctas, incosistentes)
    def test(self, modelo):
        if self.input_file_test.text():
            test_dataset_path = self.input_file_test.text()
            predicciones = test(test_dataset_path, modelo)

            while (self.corr_tableWidget.rowCount() > 0):
                    self.corr_tableWidget.removeRow(0);

            while (self.nopred_tableWidget.rowCount() > 0):
                    self.nopred_tableWidget.removeRow(0);

            while (self.incorr_tableWidget.rowCount() > 0):
                    self.incorr_tableWidget.removeRow(0);

            rowPosition = self.corr_tableWidget.rowCount()  # añado cada item a la tabla correctos
            if len(predicciones['correctos']) > 0:
                for row in predicciones['correctos']:
                    self.corr_tableWidget.insertRow(rowPosition)
                    self.corr_tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(row['x'])))
                    self.corr_tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(row['y'])))
                    self.corr_tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(row['clase'])))
                    rowPosition += 1

            rowPosition = self.nopred_tableWidget.rowCount()  # añado cada item a la tabla incosistentes
            for row in predicciones['inciertos']:
                self.nopred_tableWidget.insertRow(rowPosition)
                self.nopred_tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(row['x'])))
                self.nopred_tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(row['y'])))
                self.nopred_tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(row['clase'])))
                rowPosition += 1

            rowPosition = self.incorr_tableWidget.rowCount() # añado cada item a la tabla incorrectos
            for row in predicciones['incorrectos']:
                self.incorr_tableWidget.insertRow(rowPosition)
                self.incorr_tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(row['x'])))
                self.incorr_tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(row['y'])))
                self.incorr_tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(row['clase'])))
                self.incorr_tableWidget.setItem(rowPosition, 3, QTableWidgetItem(str(row['pred'])))
                rowPosition += 1




app = QApplication([])
window = MatplotlibWidget()
window.tabWidget.setCurrentIndex(0)
window.show()
app.exec_()