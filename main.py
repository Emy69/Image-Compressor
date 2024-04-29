import customtkinter as ctk
from tkinter import filedialog, ttk, N, S, E, W, font as tkFont, Label, IntVar
from PIL import Image
import os
import threading
import shutil
from concurrent.futures import ThreadPoolExecutor

def calcular_calidad(size_original):
    thresholds = [(2 * 1024 * 1024, 45), (1024 * 1024, 60), (512 * 1024, 70), (100 * 1024, 40)]
    for threshold, quality in thresholds:
        if size_original > threshold:
            return quality
    return 65

def get_save_options(formato, calidad):
    options = {
        'JPEG': {'quality': calidad},
        'JPG': {'quality': calidad},
        'WEBP': {'quality': calidad},
        'PNG': {'palette': Image.ADAPTIVE, 'colors': 256},
        'TIFF': {'compression': 'tiff_deflate'}
    }
    return options.get(formato, {})

def process_image(ruta, calidad):
    img = Image.open(ruta)
    formato = img.format
    nombre_archivo = os.path.basename(ruta)
    size_original = os.path.getsize(ruta)
    if size_original <= 100 * 1024:
        shutil.copy(ruta, f'optimized/{nombre_archivo}')
        return size_original, 0
    opciones_guardado = get_save_options(formato, calidad)
    ruta_optimizada = f'optimized/{nombre_archivo}'
    img.save(ruta_optimizada, formato, **opciones_guardado)
    size_nuevo = os.path.getsize(ruta_optimizada)
    if size_nuevo > size_original:
        shutil.copy(ruta, ruta_optimizada)
        size_nuevo = size_original
    return size_nuevo, 100 - (size_nuevo / size_original * 100)

def cargar_imagenes():
    # Abre un diálogo para seleccionar archivos de imagen con los tipos especificados
    rutas_imagenes = filedialog.askopenfilenames(title="Select images", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    
    # Si no se seleccionan imágenes, la función termina prematuramente
    if not rutas_imagenes:
        return

    # Establece el total de imágenes seleccionadas en una variable de control de la interfaz
    total_imagenes.set(len(rutas_imagenes))
    imagenes_completadas.set(0)  # Inicializa el contador de imágenes procesadas
    
    # Variables para acumular el tamaño original y optimizado de las imágenes
    total_size_original = 0
    total_size_optimized = 0
    
    # Asegura que el directorio 'optimized' existe para guardar las imágenes procesadas
    os.makedirs('optimized', exist_ok=True)
    
    # Función interna para procesar las imágenes
    def process_images():
        nonlocal total_size_original, total_size_optimized
        for index, ruta in enumerate(rutas_imagenes):
            calidad = calcular_calidad(os.path.getsize(ruta))
            size_nuevo, optimizacion = process_image(ruta, calidad)
            total_size_original += os.path.getsize(ruta)
            total_size_optimized += size_nuevo

            # Actualiza la interfaz de usuario después de cada imagen procesada
            root.after(0, lambda ruta=ruta, optimizacion=optimizacion: update_gui(ruta, optimizacion, index))

        # Al final del procesamiento, actualiza la interfaz con el resultado final
        if total_size_original > 0:
            total_optimizado_mb = (total_size_original - total_size_optimized) / (1024 * 1024)
            total_optimizado_percent = (total_size_original - total_size_optimized) / total_size_original * 100
            root.after(0, lambda: label_resultado.configure(text=f"Optimization completed: Saved {total_optimizado_mb:.2f} MB, {total_optimizado_percent:.2f}% total"))
        else:
            root.after(0, lambda: label_resultado.configure(text="No optimization needed"))

    # Función interna para actualizar la interfaz de usuario
    def update_gui(nombre_archivo, optimizacion, index):
        item = tree.insert("", "end", text=nombre_archivo, values=(f"{optimizacion:.2f}% optimized", "Completed"))
        imagenes_completadas.set(index + 1)
        tree.see(item)

    # Inicia un nuevo hilo para procesar las imágenes
    threading.Thread(target=process_images).start()


# Configuración de la ventana principal usando customtkinter
root = ctk.CTk()
root.title("Image Compressor")
root.geometry("800x600")

# Variables de estado
total_imagenes = IntVar(value=0)
imagenes_completadas = IntVar(value=0)

# Configurar fuentes
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)
root.option_add("*Font", default_font)

# Configurar grid
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.iconbitmap("resources/img/window.ico") 

# Widgets usando customtkinter
boton_cargar = ctk.CTkButton(root, text="Upload Images", command=cargar_imagenes)
boton_cargar.grid(row=0, column=0, pady=10, padx=10, sticky=N+E+W)

# Configurar Treeview para listado de archivos con estado de progreso
columns = ("Status", "Progress")
tree = ttk.Treeview(root, columns=columns, show="tree headings")
tree.column("#0", width=300)
tree.heading("#0", text="File")
tree.column("Status", width=150)
tree.heading("Status", text="Status")
tree.column("Progress", width=150)
tree.heading("Progress", text="Progress")
tree.grid(row=1, column=0, sticky=N+S+E+W)

label_total = ctk.CTkLabel(root, textvariable=imagenes_completadas)
label_total.grid(row=2, column=0, sticky=W+E, padx=10)

label_resultado = ctk.CTkLabel(root, text="")
label_resultado.grid(row=3, column=0, sticky=W+E, padx=10)

if __name__ == "__main__":
    # Iniciar GUI
    root.mainloop()
 