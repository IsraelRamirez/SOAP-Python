from models.carrera import carrera as carreras
from models.rut import rut as ruts
import pyodbc
import os

query = "SELECT codCarrera, vacant, nem, ranking,matematica,lenguaje,histociencia, first FROM ponderado"

def indexador(rut,ponderacion,carrera,listofcarreras):
    for i in range(0,len(rut.carreraPondera)):
        if(ponderacion > rut.carreraPondera[i][1]):
            return i
        elif(ponderacion == rut.carreraPondera[i][1]):
            for j in range(0,len(listofcarreras)):
                if(listofcarreras[j].codCarrera == rut.carreraPondera[i][0]):
                    if(carrera.first == listofcarreras[j].first):
                        if(carrera.vacant<=listofcarreras[j].vacant):
                            return i
                        else:
                            break
                    elif(carrera.first > listofcarreras[j].first):
                        return i
                    else:
                        break
    return -1

def dbquery(query):
    print(os.getcwd())
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.getcwd()+'/static/db/ponderadosDB.accdb;')
    cursor = conn.cursor()
    cursor.execute(query)
    
    return cursor.fetchall()

def initCarreras(): ### on develop
    listofcarreras = []
    queryResult = dbquery(query)
    for row in queryResult:
        if(row[0]):
            tmpCarrera = carreras()
            tmpCarrera.codCarrera = int(row[0])
            tmpCarrera.vacant = int(row[1])
            tmpCarrera.ponderaciones.append(float(row[2]))
            tmpCarrera.ponderaciones.append(float(row[3]))
            tmpCarrera.ponderaciones.append(float(row[4]))
            tmpCarrera.ponderaciones.append(float(row[5]))
            tmpCarrera.ponderaciones.append(float(row[6]))
            tmpCarrera.first = float(row[7])
            listofcarreras.append(tmpCarrera)
        else:
            break
    return listofcarreras
