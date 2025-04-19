# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Plot.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QMainWindow,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(895, 595)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ComName = QTextEdit(self.centralwidget)
        self.ComName.setObjectName(u"ComName")
        self.ComName.setGeometry(QRect(0, 0, 91, 31))
        self.BaudName = QTextEdit(self.centralwidget)
        self.BaudName.setObjectName(u"BaudName")
        self.BaudName.setGeometry(QRect(0, 30, 91, 31))
        self.start = QPushButton(self.centralwidget)
        self.start.setObjectName(u"start")
        self.start.setGeometry(QRect(0, 70, 161, 31))
        self.port_combo = QComboBox(self.centralwidget)
        self.port_combo.setObjectName(u"port_combo")
        self.port_combo.setGeometry(QRect(90, 0, 80, 31))
        self.baud_combo = QComboBox(self.centralwidget)
        self.baud_combo.setObjectName(u"baud_combo")
        self.baud_combo.setGeometry(QRect(90, 30, 80, 31))
        self.image = QGraphicsView(self.centralwidget)
        self.image.setObjectName(u"image")
        self.image.setGeometry(QRect(0, 150, 171, 441))
        self.close = QPushButton(self.centralwidget)
        self.close.setObjectName(u"close")
        self.close.setGeometry(QRect(0, 110, 161, 31))
        self.plotWidget = QWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")
        self.plotWidget.setGeometry(QRect(170, 0, 731, 221))
        self.cube3dContainer = QWidget(self.centralwidget)
        self.cube3dContainer.setObjectName(u"cube3dContainer")
        self.cube3dContainer.setGeometry(QRect(180, 429, 171, 161))
        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setGeometry(QRect(370, 470, 75, 81))
        icon = QIcon()
        icon.addFile(u"resource/reset.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.reset_button.setIcon(icon)
        self.plotWidget2 = QWidget(self.centralwidget)
        self.plotWidget2.setObjectName(u"plotWidget2")
        self.plotWidget2.setGeometry(QRect(170, 220, 721, 221))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ComName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u7aef\u53e3\u53f7", None))
        self.BaudName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6ce2\u7279\u7387", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u7aef\u53e3", None))
        self.close.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u7aef\u53e3", None))
        self.reset_button.setText("")
    # retranslateUi

