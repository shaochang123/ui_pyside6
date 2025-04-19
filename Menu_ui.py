# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Menu.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"\n"
"/* \u83dc\u5355\u680f\u80cc\u666f */\n"
"QMenuBar {\n"
"    background-color: #2196F3;  /* \u84dd\u8272\u80cc\u666f */\n"
"    color: white;               /* \u767d\u8272\u6587\u5b57 */\n"
"}\n"
"\n"
"/* \u83dc\u5355\u9879\u6837\u5f0f */\n"
"QMenuBar::item {\n"
"    background-color: transparent;  /* \u9ed8\u8ba4\u900f\u660e\u80cc\u666f */\n"
"    padding: 5px 10px;             /* \u5185\u8fb9\u8ddd */\n"
"}\n"
"\n"
"/* \u9f20\u6807\u60ac\u505c\u5728\u83dc\u5355\u9879\u4e0a\u65f6 */\n"
"QMenuBar::item:selected {\n"
"    background-color: #0d47a1;  /* \u6df1\u84dd\u8272 */\n"
"}\n"
"QPushButton {\n"
"    color: white;  /* \u767d\u8272\u5b57\u4f53 */\n"
"    border-radius: 8px;  /* \u5706\u89d2\u8fb9\u6846 */\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                               stop:0 #2196F3, stop:1 #1976D2);  /* \u6e10\u53d8\u84dd\u8272 */\n"
"    padding: 5px 15px;  /* \u5185\u8fb9\u8ddd */\n"
"    font-weight: bold;  /* \u7c97\u4f53 */\n"
"    border: 1px solid #1565C0;  /* \u8fb9"
                        "\u6846\u989c\u8272 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                               stop:0 #42A5F5, stop:1 #2196F3);  /* \u60ac\u505c\u65f6\u989c\u8272\u66f4\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                               stop:0 #1976D2, stop:1 #0D47A1);  /* \u6309\u4e0b\u65f6\u989c\u8272\u66f4\u6697 */\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setStyleSheet(u"")
        self.menuMessage = QMenu(self.menubar)
        self.menuMessage.setObjectName(u"menuMessage")
        self.menuPlot = QMenu(self.menubar)
        self.menuPlot.setObjectName(u"menuPlot")
        self.menuLearn = QMenu(self.menubar)
        self.menuLearn.setObjectName(u"menuLearn")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMessage.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menubar.addAction(self.menuLearn.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuMessage.setTitle(QCoreApplication.translate("MainWindow", u"Message", None))
        self.menuPlot.setTitle(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.menuLearn.setTitle(QCoreApplication.translate("MainWindow", u"Learn", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
    # retranslateUi

