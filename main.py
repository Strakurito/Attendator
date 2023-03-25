from PyQt5 import (QtWidgets, QtGui, QtCore)
from objects import Pracik
import pickle
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self, **kwargs):
        super(Window, self).__init__(**kwargs)
        self.hesla = {}
        self.stavby = []
        self.pracici = list()
        self.PIKP = "Resources\Pracovnici.pkl"
        self.PIKS = "Resources\Stavby.pkl"
        self.PIKH = "Resources\Ps.pkl"
        self.unpickle_data()
        self.init()
    def hovno(self):
        return
    def init(self):
        main = QtWidgets.QWidget()
        self.setMinimumSize(1600, 1300)
        self.setCentralWidget(main)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.layout)
        main.setLayout(self.main_layout)

        self.pracTab = QtWidgets.QTableWidget(len(self.pracici) + 1, 11)
        self.pracTab.horizontalHeader().sectionPressed.disconnect()

        self.setWindowTitle("Attendator5000")
        self.show()
        QtGui.QFontDatabase.addApplicationFont("Resources\monty.ttf")
        self.setStyleSheet("""
                                        QMenuBar::item {
                                        font-size: 24px;
                                        }

                                        QMainWindow {
                                        border-image: url(Resources/BG.png);}

                                        QLabel {
                                        font-family: Montserrat SemiBold;
                                        font-size: 18px;
                                        }

                                        QWidget {
                                        font-family: Montserrat SemiBold;
                                        font-size: 17px;
                                        }

                                        QHeaderView::section {
                                        border: 1px solid grey;
                                        text-align: center;
                                        }

                                        QTableWidget::item:focus { 
                                        background-color:transparent; color:black;
                                        }
                                        
                                        QTableWidget::item { 
                                        border: 1px solid grey;
                                        }
                                        """)
        self.pracovnici_tabulka_load()
        title = QtWidgets.QLabel("Pracovníci")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet(
            "color: white; font-family: Montserrat SemiBold; font-size: 40px; text-decoration: underline;")
        tab_layout = QtWidgets.QHBoxLayout()
        self.menu_list_load()
        self.layout.addWidget(title)
        self.layout.addSpacing(70)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.menu)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.pracTab)
        tab_layout.addSpacing(20)
        self.layout.addLayout(tab_layout)


    def menu_list_load(self):
        self.menu = QtWidgets.QListWidget()
        self.menu.setFixedWidth(250)
        self.menu.addItem("Pracovníci")
        for stavba in self.stavby:
            self.menu.addItem(stavba)
        self.menu.addItem("Přidat")

        self.menu.itemClicked.connect(lambda: self.load_stavba(self.menu.currentItem().text()))


    def pracovnici_tabulka_load(self):
        self.pickle_data()
        self.pracTab.verticalHeader().hide()
        self.pracTab.setRowCount(len(self.pracici) + 1)


        Hheader = self.pracTab.horizontalHeader()
        Hheader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #Hheader.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        Hheader.setMinimumSectionSize(200)

        self.pracTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Jméno"))
        self.pracTab.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Odpracovaných hodin"))
        self.pracTab.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Kč/hod"))
        self.pracTab.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Mzda"))
        self.pracTab.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Vyplacené zálohy Kč"))
        self.pracTab.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("Pracovní oděvy"))
        self.pracTab.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem("Srážky ze mzdy"))
        self.pracTab.setHorizontalHeaderItem(7, QtWidgets.QTableWidgetItem("Premie"))
        self.pracTab.setHorizontalHeaderItem(8, QtWidgets.QTableWidgetItem("Celkem k výplatě"))
        self.pracTab.setHorizontalHeaderItem(9, QtWidgets.QTableWidgetItem("Platba na účet"))
        self.pracTab.setHorizontalHeaderItem(10, QtWidgets.QTableWidgetItem("Doplatek"))

        for num in range(11):
            if num not in [0,2,7,9]:
                self.pracTab.setItemDelegateForColumn(num, ReadOnlyDelegate(self))
        for pracik in self.pracici:
            self.pracTab.setItem(self.pracici.index(pracik), 0, QtWidgets.QTableWidgetItem(pracik.jmeno))
            self.pracTab.setItem(self.pracici.index(pracik), 2, QtWidgets.QTableWidgetItem(str(pracik.kchod)))
            self.pracTab.setItem(self.pracici.index(pracik), 7, QtWidgets.QTableWidgetItem(str(pracik.premie)))
            self.pracTab.setItem(self.pracici.index(pracik), 9, QtWidgets.QTableWidgetItem(str(pracik.platUct)))

        self.pracTab.setItem(len(self.pracici), 0, QtWidgets.QTableWidgetItem(""))
        self.pracTab.setItem(len(self.pracici), 2, QtWidgets.QTableWidgetItem(""))
        self.pracTab.setItem(len(self.pracici), 7, QtWidgets.QTableWidgetItem(""))
        self.pracTab.setItem(len(self.pracici), 9, QtWidgets.QTableWidgetItem(""))

        self.pracTab.itemDoubleClicked.connect(lambda: self.selectPracik(self.pracTab.currentRow()))
        self.pracTab.itemChanged.connect(lambda: self.changeData(self.pracTab.currentRow(), self.pracTab.currentColumn()))


    def load_stavba(self, stavba):
        if stavba == "Pracovníci":
            return
        elif stavba == "Přidat":
            self.add_build = AddWindow(self)
            self.add_build.show()
        else:
            self.setCentralWidget(BuildWindow(self, stavba, self.pracici, self.stavby))

    def selectPracik(self, curRow):
        for pracik in self.pracici:
            if pracik.jmeno == self.pracTab.item(curRow, 0).text():
                self.currentPracik = pracik
            elif self.pracTab.item(curRow, 0).text() == "":
                return

    def changeData(self, curRow, curCol):
        self.pracTab.itemChanged.disconnect()
        if curRow == len(self.pracici):
            if curCol == 0:
                if self.pracTab.item(curRow, curCol).text() not in [pracik.jmeno for pracik in self.pracici]:
                    self.pracici.append(Pracik(self.pracTab.item(curRow, curCol).text(), 0, 0, 0, self.stavby))

                self.pracovnici_tabulka_load()

            else:
                self.pracovnici_tabulka_load()
                return
        elif curRow <= len(self.pracici):
            if self.pracTab.item(curRow,0).text() == "":
                self.pracici.remove(self.currentPracik)
                del self.currentPracik
                self.pracovnici_tabulka_load()
            else:
                if self.pracTab.item(curRow, curCol).text() not in [pracik.jmeno for pracik in self.pracici]:
                    self.currentPracik.jmeno = self.pracTab.item(curRow, 0).text()
                self.currentPracik.kchod = int(self.pracTab.item(curRow, 2).text())
                self.currentPracik.premie = int(self.pracTab.item(curRow, 7).text())
                self.currentPracik.platUct = int(self.pracTab.item(curRow, 9).text())
                self.pracovnici_tabulka_load()

    def unpickle_data(self):
        with open(self.PIKP, "rb") as a:
            self.pracici = pickle.load(a)
        with open(self.PIKH, "rb") as a:
            self.hesla = pickle.load(a)
        with open(self.PIKS, "rb") as a:
            self.stavby = pickle.load(a)

    def pickle_data(self):
        with open(self.PIKP, "wb") as a:
            pickle.dump(self.pracici, a, protocol=4)
        with open(self.PIKH, "wb") as a:
            pickle.dump(self.hesla, a, protocol=4)
        with open(self.PIKS, "wb") as a:
            pickle.dump(self.stavby, a, protocol=4)



