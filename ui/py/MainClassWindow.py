# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainClassWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QStatusBar, QTabWidget,
    QTextBrowser, QWidget)

from qfluentwidgets import (BodyLabel, CaptionLabel, CardWidget, HyperlinkLabel,
    ListWidget, PushButton, SimpleCardWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1114, 592)
        self.actionNew_Template = QAction(MainWindow)
        self.actionNew_Template.setObjectName(u"actionNew_Template")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_4 = QAction(MainWindow)
        self.action_4.setObjectName(u"action_4")
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_7 = QAction(MainWindow)
        self.action_7.setObjectName(u"action_7")
        self.action_8 = QAction(MainWindow)
        self.action_8.setObjectName(u"action_8")
        self.action_9 = QAction(MainWindow)
        self.action_9.setObjectName(u"action_9")
        self.action_11 = QAction(MainWindow)
        self.action_11.setObjectName(u"action_11")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_3 = QAction(MainWindow)
        self.action_3.setObjectName(u"action_3")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName(u"action_6")
        self.action_12 = QAction(MainWindow)
        self.action_12.setObjectName(u"action_12")
        self.action_13 = QAction(MainWindow)
        self.action_13.setObjectName(u"action_13")
        self.action_10 = QAction(MainWindow)
        self.action_10.setObjectName(u"action_10")
        self.action_14 = QAction(MainWindow)
        self.action_14.setObjectName(u"action_14")
        self.action_16 = QAction(MainWindow)
        self.action_16.setObjectName(u"action_16")
        self.action_17 = QAction(MainWindow)
        self.action_17.setObjectName(u"action_17")
        self.action_18 = QAction(MainWindow)
        self.action_18.setObjectName(u"action_18")
        self.action_15 = QAction(MainWindow)
        self.action_15.setObjectName(u"action_15")
        self.action_19 = QAction(MainWindow)
        self.action_19.setObjectName(u"action_19")
        self.action_20 = QAction(MainWindow)
        self.action_20.setObjectName(u"action_20")
        self.action_21 = QAction(MainWindow)
        self.action_21.setObjectName(u"action_21")
        self.action_22 = QAction(MainWindow)
        self.action_22.setObjectName(u"action_22")
        self.action_23 = QAction(MainWindow)
        self.action_23.setObjectName(u"action_23")
        self.action_24 = QAction(MainWindow)
        self.action_24.setObjectName(u"action_24")
        self.action_25 = QAction(MainWindow)
        self.action_25.setObjectName(u"action_25")
        self.action_26 = QAction(MainWindow)
        self.action_26.setObjectName(u"action_26")
        self.action_28 = QAction(MainWindow)
        self.action_28.setObjectName(u"action_28")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setGeometry(QRect(270, 0, 671, 411))
        self.tabWidget_2.setStyleSheet(u"QTabWidget::pane {\n"
"    background: transparent;\n"
"    border:1;\n"
"}\n"
"QTabWidget {\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.scrollArea = QScrollArea(self.tab_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 0, 661, 391))
        self.scrollArea.setStyleSheet(u"background: transparent;border:1;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 661, 391))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.scrollArea_2 = QScrollArea(self.tab_4)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setGeometry(QRect(0, 0, 651, 391))
        self.scrollArea_2.setStyleSheet(u"background: transparent;border:1;")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 651, 391))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(670, 420, 441, 131))
        self.textBrowser.setStyleSheet(u"background-color: rgba(255, 255, 255, 127);\n"
"border-color: rgb(12, 12, 12);")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(0, 0, 271, 211))
        self.listWidget.setStyleSheet(u"background-color: rgba(255, 255, 255, 127);")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(970, -24, 75, 24))
        self.CardWidget = CardWidget(self.centralwidget)
        self.CardWidget.setObjectName(u"CardWidget")
        self.CardWidget.setGeometry(QRect(0, 210, 271, 41))
        self.BodyLabel = BodyLabel(self.CardWidget)
        self.BodyLabel.setObjectName(u"BodyLabel")
        self.BodyLabel.setGeometry(QRect(150, 10, 141, 20))
        self.BodyLabel_2 = BodyLabel(self.CardWidget)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        self.BodyLabel_2.setGeometry(QRect(10, 10, 131, 19))
        self.SimpleCardWidget_2 = SimpleCardWidget(self.centralwidget)
        self.SimpleCardWidget_2.setObjectName(u"SimpleCardWidget_2")
        self.SimpleCardWidget_2.setGeometry(QRect(0, 250, 271, 161))
        self.CaptionLabel = CaptionLabel(self.SimpleCardWidget_2)
        self.CaptionLabel.setObjectName(u"CaptionLabel")
        self.CaptionLabel.setGeometry(QRect(10, 10, 70, 16))
        self.HyperlinkLabel = HyperlinkLabel(self.SimpleCardWidget_2)
        self.HyperlinkLabel.setObjectName(u"HyperlinkLabel")
        self.HyperlinkLabel.setGeometry(QRect(230, 10, 31, 16))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(8)
        font.setBold(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.HyperlinkLabel.setFont(font)
        self.PushButton = PushButton(self.SimpleCardWidget_2)
        self.PushButton.setObjectName(u"PushButton")
        self.PushButton.setGeometry(QRect(10, 40, 61, 31))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(9)
        font1.setBold(False)
        self.PushButton.setFont(font1)
        self.PushButton_2 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_2.setObjectName(u"PushButton_2")
        self.PushButton_2.setGeometry(QRect(100, 40, 61, 31))
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(9)
        font2.setBold(False)
        self.PushButton_2.setFont(font2)
        self.PushButton_3 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_3.setObjectName(u"PushButton_3")
        self.PushButton_3.setGeometry(QRect(190, 40, 61, 31))
        self.PushButton_3.setFont(font2)
        self.PushButton_4 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_4.setObjectName(u"PushButton_4")
        self.PushButton_4.setGeometry(QRect(10, 80, 61, 31))
        self.PushButton_4.setFont(font2)
        self.PushButton_5 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_5.setObjectName(u"PushButton_5")
        self.PushButton_5.setGeometry(QRect(100, 80, 61, 31))
        self.PushButton_5.setFont(font2)
        self.PushButton_6 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_6.setObjectName(u"PushButton_6")
        self.PushButton_6.setGeometry(QRect(190, 80, 61, 31))
        self.PushButton_6.setFont(font2)
        self.PushButton_7 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_7.setObjectName(u"PushButton_7")
        self.PushButton_7.setGeometry(QRect(190, 120, 61, 31))
        self.PushButton_7.setFont(font2)
        self.PushButton_8 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_8.setObjectName(u"PushButton_8")
        self.PushButton_8.setGeometry(QRect(100, 120, 61, 31))
        self.PushButton_8.setFont(font2)
        self.PushButton_9 = PushButton(self.SimpleCardWidget_2)
        self.PushButton_9.setObjectName(u"PushButton_9")
        self.PushButton_9.setGeometry(QRect(10, 120, 61, 31))
        self.PushButton_9.setFont(font2)
        self.SimpleCardWidget = SimpleCardWidget(self.centralwidget)
        self.SimpleCardWidget.setObjectName(u"SimpleCardWidget")
        self.SimpleCardWidget.setGeometry(QRect(0, 410, 271, 81))
        self.CaptionLabel_2 = CaptionLabel(self.SimpleCardWidget)
        self.CaptionLabel_2.setObjectName(u"CaptionLabel_2")
        self.CaptionLabel_2.setGeometry(QRect(10, 10, 70, 16))
        self.PushButton_10 = PushButton(self.SimpleCardWidget)
        self.PushButton_10.setObjectName(u"PushButton_10")
        self.PushButton_10.setGeometry(QRect(10, 30, 61, 31))
        self.PushButton_10.setFont(font2)
        self.PushButton_11 = PushButton(self.SimpleCardWidget)
        self.PushButton_11.setObjectName(u"PushButton_11")
        self.PushButton_11.setGeometry(QRect(100, 30, 61, 31))
        self.PushButton_11.setFont(font2)
        self.PushButton_12 = PushButton(self.SimpleCardWidget)
        self.PushButton_12.setObjectName(u"PushButton_12")
        self.PushButton_12.setGeometry(QRect(190, 30, 61, 31))
        self.PushButton_12.setFont(font2)
        self.SimpleCardWidget_3 = SimpleCardWidget(self.centralwidget)
        self.SimpleCardWidget_3.setObjectName(u"SimpleCardWidget_3")
        self.SimpleCardWidget_3.setGeometry(QRect(0, 490, 271, 61))
        self.pushButton = PushButton(self.SimpleCardWidget_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(180, 10, 81, 31))
        self.pushButton.setFont(font2)
        self.pushButton_3 = PushButton(self.SimpleCardWidget_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 10, 71, 31))
        self.pushButton_3.setFont(font2)
        self.pushButton_4 = PushButton(self.SimpleCardWidget_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(90, 10, 71, 31))
        self.pushButton_4.setFont(font2)
        self.SimpleCardWidget_4 = SimpleCardWidget(self.centralwidget)
        self.SimpleCardWidget_4.setObjectName(u"SimpleCardWidget_4")
        self.SimpleCardWidget_4.setGeometry(QRect(270, 420, 211, 131))
        self.label_2 = QLabel(self.SimpleCardWidget_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 30, 191, 16))
        self.label_3 = QLabel(self.SimpleCardWidget_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 50, 191, 16))
        self.label_4 = QLabel(self.SimpleCardWidget_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 70, 181, 16))
        self.label_5 = QLabel(self.SimpleCardWidget_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 90, 191, 16))
        self.BodyLabel_3 = BodyLabel(self.SimpleCardWidget_4)
        self.BodyLabel_3.setObjectName(u"BodyLabel_3")
        self.BodyLabel_3.setGeometry(QRect(10, 10, 65, 19))
        self.label_6 = QLabel(self.SimpleCardWidget_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(50, 110, 191, 16))
        self.label_12 = QLabel(self.SimpleCardWidget_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(20, 30, 31, 16))
        self.label_13 = QLabel(self.SimpleCardWidget_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(20, 50, 31, 16))
        self.label_14 = QLabel(self.SimpleCardWidget_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(20, 70, 31, 16))
        self.label_15 = QLabel(self.SimpleCardWidget_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(20, 90, 31, 16))
        self.label_16 = QLabel(self.SimpleCardWidget_4)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(10, 110, 41, 16))
        self.SimpleCardWidget_5 = SimpleCardWidget(self.centralwidget)
        self.SimpleCardWidget_5.setObjectName(u"SimpleCardWidget_5")
        self.SimpleCardWidget_5.setGeometry(QRect(480, 420, 191, 131))
        self.BodyLabel_4 = BodyLabel(self.SimpleCardWidget_5)
        self.BodyLabel_4.setObjectName(u"BodyLabel_4")
        self.BodyLabel_4.setGeometry(QRect(10, 10, 65, 19))
        self.label_7 = QLabel(self.SimpleCardWidget_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(50, 30, 161, 21))
        self.label_8 = QLabel(self.SimpleCardWidget_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(50, 50, 161, 21))
        self.label_9 = QLabel(self.SimpleCardWidget_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(50, 70, 161, 21))
        self.label_10 = QLabel(self.SimpleCardWidget_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(50, 90, 161, 21))
        self.label_11 = QLabel(self.SimpleCardWidget_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(50, 110, 231, 21))
        self.label_17 = QLabel(self.SimpleCardWidget_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(20, 30, 31, 21))
        self.label_18 = QLabel(self.SimpleCardWidget_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(20, 50, 31, 21))
        self.label_19 = QLabel(self.SimpleCardWidget_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(20, 70, 31, 21))
        self.label_20 = QLabel(self.SimpleCardWidget_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(20, 90, 31, 21))
        self.label_21 = QLabel(self.SimpleCardWidget_5)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(10, 110, 41, 21))
        self.ListWidget = ListWidget(self.centralwidget)
        self.ListWidget.setObjectName(u"ListWidget")
        self.ListWidget.setGeometry(QRect(940, 20, 171, 401))
        self.ListWidget.setStyleSheet(u"ListView,\n"
"ListWidget {\n"
"    background: transparent;\n"
"    outline: none;\n"
"    border: none;\n"
"    /* font: 13px 'Segoe UI', 'Microsoft YaHei'; */\n"
"    background-color: rgba(255, 255, 255, 127);\n"
"    padding-left: 4px;\n"
"    padding-right: 4px;\n"
"}\n"
"\n"
"ListView::item,\n"
"ListWidget::item {\n"
"    background: transparent;\n"
"    border: 0px;\n"
"    padding-left: 11px;\n"
"    padding-right: 11px;\n"
"    height: 35px;\n"
"}\n"
"\n"
"\n"
"ListView::indicator,\n"
"ListWidget::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 5px;\n"
"    border: 1px solid rgba(0, 0, 0, 0.48);\n"
"    background-color: rgba(0, 0, 0, 0.022);\n"
"    margin-right: 4px;\n"
"}\n"
"\n"
"ListView::indicator:hover,\n"
"ListWidget::indicator:hover {\n"
"    border: 1px solid rgba(0, 0, 0, 0.56);\n"
"    background-color: rgba(0, 0, 0, 0.05);\n"
"}\n"
"\n"
"ListView::indicator:pressed,\n"
"ListWidget::indicator:pressed {\n"
"    border: 1px solid rgba(0, 0, 0, 0.27);\n"
"    bac"
                        "kground-color: rgba(0, 0, 0, 0.12);\n"
"}\n"
"\n"
"ListView::indicator:checke,\n"
"ListWidget::indicator:checked,\n"
"ListView::indicator:indeterminate,\n"
"ListWidget::indicator:indeterminate {\n"
"    border: 1px solid #009faa;\n"
"    background-color: #009faa;\n"
"}\n"
"\n"
"ListView::indicator:checked,\n"
"ListWidget::indicator:checked {\n"
"    image: url(:/qfluentwidgets/images/check_box/Accept_white.svg);\n"
"}\n"
"\n"
"ListView::indicator:indeterminate,\n"
"ListWidget::indicator:indeterminate {\n"
"    image: url(:/qfluentwidgets/images/check_box/PartialAccept_white.svg);\n"
"}\n"
"\n"
"ListView::indicator:checked:hove,\n"
"ListWidget::indicator:checked:hover,\n"
"ListView::indicator:indeterminate:hover,\n"
"ListWidget::indicator:indeterminate:hover {\n"
"    border: 1px solid #00a7b3;\n"
"    background-color: #00a7b3;\n"
"}\n"
"\n"
"ListView::indicator:checked:presse,\n"
"ListWidget::indicator:checked:pressed,\n"
"ListView::indicator:indeterminate:pressed,\n"
"ListWidget::indicator:indeterminate:pre"
                        "ssed {\n"
"    border: 1px solid #3eabb3;\n"
"    background-color: #3eabb3;\n"
"}\n"
"\n"
"ListView::indicator:disabled,\n"
"ListWidget::indicator:disabled {\n"
"    border: 1px solid rgba(0, 0, 0, 0.27);\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"ListView::indicator:checked:disable,\n"
"ListWidget::indicator:checked:disabled,\n"
"ListView::indicator:indeterminate:disabled,\n"
"ListWidget::indicator:indeterminate:disabled {\n"
"    border: 1px solid rgb(199, 199, 199);\n"
"    background-color: rgb(199, 199, 199);\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1114, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.actionNew_Template)
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.action_5)
        self.menu.addAction(self.action_19)
        self.menu.addAction(self.action_22)
        self.menu.addAction(self.action_18)
        self.menu.addAction(self.action_7)
        self.menu.addSeparator()
        self.menu.addAction(self.action_12)
        self.menu.addAction(self.action_13)
        self.menu.addSeparator()
        self.menu.addAction(self.action_20)
        self.menu.addAction(self.action_21)
        self.menu_2.addAction(self.action_8)
        self.menu_2.addAction(self.action_9)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action)
        self.menu_3.addAction(self.action_15)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_3)
        self.menu_3.addAction(self.action_23)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_24)
        self.menu_3.addAction(self.action_25)
        self.menu_3.addAction(self.action_26)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_28)
        self.menu_4.addAction(self.action_10)
        self.menu_4.addAction(self.action_14)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.action_16)
        self.menu_4.addAction(self.action_17)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u754c\u9762", None))
        self.actionNew_Template.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u65b0\u6a21\u677f", None))
