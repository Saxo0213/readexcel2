# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
import pandas as pd
from UIdata import Ui_MainWindow
import sys


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.students = {}
        self.student = ""
        self.file_path = ""
        self.MaxColumn = 0
        self.MaxRow = 0
        self.df = 0
        self.Sname = ""
        self.Dname = ""
        self.Dataname = ""
        
        #基本設定
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(258,219)
        #檔案管理功能設定
        
        #啟動介面設定
        
        self.setup_control()

    def setup_control(self):
        #設定按鈕功能
        self.ui.comboBox_students.currentIndexChanged.connect(self.Set_Student_DayData)
        self.ui.comboBox_day.currentIndexChanged.connect(self.Set_Day_Data)
        self.ui.comboBox_data.currentIndexChanged.connect(self.Set_Data_Data)
        self.ui.pushButton_openfile.clicked.connect(self.openfile)
    
    def Cprint(self):
        print(self.Sname,",",self.Dname,",",self.Dataname)

    def Set_Student_DayData(self):
        self.Sname =  self.ui.comboBox_students.currentText()
        self.ComboBox_Add(self.ui.comboBox_day,self.students[self.Sname].keys())

    def Set_Day_Data(self):
        self.Dname   =  self.ui.comboBox_day.currentText()
        if self.Sname != "" and self.Dname != "":
            self.ComboBox_Add(self.ui.comboBox_data,self.students[self.Sname][self.Dname].keys())

    def Set_Data_Data(self):
        self.Dataname = self.ui.comboBox_data.currentText()
        if self.Sname != "" and self.Dname != "" and self.Dataname != "":
            self.ui.label_data.setText(str(self.students[self.Sname][self.Dname][self.Dataname]))
        
    def openfile(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.ui.label_filepath.setText(self.file_path)
        self.df = pd.read_excel(self.file_path)
        self.LoadExcel_ColumnRow()
        self.loadstudent()
        self.ComboBox_Add(self.ui.comboBox_students,self.students)
        
    def ComboBox_Add(self,Combox,Dlist):
        Combox.clear()
        for k in Dlist:
            Combox.addItem(k)

    def loadstudent(self):
        print("load students")
        student= ""
        for i in range(self.MaxRow):
            C1_value = self.LoadExcel_Data(i,0)
            if  pd.notna(C1_value):
                student = C1_value
                self.students[student] = {}
            else:
                C2_value = self.LoadExcel_Data(i,1)
                if pd.isna(C2_value):
                    if pd.notna(self.LoadExcel_Data(i,2)):
                        raw_dataname = []
                        for j in range(2,self.MaxColumn):
                            raw_data = self.LoadExcel_Data(i,j)
                            if pd.isna(raw_data):
                                continue
                            raw_dataname.append(raw_data)
                else:
                    self.students[student][C2_value] = {}
                    ColumnData = list(range(2,self.MaxColumn))
                    for k in range(len(ColumnData)):
                        R_value = self.LoadExcel_Data(i,ColumnData[k])
                        if pd.isna(R_value):
                            continue
                        self.students[student][C2_value][raw_dataname[k]] = R_value
        print(self.students)

    def LoadExcel_ColumnRow(self):
        print("load Colunm,row")
        self.MaxColumn = self.df.columns.size
        self.MaxRow = self.df.index.size

    def LoadExcel_Data(self,R,C): #C=column R=row
        value = self.df.iloc[R, C]
        return  value



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())