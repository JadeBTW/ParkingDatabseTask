#Parking Database GUI (utilising custom sql backend library)

colourBackground = "#6fa074"
colourText = "#000000"
colourHighlight = "#eeeeee"
typeFont = "Arial"

# Import all required libraries
import PySimpleGUI as sg
import os
from datetime import *
import sqlite3 as db
import DBhandler as dbh
import json as js

os.system("cls||clear") # Automatically clears the terminal

directory = __file__.strip("DB_GUI.py")
print(f'[INFO] Python execution enviroment directory variable detected as {directory}')

def sqlTerminal():
    global cn
    sg.Print("Sqlite v3 Direct Databse Terminal v0.1")
    sg.Print("="*30)
    sg.Print()
    while 1 == 1:
        dat = sg.PopupGetText(">>>")
        if dat == "EXIT":
            sg.Print("[INFO] Exiting Terminal Environment")
            break
        sg.Print(f'[INFO] Executing sqlite statement: {dat}')
        sg.Print(f'[INFO] Sql handler returned data: {dbh.sqlInterface(cn, dat)}')

class Settings():
    def __init__(self) -> None:
        global directory
        global colourBackground
        global colourText
        global colourHighlight
        global typeFont
        self.directory = f'{directory}settings.json'
        json = open(self.directory).read()
        self.settings = js.loads(json)
        print(f'[INFO] Loaded settings information from {self.directory}')
        print(self.settings)
        colourBackground = self.settings["BgColour"]
        colourText = self.settings["TextColour"]
        colourHighlight = self.settings["HighlightColour"]
        typeFont = self.settings["Font"]
        pass

    def settingsUpdate(self,Dat,Target):
        global colourBackground
        global colourText
        global typeFont
        global colourHighlight
        self.settings[str(Target)] = str(Dat)
        colourBackground = self.settings["BgColour"]
        colourText = self.settings["TextColour"]
        colourHighlight = self.settings["HighlightColour"]
        typeFont = self.settings["Font"]
        file = open(self.directory, "w")
        json = js.dumps(self.settings)
        print(json)
        file.write(json)
        file.close()
        print(open(self.directory).read())

Settings.__init__(Settings)
cn = db.connect("parking.db")
cr = cn.cursor()
cr.executescript("PRAGMA foreign_keys = ON") #enabling table linking
cn.commit()
cr.close()

dbh.dbsetup(cn)

spaces = []
disabled = ["No", "Yes"]
studentOrStaff = ["Student", "Staff"]

passwordFile = open(f'{directory}password.txt', "r") # Get password
password = passwordFile.readline()

# Grab spaces from text file and append to list spaces
for line in open(f'{directory}spaces.txt', "r"):
    line = line.strip()
    spaces.append(line)