#if QT_CONFIG(shortcut)
        self.actionNew_Template.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u677f\u7ba1\u7406", None))
#if QT_CONFIG(shortcut)
        self.action_2.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+T", None))
#endif // QT_CONFIG(shortcut)
        self.action_4.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u70b9\u8bc4\uff08\u5355\u9009\uff09", None))
#if QT_CONFIG(shortcut)
        self.action_4.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_5.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u70b9\u8bc4", None))
#if QT_CONFIG(shortcut)
        self.action_5.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.action_7.setText(QCoreApplication.translate("MainWindow", u"\u64a4\u56de\u4e0a\u6b65", None))
#if QT_CONFIG(shortcut)
        self.action_7.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.action_8.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u7ec4\u89c6\u56fe", None))
#if QT_CONFIG(shortcut)
        self.action_8.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+G", None))
#endif // QT_CONFIG(shortcut)
        self.action_9.setText(QCoreApplication.translate("MainWindow", u"\u4e2a\u4eba\u89c6\u56fe", None))
#if QT_CONFIG(shortcut)
        self.action_9.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.action_11.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7\u83dc\u5355", None))
#if QT_CONFIG(shortcut)
        self.action_11.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u73ed\u7ea7\u6392\u540d", None))
#if QT_CONFIG(shortcut)
        self.action.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.action_3.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u5177\u8bbe\u7f6e", None))
