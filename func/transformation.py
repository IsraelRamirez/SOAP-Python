import base64
from models.carrera import carrera as carreras
from models.rut import rut as ruts
from func.utils import indexador
def b64toS(content):
    decodeB64 = base64.b64decode(content).decode("utf-8")
    finalcontent = decodeB64.split('\n')
    return finalcontent

def sToRutsPon(listofdata,listofcarreras):
    listofruts = []
    for data in listofdata:
        if(data):
            tmpData = data.split(';')
            
            if((int(tmpData[2])+int(tmpData[3])/2)>=450):

                tmpRut = ruts()
                tmpRut.rut = tmpData[0]

                for carrera in listofcarreras:
                    print(tmpData)
                    tmpPonderado = (int(tmpData[1]) * carrera.ponderaciones[0]) + (int(tmpData[2]) * carrera.ponderaciones[1]) + (int(tmpData[3]) * carrera.ponderaciones[2]) + (int(tmpData[4]) * carrera.ponderaciones[3])
                    
                    if(int(tmpData[5])>int(tmpData[6])):
                        tmpPonderado += (int(tmpData[5]) * carrera.ponderaciones[4])
                    else:
                        tmpPonderado += (int(tmpData[6]) * carrera.ponderaciones[4])
                    
                    tmpRutSize = len(tmpRut.carreraPondera)
                    if(tmpRutSize>0):
                        if(tmpRut.carreraPondera[tmpRutSize-1][1]<tmpPonderado):
                            tmpRut.carreraPondera.insert(indexador(tmpRut,tmpPonderado,carrera,listofcarreras),(carrera.codCarrera,tmpPonderado))
                        else:
                            if(tmpRut.carreraPondera[tmpRutSize-1][1]==tmpPonderado):
                                index = indexador(tmpRut,tmpPonderado,carrera,listofcarreras)
                                if(index == -1):
                                    tmpRut.carreraPondera.append((carrera.codCarrera,tmpPonderado))
                                else:
                                    tmpRut.carreraPondera.insert(index,(carrera.codCarrera,tmpPonderado))
                            
                            else:
                                tmpRut.carreraPondera.append((carrera.codCarrera,tmpPonderado))
                    else:
                        tmpRut.carreraPondera.append((carrera.codCarrera,tmpPonderado))
                listofruts.append(tmpRut)
    return listofruts