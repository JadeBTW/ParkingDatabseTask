import sqlite3 as db
import PySimpleGUI as gui
import datetime as t

cn = db.connect("parking.db")
cr = cn.cursor()
cr.executescript("PRAGMA foreign_keys = ON") #enabling table linking
cn.commit()
cr.close()

def termchk(): #module for determining year and school term requures year on operating maxchine to be set accurately
    print(f'[INFO] running term calculations')
    winterst = t.date(2000, 12, 29)
    wintered = t.date(2000, 1, 1)
    feb = t.date(2000, 2, 14)
    eastr = t.date(2000, 4, 6)
    may = t.date(2000, 5, 29)
    summer = t.date(2000, 7, 9)
    sept = t.date(2000, 10, 25)
    date = str(t.date.today())
    year = date[2:][:2]
    day = date.split("-")
    day = t.date(2000, int(day[1]), int(day[2]))
    print(f'[INFO] Year int: {year}')
    print(f'[INFO] Date int: {day}')
    if summer < day <= sept:
        term = 1
    elif sept < day <= winterst:
        term = 2
    elif wintered <= day <= feb:
        term = 3
    elif feb < day <= eastr:
        term = 4
    elif eastr < day <= may:
        term = 5
    elif may < day <= summer:
        term = 6
    else:
        print(f'[WARN] date somehow outside acceptable range')
    print(f'[INFO] term integer: {term}')
    return(year, term)

def spacesetup(conn): #create table if it doesnt exist
    cr = conn.cursor()
    command = f'''CREATE TABLE IF NOT EXISTS spaces (
    SpaceID text PRIMARY KEY,
    Occupied integer)'''
    print("[INFO] building spaces table")
    cr.executescript(command)
    cr.close()
    conn.commit()

def spacefill(conn): #if spaces table is empty, build data from spaces.txt
    print("[INFO] setting up table")
    cur = conn.cursor()
    cur.execute("""SELECT * from spaces;""")
    dat = cur.fetchall()
    if dat == []:
        file = open("spaces.txt").readlines()
        print("[INFO] empty Table, creating data")
        for i in file:
            tmp = i.strip("\n")
            cur.execute("INSERT INTO spaces ('SpaceID','Occupied') VALUES (?,'0')", (tmp,))
        conn.commit()
    else: print("[INFO] spaces table already assembled: skipping")
    cur.close()

def carsetup(conn): #sets up table of registered cars
    print("[INFO] building cars table")
    cur = conn.cursor()
    command = """CREATE TABLE IF NOT EXISTS cars (
    Reg text PRIMARY KEY,
    Make text NOT NULL,
    Model text NOT NULL)"""
    cur.execute(command)
    conn.commit()
    cur.close()

def carfill(conn): #populate car table if empty for testing
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars")
    dat = cur.fetchall()
    if dat == []: 
        print("[INFO] empty Table, creating placeholder data")
        data = [("BF9500","Ford","Model T"),("KPX607J","Ford","Escort"),("RK60WCE","Mercedes Benz","A Class"),("TXS105","Morris","Minor 0.9"),("S417FVE","Caterham","Seven"),("416 EB 67","Bugatti","Royal"),("L923TGN","Lada","Riva"),("YAR112S","Leyland","Mini"),("FY65POA","Great Wall","Steed"),("GWM 0RA","Funky","CAT"),("VU16OBD","Microcar","M.Gu"),("LGK708Y","MP Lafer","Sports"),("JPX63D","Volvo","131"),("RKC337","Riley","RM Series 2.5")]
        cur.executemany("INSERT INTO cars (Reg,Make,Model) VALUES (?,?,?)", data)
        conn.commit()
    else: print("[INFO] cars table already assembled: skipping")
    cur.close()

def termpricesetup(conn): #sets up term pricing table
    print("[INFO] setting up prices sheet")
    cur = conn.cursor()
    command = """CREATE TABLE IF NOT EXISTS termprice (
    Term integer PRIMARY KEY,
    StaffPr real,
    StudentPr real)"""
    cur.execute(command)
    conn.commit()
    cur.close()

def termpricefill(conn): #populate price table with deafults if empty
    cur = conn.cursor()
    cur.execute("SELECT * FROM termprice")
    dat = cur.fetchall()
    if dat == []: 
        print("[INFO] empty Table, creating data")
        datarry = [(1,50,75),(2,50,75),(3,50,75),(4,50,75),(5,50,75),(6,50,75)]
        cur.executemany("INSERT INTO termprice (Term,StaffPr,StudentPr) VALUES (?,?,?)", datarry)
        conn.commit()
    else: print("[INFO] price table already assembled: skipping")
    cur.close()

def customersetup(conn): #setup customer table
    print("[INFO] setting up customer sheet")
    cur = conn.cursor()
    command = """CREATE TABLE IF NOT EXISTS customers (
    CustomerID text PRIMARY KEY,
    CustSur text,
    CustFor text,
    CustDis text,
    CustTyp text)"""
    cur.execute(command)
    conn.commit()
    cur.close()

