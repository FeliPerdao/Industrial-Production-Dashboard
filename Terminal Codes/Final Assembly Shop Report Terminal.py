import tkinter as tk
import pandas as pd
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Configuración de Google Sheets
CREDENTIALS_FILE = "agile-earth-450520-e9-53a2ec693488.json"
SPREADSHEET_NAME = "BaseDatosListaMateriales"

# Crear el archivo CSV si no existe
archivo_csv = "datos.csv"
if not os.path.exists(archivo_csv):
    df = pd.DataFrame(columns=["Fecha/Hora de Registro", "Operacion", "Operador/Maquina"])
    df.to_csv(archivo_csv, index=False)

# Variables globales
temporizador = None

def cargar_hoja(sheet_name, label):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(SPREADSHEET_NAME).worksheet(sheet_name)
        datos = sheet.col_values(1)
        label.config(text="\n".join(datos))
    except Exception as e:
        print(f"Error cargando {sheet_name}:", e)
        label.config(text=f"Error al cargar {sheet_name}.")
    ventana.after(120000, lambda: cargar_hoja(sheet_name, label))

def guardar_datos():
    global temporizador
    
    operacion = entrada_operacion.get()
    operador = entrada_operador.get()

    if not operacion:
        mostrar_mensaje("Ingrese una operación.", "red")
        return

    if not operador:
        operador = "Operador no asignado"

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(archivo_csv)
    nuevo_dato = pd.DataFrame({
        "Fecha/Hora de Registro": [fecha_hora],
        "Operacion": [operacion],
        "Operador/Maquina": [operador]
    })
    df = pd.concat([df, nuevo_dato], ignore_index=True)
    df.to_csv(archivo_csv, index=False)

    mostrar_mensaje("Datos guardados correctamente.", "green")
    limpiar_campos()

def borrar_ultimo():
    df = pd.read_csv(archivo_csv)
    if len(df) > 0:
        df = df[:-1]
        df.to_csv(archivo_csv, index=False)
        mostrar_mensaje("Último registro eliminado.", "orange")
    else:
        mostrar_mensaje("No hay registros para borrar.", "red")

def limpiar_campos():
    global temporizador
    entrada_operacion.delete(0, tk.END)
    entrada_operador.delete(0, tk.END)
    entrada_operacion.focus()
    if temporizador:
        ventana.after_cancel(temporizador)
        temporizador = None

def mostrar_mensaje(texto, color):
    mensaje_label.config(text=texto, fg=color)
    ventana.after(3000, lambda: mensaje_label.config(text=""))

def ir_a_operador(event):
    entrada_operador.focus()

def guardar_con_enter(event):
    guardar_datos()

# Configurar la interfaz gráfica
ventana = tk.Tk()
ventana.title("Formulario de Datos")
ventana.geometry("1500x1000")  # Aumentar el tamaño de la ventana
fuente_grande = ("Arial", 16)

# Etiqueta y entrada para "Operación"
tk.Label(ventana, text="Operación:", font=fuente_grande).grid(row=0, column=0, padx=10, pady=10)
entrada_operacion = tk.Entry(ventana, font=fuente_grande)
entrada_operacion.grid(row=0, column=1, padx=10, pady=10)
entrada_operacion.bind("<Return>", ir_a_operador)

# Etiqueta y entrada para "Operador/Máquina"
tk.Label(ventana, text="Operador/Máquina:", font=fuente_grande).grid(row=1, column=0, padx=10, pady=10)
entrada_operador = tk.Entry(ventana, font=fuente_grande)
entrada_operador.grid(row=1, column=1, padx=10, pady=10)
entrada_operador.bind("<Return>", guardar_con_enter)

# Botón para borrar el último registro
boton_borrar = tk.Button(ventana, text="Borrar Último", font=fuente_grande, command=borrar_ultimo, bg="red", fg="white")
boton_borrar.grid(row=2, column=0, columnspan=2, pady=10)

# Mensaje de estado
mensaje_label = tk.Label(ventana, text="", font=("Arial", 16, "italic"))
mensaje_label.grid(row=3, column=0, columnspan=2, pady=10)

# Cuadros de datos en horizontal
tk.Label(ventana, text="Órdenes Liberadas:", font=fuente_grande).grid(row=4, column=0, padx=10, pady=10, sticky="w")
ordenes_label = tk.Label(ventana, text="Cargando...", font=("Arial", 14), bg="lightgray", width=60, height=20, anchor="nw", justify="left")
ordenes_label.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(ventana, text="Terminados Hoy:", font=fuente_grande).grid(row=4, column=1, padx=10, pady=10, sticky="w")
terminados_hoy_label = tk.Label(ventana, text="Cargando...", font=("Arial", 14), bg="lightgray", width=60, height=20, anchor="nw", justify="left")
terminados_hoy_label.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

tk.Label(ventana, text="Terminados Ayer:", font=fuente_grande).grid(row=4, column=2, padx=10, pady=10, sticky="w")
terminados_ayer_label = tk.Label(ventana, text="Cargando...", font=("Arial", 14), bg="lightgray", width=60, height=20, anchor="nw", justify="left")
terminados_ayer_label.grid(row=5, column=2, padx=10, pady=10, sticky="nsew")

# Configurar expansión de columnas y filas
ventana.rowconfigure(5, weight=1)
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.columnconfigure(2, weight=1)

# Cargar datos de Google Sheets
cargar_hoja("OrdenesLiberadas", ordenes_label)
cargar_hoja("TerminadosHoy", terminados_hoy_label)
cargar_hoja("TerminadosAyer", terminados_ayer_label)

entrada_operacion.focus()
ventana.mainloop()