class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

class BuildWindow(QtWidgets.QWidget):

    def __init__(self, main, stavba, pracici, stavby):
        super().__init__()

        self.main = main
        self.curStavba = stavba
        self.stavby = stavby
        self.pracici = pracici

        self.title = QtWidgets.QPushButton(self.curStavba)
        self.title.pressed.connect(lambda: self.change_build())
        self.title.setStyleSheet(
            "color: white; font-family: Montserrat SemiBold; font-size: 40px; text-decoration: underline; background: transparent; border: transparent")
        self.stavTab = QtWidgets.QTableWidget(len(self.pracici), len(self.pracici[0].dochazky[stavba].dny) + 1)
        self.stavTab.verticalHeader().hide()
        self.stavTab.horizontalHeader().sectionPressed.disconnect()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        date = QtWidgets.QLabel(
            str(self.pracici[0].dochazky[stavba].mesic) + ". " + str(self.pracici[0].dochazky[stavba].rok))
        date.setAlignment(QtCore.Qt.AlignCenter)
        date.setStyleSheet(
            "color: white; font-family: Montserrat SemiBold; font-size: 30px;")

        self.menu = QtWidgets.QListWidget()
        self.menu.setFixedWidth(250)
        self.menu.addItem("Pracovníci")
        for stavba in self.stavby:
            self.menu.addItem(stavba)
        self.menu.addItem("Přidat")

        self.menu.itemClicked.connect(lambda: self.load_stavba(self.menu.currentItem().text()))

        tab_layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(date)
        self.layout.addSpacing(20)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.menu)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.stavTab)
        tab_layout.addSpacing(20)
        self.layout.addLayout(tab_layout)

        Hheader = self.stavTab.horizontalHeader()
        Hheader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Hheader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.stavTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Jméno"))
        for i in range(len(self.pracici[0].dochazky[stavba].dny)):
            self.stavTab.setHorizontalHeaderItem(i + 1, QtWidgets.QTableWidgetItem(str(i + 1)))

        for pracik in self.pracici:
            self.stavTab.setItem(self.pracici.index(pracik), 0, QtWidgets.QTableWidgetItem(pracik.jmeno))
            self.stavTab.setItemDelegate(ReadOnlyDelegate(self))

            #přidat barvičky
            for i in range(len(self.pracici[0].dochazky[self.curStavba].dny)):
                self.stavTab.setItem(self.pracici.index(pracik),
                                     i + 1, QtWidgets.QTableWidgetItem(str(pracik.dochazky[self.curStavba].dny[i])))

    def load_stavba(self, stavba):
        if stavba == "Pracovníci":
            self.main.init()
        elif stavba == "Přidat":
            self.add_build = AddWindow(self.main)
            self.add_build.show()
        else:
            self.main.setCentralWidget(BuildWindow(self.main, stavba, self.pracici, self.stavby))
    def change_build(self):
        self.change_win = ChangeWindow(self.main,self.curStavba)
        self.change_win.show()



