### Clases
from models.carrera import carrera as carreras
from models.rut import rut as ruts
### Librerias internas útiles
from func.utils import indexador,indexadorSimple
### Librerias externas útiles
import base64

# Función que recibe un string base64 y devuelve el contenido como string
# @param content String encodeado en base64
# @return string con los datos decodeados
def b64toS(content):
    decodeB64 = base64.b64decode(content).decode("utf-8")
    finalcontent = decodeB64.split('\n')
    return finalcontent

# Función que recibe un array de bytes y devuelve el contenido como string en base64
# @param content array de bytes con la información
# @return string con los datos encodeados en base64
def StoB64(content):
    return base64.b64encode(content).decode('UTF-8')

# Función que recibe ruts y sus respectivos puntajes, para ponderarlos según cada carrera y ordenarlos de mayor a menor con algunas restricciones
# una ves ordenados los guarda en una lista de tipo "ruts"
# @param listofdata Datos separados por ";" y por línea, cada línea es un rut con sus puntajes
# @param listofcarreras Lista con los datos de todas la carreras en la base de datos
def sToRutsPon(listofdata,listofcarreras):
    listofruts = []
    for data in listofdata:
        if(data):
            tmpData = data.split(';')
            # Solo avanzará si el promedio simple entre los puntajes de matematicas y lenguaje es mayor o igual que 450
            if((int(tmpData[2])+int(tmpData[3])/2)>=450):
                tmpRut = ruts()
                tmpRut.rut = tmpData[0]
                for carrera in listofcarreras:
                    tmpPonderado = (int(tmpData[1]) * carrera.ponderaciones[0]) + (int(tmpData[2]) * carrera.ponderaciones[1]) + (int(tmpData[3]) * carrera.ponderaciones[2]) + (int(tmpData[4]) * carrera.ponderaciones[3])
                    if(int(tmpData[5])>int(tmpData[6])):
                        tmpPonderado += (int(tmpData[5]) * carrera.ponderaciones[4])
                    else:
                        tmpPonderado += (int(tmpData[6]) * carrera.ponderaciones[4])
                    tmpRutSize = len(tmpRut.carreraPondera)
                    #Los guarda ordenadamente según algunas condiciones 
                    #Primera condición, si existe alguna ponderación guardada antes entra a una segunda condición de orden
                    if(tmpRutSize>0):
                        #Verifica rapidamente si la ponderación actual es mayor a la menor ponderación ingresada
                        #Si se cumple la condición, se coloca donde indique el indexador
                        if(tmpRut.carreraPondera[tmpRutSize-1][1]<tmpPonderado):
                            tmpRut.carreraPondera.insert(indexador(tmpRut,tmpPonderado,carrera,listofcarreras),(carrera.codCarrera,tmpPonderado))
                        #Sino, verifica si esta es mayor o igual
                        else:
                            #Si es igual, se ejecuta el indexador
                            if(tmpRut.carreraPondera[tmpRutSize-1][1]==tmpPonderado):
                                index = indexador(tmpRut,tmpPonderado,carrera,listofcarreras)
                                #Si el indexador entrega -1 significa que no cumple los requerimientos para estar en posiciones más altas y se agrega al final de la lista
                                if(index == -1):
                                    tmpRut.carreraPondera.append((carrera.codCarrera,tmpPonderado))
                                #En caso contrario se agrega donde el index lo indique
                                else:
                                    tmpRut.carreraPondera.insert(index,(carrera.codCarrera,tmpPonderado))
                            else:
                                tmpRut.carreraPondera.append((carrera.codCarrera,tmpPonderado))
                    #Si no existe ninguna ponderación guarda, la guarda simplemente
                    else:
                        tmpRut.carreraPondera.append((carrera.codCarrera,tmpPonderado))
                listofruts.append(tmpRut)
    return listofruts

