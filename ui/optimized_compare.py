# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optimized_compare.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QVBoxLayout,
    QWidget)
class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(773, 657)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutTop = QHBoxLayout()
        self.horizontalLayoutTop.setObjectName(u"horizontalLayoutTop")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutTop.addItem(self.horizontalSpacer)

        self.title = QLabel(Form)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"font: 700 16pt \"Microsoft YaHei UI\"; color: #000;")

        self.horizontalLayoutTop.addWidget(self.title)

        self.horizontalSpacerTop = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutTop.addItem(self.horizontalSpacerTop)

        self.compareButton = QPushButton(Form)
        self.compareButton.setObjectName(u"compareButton")

        self.horizontalLayoutTop.addWidget(self.compareButton)

        self.exportButton = QPushButton(Form)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayoutTop.addWidget(self.exportButton)


        self.verticalLayout.addLayout(self.horizontalLayoutTop)

        self.horizontalLayoutImport = QHBoxLayout()
        self.horizontalLayoutImport.setObjectName(u"horizontalLayoutImport")
        self.importOriginalFileButton = QPushButton(Form)
        self.importOriginalFileButton.setObjectName(u"importOriginalFileButton")

        self.horizontalLayoutImport.addWidget(self.importOriginalFileButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutImport.addItem(self.horizontalSpacer_4)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayoutImport.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutImport.addItem(self.horizontalSpacer_3)

        self.historyButton = QPushButton(Form)
        self.historyButton.setObjectName(u"historyButton")

        self.horizontalLayoutImport.addWidget(self.historyButton)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutImport.addItem(self.horizontalSpacer_5)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutImport.addItem(self.horizontalSpacer_6)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayoutImport.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutImport.addItem(self.horizontalSpacer_2)

        self.importCompareFileButton = QPushButton(Form)
        self.importCompareFileButton.setObjectName(u"importCompareFileButton")

        self.horizontalLayoutImport.addWidget(self.importCompareFileButton)


        self.verticalLayout.addLayout(self.horizontalLayoutImport)

        self.splitterMain = QSplitter(Form)
        self.splitterMain.setObjectName(u"splitterMain")
        self.splitterMain.setOrientation(Qt.Orientation.Horizontal)
        self.leftPanel = QWidget(self.splitterMain)
        self.leftPanel.setObjectName(u"leftPanel")
        self.verticalLayoutLeft = QVBoxLayout(self.leftPanel)
        self.verticalLayoutLeft.setObjectName(u"verticalLayoutLeft")
        self.verticalLayoutLeft.setContentsMargins(0, 0, 0, 0)
        self.webEngineOriginView = QWebEngineView(self.leftPanel)
        self.webEngineOriginView.setObjectName(u"webEngineOriginView")
        self.webEngineOriginView.setUrl(QUrl(u"about:blank"))

        self.verticalLayoutLeft.addWidget(self.webEngineOriginView)

        self.splitterMain.addWidget(self.leftPanel)
        self.rightPanel = QWidget(self.splitterMain)
        self.rightPanel.setObjectName(u"rightPanel")
        self.verticalLayoutRight = QVBoxLayout(self.rightPanel)
        self.verticalLayoutRight.setObjectName(u"verticalLayoutRight")
        self.verticalLayoutRight.setContentsMargins(0, 0, 0, 0)
        self.webEngineCompareView = QWebEngineView(self.rightPanel)
        self.webEngineCompareView.setObjectName(u"webEngineCompareView")
        self.webEngineCompareView.setUrl(QUrl(u"about:blank"))

        self.verticalLayoutRight.addWidget(self.webEngineCompareView)

        self.splitterMain.addWidget(self.rightPanel)

        self.verticalLayout.addWidget(self.splitterMain)

        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6587\u4ef6\u5bf9\u6bd4\u5de5\u5177", None))
        self.title.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6/\u5408\u540c\u4fee\u6539\u68c0\u67e5\u8f6f\u4ef6", None))
        self.compareButton.setText(QCoreApplication.translate("Form", u"\u70b9\u51fb\u5bf9\u6bd4", None))
        self.exportButton.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa", None))
        self.importOriginalFileButton.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165\u539f\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u539f\u6587\u4ef6", None))
        self.historyButton.setText(QCoreApplication.translate("Form", u"\u5386\u53f2\u6587\u4ef6\u67e5\u8be2", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6bd4\u5bf9\u6587\u4ef6", None))
        self.importCompareFileButton.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165\u5bf9\u6bd4\u6587\u4ef6", None))
    # retranslateUi

