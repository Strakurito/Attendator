from PyQt5 import (QtWidgets, QtGui, QtCore)
from objects import Pracik
from datetime import datetime
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
        self.PIKM = "Resources\Lm.pkl"
        self.unpickle_data()
        self.checkMonth()


        self.init()

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
        self.menu.addItem("Srážky ze mzdy")
        self.menu.addItem("Pracovní oděvy")
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
            self.pracTab.item(self.pracici.index(pracik), 0).setBackground(QtGui.QColor(224, 224, 224))

            self.pracTab.setItem(self.pracici.index(pracik), 2, QtWidgets.QTableWidgetItem(str(pracik.kchod)))
            self.pracTab.item(self.pracici.index(pracik), 2).setTextAlignment(QtCore.Qt.AlignCenter)
            self.pracTab.item(self.pracici.index(pracik), 2).setBackground(QtGui.QColor(224, 224, 224))

            self.pracTab.setItem(self.pracici.index(pracik), 7, QtWidgets.QTableWidgetItem(str(pracik.premie)))
            self.pracTab.item(self.pracici.index(pracik), 7).setTextAlignment(QtCore.Qt.AlignCenter)
            self.pracTab.item(self.pracici.index(pracik), 7).setBackground(QtGui.QColor(224, 224, 224))

            self.pracTab.setItem(self.pracici.index(pracik), 9, QtWidgets.QTableWidgetItem(str(pracik.platUct)))
            self.pracTab.item(self.pracici.index(pracik), 9).setTextAlignment(QtCore.Qt.AlignCenter)
            self.pracTab.item(self.pracici.index(pracik), 9).setBackground(QtGui.QColor(224, 224, 224))

            self.pracTab.setItem(self.pracici.index(pracik), 6, QtWidgets.QTableWidgetItem(pracik.srazCelk()))
            self.pracTab.item(self.pracici.index(pracik), 6).setTextAlignment(QtCore.Qt.AlignCenter)

            self.pracTab.setItem(self.pracici.index(pracik), 1, QtWidgets.QTableWidgetItem(pracik.hodinyCelk()))
            self.pracTab.item(self.pracici.index(pracik), 1).setTextAlignment(QtCore.Qt.AlignCenter)

            self.pracTab.setItem(self.pracici.index(pracik), 5, QtWidgets.QTableWidgetItem(pracik.odevyCelk()))
            self.pracTab.item(self.pracici.index(pracik), 5).setTextAlignment(QtCore.Qt.AlignCenter)

            self.pracTab.setItem(self.pracici.index(pracik), 4, QtWidgets.QTableWidgetItem(pracik.zalohyCelk()))
            self.pracTab.item(self.pracici.index(pracik), 4).setTextAlignment(QtCore.Qt.AlignCenter)

            self.pracTab.setItem(self.pracici.index(pracik), 3,
                                 QtWidgets.QTableWidgetItem(str(int(pracik.hodinyCelk()) *
                                                                int(self.pracTab.item(self.pracici.index(pracik), 2).text()))))
            self.pracTab.item(self.pracici.index(pracik), 3).setTextAlignment(QtCore.Qt.AlignCenter)

            self.pracTab.setItem(self.pracici.index(pracik), 8, QtWidgets.QTableWidgetItem(str(
                                                                int(self.pracTab.item(self.pracici.index(pracik), 3).text()) -
                                                                    (int(pracik.srazCelk()) +
                                                                     int(pracik.odevyCelk()) +
                                                                     int(pracik.zalohyCelk())) +
                                                                int(self.pracTab.item(self.pracici.index(pracik), 7).text()))))
            self.pracTab.item(self.pracici.index(pracik), 8).setTextAlignment(QtCore.Qt.AlignCenter)

            self.pracTab.setItem(self.pracici.index(pracik), 10, QtWidgets.QTableWidgetItem(str(
                int(self.pracTab.item(self.pracici.index(pracik), 8).text()) - int(
                    self.pracTab.item(self.pracici.index(pracik), 9).text()))))
            self.pracTab.item(self.pracici.index(pracik), 10).setTextAlignment(QtCore.Qt.AlignCenter)

        self.pracTab.setItem(len(self.pracici), 0, QtWidgets.QTableWidgetItem(""))
        self.pracTab.setItem(len(self.pracici), 2, QtWidgets.QTableWidgetItem(""))
        self.pracTab.setItem(len(self.pracici), 7, QtWidgets.QTableWidgetItem(""))
        self.pracTab.setItem(len(self.pracici), 9, QtWidgets.QTableWidgetItem(""))


        self.pracTab.itemDoubleClicked.connect(lambda: self.selectPracik(self.pracTab.currentRow()))
        self.pracTab.itemChanged.connect(lambda: self.changeData(self.pracTab.currentRow(), self.pracTab.currentColumn()))


    def load_stavba(self, stavba):
        if stavba == "Pracovníci":
            return
        elif stavba == "Srážky ze mzdy":
            self.setCentralWidget(SrazWindow(self, self.pracici, self.stavby))
        elif stavba == "Pracovní oděvy":
            self.setCentralWidget(OdevWindow(self, self.pracici, self.stavby))
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
                if self.pracTab.item(curRow, curCol).text().isnumeric():
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
        with open(self.PIKM, "rb") as a:
            self.lastMonth = pickle.load(a)

    def pickle_data(self):
        with open(self.PIKP, "wb") as a:
            pickle.dump(self.pracici, a, protocol=4)
        with open(self.PIKH, "wb") as a:
            pickle.dump(self.hesla, a, protocol=4)
        with open(self.PIKS, "wb") as a:
            pickle.dump(self.stavby, a, protocol=4)
        with open(self.PIKM, "wb") as a:
            pickle.dump(self.lastMonth, a, protocol=4)

    def checkMonth(self):
        if self.lastMonth != datetime.now().month:
            self.archive()

    def archive(self):
        pass



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
        self.stavTab = QtWidgets.QTableWidget(len(self.pracici), len(self.pracici[0].dochazky[stavba].dny) + 14)
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
        self.menu.addItem("Srážky ze mzdy")
        self.menu.addItem("Pracovní oděvy")
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

        pocetDni = len(self.pracici[0].dochazky[stavba].dny)

        self.stavTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Jméno"))
        for i in range(len(self.pracici[0].dochazky[stavba].dny)):
            self.stavTab.setHorizontalHeaderItem(i + 1, QtWidgets.QTableWidgetItem(str(i + 1)))
        self.stavTab.setHorizontalHeaderItem(pocetDni + 1,
                                             QtWidgets.QTableWidgetItem("Celkem"))
        self.stavTab.setHorizontalHeaderItem(pocetDni + 2,
                                             QtWidgets.QTableWidgetItem("Jméno"))
        for i in [pocetDni + 3, pocetDni + 5,pocetDni + 7 ,pocetDni + 9 ,pocetDni + 11]:
            self.stavTab.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem("  Záloha  "))
        for i in [pocetDni + 4, pocetDni + 6,pocetDni + 8 ,pocetDni + 10 ,pocetDni + 12]:
            self.stavTab.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem("  Datum  "))
        self.stavTab.setHorizontalHeaderItem(pocetDni + 13, QtWidgets.QTableWidgetItem("  Celkem  "))
        self.stavTab.setHorizontalHeaderItem(len(self.pracici[0].dochazky[stavba].dny) + 2,
                                             QtWidgets.QTableWidgetItem("Jméno"))


        for pracik in self.pracici:
            self.stavTab.setItem(self.pracici.index(pracik), 0, QtWidgets.QTableWidgetItem(pracik.jmeno))
            self.stavTab.item(self.pracici.index(pracik), 0).setBackground(QtGui.QColor(224, 224, 224))
            self.stavTab.setItem(self.pracici.index(pracik),pocetDni + 2, QtWidgets.QTableWidgetItem(pracik.jmeno))
            self.stavTab.item(self.pracici.index(pracik),pocetDni + 2).setBackground(QtGui.QColor(224, 224, 224))
            self.stavTab.setItemDelegate(ReadOnlyDelegate(self))
            self.stavTab.setItem(self.pracici.index(pracik), pocetDni + 1,QtWidgets.QTableWidgetItem(
                str(sum((pracik.dochazky[self.curStavba].dny)))))
            self.stavTab.item(self.pracici.index(pracik),pocetDni + 1).setTextAlignment(QtCore.Qt.AlignCenter)
            self.stavTab.item(self.pracici.index(pracik),pocetDni + 1).setBackground(QtGui.QColor(50, 100, 255))
            self.stavTab.item(self.pracici.index(pracik),pocetDni + 1).setForeground(QtGui.QColor("white"))

            for i,j in zip([pocetDni + 3, pocetDni + 5, pocetDni + 7, pocetDni + 9, pocetDni + 11],[0,1,2,3,4]):
                self.stavTab.setItem(self.pracici.index(pracik), i, QtWidgets.QTableWidgetItem(str(pracik.zalohy[j].castka)))
            for i,j in zip([pocetDni + 4, pocetDni + 6, pocetDni + 8, pocetDni + 10, pocetDni + 12],[0,1,2,3,4]):
                self.stavTab.setItem(self.pracici.index(pracik), i, QtWidgets.QTableWidgetItem(pracik.zalohy[j].datum))

            for i in range(len(self.pracici[0].dochazky[self.curStavba].dny)):
                if pracik.dochazky[self.curStavba].dny[i] == 0:
                    self.stavTab.setItem(self.pracici.index(pracik),
                                         i + 1, QtWidgets.QTableWidgetItem(""))
                else:
                    self.stavTab.setItem(self.pracici.index(pracik),
                                         i + 1, QtWidgets.QTableWidgetItem(str(pracik.dochazky[self.curStavba].dny[i])))
                if i in pracik.dochazky[self.curStavba].vikendy:
                    self.stavTab.item(self.pracici.index(pracik), i + 1).setBackground(QtGui.QColor(150,200,255))

    def load_stavba(self, stavba):
        if stavba == "Pracovníci":
            self.main.init()
        elif stavba == "Srážky ze mzdy":
            self.main.setCentralWidget(SrazWindow(self.main, self.pracici, self.stavby))
        elif stavba == "Pracovní oděvy":
            self.main.setCentralWidget(OdevWindow(self.main, self.pracici, self.stavby))
        elif stavba == "Přidat":
            self.add_build = AddWindow(self.main)
            self.add_build.show()
        else:
            self.main.setCentralWidget(BuildWindow(self.main, stavba, self.pracici, self.stavby))
    def change_build(self):
        self.change_win = ChangeWindow(self.main,self.curStavba)
        self.change_win.show()