class AddWindow(QtWidgets.QWidget):

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Přidat stavbu")
        self.setFixedWidth(500)
        QtGui.QFontDatabase.addApplicationFont("Resources\monty.ttf")
        self.setStyleSheet("""
                                                QMenuBar::item {
                                                font-size: 24px;
                                                }

                                                QMainWindow {
                                                border-image: url(Resources/BG.png);}

                                                QLabel {
                                                font-family: Montserrat SemiBold;
                                                font-size: 18px;
                                                }

                                                QWidget {
                                                font-family: Montserrat SemiBold;
                                                font-size: 17px;
                                                }

                                                QHeaderView::section {
                                                border: 1px solid grey;
                                                text-align: center;
                                                }

                                                QTableWidget::item:focus { 
                                                background-color:transparent; color:black;
                                                }
                                                """)

        nameL = QtWidgets.QLabel("Název")
        nameB = QtWidgets.QLineEdit()

        passL = QtWidgets.QLabel("Heslo")
        passB = QtWidgets.QLineEdit()

        butt = QtWidgets.QPushButton("Přidat")

        self.layout.addWidget(nameL)
        self.layout.addWidget(nameB)
        self.layout.addWidget(passL)
        self.layout.addWidget(passB)
        self.layout.addWidget(butt)

        butt.pressed.connect(lambda: self.addBuild(nameB.text(), passB.text()))

    def addBuild(self, name, heslo):
        if name in self.main.stavby:
            return
        self.main.stavby.append(name)
        self.main.stavby.sort()
        self.main.hesla[name] = heslo
        for pracik in self.main.pracici:
            pracik.novaDochazka(name)
        self.main.init()
        self.main.pickle_data()
        self.close()

class ChangeWindow(QtWidgets.QWidget):

    def __init__(self, main, stavba):
        super().__init__()
        self.main = main
        self.stavba = stavba
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Změnit")
        self.setFixedWidth(500)
        QtGui.QFontDatabase.addApplicationFont("Resources\monty.ttf")
        self.setStyleSheet("""
                                                QMenuBar::item {
                                                font-size: 24px;
                                                }

                                                QMainWindow {
                                                border-image: url(Resources/BG.png);}

                                                QLabel {
                                                font-family: Montserrat SemiBold;
                                                font-size: 18px;
                                                }

                                                QWidget {
                                                font-family: Montserrat SemiBold;
                                                font-size: 17px;
                                                }

                                                QHeaderView::section {
                                                border: 1px solid grey;
                                                text-align: center;
                                                }

                                                QTableWidget::item:focus { 
                                                background-color:transparent; color:black;
                                                }
                                                """)

        nameL = QtWidgets.QLabel("Název")
        nameB = QtWidgets.QLineEdit(stavba)

        passL = QtWidgets.QLabel("Heslo")
        passB = QtWidgets.QLineEdit(self.main.hesla[stavba])

        butt = QtWidgets.QPushButton("Změnit")

        delete = QtWidgets.QPushButton("Smazat")

        self.layout.addWidget(nameL)
        self.layout.addWidget(nameB)
        self.layout.addWidget(passL)
        self.layout.addWidget(passB)
        self.layout.addSpacing(20)
        self.layout.addWidget(butt)
        self.layout.addSpacing(20)
        self.layout.addWidget(delete)

        butt.pressed.connect(lambda: self.changeBuild(nameB.text(), passB.text()))
        delete.pressed.connect(lambda: self.deleteBuild())

    def changeBuild(self, name, heslo):
        self.main.stavby.remove(self.stavba)
        self.main.hesla[name] = heslo
        for pracik in self.main.pracici:
            pracik.dochazky[name] = pracik.dochazky[self.stavba]
        del self.stavba
        self.main.stavby.append(name)
        self.main.stavby.sort()
        self.main.init()
        self.main.pickle_data()
        self.close()

    def deleteBuild(self):
        self.main.stavby.remove(self.stavba)
        del self.main.hesla[self.stavba]
        del self.stavba
        self.main.init()
        self.main.pickle_data()
        self.close()




app = QtWidgets.QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())