# Define layout
def inputFormCustomer():
    global colourBackground
    global colourText
    global typeFont
    global colourHighlight
    layout = [
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="date_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="time_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text(("Parking Database Input Form"), size=(200, 1), font=(typeFont, 20), justification="c", text_color=colourText, background_color=colourBackground)],
        [sg.Text(("Please populate all fields and click submit and exit when done."), size=(200, 1), justification="c", background_color=colourBackground, text_color=colourText)],
        [sg.Text("Forename", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.InputText((), size=(20, 1), key="inputForename", enable_events=True)],
        [sg.Text("Surname", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.InputText((), size=(20, 1), key="inputSurname", enable_events=True)],
        [sg.Text("Student or Staff", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.Combo((["Student", "Staff"]), size=(20, 1), key="type", enable_events=True)],
        [sg.Text("Disabled?", size=(20, 1), text_color=colourText, background_color=colourBackground), sg.Combo((["No", "Yes"]), enable_events=True, key="disabled?", size=(20, 1), readonly=True)],
        [sg.Col([[sg.Button("Submit and Exit", button_color=colourText, disabled=True)]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Exit", button_color=colourText)]], justification="center", background_color=colourBackground)],
    ]

    # Create the window
    window = sg.Window("Parking Database Form", layout, background_color=colourBackground, size=(500, 500), resizable=False)

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
    global colourBackground
    global colourText
    global typeFont
    global colourHighlight

    toprow = ['Cust. ID', 'Surname', 'Forename', 'Disabled?', "Type"]
    rows = dbh.getAll(cn, "customers")

    tbl1 = sg.Table(values=rows, headings=toprow, auto_size_columns=True, display_row_numbers=False, justification='center', key='-TABLE-', selected_row_colors='red on yellow', enable_events=True, expand_x=True, expand_y=True, enable_click_events=True)
    layout = [
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="date_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="time_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text(("View Data"), size=(200, 1), font=(typeFont, 20), justification="c", text_color=colourText, background_color=colourBackground)],
        [sg.Col([[sg.Button("Exit", button_color=colourText)]], justification="center", background_color=colourBackground)],
        [tbl1]
    ]

    window = sg.Window("View Data", layout, background_color=colourBackground, size=(500, 500), resizable=False)

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
    global colourBackground
    global colourText
    global typeFont
    global colourHighlight

    layout = [
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="date_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="time_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text(("Debug Menu"), size=(200, 1), font=(typeFont, 20), justification="c", text_color=colourText, background_color=colourBackground)],
        [sg.Col([[sg.Button("Debug Spaces", button_color=colourText)]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Debug Password", button_color=colourText)]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Direct Sql Terminal", button_color=colourText)]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Exit Debug Menu", button_color=colourText)]], justification="center", background_color=colourBackground)],
    ]

    window = sg.Window("Debug Menu", layout, size=(500, 500), background_color=colourBackground, resizable=False)
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
        if event == "Direct Sql Terminal":
            sqlTerminal()

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


def passwordPrompt():
    global colourBackground
    global colourText
    global typeFont
    global colourHighlight

    layout = [
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="date_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="time_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text(("Please Enter Administrator Password"), size=(200, 1), font=(typeFont, 20), justification="c", text_color=colourText, background_color=colourBackground)],
        [sg.InputText((), size=(20, 1), key="inputPassword", pad=(175, 0), password_char="*")],
        [sg.Col([[sg.Button("Submit", button_color=colourText, key="submitPassword")]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Cancel", button_color=colourText)]], justification="center", background_color=colourBackground)],
    ]

    window = sg.Window("Enter Password", layout, size=(500, 500), background_color=colourBackground, resizable=False)
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

def settings(settings):
    global colourBackground
    global colourText
    global typeFont
    global colourHighlight

    layout = [
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="date_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="time_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text(("Database Settings"), size=(200, 1), font=(typeFont, 20), justification="c", text_color=colourText, background_color=colourBackground)],
        [sg.Text("Background Colour", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.InputText((), size=(20, 1), key="inputColourBackground", enable_events=True)],
        [sg.Text("Highlight Colour", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.InputText((), size=(20, 1), key="inputColourHighlight", enable_events=True)],
        [sg.Text("Text Colour", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.InputText((), size=(20, 1), key="inputColourText", enable_events=True)],
        [sg.Text("Font", size =(20, 1), text_color=colourText, background_color=colourBackground), sg.InputText((), size=(20, 1), key="inputFont", enable_events=True)],
        [sg.Col([[sg.Button("Save and Exit", button_color=colourText)]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Exit", button_color=colourText)]], justification="center", background_color=colourBackground)],
    ]

    window = sg.Window("Settings", layout, size=(500, 500), background_color=colourBackground, resizable=False)
    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Save and Exit":
            if values["inputColourBackground"] != "": settings.settingsUpdate(settings, values["inputColourBackground"], "BgColour")
            if values["inputColourHighlight"] != "": settings.settingsUpdate(settings, values["inputColourHighlight"], "HighlightColour")
            if values["inputColourText"] != "": settings.settingsUpdate(settings, values["inputColourText"], "TextColour")
            if values["inputFont"] != "": settings.settingsUpdate(settings, values["inputFont"], "Font")
            break

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


def main():
    global colourBackground
    global colourText
    global typeFont
    global colourHighlight

    layout = [
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="date_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text("", size=(20, 1), font=(typeFont, 10), key="time_display", justification="left", background_color=colourBackground, text_color=colourText)],
        [sg.Text(("Parking Database Main Menu"), size=(200, 1), font=(typeFont, 20), justification="c", text_color=colourText, background_color=colourBackground)],
        [sg.Col([[sg.Button("Add Customer", pad=(20, 10), button_color=colourText, key="addCustomer", size=(15, 3), font=(typeFont, 10)), sg.Button("View Data", pad=(20, 10), button_color=colourText, key="viewData", size=(15, 3), font=(typeFont, 10))]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Settings", pad=(20, 10), button_color=colourText, key="settings", size=(15, 3), font=(typeFont, 10)), sg.Button("Debug Menu", pad=(20, 10), button_color=colourText, key="debugMenu", size=(15, 3), font=(typeFont, 10))]], justification="center", background_color=colourBackground)],
        [sg.Col([[sg.Button("Exit", pad=(20, 10), button_color=colourText, key="exit", size=(15, 3), font=(typeFont, 10))]], justification="center", background_color=colourBackground)],
    ]

    window = sg.Window("Main Menu", layout, size=(500, 500), background_color=colourBackground, resizable=False)
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
            settings(Settings)
            pass
        if event == "debugMenu":
            passwordPrompt()

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()
        window["time_display"].update(current_time)
        window["date_display"].update(current_date)

    window.close()


if __name__ == "__main__":
    main()