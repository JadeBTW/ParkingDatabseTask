#Wilson Warrington | 2023
#Parking Database GUI

# Import all required libraries
import PySimpleGUI as sg
import os
from datetime import *
import sqlite3 as db
import DBhandler as dbh

os.system("cls||clear") # Automatically clears the terminal

cn = db.connect("parking.db")
cr = cn.cursor()
cr.executescript("PRAGMA foreign_keys = ON") #enabling table linking
cn.commit()
cr.close()

dbh.dbsetup(cn)
print(dbh.getAll(cn, "customers"))

spaces = []
disabled = ["No", "Yes"]
studentOrStaff = ["Student", "Staff"]

passwordFile = open("password.txt", "r") # Get password
password = passwordFile.readline()

# Grab spaces from text file and append to list spaces
for line in open("spaces.txt", "r"):
    line = line.strip()
    spaces.append(line)

# Define layout
def inputFormCustomer():
    layout = [
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="date_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="time_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text(("Parking Database Input Form"), size=(200, 1), font=("Arial", 20), justification="c", text_color="black", background_color="#EEE5DE")],
        [sg.Text(("Please populate all fields and click submit and exit when done."), size=(200, 1), justification="c", background_color="#EEE5DE", text_color="black")],
        [sg.Text("Forename", size =(20, 1), text_color="black", background_color="#EEE5DE"), sg.InputText((), size=(20, 1), key="inputForename", enable_events=True)],
        [sg.Text("Surname", size =(20, 1), text_color="black", background_color="#EEE5DE"), sg.InputText((), size=(20, 1), key="inputSurname", enable_events=True)],
        [sg.Text("Student or Staff", size =(20, 1), text_color="black", background_color="#EEE5DE"), sg.Combo((["Student", "Staff"]), size=(20, 1), key="type", enable_events=True)],
        [sg.Text("Disabled?", size=(20, 1), text_color="black", background_color="#EEE5DE"), sg.Combo((["No", "Yes"]), enable_events=True, key="disabled?", size=(20, 1), readonly=True)],
        [sg.Col([[sg.Button("Submit and Exit", button_color="black", disabled=True)]], justification="center", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Exit", button_color="black")]], justification="center", background_color="#EEE5DE")],
    ]

    # Create the window
    window = sg.Window("Parking Database Form", layout, background_color="#EEE5DE", size=(500, 500), resizable=False)

    # Main loop
    while True:
        event, values = window.read(timeout=1000) # Update window every second
        if event == sg.WIN_CLOSED or event == "Exit": # Close the window if user clicks "x" icon
            break
        if event == "inputForename" or event == "inputSurname" or event == "type" or event == "disabled?": # Check to see if all fields have been populated
            input1_value = values["inputForename"]
            input2_value = values["inputSurname"]
            input3_value = values["type"]
            input4_value = values["disabled?"]
            is_submit_disabled = not (input1_value and input2_value and input3_value and input4_value)
            window["Submit and Exit"].update(disabled=is_submit_disabled) # Enable button once all fields are populated
        if event == "Submit and Exit": # Print all data collected
            forename = values["inputForename"]
            surname = values["inputSurname"]
            disabled = values["disabled?"]
            if disabled == "No":
                disabled = 0
            else:
                disabled = 1
            studentOrStaff = values["type"]
            print("-" * 30)
            print("Forname: " + forename)
            print("Surname: " + surname)
            print("Type: " + studentOrStaff)
            print("Disabled?: " + str(disabled))
            print("-" * 30)
            break # Breaks out of the loop and closes the window
        current_time = datetime.now().strftime("%H:%M:%S") # Get current time to display
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)
    window.close()


