import sys
import ctypes
import writer
from typing import Tuple
from gui import YoutubeDownloaderGui
from core.statics import resource_path
from multiprocessing import freeze_support
from PyQt5 import QtWidgets, QtGui, QtCore
# from save_directories import SaveDirectories


def set_custom_fusion() -> Tuple[str, QtGui.QPalette]:
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(75, 75, 75))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

    return "Fusion", palette


def main():
    freeze_support()

    my_app_id = u'yt_downloader.v2'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
    style, pal = set_custom_fusion()
    writer.clear()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(style)
    app.setWindowIcon(QtGui.QIcon(resource_path('app_img.png')))
    yt_main_window = QtWidgets.QMainWindow()
    yt_main_window.setPalette(pal)
    ui = YoutubeDownloaderGui(yt_main_window)
    yt_main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