def customersfill(conn): #populate customer table if empty with existing data
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    dat = cur.fetchall()
    if dat == []: 
        year, term = termchk()
        term = 2
        print("[INFO] empty Table, creating data")
        dataray = [("wood","jakob","p",0),("calderbank","edward","p",0),("norris","benjamin","p",0),("shelly","luke","p",1,),("townsend","aled","p",0),("weston","joe","p",0),("murphy","tom","s",0),("lewis","michelle","s",0),("tillet","bradley","s",1),("forbes","carl","s",0),("hemmings","jade","p",0),("oyawaye","ayo","p",0),("radcliffe","oscar","p",0),("sutton","tommy","p",0)]
        for i in dataray:
            studid = f'{year}{term}{i[0][:3]}{i[1][:3]}{i[2]}'
            print(f'[INFO] built studentid: {studid}')
            cur.execute("INSERT INTO customers VALUES (?,?,?,?,?)", (studid, i[0], i[1], i[3], i[2]))
        conn.commit()
    else: print("[INFO] customers table already assembled: skipping")
    cur.close()

def ownersetup(conn): #setup table defining relationships between cars and users
    print("[INFO] setting up ownership sheet")
    cur = conn.cursor()
    try:
        command = """CREATE TABLE IF NOT EXISTS ownership (
        CustomerID text,
        Reg text,
        FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
        FOREIGN KEY (Reg) REFERENCES cars(Reg))"""
        cur.execute(command)
        conn.commit()
    except db.IntegrityError:
        print(f'[WARN] oopsies something happened building foreign keys')
    cur.close()

def ownerfill(conn): #populate ownership table if empty for testing
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownership")
    dat = cur.fetchall()
    if dat == []: 
        print("[INFO] empty Table, creating placeholder data")
        data = [("BF9500","232woojakp"),("KPX607J","232caledwp"),("RK60WCE","232norbenp"),("TXS105","232shelukp"),("S417FVE","232towalep"),("416 EB 67","232wesjoep"),("L923TGN","232murtoms"),("YAR112S","232lewmics"),("FY65POA","232tilbras"),("GWM 0RA","232forcars"),("VU16OBD","232hemjadp"),("LGK708Y","232oyaayop"),("JPX63D","232radoscp"),("RKC337","232suttomp")]
        cur.executemany("INSERT INTO ownership (Reg,CustomerID) VALUES (?,?)", data)
        conn.commit()
    else: print("[INFO] ownership table already assembled: skipping")
    cur.close()

def permitssetup(conn): #setup permit sheet and create foreign data linking structure
    print("[INFO] setting up permits sheet")
    cur = conn.cursor()
    command = """CREATE TABLE IF NOT EXISTS permits (
    PermitNo text PRIMARY KEY,
    CustomerID text,
    Term integer,
    SpaceID text,
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (Term) REFERENCES termprice(Term),
    FOREIGN KEY (SpaceID) REFERENCES spaces(SpaceID))"""
    cur.execute(command)
    conn.commit()
    cur.close()

def permitsfill(conn): #populate permit sheet with deafults if empty
    cur = conn.cursor()
    cur.execute("SELECT * FROM permits")
    dat = cur.fetchall()
    if dat == []: 
        yr = 23
        print("[INFO] empty Table, creating placeholder data")
        data = [("232woojakp",2,"NMA001"),("232caledwp",2,"NMA002"),("232norbenp",2,"NMA003"),("232shelukp",2,"NMD001"),("232towalep",2,"NMA004"),("232wesjoep",2,"NMA007"),("232murtoms",2,"NMA008"),("232lewmics",2,"NMA009"),("232tilbras",2,"NMA010"),("232forcars",2,"NMA011"),("232hemjadp",2,"NMA012"),("232oyaayop",2,"NMA013"),("232radoscp",2,"NMA014"),("232suttomp",2,"NMA015")]
        for i in data:
            permit = f'{i[0]}{yr}{i[1]}{i[2]}'
            print(f'[INFO] Inserting data {permit, i[0], i[1], i[2]}')
            cur.execute("INSERT INTO permits (PermitNo,CustomerID,Term,SpaceID) VALUES (?,?,?,?)", (permit, i[0], i[1], i[2],))
        conn.commit()
    else: print("[INFO] permits table already assembled: skipping")
    cur.close()

def dbsetup(conn):
    spacesetup(cn)
    spacefill(cn)
    carsetup(cn)
    carfill(cn)
    termpricesetup(cn)
    termpricefill(cn)
    customersetup(cn)
    customersfill(cn)
    ownersetup(cn)
    ownerfill(cn)
    permitssetup(cn)
    permitsfill(cn)

dbsetup(cn) #initialise the databse