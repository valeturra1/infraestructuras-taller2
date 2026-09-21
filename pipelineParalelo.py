import multiprocessing
import time

def readFile(input ,colaTextoLeido):
    try:
        with open(input, 'r') as file:
            texto = file.read()
            texto_en_lineas = texto.splitlines()

            for linea in texto_en_lineas:
                colaTextoLeido.put(linea)
            colaTextoLeido.put(None)
    except FileNotFoundError: 
        print("Error: No se encontró el archivo texto_entrada")

def cleanLines(colaTextoLeido, colaTextoLimpiado):
    while(True):
        linea_leida = colaTextoLeido.get()
        if(linea_leida == None):
            colaTextoLimpiado.put(None)
            break
        else:
            colaTextoLimpiado.put(linea_leida.strip())
        


def toUpper(colaTextoLimpiado, colaTextoEnMayusculas):

    while(True):
        linea_limpia = colaTextoLimpiado.get()

        if(linea_limpia == None):
            colaTextoEnMayusculas.put(None)
            break
        else:
            colaTextoEnMayusculas.put(linea_limpia.upper())

def writeText(colaTextoEnMayusculas, output):
    with open(output, 'w') as rFile:

        while(True):
            linea_en_mayusculas = colaTextoEnMayusculas.get()

            if(linea_en_mayusculas == None):
                break
            else:
                rFile.write(linea_en_mayusculas + '\n')

if __name__ == '__main__':
    colaTextoLeido = multiprocessing.Queue()
    colaTextoLimpiado = multiprocessing.Queue()
    colaTextoEnMayusculas = multiprocessing.Queue()

    input = 'texto_entrada.txt'
    output = 'texto_salida.txt'

    procesos = [None]*4

    procesos[0] = multiprocessing.Process(target=readFile, args=(input, colaTextoLeido))
    procesos[1] = multiprocessing.Process(target=cleanLines, args=(colaTextoLeido, colaTextoLimpiado))
    procesos[2] = multiprocessing.Process(target=toUpper, args=(colaTextoLimpiado, colaTextoEnMayusculas))
    procesos[3] = multiprocessing.Process(target=writeText, args=(colaTextoEnMayusculas, output))

    time1 = time.time()
    for i in range(4):
        procesos[i].start()

    for j in range(4):
        procesos[j].join()

    time2 = time.time()

    tiempo_paralelo = time2 - time1

    print(f"Tiempo paralelo en segundos: {tiempo_paralelo} \n")
    print(f"Archivo guardado en {output}")