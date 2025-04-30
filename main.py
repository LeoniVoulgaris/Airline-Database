import sqlite3
from prettytable import from_db_cursor
conn = sqlite3.connect("airline.db")
curs = conn.cursor()

#creating tables 
curs.execute("""
CREATE TABLE IF NOT EXISTS PILOTS(
    PilotName VARCHAR(50),
    PilotID INT,
    LocationID INT,
    PRIMARY KEY (PilotID),
    FOREIGN KEY (LocationID) REFERENCES LOCATIONS (LocationID)
);
""")

curs.execute("""
CREATE TABLE IF NOT EXISTS FLIGHTS(
    FlightID INT,
    PilotID INT,
    AircraftID INT,
    Departure DATETIME,
    PRIMARY KEY (FlightID),
    FOREIGN KEY (PilotID) REFERENCES PILOTS(PilotID),
    FOREIGN KEY (AircraftID) REFERENCES AIRCRAFT (AircraftID)
);
""" )


curs.execute("""
CREATE TABLE IF NOT EXISTS AIRCRAFT(
    AircraftID INT,
    FlightID INT,
    DestinationID INT,
    LocationID INT,
    PRIMARY KEY (AircraftID),
    FOREIGN KEY (FlightID) REFERENCES FLIGHTS (FlightID),
    FOREIGN KEY (DestinationID) REFERENCES DESTINATIONS (DestinationID),
    FOREIGN KEY (LocationID) REFERENCES LOCATIONS (LocationID)
);
""" )

curs.execute("""
CREATE TABLE IF NOT EXISTS DESTINATIONS(
    DestinationNAME VARCHAR(50),
    FlightID INT,
    DestinationID INT,
    PRIMARY KEY (DestinationID)
    FOREIGN KEY (FlightID) REFERENCES FLIGHTS (FlightID)
);
""")

curs.execute("""
CREATE TABLE IF NOT EXISTS LOCATIONS(
    LocationID INT,
    LocationName VARCHAR(50),
    PilotID INT,
    AircraftID INT,
    PRIMARY KEY (LocationID),
    FOREIGN KEY (PilotID) REFERENCES PILOTS (PilotID),
    FOREIGN KEY (AircraftID) REFERENCES AIRCRAFT (AircraftID)
);  
""")




#Initial menu
def menu():
    global y
    print("What would you like to do: " )
    print("1. Add data \n2. Remove data \n3. View table \n4. Add column \n5. Remove column \n6. Rename table \n7. Rename comlumn \n8. Remove table \n9. Edit data \n10. Search for data \n11. Summary \n12. Exit")
    y = int(input("Select an option:"))



#Gives options to continue or quit after a task is done
def askifdone():
    print("1. Main menu \n2.Exit")
    x = input("Select an option:")
    if x == '1':
        program()
    elif x == '2':
        quit()


#The search function is the only function that has a different menu therefore if it is selected the program will take a different path
def ifsearch():
    if y == 10:
        print("What data would you like to look for: ")
        print("1.Flights \n2.Pilots \n3.Destinations \n4.Departure times")
        z = int(input("Select an option: "))
        if z == 1:
            pilotname = input("Who is the pilot on the flight: ")
            try:                                                      #Ensuring the pilot exists and giving an error if the flight is not found
              pilotid = curs.execute("SELECT PilotID FROM PILOTS WHERE PilotName = ?", (pilotname,)).fetchone()
              result = curs.execute("SELECT FlightID FROM FLIGHTS WHERE PilotID = ?",(pilotid[0],)).fetchone()
              result_str = '\n'.join(map(str, result))
              print("The FlightID is: ",result_str)
              askifdone()
            except:
                print("No flight found")
                askifdone()
        elif z == 2:
            pilotlocation = input("Where is the pilot you are looking for:")
            try:                                                      #Ensuring the location exists and giving an error if the pilot is not found
               locationid = curs.execute("SELECT LocationID FROM LOCATIONS WHERE LocationName = ?", (pilotlocation,)).fetchone()
               result = curs.execute("SELECT PilotName FROM PILOTS WHERE LocationID = ?",(locationid[0],)).fetchall()
               result_str = ', '.join(map(str, result))
               print("The Pilots are: \n: ",result_str)
               askifdone()
            except:
                print("No pilot found")
                askifdone()
        elif z == 3:
            flightid = input("What is the FlightID of the flight: ")
            try:                                                      #Ensuring the flightid exists and giving an error if the destination is not found
               result = curs.execute("SELECT DestinationName FROM DESTINATIONS WHERE FlightID = ?", (flightid,)).fetchone()
               result_str = ', '.join(map(str, result))
               print("The Destination is: ",result_str)
               askifdone()
            except:
                print("No destination found")
                askifdone()
        elif z == 4:
            flightid = input("What is the FlightID:") 
            try:                                                       ##Ensuring the flightid exists and giving an error if the departure time is not found
               departure = curs.execute("SELECT Departure FROM FLIGHTS WHERE FlightID = ?", (flightid,)).fetchone()
               result_str = ', '.join(map(str, departure))
               print("The departure time of the flight is: ",result_str)
               askifdone()
            except:
                print("No departure time found")
                askifdone()
        else:
            return






