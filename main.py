import customtkinter as ctk
from tkinter import filedialog, ttk, N, S, E, W, font as tkFont
from tkinter import IntVar, StringVar
from PIL import Image
import os
import threading
import shutil

def calcular_calidad(size_original):
    if size_original > 2 * 1024 * 1024:
        return 45
    elif size_original > 1024 * 1024:
        return 60
    elif size_original > 512 * 1024:
        return 70
    elif size_original > 100 * 1024:
        return 40
    else:
        return 65

def cargar_imagenes():
    rutas_imagenes = filedialog.askopenfilenames(title="Select images", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if rutas_imagenes:
        total_imagenes.set(len(rutas_imagenes))
        imagenes_completadas.set(0)
        total_size_original = 0
        total_size_optimized = 0

        # Asegurarse de que la carpeta 'optimized' exista
        os.makedirs('optimized', exist_ok=True)

        def process_images():
            nonlocal total_size_original, total_size_optimized
            for index, ruta in enumerate(rutas_imagenes):
                img = Image.open(ruta)
                formato = img.format
                nombre_archivo = os.path.basename(ruta)
                size_original = os.path.getsize(ruta)
                total_size_original += size_original
                calidad = calcular_calidad(size_original)

                if size_original <= 100 * 1024:  # Si es menor de 100 KB, copiar en lugar de optimizar
                    shutil.copy(ruta, f'optimized/{nombre_archivo}')
                    size_nuevo = size_original
                else:
                    opciones_guardado = {}
                    if formato in ['JPEG', 'JPG', 'WEBP']:
                        opciones_guardado['quality'] = calidad
                    elif formato == 'PNG':
                        img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
                    elif formato == 'TIFF':
                        opciones_guardado['compression'] = 'tiff_deflate'

                    ruta_optimizada = f'optimized/{nombre_archivo}'
                    img.save(ruta_optimizada, formato, **opciones_guardado)

                    size_nuevo = os.path.getsize(ruta_optimizada)
                    if size_nuevo > size_original:
                        shutil.copy(ruta, ruta_optimizada)
                        size_nuevo = size_original

                total_size_optimized += size_nuevo
                optimizacion = 100 - (size_nuevo / size_original * 100)

                def update_gui():
                    tree.insert("", "end", text=nombre_archivo, values=(f"{optimizacion:.2f}% optimized", "Completed"))
                    imagenes_completadas.set(index + 1)

                root.after(0, update_gui)

            total_optimizado_mb = (total_size_original - total_size_optimized) / (1024 * 1024)
            total_optimizado_percent = (total_size_original - total_size_optimized) / total_size_original * 100

            def update_final_results():
                label_resultado.configure(text=f"Optimization completed: Saved {total_optimizado_mb:.2f} MB, {total_optimizado_percent:.2f}% total")

            root.after(0, update_final_results)

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
