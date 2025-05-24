# Industrial-Production-Dashboard

A production system fed by job task completion signs from operators, returning a real-time dashboard of operations.

## Objective

The goal of this production system is to provide:

- A real-time dashboard.
- A view of the partial results of the current day.
- An overview of the previous day.
- A visualization of the waiting line for the next finishing projects in the Assembly Shop.

## System Functionality

### **Welding and Machining Shop Terminal**

This terminal interacts with the respective application, running a Python script with the Tkinter module for interactivity.

- Updates a CSV file in Google Drive.
- Feeds a dashboard displaying the construction phases of the final product.

### **Assembly Shop Terminal**

This terminal has the same functionality but with additional features:

- Displays the current day's progress in real-time.
- Shows an overview of the previous day.
- Lists remaining projects ready for assembly to help operators prepare for upcoming projects.

## **Technologies Used**

- **Python** – Main programming language.
- **Tkinter** – GUI (Graphical User Interface) library for building the application window.
- **Pandas** – Used for handling and saving data in CSV format.
- **gspread** – Google Sheets API library for Python.
- **OAuth 2.0** – Authentication method for Google Sheets API.

## **App Images**

### Assembly Shop Terminal Screen
![Assembly Shop Terminal Screen](App%20Screenshots/Assembly%20Shop%20Terminal%20Screen.png)
### Welding/Machining Shop Terminal Screen
![Welding Terminal Screen](App%20Screenshots/Welding%20Terminal%20Screen.png)
### Google Sheets Proyect Dashboard
![Google Sheets Proyect Dashboard](App%20Screenshots/Proyect%20Progress%20Dashboard.png)