#Functions which continues the program after the initial menu
def cont():
    global x
    print("Select a table from below by entering the appropriate integer:")
    print("1. PILOTS \n2. FLIGHTS \n3. AIRCRAFT \n4. DESTINATIONS \n5. LOCATIONS")
    x = int(input("Select a table:"))


#Function which keeps track of the current table chosen by the user
def currenttable(x):
    global selection
    if x == 1:
        selection = "PILOTS"
        return selection
    elif x == 2:
        selection = "FLIGHTS"
        return selection
    elif x == 3:
        selection = "AIRCRAFT"
        return selection
    elif x == 4:
        selection = "DESTINATIONS"
        return selection
    elif x == 5:
        selection = "LOCATIONS"
        return selection 





def addpilot():
    pilotname = input("PilotName:")
    pilotid = int(input("PilotID:"))
    locationid = int(input("LocationID:"))
    if pilotname.isalpha() and len(pilotname) < 50 and isinstance(pilotid, int) and isinstance(pilotid, int): #Ensure all values are of the appropriate type
        curs.execute("INSERT INTO PILOTS(PilotName, PilotID, LocationID) VALUES (?,?,?)",(pilotname,pilotid,locationid))
        curs.execute("SELECT * FROM " + selection)
        x = from_db_cursor(curs)
        print(x)
        askifdone()
    else:
        print("Make sure PilotName is under 50 charachters and PilotID and LocationID are integers")
        addpilot()

def addflight():
    flightid = int(input("FlightID:"))
    pilotid = int(input("PilotID:"))
    aircraftid = int(input("AircraftID:"))
    departure = int(input("Departure:"))
    if isinstance(flightid, int) and isinstance(pilotid, int) and isinstance(aircraftid, int) and isinstance(departure, int) : #Ensure all values are of the appropriate type
        curs.execute("INSERT INTO FLIGHTS(FlightID, PilotID, AircraftID, Departure) VALUES (?,?,?,?)",(flightid,pilotid,aircraftid, departure))
        curs.execute("SELECT * FROM " + selection)
        x = from_db_cursor(curs)
        print(x)   
        askifdone()
    else:
        print("Make sure all values are integers")
        addflight()

def addaircraft():
    aircraftid = int(input("AircraftID:"))
    flightid = int(input("FlightID:"))
    destinationid = int(input("DestinationID:"))
    locationid = int(input("LocationID:"))
    if isinstance(aircraftid, int) and isinstance(flightid, int) and isinstance(destinationid, int) and isinstance(locationid, int): #Ensure all values are of the appropriate type
        curs.execute("INSERT INTO AIRCRAFT(AircraftID ,FlightID,DestinationID, LocationID) VALUES (?,?,?,?)",(aircraftid,flightid,destinationid,locationid))
        curs.execute("SELECT * FROM " + selection)
        x = from_db_cursor(curs)
        print(x)  
        askifdone()
    else:
        print("Make sure all values are integers")
        addaircraft()

def adddestination():
    destinationame = input("DestinationName: ")
    flightid = int(input("FlightID: "))
    destinationid = int(input("DestinationID: "))
    if destinationame.isalpha() and len(destinationame) < 50 and isinstance(flightid, int) and isinstance(destinationid, int) : #Ensure all values are of the appropriate type
        curs.execute("INSERT INTO DESTINATIONS(DestinationName, FlightID, DestinationID) VALUES (?,?,?)",(destinationame,flightid,destinationid))
        curs.execute("SELECT * FROM " + selection)
        x = from_db_cursor(curs)
        print(x) 
        askifdone()
    else:
        print("Make sure DestinationName is less than 50 characters and FlightID and DestinationID are integers")
        adddestination()

def addlocation():
    locationid = int(input("LocationID:"))
    locationame = input("LocationName:")
    pilotid = int(input("PilotID:"))
    aircraftid = int(input("AircraftID:"))
    if locationame.isalpha() and len(locationame) < 50 and isinstance(locationid, int) and isinstance(pilotid, int) and isinstance(aircraftid, int) : #Ensure all values are of the appropriate type
        curs.execute("INSERT INTO LOCATIONS(LocationID ,LocationName,PilotID, AircraftID) VALUES (?,?,?,?)",(locationid,locationame,pilotid,aircraftid))
        curs.execute("SELECT * FROM " + selection)
        x = from_db_cursor(curs)
        print(x)  
        askifdone()
    else:
        print("Make sure LocationName is less than 50 characters and LocationID, AircraftID and PilotID are integers")

def remove():
    print("Select a column from",selection,"to remove data from:")
    data = curs.execute("PRAGMA table_info('" + selection + "')")
    columns = []
    for i, column_info in enumerate(data.fetchall(), start=1): #Appends the names of the columns in the table into the list columns in order to use the index together with the user input to select a column
        column_name = column_info[1]
        columns.append(column_name)
        print(f"{i}. {column_name}")
    chosen_index = int(input("Select a column:")) -1 
    chosen_column = columns[chosen_index]
    datatoremove = input("What would you like to remove:")
    curs.execute("DELETE FROM " + selection + " WHERE " + chosen_column + " = ?", (datatoremove,))
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    askifdone()

