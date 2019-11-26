import sys
import numpy as np
from parse_config import OverlayConfig
from PyQt5 import QtGui, QtCore, QtWidgets

class Overlay(QtWidgets.QMainWindow):
    def __init__(self, colored_noise=True, config=OverlayConfig()):
        QtWidgets.QMainWindow.__init__(self)
        # user configuration
        self.colored_noise = colored_noise
        self.opacity = config.opacity

        # state variable
        self.show_noise = False

        # get all screen resolutinos (currently only support one screen)
        self.screen_resolutions = self.get_screen_resolutions()

        # configure window
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
            )
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
            QtCore.QSize(
                self.screen_resolutions[0].width(), 
                self.screen_resolutions[0].height()
            ),
            QtWidgets.qApp.desktop().availableGeometry()))
        
        # clickthrough
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        
        # transparent background
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # no frame and stay on top flags
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    # find all screen resolutions
    def get_screen_resolutions(self):
        resolutions = []
        for displayNr in range(QtWidgets.QDesktopWidget().screenCount()):
            resolutions.append(QtWidgets.QDesktopWidget().screenGeometry(displayNr))
        return resolutions
    
    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)

        if self.show_noise:
            painter.setOpacity(self.opacity)
        else:
            painter.setOpacity(0)

        X = self.screen_resolutions[0].width()
        Y = self.screen_resolutions[0].height()

        if self.colored_noise:
            # colored
            img = np.random.randint(0, 256, (X, Y, 3), dtype=np.uint8)
        else:
            # black and white
            img_arrays = np.random.randint(0, 256, (X, Y), dtype=np.uint8)
            img[:,:,0] = img_arrays
            img[:,:,1] = img[:,:,0]
            img[:,:,2] = img[:,:,0]
        
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

        painter.setBrush(
                QtGui.QBrush(qImg)
            )
        painter.setPen(QtGui.QPen(QtCore.Qt.white))   
        painter.drawRect(self.rect())

    def enable_noise(self):
        self.show_noise = True
        self.update()

    def disable_noise(self):
        self.show_noise = False
        self.update()

    # def mousePressEvent(self, event):
    #     QtWidgets.qApp.quit()

def init(config=OverlayConfig()):
    app = QtWidgets.QApplication(sys.argv)
    window = Overlay(config=config)
    return window, app

def start(window, app):
    window.show()
    app.exec_()

if __name__ == "__main__":
    init()
    start()