#if QT_CONFIG(shortcut)
        self.action_3.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+,", None))
#endif // QT_CONFIG(shortcut)
        self.action_6.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
#if QT_CONFIG(shortcut)
        self.action_6.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_12.setText(QCoreApplication.translate("MainWindow", u"\u5468\u7ed3\u7b97", None))
#if QT_CONFIG(shortcut)
        self.action_12.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.action_13.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u5386\u53f2\u8bb0\u5f55", None))
#if QT_CONFIG(shortcut)
        self.action_13.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+H", None))
#endif // QT_CONFIG(shortcut)
        self.action_10.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5b58\u6863", None))
#if QT_CONFIG(shortcut)
        self.action_10.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_14.setText(QCoreApplication.translate("MainWindow", u"\u5c06\u5b58\u6863\u53e6\u5b58\u4e3a", None))
#if QT_CONFIG(shortcut)
        self.action_14.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+J", None))
#endif // QT_CONFIG(shortcut)
        self.action_16.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u8fd8\u539f\u70b9", None))
#if QT_CONFIG(shortcut)
        self.action_16.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+M", None))
#endif // QT_CONFIG(shortcut)
        self.action_17.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u8fd8\u539f\u70b9", None))
#if QT_CONFIG(shortcut)
        self.action_17.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.action_18.setText(QCoreApplication.translate("MainWindow", u"\u536b\u751f\u7ed3\u7b97", None))
