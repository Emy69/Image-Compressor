import customtkinter as ctk
from tkinter import ttk, N, S, E, W, font as tkFont, IntVar, filedialog
import os
import threading
from utils.image_utils import calcular_calidad, get_save_options, process_image

class ImageOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Image Compressor")
        self.root.geometry("800x600")
        self.root.iconbitmap("resources/img/window.ico")

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.root.option_add("*Font", default_font)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.boton_cargar = ctk.CTkButton(self.root, text="Upload Images", command=self.cargar_imagenes)
        self.boton_cargar.grid(row=0, column=0, pady=10, padx=10, sticky=N+E+W)

        columns = ("Status", "Progress")
        self.tree = ttk.Treeview(self.root, columns=columns, show="tree headings")
        self.tree.column("#0", width=300)
        self.tree.heading("#0", text="File")
        self.tree.column("Status", width=150)
        self.tree.heading("Status", text="Status")
        self.tree.column("Progress", width=150)
        self.tree.heading("Progress", text="Progress")
        self.tree.grid(row=1, column=0, sticky=N+S+E+W)

        self.label_total = ctk.CTkLabel(self.root, textvariable=IntVar(value=0))
        self.label_total.grid(row=2, column=0, sticky=W+E, padx=10)

        self.label_resultado = ctk.CTkLabel(self.root, text="")
        self.label_resultado.grid(row=3, column=0, sticky=W+E, padx=10)

    def cargar_imagenes(self):
        rutas_imagenes = filedialog.askopenfilenames(title="Select images", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if not rutas_imagenes:
            return

        self.total_imagenes = IntVar(value=len(rutas_imagenes))
        self.imagenes_completadas = IntVar(value=0)
        os.makedirs('optimized', exist_ok=True)

        def process_images():
            total_size_original = 0
            total_size_optimized = 0
            for index, ruta in enumerate(rutas_imagenes):
                calidad = calcular_calidad(os.path.getsize(ruta))
                size_nuevo, optimizacion = process_image(ruta, calidad)
                total_size_original += os.path.getsize(ruta)
                total_size_optimized += size_nuevo

                self.root.after(0, lambda ruta=ruta, optimizacion=optimizacion: self.update_gui(ruta, optimizacion, index))

            if total_size_original > 0:
                total_optimizado_mb = (total_size_original - total_size_optimized) / (1024 * 1024)
                total_optimizado_percent = (total_size_original - total_size_optimized) / total_size_original * 100
                self.root.after(0, lambda: self.label_resultado.configure(text=f"Optimization completed: Saved {total_optimizado_mb:.2f} MB, {total_optimizado_percent:.2f}% total"))
            else:
                self.root.after(0, lambda: self.label_resultado.configure(text="No optimization needed"))

        threading.Thread(target=process_images).start()

    def update_gui(self, nombre_archivo, optimizacion, index):
        item = self.tree.insert("", "end", text=nombre_archivo, values=(f"{optimizacion:.2f}% optimized", "Completed"))
        self.imagenes_completadas.set(index + 1)
        self.tree.see(item)
