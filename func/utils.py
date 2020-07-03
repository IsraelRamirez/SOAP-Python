### Clases internas
from models.carrera import carrera as carreras
from models.rut import rut as ruts
### Librerias útiles
import pyodbc
from openpyxl import Workbook
import os

query = "SELECT codCarrera, vacant, nem, ranking,matematica,lenguaje,histociencia, first FROM ponderado"

# Entrega el inidice donde se debe situar la mejor carrera dentro de la listas de ponderaciones para ese rut
# @param rut Objeto "ruts" con la información del postulante
# @param ponderacion ponderación obtenida para una cierta carrera
# @param carrera carrera a la que se le calcula la ponderación
# @param listofcarreras lista de todas las carreras
# @return devuelve el indice
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

# Función que entrega el índice donde debe ir el rut dentro de la carrera.
# Nota: Se considera que tiene mayor prioridad alquien que entró antes a la carrera, es por eso que solo verifica
# si es estrictamente mayor que...
# @param rut Objeto "ruts" con los datos de los ruts
# @param carrera Objeto "carreras" con los datos de una carrera
# @return Devuelve el índice donde debe ingresarse el rut dentro de la carrera
def indexadorSimple(rut,carrera):
    for i in range(0,len(carrera.personas)):
        if(rut.carreraPondera[0][1] > carrera.personas[i].carreraPondera[0][1]):
            return i
    return -1

# Función que se conecta a la base de datos y devuelve los resultados de la consulta
# @param query sentencia SQL
# @param devuelve los resultados de la sentencia SQL
def dbquery(query):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.getcwd()+'/static/db/ponderadosDB.accdb;')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Función que genera una lista de carreras, con el codigo de carrera correspondiente.
# @return Devuelve una lista de las carreras inicialiazadas con el código de carrera.
def initCarreras():
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


# Función que genera, según los ruts ingresados en la carrera, un excel con los datos obtenidos
# @param listofcarreras con las carreras, sus ruts ingresados y sus ponderaciones
def getExcel(listofcarreras):
    wb = Workbook()
    for i in range(0,len(listofcarreras)):
        sheet = wb.create_sheet(str(listofcarreras[i].codCarrera)) ###...Crea una nueva hoja...
        row = 0
        for j in range(0,len(listofcarreras[i].personas)): ###...Y procede finlamente a registrar a cada estudiante en el excel
            row+=1
            sheet['A'+str(row)] = str(listofcarreras[i].personas[j].rut)
            sheet['B'+str(row)] = listofcarreras[i].personas[j].carreraPondera[0][1]
    del wb['Sheet']
    nombre="tmp.xlsx"
    wb.save(nombre)