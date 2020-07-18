### Librerias 
import logging
logging.basicConfig(level=logging.DEBUG)

### Librerias dedicadas al levantamiento del WS soap
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne.model.primitive import String

### Librerias internas útiles para el trabajo
import os
    ### Funciones
from func.transformation import *
from func.utils import initCarreras,getExcel
    ### Clases
from models.rut import rut as ruts
from models.carrera import carrera as carreras

### Variables globales estaticas
finalname = "Puntajes.xlsx"
finalmime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

### Clase principal
class wsSoap(ServiceBase):
    # Función principal del WS soap, calcula las ponderaciones de los de acuerdo a sus puntajes PSU y la carrera que eligen
    # @param ctx Contexto
    # @param filename Nombre del archivo por llegar
    # @param mimetype Tipo mime del archivo
    # @param content Contenido del archivo, en base64
    # @yields Entregan nombre final del archivo, tipo mime, contenido final del archivo
    @rpc(Unicode, Unicode, Unicode, _returns = Iterable(Unicode))
    def calculadorPuntajePsu(ctx,filename,mimetype,content):
        listofcarreras = initCarreras()
        listofdata = b64toS(content)
        listofruts = sToRutsPon(listofdata,listofcarreras)
        acomodar(listofcarreras,listofruts)
        getExcel(listofcarreras)
        excel = open("tmp.xlsx",'rb').read()
        finalcontent = StoB64(excel)
        os.remove("tmp.xlsx")
        yield(finalname)
        yield(finalmime)
        yield(finalcontent)

### Configuración endpoint
app = Application( 
    [ wsSoap ],
    tns = 'soap.psu.calculator',
    in_protocol = Soap11(),
    out_protocol = Soap11(),
    )

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(app, chunked=True, max_content_length=2097152*100,block_length=1024*1024*500)
    server = make_server('127.0.0.1', 8000, wsgi_app)
    print("\nServer Online")
    print("\nctrl-LMB on http://localhost:8000/wsSoap/calculadorPuntajePsu.wsdl to wsdl definition site")
    print("\nctrl-c to break connection")
    server.serve_forever()