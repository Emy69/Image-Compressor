import customtkinter as ctk
from tkinter import ttk, N, S, E, W, filedialog
import os
import threading
from utils.image_utils import calcular_calidad, process_image


class ImageOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor")
        self.root.geometry("800x600")
        self.root.iconbitmap("resources/img/window.ico")

        # Aseguramos que customtkinter use el modo "System"
        ctk.set_appearance_mode("System")

        self._setup_widgets()
        self._configure_layout()

        # Variables para seguimiento
        self.total_imagenes = 0
        self.imagenes_completadas = 0

    def _setup_widgets(self):
        """Configura los widgets de la interfaz."""
        # Botón para cargar imágenes
        self.boton_cargar = ctk.CTkButton(
            self.root, 
            text="Upload Images", 
            command=self.cargar_imagenes
        )
        self.boton_cargar.grid(row=0, column=0, pady=10, padx=10, sticky=N+E+W)

        # Definimos las columnas para el Treeview
        self.tree = ttk.Treeview(self.root, columns=("Status", "Progress"), show="headings")
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=150, anchor="center")
        self.tree.heading("Progress", text="Progress")
        self.tree.column("Progress", width=100, anchor="center")
        self.tree.grid(row=1, column=0, sticky=N+S+E+W, padx=10)

        # Barra de progreso global
        self.progress_var = ctk.DoubleVar(value=0.0)
        self.progress_bar = ctk.CTkProgressBar(self.root, variable=self.progress_var, width=300)
        self.progress_bar.grid(row=2, column=0, pady=10)

        # Etiqueta para información resumida
        self.label_info = ctk.CTkLabel(self.root, text="")
        self.label_info.grid(row=3, column=0, sticky=W+E, padx=10)

    def _configure_layout(self):
        """Configura el layout de la ventana."""
        # Expandir la fila 1 (Treeview) para que crezca con la ventana
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def cargar_imagenes(self):
        """Abre un cuadro de diálogo para seleccionar imágenes y lanza el hilo de procesamiento."""
        rutas_imagenes = filedialog.askopenfilenames(
            title="Select images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff")]
        )
        if not rutas_imagenes:
            return

        self.total_imagenes = len(rutas_imagenes)
        self.imagenes_completadas = 0
        self.label_info.configure(text="Processing images...")
        self.tree.delete(*self.tree.get_children())  # Limpia la tabla antes de llenar

        # Creamos la carpeta "optimized" si no existe
        os.makedirs("optimized", exist_ok=True)

        # Insertamos filas en el Treeview (una por cada imagen).
        for ruta in rutas_imagenes:
            nombre_archivo = os.path.basename(ruta)
            self.tree.insert(
                "", 
                "end", 
                iid=ruta,  # Usamos la ruta como identificador único
                values=("Pending", "0.00%")
            )

        # Lanzamos el proceso en segundo plano
        threading.Thread(
            target=self._process_images, 
            args=(rutas_imagenes,), 
            daemon=True
        ).start()

    def _process_images(self, rutas_imagenes):
        """Procesa las imágenes en segundo plano."""
        total_size_original = 0
        total_size_optimized = 0

        for index, ruta in enumerate(rutas_imagenes, start=1):
            try:
                calidad = calcular_calidad(os.path.getsize(ruta))
                size_nuevo, optimizacion = process_image(ruta, calidad)

                total_size_original += os.path.getsize(ruta)
                total_size_optimized += size_nuevo

                self.imagenes_completadas += 1
                progreso = (self.imagenes_completadas / self.total_imagenes) * 100

                # Actualizamos la GUI
                self._update_gui(ruta, optimizacion, progreso)

            except Exception as e:
                # Si hay algún error, lo reflejamos en el Treeview
                self.root.after(0, lambda r=ruta: self.tree.set(r, "Status", "Error"))

        # Al terminar, mostramos resultado de optimización
        if total_size_original > 0:
            total_optimizado_mb = (total_size_original - total_size_optimized) / (1024 * 1024)
            total_optimizado_percent = (total_size_original - total_size_optimized) / total_size_original * 100
            texto = f"Optimization completed: Saved {total_optimizado_mb:.2f} MB ({total_optimizado_percent:.2f}%)."
        else:
            texto = "No optimization was applied (files may have been too small)."

        self.root.after(0, lambda: self.label_info.configure(text=texto))

    def _update_gui(self, ruta, optimizacion, progreso):
        """Actualiza el estado del Treeview y la barra de progreso global."""
        self.root.after(0, lambda: [
            self.tree.set(ruta, "Status", "Completed"),
            self.tree.set(ruta, "Progress", f"{optimizacion:.2f}%"),
            self.progress_var.set(progreso / 100.0),
        ])
