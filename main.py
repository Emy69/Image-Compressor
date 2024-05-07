from gui.app import ImageOptimizerApp
import customtkinter as ctk

def main():
    root = ctk.CTk()
    app = ImageOptimizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()