class SrazWindow(QtWidgets.QWidget):

    def __init__(self, main, pracici, stavby):
        super().__init__()

        self.main = main
        self.stavby = stavby
        self.pracici = pracici

        self.title = QtWidgets.QLabel("Srážky ze mzdy")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(
            "color: white; font-family: Montserrat SemiBold; font-size: 40px; text-decoration: underline; background: transparent; border: transparent")
        self.srazTab = QtWidgets.QTableWidget(len(self.pracici), 5)
        self.srazTab.verticalHeader().hide()
        self.srazTab.horizontalHeader().sectionPressed.disconnect()
        self.load_tabulka()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.menu = QtWidgets.QListWidget()
        self.menu.setFixedWidth(250)
        self.menu.addItem("Pracovníci")
        self.menu.addItem("Srážky ze mzdy")
        self.menu.addItem("Pracovní oděvy")
        for stavba in self.stavby:
            self.menu.addItem(stavba)
        self.menu.addItem("Přidat")

        self.menu.itemClicked.connect(lambda: self.load_stavba(self.menu.currentItem().text()))

        tab_layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addSpacing(70)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.menu)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.srazTab)
        tab_layout.addSpacing(20)
        self.layout.addLayout(tab_layout)

    def load_tabulka(self):
        Hheader = self.srazTab.horizontalHeader()
        Hheader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.srazTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("    Jméno    "))
        self.srazTab.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem(" Srážka za vizum "))
        self.srazTab.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem(" Srážka za Covid test "))
        self.srazTab.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem(" Pokuta "))
        self.srazTab.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem(" Celkem "))

        for pracik in self.pracici:
            self.srazTab.setItem(self.pracici.index(pracik), 0, QtWidgets.QTableWidgetItem(pracik.jmeno))
            self.srazTab.item(self.pracici.index(pracik), 0).setBackground(QtGui.QColor(224, 224, 224))
            self.srazTab.setItem(self.pracici.index(pracik), 1, QtWidgets.QTableWidgetItem(str(pracik.srazy["V"])))
            self.srazTab.item(self.pracici.index(pracik), 1).setTextAlignment(QtCore.Qt.AlignRight)
            self.srazTab.setItem(self.pracici.index(pracik), 2, QtWidgets.QTableWidgetItem(str(pracik.srazy["C"])))
            self.srazTab.item(self.pracici.index(pracik), 2).setTextAlignment(QtCore.Qt.AlignRight)
            self.srazTab.setItem(self.pracici.index(pracik), 3, QtWidgets.QTableWidgetItem(str(pracik.srazy["P"])))
            self.srazTab.item(self.pracici.index(pracik), 3).setTextAlignment(QtCore.Qt.AlignRight)
            self.srazTab.setItem(self.pracici.index(pracik), 4, QtWidgets.QTableWidgetItem(pracik.srazCelk()))
            self.srazTab.item(self.pracici.index(pracik), 4).setTextAlignment(QtCore.Qt.AlignRight)
            self.srazTab.setItemDelegateForColumn(0,ReadOnlyDelegate(self))
            self.srazTab.setItemDelegateForColumn(4,ReadOnlyDelegate(self))
        self.srazTab.itemChanged.connect(
            lambda: self.changeData(self.srazTab.currentRow(), self.srazTab.currentColumn()))

    def changeData(self, curRow, curCol):
        self.srazTab.itemChanged.disconnect()
        pracik = self.pracici[curRow]
        if curCol == 0 or self.srazTab.item(curRow, curCol).text().isnumeric() is False:
            pass
        elif curCol == 1:
            pracik.srazy["V"] = int(self.srazTab.item(curRow, curCol).text())
        elif curCol == 2:
            pracik.srazy["C"] = int(self.srazTab.item(curRow, curCol).text())
        elif curCol == 3:
            pracik.srazy["P"] = int(self.srazTab.item(curRow, curCol).text())
        elif curCol == 4:
            pass
        self.load_tabulka()
        self.srazTab.itemChanged.connect(
            lambda: self.changeData(self.srazTab.currentRow(), self.srazTab.currentColumn()))
        self.main.pickle_data()

    def load_stavba(self, stavba):
        if stavba == "Pracovníci":
            self.main.init()
        elif stavba == "Srážky ze mzdy":
            self.main.setCentralWidget(SrazWindow(self.main, self.pracici, self.stavby))
        elif stavba == "Pracovní oděvy":
            self.main.setCentralWidget(OdevWindow(self.main, self.pracici, self.stavby))
        elif stavba == "Přidat":
            self.add_build = AddWindow(self.main)
            self.add_build.show()
        else:
            self.main.setCentralWidget(BuildWindow(self.main, stavba, self.pracici, self.stavby))


