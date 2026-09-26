import multiprocessing
import time


CHUNK_SIZE = 50000

def verification(lista, chunk_size):
    if(len(lista) >= chunk_size):
        return True
    else:
        return False

def readFile(input ,colaTextoLeido):
    try:
        with open(input, 'r') as file:

            listaTemporal = list()

            for linea in file:
                listaTemporal.append(linea)
                if verification(listaTemporal, CHUNK_SIZE):
                    colaTextoLeido.put(listaTemporal)
                    listaTemporal = list()
                    
            if len(listaTemporal) != 0:
                colaTextoLeido.put(listaTemporal)
                listaTemporal = list()
            colaTextoLeido.put(None)
    except FileNotFoundError: 
        print("Error: No se encontró el archivo texto_entrada")
        colaTextoLeido.put(None)

def cleanLines(colaTextoLeido, colaTextoLimpiado):
    
    while(True):
        listaTemporal = list()

        listaEntrada = colaTextoLeido.get()
        if(listaEntrada == None):
            colaTextoLimpiado.put(None)
            break
        else:
            for linea_leida in listaEntrada:
                listaTemporal.append(linea_leida.strip())
            colaTextoLimpiado.put(listaTemporal)
            
        


def toUpper(colaTextoLimpiado, colaTextoEnMayusculas):
    
    
    while(True):
        listaTemporal = list()
        listaEntrada = colaTextoLimpiado.get()

        if(listaEntrada == None):
            colaTextoEnMayusculas.put(None)
            break
        else:
            for linea_limpia in listaEntrada:
                listaTemporal.append(linea_limpia.upper())
            colaTextoEnMayusculas.put(listaTemporal)
            

def writeText(colaTextoEnMayusculas, output):
    with open(output, 'w') as rFile:

        while(True):
            listaEntrada = colaTextoEnMayusculas.get()

            if(listaEntrada == None):
                break
            else:
                for linea_en_mayusculas in listaEntrada:
                    rFile.write(linea_en_mayusculas + '\n')

if __name__ == '__main__':
    colaTextoLeido = multiprocessing.Queue()
    colaTextoLimpiado = multiprocessing.Queue()
    colaTextoEnMayusculas = multiprocessing.Queue()

    input = 'texto_entrada.txt'
    output = 'texto_salida.txt'

    procesos = [None]*3

    procesos[0] = multiprocessing.Process(target=cleanLines, args=(colaTextoLeido, colaTextoLimpiado))
    procesos[1] = multiprocessing.Process(target=toUpper, args=(colaTextoLimpiado, colaTextoEnMayusculas))
    procesos[2] = multiprocessing.Process(target=writeText, args=(colaTextoEnMayusculas, output))

    time1 = time.time()
    

    for i in range(3):
        procesos[i].start()

    readFile(input, colaTextoLeido)
    

    for j in range(3):
        procesos[j].join()

    

    time2 = time.time()

    tiempo_paralelo = time2 - time1

    print(f"Tiempo paralelo en segundos: {tiempo_paralelo} \n")
    print(f"Archivo guardado en {output}")