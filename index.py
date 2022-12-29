from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qdarktheme
import sys
from PyQt5.uic import loadUiType
import sqlite3
# Load Ui file
UI, _ = loadUiType('UI.ui')
# Class for Gui


class MainWindowClass(QMainWindow, QTableWidgetItem, UI):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Airlines DBMS")
        self.setWindowIcon(QIcon('icon.ico'))
        self.InitializeUI()

    def updateTable(self, string, Tablewidget):
        # first Clearing table
        Tablewidget.setColumnCount(0)
        Tablewidget.setRowCount(0)
        # then performing query
        QueryResult = self.DB_Query(string)
        numrows = len(QueryResult[0])
        if numrows == 0:
            pass
        else:
            numcols = len(QueryResult[0][0])
            Tablewidget.setColumnCount(numcols)
            Tablewidget.setRowCount(numrows)
            Tablewidget.setHorizontalHeaderLabels(QueryResult[1])
            for row in range(numrows):
                for column in range(numcols):
                    Tablewidget.setItem(
                        row, column,
                        QTableWidgetItem(str((QueryResult[0][row][column]))))

    def DB_Query(self, str):
        conn = sqlite3.connect("Airlines.db")
        c = conn.cursor()
        c.execute(str)
        columnNames = [description[0] for description in c.description]
        table = c.fetchall()
        conn.close()
        return table, columnNames

    # Initianlizing function

    def updateAllTables(self):
        self.updateTable("SELECT * From AirCraft", self.tableWidget_AirCraft)
        self.updateTable("SELECT * From Branch", self.tableWidget_Branches)
        self.updateTable("SELECT * From Charges", self.tableWidget_Charges)
        self.updateTable("SELECT * From Country", self.tableWidget_Countries)
        self.updateTable("SELECT * From Discounts", self.tableWidget_Discounts)
        self.updateTable("SELECT * From Employee", self.tableWidget_Employee)
        self.updateTable("SELECT * From Flight_schedule",
                         self.tableWidget_Flight_Schedule)
        self.updateTable("SELECT * From Route", self.tableWidget_Route)
        self.updateTable("SELECT * From State", self.tableWidget_State)
        self.updateTable("SELECT * From Transactions",
                         self.tableWidget_Transactions)
        self.updateTable("SELECT * From Contact", self.tableWidget_Contact)
        self.updateTable("SELECT * From Passengers",
                         self.tableWidget_Passenger)

    def InitializeUI(self):
        self.updateAllTables()
        self.pushButton_Perform_Query.clicked.connect(self.PerformQuery)
        self.loadFLights_Query1()
        self.loadFlightDatesAndCountries_Query2()
        self.loadFlightDates_Query3()
        self.loadFlightsAirports_Query4()
        self.loadFlightDates_Query6()
        self.actionDark_2.triggered.connect(lambda: self.setStyleSheet(
            qdarktheme.load_stylesheet(theme="dark")))
        self.actionLight_2.triggered.connect(
            lambda: self.setStyleSheet("QLabel {}"))
        self.tabWidget_Perform_Selection.tabBarClicked.connect(
            self.ClearQueryTable)
        self.tabWidget_Tables.tabBarClicked.connect(self.updateAllTables)

    def PerformQuery(self):
        currentPerformTabIndex = self.tabWidget_Perform_Selection.currentIndex(
        )
        if currentPerformTabIndex == 0:
            selectedFlightID = self.comboBox_Flights.currentText().split(
                ',')[0][1:]
            if self.comboBox_travelllersSelection.currentIndex() == 0:
                self.updateTable(
                    "SELECT P.PassengerId, P.Name, P.Age, P.Address, P.Nationality,\
                     P.Contact_id, C.Email, C.CellPhone, C.State_id FROM Transactions AS T,\
                         Passengers AS P, Contact AS C WHERE T.Passenger_id=P.PassengerId  AND \
                            P.Contact_id=C.ContactId AND T.Flight_id=" +
                    selectedFlightID + " AND P.Nationality NOT LIKE'Egy%'",
                    self.tableWidget_PerformQuery)
            else:
                self.updateTable(
                    "SELECT P.PassengerId, P.Name, P.Age, P.Address, P.Nationality,\
                     P.Contact_id, C.Email, C.CellPhone, C.State_id FROM Transactions AS T,\
                         Passengers AS P, Contact AS C WHERE T.Passenger_id=P.PassengerId  \
                            AND P.Contact_id=C.ContactId AND T.Flight_id=" +
                    selectedFlightID, self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 1:
            SelectedDate = self.comboBox_FlightDateSelection.currentText()
            SelectedDistination = self.comboBox_FlightDistinationSelection.currentText(
            )
            self.updateTable(
                "SELECT DISTINCT F.FlightId, F.Flight_Date, F.Departure, \
                F.Arrival, R.Airport_Src, R.Destination, R.Route_Code FROM Flight_Schedule AS F,\
                     Route AS R WHERE F.Route_id=R.RouteId AND F.Flight_Date='"
                + SelectedDate + "' AND R.Destination='" +
                SelectedDistination + "'", self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 2:
            SelectedDate = self.comboBox_FlightDateSelection_Q3.currentText()
            self.updateTable(
                "SELECT COUNT(FlightPrice) AS 'Number of Flights', sum(FlightPrice) AS 'TOTAL INCOME' FROM Transactions AS T \
                WHERE T.BookingDate = '" + SelectedDate + "'",
                self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 3:
            selectedFlightID = self.comboBox_AirportSources_Q4.currentText()
            self.updateTable(
                "SELECT F.FlightId, F.Flight_Date, F.Departure, F.Arrival, R.Airport_Src,\
                 R.Destination, R.Route_Code FROM Flight_Schedule AS F, Route AS R WHERE F.Route_id=R.RouteId \
                    AND R.Airport_Src = '" + selectedFlightID + "'",
                self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 4:
            self.updateTable(
                "SELECT Passengers.Name, Transactions.Passenger_id, Transactions.Flight_id,\
                             Transactions.FlightPrice, Transactions.Discount_id, Discounts.Title, \
                             Discounts.Amount, (FlightPrice - (FlightPrice*Amount)) AS 'price after discount'\
                             FROM Transactions INNER JOIN Discounts INNER JOIN Passengers\
                             ON Transactions.Discount_id=Discounts.DiscId \
                                AND Transactions.Passenger_id=Passengers.PassengerId\
                             ORDER BY Transactions.Discount_id",
                self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 5:
            Date1 = self.comboBox_Date1_Q6.currentText()
            Date2 = self.comboBox_Date2_Q6.currentText()
            self.updateTable(
                "SELECT T.BookingDate, T.FlightPrice, P.PassengerId, P.Name, P.Age, P.Address, P.Nationality\
                             FROM Transactions AS T, Passengers AS P\
                             WHERE T.Passenger_id=P.PassengerId \
                             AND T.BookingDate >= '" + Date1 +
                "' AND T.BookingDate <= '" + Date2 + "'\
                             ORDER BY T.BookingDate ",
                self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 6:
            self.updateTable(
                "SELECT * From Transactions\
                Where FlightPrice IN(Select max(FlightPrice) From Transactions)\
                Or FlightPrice IN(Select min(FlightPrice) From Transactions )\
                ", self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 7:
            self.updateTable(
                "Select * From Transactions T Join Passengers p on T.Passenger_id == p.PassengerId\
                GROUP BY T.Passenger_id\
                Having Count(T.Passenger_id) >= 3 AND Max(T.TransId)", self.tableWidget_PerformQuery)
        elif currentPerformTabIndex == 8:
            self.updateTable(
                "SELECT B.BranchId, B.Center, S.StateId, S.StateName\
                FROM Branch AS B LEFT OUTER JOIN State AS S\
                ON B.State_id = S.StateId", self.tableWidget_PerformQuery)

    def ClearQueryTable(self):
        self.tableWidget_PerformQuery.setRowCount(0)
        self.tableWidget_PerformQuery.setColumnCount(0)

    def loadFLights_Query1(self):
        Flights = self.DB_Query(
            "SELECT F.FlightId ,F.Flight_Date, F.Departure, R.Destination \
                FROM Flight_Schedule AS F, Route AS R WHERE F.Route_id=R.RouteId "
        )[0]
        for i in range(0, len(Flights)):
            Flights[i] = str(Flights[i])
        self.comboBox_Flights.addItems(Flights)

    def loadFlightDatesAndCountries_Query2(self):
        flightsDates = self.DB_Query(
            "SELECT Flight_Date FROM Flight_Schedule")[0]
        for i in range(0, len(flightsDates)):
            self.comboBox_FlightDateSelection.addItem(flightsDates[i][0])
        destinations = self.DB_Query(
            "SELECT DISTINCT R.Destination  FROM Flight_Schedule AS F, \
                Route AS R WHERE f.Route_id=r.RouteId")[0]
        for i in range(0, len(destinations)):
            self.comboBox_FlightDistinationSelection.addItem(
                destinations[i][0])

    def loadFlightDates_Query3(self):
        flightsDates = self.DB_Query(
            "SELECT DISTINCT BookingDate FROM Transactions")[0]
        for i in range(0, len(flightsDates)):
            self.comboBox_FlightDateSelection_Q3.addItem(flightsDates[i][0])

    def loadFlightsAirports_Query4(self):
        flightsAirports = self.DB_Query(
            "SELECT DISTINCT R.Airport_Src FROM Flight_Schedule AS F , Route AS R WHERE F.Route_id =R.RouteID "
        )
        for i in range(0, len(flightsAirports[0])):
            self.comboBox_AirportSources_Q4.addItem(
                str(flightsAirports[0][i][0]))

    def loadFlightDates_Query6(self):
        flightsDates = self.DB_Query(
            "SELECT DISTINCT BookingDate FROM Transactions")[0]
        for i in range(0, len(flightsDates)):
            self.comboBox_Date1_Q6.addItem(flightsDates[i][0])
            self.comboBox_Date2_Q6.addItem(flightsDates[i][0])


# Main Function
def main():
    App = QApplication(sys.argv)
    MainWindowVar = MainWindowClass()
    MainWindowVar.setStyleSheet(qdarktheme.load_stylesheet())
    MainWindowVar.show()
    App.exec_()


if __name__ == '__main__':
    main()
