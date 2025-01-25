from PyQt5 import QtCore, QtGui, QtWidgets
from EIT.AppTie import Ui_MainWindow


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(QMainWindow)
    QMainWindow.show()
    sys.exit(app.exec_())