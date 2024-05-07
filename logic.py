from PyQt6.QtWidgets import *
from PyQt6.uic import *
import sys

from extended import *
from start import *
import os
from PIL import Image

class Start(QMainWindow, Ui_StartWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start_push.clicked.connect(self.changeWindow)

    def changeWindow(self):
        self.window = Logic()
        self.window.show()
        self.close()

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.select_push.clicked.connect(self.getFileName)
        self.compress_push.clicked.connect(self.compress)

        self.filenames = ''

        #quality
        self.quality = None

        self.width = None
        self.height = None

        self.new_filename = ''

    def getFileName(self):
        file_filter = 'Image File (*.png *.jpg);; Video File (*.mp4);; Audio File (*.mp3)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            filter=file_filter,
        )
        self.filenames = str(response).split(',')

    def compress(self):

        if self.filenames:
            file_type = self.filenames[0][-4:-1]

            if self.thirty_radio.isChecked():
                self.quality = 30
            elif self.fifty_radio.isChecked():
                self.quality = 50
            elif self.seventy_radio.isChecked():
                self.quality = 70
            elif self.ninety_radio.isChecked():
                self.quality = 90
            else:
                self.label_2.setText('Please select any compress ratio')
                self.setStyleSheet("QRadioButton::indicator:!checked { color: rgb(170, 0, 0); }")
                return

            if (file_type == 'png' or file_type == 'jpg') and (self.x_value.text().isdigit()
                                                               and self.y_value.text().isdigit()):
                self.width = int(self.x_value.text())
                self.height = int(self.y_value.text())
                self.new_filename = str(self.new_name.text()) + '.' + str(file_type)
                image = Image.open(self.filenames[0][2:-1])
                new_size = (self.width, self.height)
                resized_image = image.resize(new_size)
                resized_image.save(self.new_filename, optimize=True, quality=self.quality)
                original_size = os.path.getsize(self.filenames[0][2:-1])
                compressed_size = os.path.getsize(self.new_filename)

                print("Original Size: ", original_size)
                print("Compressed Size: ", compressed_size)

            elif file_type == 'mp4':
                print("hi")

            elif file_type == 'mp3':
                print('whats good')

            else:
                self.label_2.setText('Fill all options; dimensions must be numeric')


        else:
            self.label_2.setText('Upload a file')
