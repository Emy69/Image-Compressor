from PIL import Image
import os
import shutil

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
