import tkinter as tk
import pandas as pd
import os
from datetime import datetime

# Crear el archivo CSV si no existe
archivo_csv = "datos.csv"
if not os.path.exists(archivo_csv):
    df = pd.DataFrame(columns=["Fecha/Hora de Registro", "Operacion", "Operador/Maquina"])
    df.to_csv(archivo_csv, index=False)

# Variables globales
mensaje_temporizador = None  # Temporizador para borrar mensaje
registro_temporizador = None  # Temporizador para guardar después de 10 segundos
botones_nombres = [
    "ALFREDO", "BRIAN", "CRISTIAN",
    "ALAN", "FERNANDO", "MAXIMILIANO", "JONATAN",
    "M44", "M38", "M33", "M06", "M36"
]

# Función para guardar los datos
def guardar_datos():
    global registro_temporizador
    if registro_temporizador:
        ventana.after_cancel(registro_temporizador)  # Cancelar temporizador si el usuario completa antes de 10s

    operacion = entrada_operacion.get().strip()
    operador = entrada_operador.get().strip()

    if not operacion:
        operacion = "SIN REGISTRO"
    if not operador:
        operador = "SIN REGISTRO"

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df = pd.read_csv(archivo_csv)
    nuevo_dato = pd.DataFrame({
        "Fecha/Hora de Registro": [fecha_hora],
        "Operacion": [operacion],
        "Operador/Maquina": [operador]
    })

    df = pd.concat([df, nuevo_dato], ignore_index=True)
    df.to_csv(archivo_csv, index=False)

    mostrar_mensaje("Registro guardado con éxito.", "green")
    limpiar_campos()

# Función para limpiar campos y resetear el temporizador
def limpiar_campos():
    entrada_operacion.delete(0, tk.END)
    entrada_operador.delete(0, tk.END)
    entrada_operacion.focus()

# Función para mostrar un mensaje temporal en la ventana
def mostrar_mensaje(texto, color):
    global mensaje_temporizador
    mensaje_label.config(text=texto, fg=color)
    if mensaje_temporizador:
        ventana.after_cancel(mensaje_temporizador)  # Cancelar cualquier temporizador previo
    mensaje_temporizador = ventana.after(5000, lambda: mensaje_label.config(text=""))  # Borrar mensaje en 5 seg

# Función para manejar la entrada del primer campo
def manejar_operacion(event):
    global registro_temporizador
    entrada = entrada_operacion.get().strip()
    
    # Si el texto ingresado coincide con un botón, moverlo al campo 2
    if entrada in botones_nombres:
        entrada_operador.delete(0, tk.END)
        entrada_operador.insert(0, entrada)
        entrada_operacion.delete(0, tk.END)
        entrada_operacion.focus()
        return
    
    # Si el campo 2 está vacío, mover el cursor allí
    if entrada_operador.get() == "":
        entrada_operador.focus()
    else:
        guardar_datos()
    
    # Iniciar temporizador para auto-guardar después de 10s si no se completa el registro
    if registro_temporizador:
        ventana.after_cancel(registro_temporizador)
    registro_temporizador = ventana.after(5000, guardar_datos)

# Función para manejar los botones
def boton_presionado(nombre):
    if entrada_operacion.get().strip():
        entrada_operador.delete(0, tk.END)
        entrada_operador.insert(0, nombre)
        guardar_datos()
    else:
        entrada_operador.delete(0, tk.END)
        entrada_operador.insert(0, nombre)
        entrada_operacion.focus()

# Configurar la interfaz gráfica
ventana = tk.Tk()
ventana.title("Formulario de Datos")
ventana.geometry("900x400")  # Tamaño fijo
fuente_grande = ("Arial", 16)

# Etiqueta y entrada para "Operación"
tk.Label(ventana, text="Operación:", font=fuente_grande).grid(row=0, column=0, padx=10, pady=10)
entrada_operacion = tk.Entry(ventana, font=fuente_grande)
entrada_operacion.grid(row=0, column=1, padx=10, pady=10)
entrada_operacion.bind("<Return>", manejar_operacion)

# Etiqueta y entrada para "Operador/Máquina"
tk.Label(ventana, text="Operador/Máquina:", font=fuente_grande).grid(row=1, column=0, padx=10, pady=10)
entrada_operador = tk.Entry(ventana, font=fuente_grande)
entrada_operador.grid(row=1, column=1, padx=10, pady=10)
entrada_operador.bind("<Return>", lambda event: guardar_datos())

# Botones en tres filas
botones_filas = [
    ["ALFREDO", "BRIAN", "CRISTIAN"],
    ["ALAN", "FERNANDO", "MAXIMILIANO", "JONATAN"],
    ["M44", "M38", "M33", "M06", "M36"]
]

fila_inicio = 2
for i, fila in enumerate(botones_filas):
    for j, nombre in enumerate(fila):
        tk.Button(ventana, text=nombre, font=fuente_grande, command=lambda n=nombre: boton_presionado(n)).grid(row=fila_inicio + i, column=j, padx=5, pady=5)

# Mensaje de éxito
mensaje_label = tk.Label(ventana, text="", font=("Arial", 16, "bold"))
mensaje_label.grid(row=fila_inicio + len(botones_filas), column=0, columnspan=4, pady=20)

# Enfocar el primer campo al iniciar
entrada_operacion.focus()

ventana.mainloop()