class OdevWindow(QtWidgets.QWidget):

    def __init__(self, main, pracici, stavby):
        super().__init__()

        self.main = main
        self.stavby = stavby
        self.pracici = pracici

        self.title = QtWidgets.QLabel("Pracovní oděvy")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(
            "color: white; font-family: Montserrat SemiBold; font-size: 40px; text-decoration: underline; background: transparent; border: transparent")
        self.odevTab = QtWidgets.QTableWidget(len(self.pracici), 5)
        self.odevTab.verticalHeader().hide()
        self.odevTab.horizontalHeader().sectionPressed.disconnect()
        self.odevTab.itemChanged.connect(lambda: self.changeData(self.odevTab.currentRow(), self.odevTab.currentColumn()))
        self.load_tabulka()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.menu = QtWidgets.QListWidget()
        self.menu.setFixedWidth(250)
        self.menu.addItem("Pracovníci")
        self.menu.addItem("Srážky ze mzdy")
        self.menu.addItem("Pracovní oděvy")
        for stavba in self.stavby:
            self.menu.addItem(stavba)
        self.menu.addItem("Přidat")

        self.menu.itemClicked.connect(lambda: self.load_stavba(self.menu.currentItem().text()))

        tab_layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addSpacing(70)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.menu)
        tab_layout.addSpacing(20)
        tab_layout.addWidget(self.odevTab)
        tab_layout.addSpacing(20)
        self.layout.addLayout(tab_layout)

    def load_tabulka(self):
        Hheader = self.odevTab.horizontalHeader()
        Hheader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.odevTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("    Jméno    "))
        self.odevTab.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("      Typ      "))
        self.odevTab.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem(" Cena "))
        self.odevTab.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem(" Počet ks "))
        self.odevTab.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem(" Celkem "))

        for pracik in self.pracici:
            self.odevTab.setItem(self.pracici.index(pracik), 0, QtWidgets.QTableWidgetItem(pracik.jmeno))
            self.odevTab.item(self.pracici.index(pracik), 0).setBackground(QtGui.QColor(224, 224, 224))
            self.odevTab.setItem(self.pracici.index(pracik), 1, QtWidgets.QTableWidgetItem(str(pracik.odevy["T"])))
            self.odevTab.item(self.pracici.index(pracik), 1).setTextAlignment(QtCore.Qt.AlignRight)
            self.odevTab.setItem(self.pracici.index(pracik), 2, QtWidgets.QTableWidgetItem(str(pracik.odevy["C"])))
            self.odevTab.item(self.pracici.index(pracik), 2).setTextAlignment(QtCore.Qt.AlignRight)
            self.odevTab.setItem(self.pracici.index(pracik), 3, QtWidgets.QTableWidgetItem(str(pracik.odevy["P"])))
            self.odevTab.item(self.pracici.index(pracik), 3).setTextAlignment(QtCore.Qt.AlignRight)
            self.odevTab.setItem(self.pracici.index(pracik), 4, QtWidgets.QTableWidgetItem(pracik.odevyCelk()))
            self.odevTab.item(self.pracici.index(pracik), 4).setTextAlignment(QtCore.Qt.AlignRight)
            self.odevTab.setItemDelegateForColumn(0, ReadOnlyDelegate(self))
            self.odevTab.setItemDelegateForColumn(4, ReadOnlyDelegate(self))

    def changeData(self, curRow, curCol):
        self.odevTab.itemChanged.disconnect()
        pracik = self.pracici[curRow]
        if curCol == 0:
            pass
        elif curCol == 1:
            pracik.odevy["T"] = self.odevTab.item(curRow, curCol).text()
        elif curCol == 2 and self.odevTab.item(curRow, curCol).text().isnumeric():
            pracik.odevy["C"] = int(self.odevTab.item(curRow, curCol).text())
        elif curCol == 3 and self.odevTab.item(curRow, curCol).text().isnumeric():
            pracik.odevy["P"] = int(self.odevTab.item(curRow, curCol).text())
        elif curCol == 4 and self.odevTab.item(curRow, curCol).text().isnumeric():
            pass
        self.load_tabulka()
        self.odevTab.itemChanged.connect(
            lambda: self.changeData(self.odevTab.currentRow(), self.odevTab.currentColumn()))
        self.main.pickle_data()

    def load_stavba(self, stavba):
        if stavba == "Pracovníci":
            self.main.init()
        elif stavba == "Srážky ze mzdy":
            self.main.setCentralWidget(SrazWindow(self.main, self.pracici, self.stavby))
        elif stavba == "Pracovní oděvy":
            self.main.setCentralWidget(OdevWindow(self.main, self.pracici, self.stavby))
        elif stavba == "Přidat":
            self.add_build = AddWindow(self.main)
            self.add_build.show()
        else:
            self.main.setCentralWidget(BuildWindow(self.main, stavba, self.pracici, self.stavby))


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