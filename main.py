from gui.app import ImageOptimizerApp
import customtkinter as ctk

def main():
    ctk.set_default_color_theme("blue")  # Puedes cambiar "blue" por "dark-blue" o "green"
    root = ctk.CTk()
    app = ImageOptimizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