# Esta función, Principalmente acomoda cada rut en la carrera que mejor pondere
# @param listofcarreras Lista con todas las carreras en la base de datos y algunos datos
# @param listofruts Lista con todos los ruts ingresados y por analizar
def acomodar(listofcarreras,listofruts):
    carrerasSize = len(listofcarreras)
    #Condición simple, sólo si no quedan más ruts por analizar se termina la función
    while(len(listofruts)>0):
        rutsSize = len(listofruts)
        #Empieza a recorrer cada rut
        for i in range(rutsSize-1,-1,-1):
            for j in range(0, carrerasSize):
                #Si la ponderación más alta es de la carrera indexada proceda.
                if(listofcarreras[j].codCarrera == listofruts[i].carreraPondera[0][0]):
                    personasEnCarreraSize = len(listofcarreras[j].personas)
                    #Explicación de las condiciones: Se colocaron tantas restricciones para optimizar los tiempos en las fases tempranas de ejecución
                    #Las condiciones que se espera que se cumplan en fase media-fin de la función son las marcadas por "(*)"
                    #(*) Verifica que existan ruts ingresados en la lista, proceda.
                    if(personasEnCarreraSize>0):
                        #(*) Si la cantidad de ruts es igual a la cantidad de cupos máximos permitidos en la carrera, proceda.
                        if(listofcarreras[j].vacant == personasEnCarreraSize):
                            #(*) Si la ponderación actual es mayor a la ponderación del último rut ingresado entonces se ingrea el rut donde
                            #el indexador simple indique, se remueve el rut actual de la lista de ruts, se quita la primera ponderación
                            #de la lista de ponderaciones del último rut, si ya no le quedan ponderaciones no se agrega a la lista de ruts,
                            #en caso contrario, se agrega a la lista de ruts, y finalmente se remueve el último rut de la carrera
                            if(listofruts[i].carreraPondera[0][1] > listofcarreras[j].personas[personasEnCarreraSize-1].carreraPondera[0][1]):
                                listofcarreras[j].personas.insert(indexadorSimple(listofruts[i],listofcarreras[j]),listofruts[i])
                                del listofruts[i]
                                del listofcarreras[j].personas[personasEnCarreraSize].carreraPondera[0]
                                #Verifica si aún contiene ponderaciones de otras carreras.
                                if(len(listofcarreras[j].personas[personasEnCarreraSize].carreraPondera)>0):
                                    listofruts.append(listofcarreras[j].personas[personasEnCarreraSize])
                                del listofcarreras[j].personas[personasEnCarreraSize]
                            #(*) Si la ponderación actual es menor a la ponderación del último rut ingresado, significa que no merece estar en esa carrera
                            #por lo tanto simplemente se remueve la ponderación más alta de la lista de ponderaciones de ese rut, si ya no le quedan
                            #ponderaciones, simplemente se remueve el rut de la lista de ruts.
                            else:
                                del listofruts[i].carreraPondera[0]
                                if(len(listofruts[i].carreraPondera)<1):
                                    del listofruts[i]
                        #Si la cantidad de ruts es menor o mayor(está programado para que no sea mayor nunca) a la cantidad de cupos máximos permitidos en la carrera, proceda.
                        else:
                            #Si la ponderación del rut actual es menor o igual a la del último ingresado a la carrera, se inyecta en la última posición de la lista y se remueve de la lista de ruts.
                            if(listofruts[i].carreraPondera[0][1] <= listofcarreras[j].personas[personasEnCarreraSize-1].carreraPondera[0][1]):
                                listofcarreras[j].personas.append(listofruts[i])
                                del listofruts[i]
                            #Si la ponderación del rut actual es mayor a la del último ingresado a la carrera, se inyecta en la posición de la lista donde indique el indexador simple y se remueve de la lista de ruts.
                            else:
                                listofcarreras[j].personas.insert(indexadorSimple(listofruts[i],listofcarreras[j]),listofruts[i])
                                del listofruts[i]
                    #Si no existe nadie registrado en la carrera, simplemente se agrega y se remueve el rut de la lista de ruts
                    #Para que este no sea consultado nuevamente
                    else:
                        listofcarreras[j].personas.append(listofruts[i])
                        del listofruts[i]
                    #(*) No tiene sentido seguir consultando por otra carrera, se pasa al siguiente rut.
                    break