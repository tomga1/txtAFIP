import tkinter as tk
from tkinter import filedialog, messagebox

# Función para leer el archivo de texto
def leer_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            contenido = file.readlines()
        return contenido
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return None
    
def guardar_txt(filepath, contenido):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(contenido)
        messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

def transformar_contenido(contenido):
    contenido_transformado = ""
    for linea in contenido:
        regimen = linea[:3]  
        cuit_agente = linea[3:16].replace('-', '') 
        fecha = linea[16:26]  
        numero_comprobante = linea[26:42].strip() 
        importe_retencion = linea[42:].strip()  
        
        if len(cuit_agente) == 11 and fecha.count('/') == 2:
            nueva_linea = f"{regimen}{cuit_agente}{fecha}{numero_comprobante}{importe_retencion:>15}\n"
            contenido_transformado += nueva_linea
        else:
            messagebox.showwarning("Advertencia", f"Línea con formato incorrecto: {linea}")
            return
    return contenido_transformado

def convertir_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if filepath:
        contenido = leer_txt(filepath)
        if contenido is not None:
            # Transformar el contenido
            contenido_convertido = transformar_contenido(contenido)
            
            if contenido_convertido:
                # Solo se pide guardar el archivo después de la transformación
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
                if save_path:
                    guardar_txt(save_path, contenido_convertido)
            else:
                messagebox.showwarning("Advertencia", "El archivo no contiene datos válidos para transformar.")
        else:
            messagebox.showwarning("Advertencia", "No se pudo leer el archivo.")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

# Configuración de la interfaz gráfica con tkinter
root = tk.Tk()
root.title("Convertidor de Formato de Texto")
root.geometry("400x200")

label = tk.Label(root, text="Presiona el botón para seleccionar un archivo .txt y convertirlo.")
label.pack(pady=20)

boton_convertir = tk.Button(root, text="Seleccionar y Convertir Archivo", command=convertir_archivo)
boton_convertir.pack(pady=10)

root.mainloop()