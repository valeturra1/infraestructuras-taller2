import multiprocessing
import time

def cleanLine(line):
    cleaned_line = line.strip()
    return cleaned_line

def toUpperLine(line):
    upper_line = line.upper()
    return upper_line

def readFile(input ,colaTextoLeido):
    try:
        with open(input, 'r') as file:

            listaTemporal = list()

            for linea in file:
                listaTemporal.append(linea)
                if len(listaTemporal) >= CHUNK_SIZE:
                    colaTextoLeido.put(listaTemporal)
                    listaTemporal = list()
                    
            if len(listaTemporal) != 0:
                colaTextoLeido.put(listaTemporal)
                listaTemporal = list()
            colaTextoLeido.put(None)
    except FileNotFoundError: 
        print("Error: No se encontró el archivo texto_entrada")
        colaTextoLeido.put(None)

def cleanAndToUpperLines(colaTextoLeido, colaTextoTransformado):
    
    while(True):
        listaTemporal = list()

        listaEntrada = colaTextoLeido.get()
        if(listaEntrada == None):
            colaTextoTransformado.put(None)
            break
        else:
            for linea_leida in listaEntrada:

                lineaLimpiada = cleanLine(linea_leida)
                lineaMayusculasLimpiada = toUpperLine(lineaLimpiada)

                listaTemporal.append(lineaMayusculasLimpiada)
            colaTextoTransformado.put(listaTemporal)
            

def writeText(colaTextoTransformado, output):
    with open(output, 'w') as rFile:

        while(True):
            listaEntrada = colaTextoTransformado.get()

            if(listaEntrada == None):
                break
            else:
                for linea_en_mayusculas in listaEntrada:
                    rFile.write(linea_en_mayusculas + '\n')

if __name__ == '__main__':

    CHUNK_SIZE = 200_000

    LINEAS = [
        "     Morir de amor, que no es morir solo y en desamor. Morir de amor, que no es morir solo y en desamor.     ",
        "    y no tener un nombre a quien decirle.  y no tener un nombre a quien decirle.            ",
        "     AL VIENTO.    AL VIENTO.     AL VIENTO.    AL V  IENTO.   AL VIENTO.    AL VIENTO.       "
    ]
    
    NUM_LINEAS = 10_000_000

    with open("texto_entrada.txt", "w", encoding="utf-8") as archivo:
        for i in range(NUM_LINEAS):
            archivo.write(LINEAS[i % len(LINEAS)] + "\n")


    colaTextoLeido = multiprocessing.Queue()
    colaTextoTransformado = multiprocessing.Queue()

    input = 'texto_entrada.txt'
    output = 'texto_salida.txt'

    procesos = [None]*2

    procesos[0] = multiprocessing.Process(target=cleanAndToUpperLines, args=(colaTextoLeido, colaTextoTransformado))
    procesos[1] = multiprocessing.Process(target=writeText, args=(colaTextoTransformado, output))

    time1 = time.time()
    

    for i in range(2):
        procesos[i].start()

    readFile(input, colaTextoLeido)
    

    for j in range(2):
        procesos[j].join()

    

    time2 = time.time()

    tiempo_paralelo = time2 - time1

    print(f"Tiempo paralelo en segundos: {tiempo_paralelo} \n")
    print(f"Archivo guardado en {output}")