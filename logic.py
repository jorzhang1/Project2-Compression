from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from extended import *
from start import *
import os
import subprocess
from PIL import Image


class Start(QMainWindow, Ui_StartWindow):
    """
    Class that builds the start window
    and contains a method to switch windows
    """

    def __init__(self) -> None:
        """
        Method that sets up the ui when the program is run
        """
        super().__init__()
        self.setupUi(self)

        self.start_push.clicked.connect(self.changeWindow)

    def changeWindow(self) -> None:
        """
        Method that switches windows to compression screen when button
        is pressed
        """
        self.window = Logic()
        self.window.show()
        self.close()


class Logic(QMainWindow, Ui_MainWindow):
    """
    Class that builds the main window
    and contains methods that can compress media files
    """

    def __init__(self) -> None:
        """
        Method that sets up ui when the program is run
        Also calls other methods when buttons are pressed
        """
        super().__init__()
        self.setupUi(self)
        self.select_push.clicked.connect(self.getFileName)
        self.compress_push.clicked.connect(self.compress)
        self.filenames: str = ''

        self.quality = None

        self.width = None
        self.height = None

        self.new_filename: str = ''

    def getFileName(self) -> None:
        """
        Method that prompts the user to select a file from their computer
        """
        file_filter: str = 'Image File (*.png *.jpg);; Video File (*.mp4);; Audio File (*.mp3)'
        response: tuple = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            filter=file_filter,
        )
        self.filenames: list = str(response).split(',')
        self.change_labels()

    def compress(self) -> None:
        """
        Method that changes the file size and quality of the file
        the user selected and makes a new file in the working directory
        """
        if self.filenames:
            file_type: str = self.filenames[0][-4:-1]

            if ((file_type == 'png' or file_type == 'jpg') and (self.x_value.text().isdigit()
                                                                and int(self.x_value.text()) > 0
                                                                and self.y_value.text().isdigit()
                                                                and int(self.x_value.text()) > 0)
                    and self.new_filename != ''):
                if self.thirty_radio.isChecked():
                    self.quality = 30
                elif self.fifty_radio.isChecked():
                    self.quality = 50
                elif self.seventy_radio.isChecked():
                    self.quality = 70
                elif self.ninety_radio.isChecked():
                    self.quality = 90
                else:
                    self.label_2.setText('Please select any compression ratio')
                    self.label_2.show()
                    self.label_2.setStyleSheet("QRadioButton::indicator:!checked { color: rgb(170, 0, 0); }")
                    return
                self.width = int(self.x_value.text())
                self.height = int(self.y_value.text())
                if self.width < 3840 and self.height < 2160:
                    self.new_filename: str = str(self.new_name.text()) + '.' + str(file_type)
                    image = Image.open(self.filenames[0][2:-1])
                    new_size: tuple = (self.width, self.height)
                    resized_image = image.resize(new_size)
                    resized_image.save(self.new_filename, optimize=True, quality=self.quality)

                    pixmap = QPixmap(self.new_filename)
                    self.label_2.setPixmap(pixmap)
                    self.label_2.setScaledContents(True)
                    self.label_2.show()

            elif file_type == 'mp4':

                quality = -1
                try:
                    quality = int(self.x_value.text())
                except ValueError:
                    self.label_2.setText('Enter a numeric value')
                    self.label_2.show()

                self.new_filename = str(self.new_name.text()) + '.' + str(file_type)
                if not str(self.new_name.text()).isalnum():
                    self.label_2.setText('Video file name must be alphanumeric')
                    self.label_2.show()
                else:
                    if 0 <= quality <= 51:
                        input_path: str = self.filenames[0][2:-1]
                        self.new_filename = str(self.new_name.text()) + '.' + str(file_type)
                        output_path: str = self.new_filename
                        ffmpeg_cmd: str = f'ffmpeg -i {input_path} -c:v libx264 -c:a copy -crf {quality} {output_path}'
                        subprocess.run(ffmpeg_cmd, shell=True)

                        """
                        The quality in the video command is the -crf 20. The range is 0-51 where 0 is lossless,
                        23 is default, and 51 is the worst quality.
                        """

                        original_size: int = os.path.getsize(self.filenames[0][2:-1])
                        compressed_size: int = os.path.getsize(self.new_filename)

                        self.label_2.setText(f'Compression complete; Check working directory\n'
                                             f'\nOriginal size: {original_size}\nNew size: {compressed_size}')
                        self.label_2.show()

            elif file_type == 'mp3':

                quality = -1
                try:
                    quality = int(self.x_value.text())
                except ValueError:
                    self.label_2.setText('Enter a numeric value')
                    self.label_2.show()

                self.new_filename = str(self.new_name.text()) + '.' + str(file_type)
                if not str(self.new_name.text()).isalnum():
                    print(self.new_filename)
                    self.label_2.setText('Audio file name must be alphanumeric')
                    self.label_2.show()
                else:
                    if 32 <= quality <= 320:
                        input_path: str = self.filenames[0][2:-1]
                        output_path: str = self.new_filename
                        ffmpeg_cmd: str = f'ffmpeg -i {input_path} -c:a libmp3lame -b:a {quality}k {output_path}'
                        subprocess.run(ffmpeg_cmd, shell=True)

                        # The quality in the audio command is the 128k. The range is typically 32 to 320 kilobits.

                        original_size: int = os.path.getsize(self.filenames[0][2:-1])
                        compressed_size: int = os.path.getsize(self.new_filename)

                        self.label_2.setText(f'Compression complete; Check working directory\n'
                                             f'\nOriginal size: {original_size}\nNew size: {compressed_size}')
                        self.label_2.show()

            else:
                self.label_2.setText('Fill all options; dimensions must be numeric')
                self.label_2.show()

        else:
            self.label_2.setText('Upload a file')
            self.label_2.show()

    def change_labels(self) -> None:
        """
        Method that changes the labels and input areas depending on
        the file type the user selects
        """
        file_type: str = self.filenames[0][-4:-1]
        if file_type == 'jpg' or file_type == 'png':

            self.ratio_label.show()
            self.thirty_radio.show()
            self.fifty_radio.show()
            self.seventy_radio.show()
            self.ninety_radio.show()

            self.dimension_label.show()
            self.dimension_label.setText('New dimensions (Max 3840x2160')
            self.x_label.show()
            self.y_label.show()
            self.x_label.setText('x:')
            self.y_label.setText('y:')
            self.x_value.show()
            self.y_value.show()

            self.x_value.setText('')
            self.y_value.setText('')
            self.new_name.setText('')

            self.name_label.show()
            self.new_name.show()
            self.label_2.hide()

        elif file_type == 'mp4':

            self.ratio_label.hide()
            self.thirty_radio.hide()
            self.fifty_radio.hide()
            self.seventy_radio.hide()
            self.ninety_radio.hide()

            self.dimension_label.show()
            self.dimension_label.setText('Bit rate (0-51)')

            self.x_label.setText('')
            self.x_value.show()

            self.y_label.hide()
            self.y_value.hide()
            self.y_label.setText('')

            self.x_value.setText('')
            self.y_value.setText('')
            self.new_name.setText('')

            self.name_label.show()
            self.new_name.show()
            self.label_2.hide()

        elif file_type == 'mp3':
            self.ratio_label.hide()
            self.thirty_radio.hide()
            self.fifty_radio.hide()
            self.seventy_radio.hide()
            self.ninety_radio.hide()

            self.dimension_label.show()
            self.dimension_label.setText('Bit rate (32-320)')

            self.x_label.setText('Kilobits:')
            self.x_value.show()

            self.y_label.hide()
            self.y_value.hide()
            self.y_label.setText('')

            self.x_value.setText('')
            self.y_value.setText('')
            self.new_name.setText('')

            self.name_label.show()
            self.new_name.show()
            self.label_2.hide()
