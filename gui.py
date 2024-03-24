import time
import writer as wt
from pathlib import Path
import downloader as dn
from multiprocessing import Process
from PyQt5 import QtCore, QtGui, QtWidgets
from save_directories import SaveDirectories
from PyQt5.Qt import QApplication, QClipboard

sd = SaveDirectories()


class YoutubeDownloaderGui(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.status_bar = QtWidgets.QStatusBar(self.main_window)
        self.menu_bar = QtWidgets.QMenuBar(self.main_window)
        self.label = QtWidgets.QLabel(self.central_widget)
        self.text_output = QtWidgets.QTextEdit(self.central_widget)

        self.save_dirs = sd

        self.download_info_dir = QtWidgets.QLineEdit(self.central_widget)

        self.yt_url_label_2 = QtWidgets.QLabel(self.central_widget)
        self.download_type_comboBox = QtWidgets.QComboBox(self.central_widget)
        self.url_edit = QtWidgets.QLineEdit(self.central_widget)
        self.yt_url_label = QtWidgets.QLabel(self.central_widget)
        self.pushButton = QtWidgets.QPushButton(self.central_widget)

        self.select_dir_button = QtWidgets.QPushButton(self.central_widget)

        QApplication.clipboard().dataChanged.connect(self.clipboard_changed)

        self.setup_ui()

    def _toggle_on(self):
        self.pushButton.setEnabled(True)

    def clear_and_disable(self):
        self.text_output.clear()
        self.pushButton.setEnabled(False)

    def setup_ui(self):
        self.main_window.setObjectName("yt_main_window")
        self.main_window.resize(829, 574)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.main_window.sizePolicy().hasHeightForWidth())
        self.main_window.setSizePolicy(size_policy)
        self.main_window.setMinimumSize(QtCore.QSize(829, 574))
        self.main_window.setMaximumSize(QtCore.QSize(829, 574))
        self.main_window.setToolTip("")
        self.main_window.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.central_widget.setObjectName("central_widget")

        self.pushButton.setGeometry(QtCore.QRect(34, 422, 761, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.check_url)

        self.select_dir_button.setGeometry(QtCore.QRect(670, 140, 125, 51))
        self.select_dir_button.setObjectName("select_dir_button")
        self.select_dir_button.clicked.connect(self._update_directory)

        self.download_info_dir.setAlignment(QtCore.Qt.AlignCenter)

        self.yt_url_label.setGeometry(QtCore.QRect(16, 20, 131, 31))
        self.yt_url_label.setObjectName("yt_url_label")

        self.url_edit.setGeometry(QtCore.QRect(160, 20, 591, 31))
        self.url_edit.returnPressed.connect(self.check_url)
        self.url_edit.setObjectName("url_edit")

        self.download_type_comboBox.setGeometry(QtCore.QRect(160, 70, 171, 31))
        self.download_type_comboBox.setObjectName("download_type_comboBox")
        self.download_type_comboBox.addItem("Audio (mp3)")
        self.download_type_comboBox.addItem("Video (mp4)")

        self.yt_url_label_2.setGeometry(QtCore.QRect(20, 70, 131, 31))
        self.yt_url_label_2.setObjectName("yt_url_label_2")

        self.download_info_dir.setEnabled(True)
        self.download_info_dir.setGeometry(QtCore.QRect(34, 140, 610, 51))

        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)

        self.text_output.setEnabled(True)
        self.text_output.setGeometry(QtCore.QRect(33, 210, 761, 191))
        self.text_output.setAcceptRichText(False)
        self.text_output.setObjectName("text_output")
        self.text_output.setReadOnly(True)

        self.label.setGeometry(QtCore.QRect(660, 520, 161, 16))
        self.label.setObjectName("label")

        self.main_window.setCentralWidget(self.central_widget)

        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 829, 21))
        self.menu_bar.setObjectName("menu_bar")

        self.main_window.setMenuBar(self.menu_bar)
        self.status_bar.setObjectName("status_bar")

        self.main_window.setStatusBar(self.status_bar)

        self.re_translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("yt_main_window", "Youtube Downloader"))
        self.pushButton.setText(_translate("yt_main_window", "Download Now!!"))
        self.select_dir_button.setText(_translate("yt_main_window", 'Change Folder'))
        self.yt_url_label.setToolTip(
            _translate("yt_main_window", "Paste Youtube video URL on the right"))
        self.yt_url_label.setText(_translate("yt_main_window",
                                             "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; "
                                             "font-weight:600; text-decoration: underline;\">Youtube "
                                             "URL:</span></p></body></html>"))

        self.download_info_dir.setText(_translate("yt_main_window", self.save_dirs.main_path))

        self.url_edit.setToolTip(_translate("yt_main_window",
                                            "<html><head/><body><p>Paste Youtube video or playlist URL "
                                            "here</p></body></html>"))
        self.url_edit.setPlaceholderText(
            _translate("yt_main_window", "Paste youtube video or playlist URL here"))
        self.download_type_comboBox.setItemText(0, _translate("yt_main_window", "Audio (mp3)"))
        self.download_type_comboBox.setItemText(1, _translate("yt_main_window", "Video (mp4)"))
        self.yt_url_label_2.setToolTip(
            _translate("yt_main_window", "Select if you want to download a music or a video file"))
        self.yt_url_label_2.setText(_translate("yt_main_window",
                                               "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; "
                                               "font-weight:600; text-decoration: underline;\">Download "
                                               "Type:</span></p></body></html>"))
        self.label.setText(_translate("yt_main_window",
                                      "<html><head/><body><p align=\"right\"><span style=\" font-size:7pt;\">Have "
                                      "fun using it</span></p></body></html>"))

    def append(self, text):
        cursor = self.text_output.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)

    def _update_directory(self):

        text = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select save folder', str(Path.home()),
                                                          QtWidgets.QFileDialog.ShowDirsOnly)

        wt.clear(file_name='save_path.txt')
        wt.write(msg='{}'.format(text), file_name='save_path.txt')
        sd.path_refresh()
        self.download_info_dir.setText(sd.main_path)

    def clipboard_changed(self):
        text = QApplication.clipboard().text()
        if text.startswith("https://www.youtube.com"):
            if text.find('&'):
                text = text.split('&')[0]
            self.text_output.setText("Copied URL: " + text)
            self.url_edit.setText(text)
            self.check_url()

    def check_url(self):
        self.pushButton.setEnabled(False)
        if self.url_edit.text() == '' or len(self.url_edit.text()) <= 12:
            self.text_output.append('\n' + 'Enter a valid URL')
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
            only_audio = True if self.download_type_comboBox.currentIndex() == 0 else False
            process = Process(target=dn.download_chooser, args=(str(self.url_edit.text()), only_audio))
            wt.clear()
            process.start()
            while process.is_alive():
                self.text_output.setText(wt.read())
                self.text_output.ensureCursorVisible()
                self.text_output.verticalScrollBar().setValue(self.text_output.verticalScrollBar().maximum())
                QtGui.QGuiApplication.processEvents()
            self.pushButton.setEnabled(True)
            time.sleep(0.05)
