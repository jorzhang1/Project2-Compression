from PyQt6.QtWidgets import *
from PyQt6.uic import *
import sys

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
        file_filter = 'Image File (*.png, *.jpg);; Video File (*.mp4);; Audio File (*.mp3)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
        )
        self.filename = str(response).split(',')

    def compress(self):
        if self.filename:
            file_type = self.filename[0][-4:-1]

            if file_type == 'png' or file_type == 'jpg':
                image = Image.open(self.filename[0][2:-1])
                width, height = image.size
                print(width, height)
                new_size = 0
        else:
            self.label_2.setText('Upload a file')
