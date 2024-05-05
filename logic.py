from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QTextEdit, QFileDialog)
from extended import *
import os
from PIL import Image


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.getFileName)
        self.pushButton_3.clicked.connect(self.compress)

        self.filename = ''

    def getFileName(self):
        file_filter = 'Image File (*.jpg, *.png)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Image File (*.jpg, *.png)'
        )
        self.filename = str(response)
        print(self.filename)

    def compress(self):
        image = Image.open(str(self.filename))
