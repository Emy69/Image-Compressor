from PIL import Image
import os
import shutil

def calcular_calidad(size_original):
    """
    Devuelve la calidad recomendada (0-100) basándose en umbrales de tamaño.
    """
    thresholds = [
        (2 * 1024 * 1024, 45),  # mayor a 2 MB
        (1024 * 1024, 60),      # mayor a 1 MB
        (512 * 1024, 70),       # mayor a 512 KB
        (100 * 1024, 40)        # mayor a 100 KB
    ]
    for threshold, quality in thresholds:
        if size_original > threshold:
            return quality
    return 65  # valor por defecto


def get_save_options(formato, calidad):
    """
    Devuelve las opciones adecuadas para la función .save() de PIL 
    según el formato y la calidad indicados.
    """
    # Forzamos mayúsculas para estandarizar
    formato_mayus = formato.upper()
    options = {
        'JPEG': {'quality': calidad, 'optimize': True},
        'JPG': {'quality': calidad, 'optimize': True},
        'WEBP': {'quality': calidad},
        'PNG': {'optimize': True},  # Se puede usar 'compress_level': 6
        'TIFF': {'compression': 'tiff_deflate'}
    }
    return options.get(formato_mayus, {'quality': calidad, 'optimize': True})


def process_image(ruta, calidad):
    """
    Procesa la imagen en 'ruta' con la calidad dada.
    Si el resultado es mayor que el original, se copia el original.
    
    Devuelve una tupla (size_nuevo, optimizacion),
    donde 'size_nuevo' es el tamaño final en bytes
    y 'optimizacion' es el % de mejora.
    """
    img = Image.open(ruta)
    formato = img.format or 'JPEG'  # si no se detecta formato, por defecto 'JPEG'
    nombre_archivo = os.path.basename(ruta)
    size_original = os.path.getsize(ruta)

    # Si la imagen es muy pequeña (< 100 KB), solo la copiamos.
    if size_original <= 100 * 1024:
        shutil.copy(ruta, f'optimized/{nombre_archivo}')
        return size_original, 0.0

    # Opciones de guardado según formato y calidad
    opciones_guardado = get_save_options(formato, calidad)
    ruta_optimizada = f'optimized/{nombre_archivo}'

    # Guardar la imagen con las opciones definidas
    img.save(ruta_optimizada, formato, **opciones_guardado)

    size_nuevo = os.path.getsize(ruta_optimizada)

    # Si no se mejoró (o es peor), se deja la original
    if size_nuevo > size_original:
        shutil.copy(ruta, ruta_optimizada)
        size_nuevo = size_original

    optimizacion = 100 - (size_nuevo / size_original * 100)
    return size_nuevo, optimizacion
