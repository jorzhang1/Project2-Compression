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

        self.filenames = ''

        #radio stuff bruh
        #self.quality = self.

        self.width = None
        self.height = None

        self.new_filename = ''

    def getFileName(self):
        file_filter = 'Image File (*.png, *.jpg);; Video File (*.mp4);; Audio File (*.mp3)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
        )
        self.filenames = str(response).split(',')

    def compress(self):
        if self.filenames:
            file_type = self.filenames[0][-4:-1]
            self.width = int(self.x_value.text())
            self.height = int(self.y_value.text())
            self.new_filename = str(self.new_name.text()) + '.' + str(file_type)

            if file_type == 'png' or file_type == 'jpg':
                image = Image.open(self.filenames[0][2:-1])
                new_size = (self.width, self.height)
                resized_image = image.resize(new_size)
                resized_image.save(self.new_filename, optimize=True, quality=50)
                original_size = os.path.getsize(self.filenames[0][2:-1])
                compressed_size = os.path.getsize(self.new_filename)

                print("Original Size: ", original_size)
                print("Compressed Size: ", compressed_size)

            elif file_type == 'mp4':

            elif file_type == 'mp3':

        else:
            self.label_2.setText('Upload a file')