def view():
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    askifdone()

def renamecolumn():
    print("Select a column from",selection,"to rename:")
    data = curs.execute("PRAGMA table_info('" + selection + "')")
    columns = []
    for i, column_info in enumerate(data.fetchall(), start=1): #Appends the names of the columns in the table into the list columns in order to use the index together with the user input to select a column
        column_name = column_info[1]
        columns.append(column_name)
        print(f"{i}. {column_name}")
    chosen_index = int(input("Select a column:")) -1 
    chosen_column = columns[chosen_index] 
    newname = input("What would you to rename this column to:")
    curs.execute("ALTER TABLE " + selection + " RENAME COLUMN " + chosen_column + " TO " + newname + "" )
    columns = curs.execute("PRAGMA column_info('" + selection + "')").fetchall()
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    print(columns)
    askifdone()

def addcolumn(): 
    newcolumn = input("What would you to call this new column:")
    type = input("What type will the new column have:")
    curs.execute("ALTER TABLE " + selection + " ADD COLUMN " + newcolumn + "" + type  )
    columns = curs.execute("PRAGMA column_info('" + selection + "')").fetchall()
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    print(columns)
    askifdone()

def removecolumn(): 
    print("Select a column from",selection,"to remove:")
    data = curs.execute("PRAGMA table_info('" + selection + "')")
    columns = []
    for i, column_info in enumerate(data.fetchall(), start=1): #Appends the names of the columns in the table into the list columns in order to use the index together with the user input to select a column
        column_name = column_info[1]
        columns.append(column_name)
        print(f"{i}. {column_name}")
    chosen_index = int(input("Select a column:")) -1 
    chosen_column = columns[chosen_index]
    curs.execute("ALTER TABLE " + selection + " DROP COLUMN " + chosen_column + "")
    columns = curs.execute("PRAGMA column_info('" + selection + "')").fetchall()
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    print(columns)
    askifdone()

def removetable():
    curs.execute("ALTER TABLE" + selection + "DROP TABLE")
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    askifdone()

def renametable():
    newname = input("What would you to rename this table to:")
    curs.execute("ALTER TABLE " + selection + " RENAME "  + newname + "" )
    columns = curs.execute("PRAGMA column_info('" + selection + "')").fetchall()
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    print(columns)
    askifdone()

def edit():
    print("Select a column from",selection,"to edit:")
    data = curs.execute("PRAGMA table_info('" + selection + "')")
    columns = []
    for i, column_info in enumerate(data.fetchall(), start=1): #Appends the names of the columns in the table into the list columns in order to use the index together with the user input to select a column
        column_name = column_info[1]
        columns.append(column_name)
        print(f"{i}. {column_name}")
    chosen_index = int(input("Select a column:")) -1 
    chosen_column = columns[chosen_index]
    datatoremove = input("What would you like to edit:")
    datatoadd = input("What would you like to change it to: ")
    curs.execute("DELETE FROM " + selection + " WHERE " + chosen_column + " = ?", (datatoremove,))
    curs.execute("INSERT INTO " + selection + "(" + chosen_column + ") VALUES (?)",(datatoadd,))
    curs.execute("SELECT * FROM " + selection)
    x = from_db_cursor(curs)
    print(x)
    askifdone()


def summary():
    if y == 11:
        flights = curs.execute("SELECT COUNT(FlightID) FROM FLIGHTS").fetchall()
        pilots = curs.execute("SELECT COUNT(PilotName) FROM PILOTS").fetchall()
        destinations = curs.execute("SELECT COUNT(DestinationID) FROM DESTINATIONS").fetchall()
        flights_str = '\n'.join(map(str, flights))
        pilots_str = '\n'.join(map(str, pilots))
        destinations_str = '\n'.join(map(str, destinations))
        print("Number of pilots in database: ",pilots_str,"\nNumber of flights in database: ",flights_str,"/nNumber of destination in database: ",destinations_str,)
        askifdone()
    else:
        return











#Function which decides which function to call depending on the user's input
def decision():
    if y == 1 and x == 1:
        addpilot()
    elif y == 1 and x == 2:
        addflight()
    elif y == 1 and x == 3:
        addaircraft()
    elif y == 1 and x == 4:
        adddestination()
    elif y == 1 and x == 5:
        addlocation()
    elif y == 2:
        remove()
    elif y == 3:
        view()
    elif y == 4:
        addcolumn()
    elif y == 5:
        removecolumn()
    elif y == 6:
        renametable()
    elif y == 7:
        renamecolumn()
    elif y == 8:
        removetable()
    elif y == 9:
        edit()
    elif y == 10:
        pass
    elif y == 11:
        pass









#Function which contains the order inn which the functions are called to make the program work, if the user chooses option 12 the program terminates 
def program():
    while True:
        menu()
        if y == 12:  
            break
        ifsearch()
        summary()
        cont()
        currenttable(x)
        decision()
program()

conn.commit()
conn.close()