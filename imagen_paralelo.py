from PIL import Image
import os
import time
import multiprocessing

def convertir_a_gris(ruta_imagen):
    """Convierte una imagen a escala de grises."""
    try:
        imagen = Image.open(ruta_imagen)
        imagen_gris = imagen.convert('L')  # 'L' representa escala de grises
        nombre_archivo, extension = os.path.splitext(ruta_imagen)
        ruta_gris = nombre_archivo + "_gris" + extension
        imagen_gris.save(ruta_gris)
        print(f"Imagen convertida: {ruta_imagen} -> {ruta_gris}")

    except FileNotFoundError:
        print(f"Error: No se encontró la imagen {ruta_imagen}")

    except Exception as e:
        print(f"Error al procesar {ruta_imagen}: {e}")

def procesar_imagenes(lista_imagenes, inicio, fin):
    """Procesa una lista de imágenes."""
    lista_porcion = lista_imagenes[inicio:fin]

    for ruta_imagen in lista_porcion:
        convertir_a_gris(ruta_imagen)

if __name__ == '__main__':
    directorio_imagenes = r"C:\Users\777\Downloads\ejercicio1"
    lista_imagenes = [os.path.join(directorio_imagenes, f) for f in os.listdir(directorio_imagenes) if os.path.isfile(os.path.join(directorio_imagenes, f))]

    num_procesos = 6
    cantidad_img = len(lista_imagenes)
    tamaño_porcion = cantidad_img // num_procesos

    procesos = []

    inicio = time.time()

    for i in range(num_procesos):
        inicio_porcion = i * tamaño_porcion
        fin_porcion = (i+1) * tamaño_porcion if i < num_procesos -1 else cantidad_img

        p = multiprocessing.Process(target=procesar_imagenes, args=(lista_imagenes, inicio_porcion, fin_porcion))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()
    
    fin = time.time()

    print(f"Tiempo total de procesamiento paralelo: {fin - inicio:.2f} segundos")
