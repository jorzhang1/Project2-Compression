from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QTextEdit, QFileDialog)
from extended import *
import os
from PIL import Image


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.select_push.clicked.connect(self.getFileName)
        self.compress_push.clicked.connect(self.compress)

        self.filename = ''

    def getFileName(self):
        file_filter = 'Image File (*.jpg, *.png);; Video File (*.mp4);; Audio File (*.mp3)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
        )
        self.filename = str(response).split(',')
        print(self.filename)
        file_type = self.filename[0][-4:-1]
        print(file_type)

    def compress(self):
        file_type = self.filename[-1][-3:]

        image = Image.open(str(self.filename))
        width, height = image.size
        new_size = 0
