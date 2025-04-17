# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(867, 615)
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_7 = QHBoxLayout(self.widget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"border-image: url(:/image/resource/img.png);")

        self.horizontalLayout_6.addWidget(self.widget_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget1 = QWidget(self.frame_3)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 30, 271, 111))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.login_0 = QPushButton(self.layoutWidget1)
        self.login_0.setObjectName(u"login_0")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.login_0.sizePolicy().hasHeightForWidth())
        self.login_0.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"\u7b49\u7ebf"])
        font.setPointSize(28)
        font.setBold(True)
        self.login_0.setFont(font)

        self.horizontalLayout.addWidget(self.login_0)

        self.register_0 = QPushButton(self.layoutWidget1)
        self.register_0.setObjectName(u"register_0")
        self.register_0.setFont(font)

        self.horizontalLayout.addWidget(self.register_0)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy2)
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutWidget = QWidget(self.frame_4)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 20, 301, 301))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.horizontalLayoutWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.login_1 = QPushButton(self.page)
        self.login_1.setObjectName(u"login_1")
        self.login_1.setGeometry(QRect(100, 220, 107, 39))
        font1 = QFont()
        font1.setFamilies([u"\u7b49\u7ebf"])
        font1.setPointSize(22)
        font1.setBold(True)
        self.login_1.setFont(font1)
        self.layoutWidget2 = QWidget(self.page)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(20, 40, 281, 121))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_5 = QLabel(self.layoutWidget2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        font2 = QFont()
        font2.setFamilies([u"\u7b49\u7ebf"])
        font2.setPointSize(20)
        font2.setBold(True)
        self.label_5.setFont(font2)

        self.verticalLayout_4.addWidget(self.label_5)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)

        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)
        self.label_7.setFont(font2)

        self.verticalLayout_4.addWidget(self.label_7)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lineEdit_6 = QLineEdit(self.layoutWidget2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy4)

        self.verticalLayout_5.addWidget(self.lineEdit_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.lineEdit_7 = QLineEdit(self.layoutWidget2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy5)

        self.verticalLayout_5.addWidget(self.lineEdit_7)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.layoutWidget3 = QWidget(self.page_2)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(20, 20, 271, 191))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.layoutWidget3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_3)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.label_4 = QLabel(self.layoutWidget3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_4)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.label_6 = QLabel(self.layoutWidget3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_6)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEdit_3 = QLineEdit(self.layoutWidget3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy6)

        self.verticalLayout_3.addWidget(self.lineEdit_3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.lineEdit_4 = QLineEdit(self.layoutWidget3)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy6.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy6)

        self.verticalLayout_3.addWidget(self.lineEdit_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.lineEdit_5 = QLineEdit(self.layoutWidget3)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy6.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy6)

        self.verticalLayout_3.addWidget(self.lineEdit_5)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(4, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.layoutWidget = QWidget(self.page_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 240, 221, 41))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.register_1 = QPushButton(self.layoutWidget)
        self.register_1.setObjectName(u"register_1")
        self.register_1.setFont(font1)

        self.horizontalLayout_5.addWidget(self.register_1)

        self.cancel_1 = QPushButton(self.layoutWidget)
        self.cancel_1.setObjectName(u"cancel_1")
        self.cancel_1.setFont(font1)

        self.horizontalLayout_5.addWidget(self.cancel_1)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout_2.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frame_4)


        self.horizontalLayout_6.addLayout(self.verticalLayout)


        self.horizontalLayout_7.addWidget(self.frame)

        MainWindow.setCentralWidget(self.widget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.login_0.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.register_0.setText(QCoreApplication.translate("MainWindow", u"\u6ce8\u518c", None))
        self.login_1.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u518d\u6b21\u8f93\u5165", None))
        self.register_1.setText(QCoreApplication.translate("MainWindow", u"\u6ce8\u518c", None))
        self.cancel_1.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u6d88", None))
    # retranslateUi

