import sys
from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QTableWidget, QTableWidgetItem, \
    QScrollArea,QMessageBox, \
    QPushButton, QLineEdit,\
    QLabel, QComboBox,QGridLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QColor,QPixmap
from ttn_mqtt import ttn_mqtt
from ttn_mqtt import ttn_constants
from ttn_mqtt import ttn_device
from collections import defaultdict
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pymysql.cursors
import time

class App(QWidget):

    ScannerList = []
    PayloadList = []
    TimeStampList = []

    HistScannerList = []
    HistPayloadList = []
    HistTimeStampList = []

    LoadListScanner = []
    LoadListTag = []
    LoadListBlock = []

    AllowListCheckScanner = []
    AllowListCheckTag = []
    AllowListCheckPermission = []

    TempList1 = []
    TempList2 = []
    TempList3 = []

    TList1 = []
    TList2 = []
    engine = create_engine('sqlite://', echo=False)

    def __init__(self):
        super().__init__()
        self.title = 'BLE LoRaWAN Application'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 950
        self.styleSheet = """
        QPushButton {
        background-color: #4e4e4e;
        color: #ffffff;
        }
        QComboBox {
        background-color: #4e4e4e;
        color: #ffffff;
        }
        QLabel {
        font-family: "Times New Roman", Times, serif;
        font-size: 25px;
        font-weight: bold;
        color: ;
        }
        QTableWidget {
        border-radius: 5px;
        border: 5px solid #4e4e4e;
        }
        App {
        background-color: #42A5F5;
        }
        """
        self.initUI()
        self.connectTTN()
        self.loadHistTable()
        self.allowListLoad()
        self._shape = np.array(['capsule', 'circle', 'rectangle'])
        self._color = np.array(['blue', 'green', 'orange', 'purple', 'red',
                                'yellow'])

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.app = QApplication([])
        self.app.setStyleSheet(self.styleSheet)
        self.window = QWidget()
        self.scroll = QScrollArea()

        # Live Table
        self.LiveLabel = QLabel("Live Table",self)
        self.LiveLabel.move(20,10)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setFixedSize(600, 400)
        self.tableWidget.move(20,50)
        #self.tableWidget.setColumnCount(3)

        # History Table
        self.HistLabel = QLabel("History Table", self)
        self.HistLabel.move(20, 460)
        self.histTable = QTableWidget(self)
        self.histTable.setFixedSize(520, 400)
        self.histTable.move(20,500)

        # Allow list
        self.AllowLabel = QLabel("Allow List", self)
        self.AllowLabel.move(600, 10)

        ###############################
        self.allowTable = QTableWidget(self)
        self.allowTable.setFixedSize(275, 400)
        self.allowTable.move(600, 50)

        ##############################
        self.scannerLabel = QLabel("Scanner", self)
        self.scannerLabel.move(900, 110)
        self.scannerDrop = QComboBox(self)
        self.scannerDrop.move(900,150)
        self.scannerDrop.addItem(" ")
        self.scannerDrop.addItem("nasrs-pycom")
        self.scannerDrop.addItem("nasrs-pycom-2")
        ##################################
        self.tagLabel = QLabel("Tag", self)
        self.tagLabel.move(1050, 110)
        self.tagDrop = QComboBox(self)
        self.tagDrop.move(1050, 150)
        self.tagDrop.addItem(" ")
        self.tagDrop.addItem("Tag1")
        self.tagDrop.addItem("Tag2")
        self.tagDrop.addItem("Tag3")

        ############################
        self.buttonAllow = QPushButton('Allow', self)
        self.buttonAllow.move(880, 200)
        self.buttonAllow.clicked.connect(self.allowListAllow)

        ###########################################
        self.buttonBlock = QPushButton('Block', self)
        self.buttonBlock.move(980, 200)
        self.buttonBlock.clicked.connect(self.allowListBlock)

        ###########################################
        self.buttonDelete = QPushButton('Delete', self)
        self.buttonDelete.move(1080, 200)
        self.buttonDelete.clicked.connect(self.allowListDelete)

        #Refresh History table
        self.button = QPushButton('Refresh', self)
        self.button.move(550, 650)
        self.button.clicked.connect(self.refresh_button)

        #Search History Table
        self.edit = QLineEdit(self)
        self.edit.move(550, 700)

        self.button2 = QPushButton('Search', self)
        self.button2.move(550, 750)
        self.button2.clicked.connect(self.searchValue)
        ########################
        label = QLabel(self)
        pixmap = QPixmap("C:/Users/nasr1/PycharmProjects/untitled/img.jpg")
        label.setPixmap(pixmap)
        label.setGeometry(10, 10, 400, 100)
        ############################################3

        # Show widget
        self.show()

    def node_callback(self,payload):
        print(payload)
        self.PayloadList.append(payload.get('payload_fields', {}).get('receivedString'))
        self.TempList1.append(payload.get('payload_fields', {}).get('receivedString'))

        self.ScannerList.append(payload.get('dev_id'))
        self.TempList2.append(payload.get('dev_id'))

        self.TimeStampList.append(payload.get('metadata', {}).get('time'))
        self.TempList3.append(payload.get('metadata', {}).get('time'))

        for x in self.PayloadList:
            if (' ' in x):
                b = x.count(' ')
                c = self.PayloadList.index(x)
                self.PayloadList = [word for line in self.PayloadList for word in line.split()]
                self.PayloadList = [w.replace('"','') for w in self.PayloadList]
                for y in self.ScannerList:
                    ay = [(y+" ")*b]
                    ay = [word for line in ay for word in line.split()]
                    pass
                for u in ay:
                    self.ScannerList.insert(c, u)
                    pass
                for z in self.TimeStampList:
                    az = [(z+" ")*b]
                    az = [word for line in az for word in line.split()]
                    pass
                for p in az:
                    self.TimeStampList.insert(c, p)
                    pass
            else:
                self.PayloadList = [w.replace('"', '') for w in self.PayloadList]
        self.TimeStampList = [w.replace('T', ' ') for w in self.TimeStampList]

        for y in self.TempList1:
            if (' ' in y):
                b = y.count(' ')
                c = self.TempList1.index(x)
                self.TempList1 = [word for line in self.TempList1 for word in line.split()]
                self.TempList1 = [w.replace('"','') for w in self.TempList1]
                for x in self.TempList2:
                    ay = [(x+" ")*b]
                    ay = [word for line in ay for word in line.split()]
                    pass
                for u in ay:
                    self.TempList2.insert(c, u)
                    pass
                for z in self.TempList3:
                    az = [(z+" ")*b]
                    az = [word for line in az for word in line.split()]
                    pass
                for p in az:
                    self.TempList3.insert(c, p)
                    pass
            else:
                self.TempList1 = [w.replace('"', '') for w in self.TempList1]
        self.TempList3 = [w.replace('T', ' ') for w in self.TempList3]

        #self.tableWidget.setRowCount(0)
        self.updateLive()

    def updateLive(self):
        column_list = pd.DataFrame(np.column_stack([self.ScannerList, self.PayloadList, self.TimeStampList]),
                                   columns=['Scanner', 'Payload', 'TimeStamp'])

        column_list.to_sql('db_table2', self.engine, if_exists='append', index=False)
        #self.constDict.extend(x)
        #y = pd.DataFrame(self.constDict)
        y = pd.read_sql_query('select * from "db_table2"', con= self.engine)
        #n = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(len(column_list.columns))
        self.tableWidget.setRowCount(len(y.index))

        self.tableWidget.setHorizontalHeaderLabels(["Scanner", "Payload", "TimeStamp"])
        #self.tableWidget.resizeColumnsToContents()

        for i in range(len(y.index)):
            for j in range(len(column_list.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(y.iloc[i, j])))

        self.TList1.extend(self.PayloadList)
        self.TList2.extend(self.ScannerList)

        time.sleep(1)
        self.allowListCheck()

        self.PayloadList.clear()
        self.TimeStampList.clear()
        self.ScannerList.clear()

        self.insertTable()

        self.TempList1.clear()
        self.TempList2.clear()
        self.TempList3.clear()

    def insertTable(self):
        scanner = self.TempList2
        payload = self.TempList1
        timestamp = self.TempList3

        con = pymysql.connect(host='localhost',user='root', password='Nasax1972', db= 'blelora', charset = 'utf8mb4',cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            sql = " INSERT INTO live(scanner,payload,timestamp) VALUES (%s,%s,%s)"
            cur.executemany(sql, zip(scanner, payload, timestamp))

            con.commit()
            print("success")

    def loadHistTable(self):
        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            sql = " SELECT * FROM live"
            cur.execute(sql)
            data = cur.fetchall()

            for x in data:
                self.HistPayloadList.append(x.get('payload'))
                self.HistScannerList.append(x.get('scanner'))
                self.HistTimeStampList.append(x.get('timestamp'))

                column_list2 = pd.DataFrame(np.column_stack([self.HistScannerList, self.HistPayloadList, self.HistTimeStampList]),
                                       columns=['Scanner', 'Payload', 'TimeStamp'])

            self.histTable.setColumnCount(len(column_list2.columns))
            self.histTable.setRowCount(len(column_list2.index))
            self.histTable.setHorizontalHeaderLabels(["Scanner", "Payload", "TimeStamp"])
            self.histTable.resizeColumnsToContents()

            for i in range(len(column_list2.index)):
                for j in range(len(column_list2.columns)):
                    self.histTable.setItem(i, j, QTableWidgetItem(str(column_list2.iloc[i, j])))
            self.allowListCheckHist()

    def refresh_button(self):
        self.HistPayloadList.clear()
        self.HistTimeStampList.clear()
        self.HistScannerList.clear()
        self.histTable.setRowCount(0)
        self.loadHistTable()

    def searchValue(self):
        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        Text = self.edit.text()
        with con.cursor() as cur:

            sql = " SELECT scanner,payload,timestamp FROM live WHERE CONCAT_WS('', scanner,payload,timestamp) LIKE %s ; "
            cur.execute(sql,("%"+Text+"%",))
            data = cur.fetchall()
            print(data)
            self.HistPayloadList.clear()
            self.HistTimeStampList.clear()
            self.HistScannerList.clear()
            self.histTable.setRowCount(0)
            for x in data:
                self.HistPayloadList.append(x.get('payload'))
                self.HistScannerList.append(x.get('scanner'))
                self.HistTimeStampList.append(x.get('timestamp'))

            column_list2 = pd.DataFrame(
                np.column_stack([self.HistScannerList, self.HistPayloadList, self.HistTimeStampList]),
                columns=['Scanner', 'Payload', 'TimeStamp'])

            self.histTable.setColumnCount(len(column_list2.columns))
            self.histTable.setRowCount(len(column_list2.index))
            self.histTable.setHorizontalHeaderLabels(["Scanner", "Payload", "TimeStamp"])
            self.histTable.resizeColumnsToContents()

            for i in range(len(column_list2.index)):
                for j in range(len(column_list2.columns)):
                    self.histTable.setItem(i, j, QTableWidgetItem(str(column_list2.iloc[i, j])))
            self.allowListCheckHist()

    def allowListAllow(self):
        scannerName = str(self.scannerDrop.currentText())
        tagName = str(self.tagDrop.currentText())

        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        with con.cursor() as cur:
            # cur = con.cursor()
            sql = " INSERT INTO data4(scanner,tag,permission) VALUES (%s,%s,%s)"
            cur.execute(sql, (scannerName, tagName, "Allow"))
            con.commit()
            print("success")

        self.LoadListScanner.clear()
        self.LoadListTag.clear()
        self.LoadListBlock.clear()
        self.allowTable.setRowCount(0)
        self.allowListLoad()

    def allowListBlock(self):
        scannerName = str(self.scannerDrop.currentText())
        tagName = str(self.tagDrop.currentText())

        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            sql = " INSERT INTO data4(scanner,tag,permission) VALUES (%s,%s,%s)"
            cur.execute(sql, (scannerName, tagName, "Block"))
            con.commit()
            print("success")

        self.LoadListScanner.clear()
        self.LoadListTag.clear()
        self.LoadListBlock.clear()
        self.allowTable.setRowCount(0)
        self.allowListLoad()

    def allowListLoad(self):

        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            sql = " SELECT * FROM data4"
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            for x in data:
                self.LoadListScanner.append(x.get('scanner'))
                self.LoadListTag.append(x.get('tag'))
                self.LoadListBlock.append(x.get('permission'))

                column_list5 = pd.DataFrame(
                    np.column_stack([self.LoadListScanner, self.LoadListTag, self.LoadListBlock]),
                    columns=['Scanner', 'Tag', 'Permission'])

            self.allowTable.setColumnCount(len(column_list5.columns))
            self.allowTable.setRowCount(len(column_list5.index))
            self.allowTable.setHorizontalHeaderLabels(["Scanner", "Tag", "Permission"])
            self.allowTable.resizeColumnsToContents()

            for i in range(len(column_list5.index)):
                for j in range(len(column_list5.columns)):
                    self.allowTable.setItem(i, j, QTableWidgetItem(str(column_list5.iloc[i, j])))

    def allowListDelete(self):
        row = self.allowTable.currentRow()
        scannerName = (self.allowTable.item(row, 0).text())
        tagName= (self.allowTable.item(row, 1).text())
        allowDeny = (self.allowTable.item(row, 2).text())
        self.allowTable.removeRow(row)

        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            # cur = con.cursor()
            sql = " DELETE FROM data4 WHERE scanner = %s AND tag = %s AND permission = %s"
            cur.execute(sql, (scannerName, tagName, allowDeny))
            con.commit()
            print("success")

    def allowListCheck(self):
        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            sql = " SELECT scanner,tag,permission FROM data4 "
            cur.execute(sql, )
            data = cur.fetchall()
            #print(data)

            for x in data:
                self.AllowListCheckTag.append(x.get('tag'))
                self.AllowListCheckPermission.append(x.get('permission'))
                self.AllowListCheckScanner.append(x.get('scanner'))

            for idx,ele in enumerate(self.TList1):
                for id,el in enumerate(self.TList2):
                    if idx == id:
                        for i,e in enumerate(self.AllowListCheckScanner):
                            for a, b in enumerate(self.AllowListCheckTag):
                                for c, d in enumerate(self.AllowListCheckPermission):
                                    if i == a and a == c:
                                        if b == ele and e == el:
                                            if d == 'Allow':
                                                self.tableWidget.item(idx, 1).setBackground(
                                                    QColor(0, 0, 255, 127))
                                                #print("allow")
                                            elif d == 'Block':
                                                self.tableWidget.item(idx, 1).setBackground(
                                                    QColor(255, 0, 0, 127))
                                                #print("block")

    def allowListCheckHist(self):
        con = pymysql.connect(host='localhost', user='root', password='Nasax1972', db='blelora', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con.cursor() as cur:
            sql = " SELECT scanner,tag,permission FROM data4 "
            cur.execute(sql, )
            data = cur.fetchall()
            # print(data)

            for x in data:
                self.AllowListCheckTag.append(x.get('tag'))
                self.AllowListCheckPermission.append(x.get('permission'))
                self.AllowListCheckScanner.append(x.get('scanner'))

            for idx, ele in enumerate(self.HistPayloadList):
                for id, el in enumerate(self.HistScannerList):
                    if idx == id:
                        for i, e in enumerate(self.AllowListCheckScanner):
                            for a, b in enumerate(self.AllowListCheckTag):
                                for c, d in enumerate(self.AllowListCheckPermission):
                                    if i == a and a == c:
                                        if b == ele and e == el:
                                            if d == 'Allow':
                                                self.histTable.item(idx, 1).setBackground(
                                                    QColor(0, 0, 255, 127))
                                                # print("allow")
                                            elif d == 'Block':
                                                self.histTable.item(idx, 1).setBackground(
                                                    QColor(255, 0, 0, 127))
                                                # print("block")

    #Connection methods
    def connectTTN(self):
        self.ttn = ttn_mqtt.ttn_mqtt(ttn_constants.EU, "nh-t",
                                "ttn-account-v2.Z3dlOAHrQkTx16ZWeav6ulHpj0aHuiS7AC_b7YoFTaA")  # Open connection

        self.ttn.connect()  # Connect to TTN

        self.test_node = ttn_device.device("nasrs-pycom")  # Register node
        self.test_node.set_uplink_callback(self.node_callback)
        self.ttn.register_device(self.test_node)

        self.test_node2 = ttn_device.device("nasrs-pycom-2")  # Register node
        self.test_node2.set_uplink_callback(self.node_callback)
        self.ttn.register_device(self.test_node2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()

    sys.exit(app.exec_())