#if QT_CONFIG(shortcut)
        self.action_18.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.action_15.setText(QCoreApplication.translate("MainWindow", u"\u64ad\u653e\u97f3\u4e50", None))
#if QT_CONFIG(shortcut)
        self.action_15.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.action_19.setText(QCoreApplication.translate("MainWindow", u"\u8003\u52e4\u8bb0\u5f55", None))
#if QT_CONFIG(shortcut)
        self.action_19.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.action_20.setText(QCoreApplication.translate("MainWindow", u"\u5168\u73ed\u95ed\u5634", None))
#if QT_CONFIG(shortcut)
        self.action_20.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_21.setText(QCoreApplication.translate("MainWindow", u"\u968f\u673a\u62bd\u4eba", None))
#if QT_CONFIG(shortcut)
        self.action_21.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.action_22.setText(QCoreApplication.translate("MainWindow", u"\u4f5c\u4e1a\u7ed3\u7b97", None))
#if QT_CONFIG(shortcut)
        self.action_22.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+B", None))
#endif // QT_CONFIG(shortcut)
        self.action_23.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e\u5de5\u5177", None))
        self.action_24.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u65e5\u5fd7", None))
        self.action_25.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u66f4\u65b0", None))
        self.action_26.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u7a97\u53e3", None))
        self.action_28.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u8bd5\u9879\u76ee", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u672c\u73ed\u5b66\u751f", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u672c\u73ed\u5c0f\u7ec4", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u6240\u6709", None))
        self.BodyLabel.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u5348\u597d\uff0c\u6b22\u8fce\u56de\u6765", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("MainWindow", u"2025/11/4 11:45:14", None))
        self.CaptionLabel.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u7ba1\u7406", None))
        self.HyperlinkLabel.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91", None))
        self.PushButton.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.CaptionLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u6700\u8fd1\u4f7f\u7528", None))
        self.PushButton_10.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_11.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.PushButton_12.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6307\u5b9a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u795e\u79d8\u6309\u94ae", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.BodyLabel_3.setText(QCoreApplication.translate("MainWindow", u"\u73ed\u7ea7\u4fe1\u606f", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u540d\u79f0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u4eba\u6570", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u6240\u5c5e", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u5747\u5206", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u4f4e\u5206", None))
        self.BodyLabel_4.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u4fe1\u606f", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"0fps; 0fps", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"0.0 s", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"114MB", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"51tps; 4tps", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u5e27\u7387", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u65f6\u95f4", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u7ebf\u7a0b", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u5185\u5b58", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u7387", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5176\u4ed6", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
    # retranslateUi