def viewData():
    toprow = ['Cust. ID', 'Surname', 'Forename', 'Disabled?', "Type"]
    rows = dbh.getAll(cn, "customers")

    tbl1 = sg.Table(values=rows, headings=toprow, auto_size_columns=True, display_row_numbers=False, justification='center', key='-TABLE-', selected_row_colors='red on yellow', enable_events=True, expand_x=True, expand_y=True, enable_click_events=True)
    layout = [
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="date_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="time_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text(("View Data"), size=(200, 1), font=("Arial", 20), justification="c", text_color="black", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Exit", button_color="black")]], justification="center", background_color="#EEE5DE")],
        [tbl1]
    ]

    window = sg.Window("View Data", layout, background_color="#EEE5DE", size=(500, 500), resizable=False)

    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


def debugMenu():
    layout = [
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="date_display", justification="left", background_color="#00FF7F", text_color="black")],
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="time_display", justification="left", background_color="#00FF7F", text_color="black")],
        [sg.Text(("Debug Menu"), size=(200, 1), font=("Arial", 20), justification="c", text_color="black", background_color="#00FF7F")],
        [sg.Col([[sg.Button("Debug Spaces", button_color="black")]], justification="center", background_color="#00FF7F")],
        [sg.Col([[sg.Button("Debug Password", button_color="black")]], justification="center", background_color="#00FF7F")],
        [sg.Col([[sg.Button("Exit Debug Menu", button_color="black")]], justification="center", background_color="#00FF7F")],
    ]

    window = sg.Window("Debug Menu", layout, size=(500, 500), background_color="#00FF7F", resizable=False)
    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Exit Debug Menu":
            print(">>> Exited Debugging Mode")
            break
        if event == "Debug Spaces":
            print(">>> Spaces Debugging Started")
            sg.Print(spaces)
        if event == "Debug Password":
            print(">>> Password Debugging Started")
            sg.Print("Password is: " + password)

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


def passwordPrompt():
    layout = [
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="date_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="time_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text(("Please Enter Administrator Password"), size=(200, 1), font=("Arial", 20), justification="c", text_color="black", background_color="#EEE5DE")],
        [sg.InputText((), size=(20, 1), key="inputPassword", pad=(175, 0), password_char="*")],
        [sg.Col([[sg.Button("Submit", button_color="black", key="submitPassword")]], justification="center", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Cancel", button_color="black")]], justification="center", background_color="#EEE5DE")],
    ]

    window = sg.Window("Enter Password", layout, size=(500, 500), background_color="#EEE5DE", resizable=False)
    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "submitPassword":
            passwordEntered = values["inputPassword"]
            if passwordEntered == password:
                print(">>> Started Debugging Mode")
                debugMenu()
                break
            else:
                break
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()

def settings():
    layout = [
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="date_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="time_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text(("Database Settings"), size=(200, 1), font=("Arial", 20), justification="c", text_color="black", background_color="#EEE5DE")],
        [sg.Text("Background Colour", size =(20, 1), text_color="black", background_color="#EEE5DE"), sg.InputText((), size=(20, 1), key="inputColourBackground", enable_events=True)],
        [sg.Col([[sg.Button("Save and Exit", button_color="black")]], justification="center", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Exit", button_color="black")]], justification="center", background_color="#EEE5DE")],
    ]

    window = sg.Window("Settings", layout, size=(500, 500), background_color="#EEE5DE", resizable=False)
    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Save and Exit":
            global colourBackground
            colourBackground = values["inputColourBackground"]
            break

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


def main():
    layout = [
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="date_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text("", size=(20, 1), font=("Arial", 10), key="time_display", justification="left", background_color="#EEE5DE", text_color="black")],
        [sg.Text(("Parking Database Main Menu"), size=(200, 1), font=("Arial", 20), justification="c", text_color="black", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Add Customer", pad=(20, 10), button_color="black", key="addCustomer", size=(15, 3), font=("Arial", 10)), sg.Button("View Data", pad=(20, 10), button_color="black", key="viewData", size=(15, 3), font=("Arial", 10))]], justification="center", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Settings", pad=(20, 10), button_color="black", key="settings", size=(15, 3), font=("Arial", 10)), sg.Button("Debug Menu", pad=(20, 10), button_color="black", key="debugMenu", size=(15, 3), font=("Arial", 10))]], justification="center", background_color="#EEE5DE")],
        [sg.Col([[sg.Button("Exit", pad=(20, 10), button_color="black", key="exit", size=(15, 3), font=("Arial", 10))]], justification="center", background_color="#EEE5DE")],
    ]

    window = sg.Window("Main Menu", layout, size=(500, 500), background_color="#EEE5DE", resizable=False)
    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "exit":
            print(">>> Database Closed")
            break
        if event == "addCustomer":
            inputFormCustomer()
        if event == "viewData":
            viewData()
        if event == "settings":
            settings()
        if event == "debugMenu":
            passwordPrompt()

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


if __name__ == "__main__":
    main()