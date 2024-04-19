from cx_Freeze import setup, Executable

# Define additional options
options = {
    'build_exe': {
        'packages': [
            "os", "tkinter", "requests", "bs4", "threading",
            "customtkinter", "urllib3", "sys", "json"
        ],
        'excludes': [
            "matplotlib", "numpy", "aiohttp", "aiosignal",
            "altgraph", "ffmpeg", "Flask", "youtube_dl", "SQLAlchemy", "pytube"
        ],
        'include_files': [
            'resources/'  
        ],
        'optimize': 2,
    }
}

# Setup configuration for the executable
setup(
    name="Image Compressor",
    version="2024.04.19",
    description="Image Compressor.",
    options=options,
    executables=[Executable("main.py", base="Win32GUI", icon="resources/img/icon.ico")]
)
