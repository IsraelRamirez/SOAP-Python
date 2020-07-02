### Librerias 
import logging
logging.basicConfig(level=logging.DEBUG)

### Librerias dedicadas al levantamiento del WS soap
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne.model.primitive import String

### Librerias externas útiles para el trabajo
from openpyxl import Workbook
import base64

### Librerias internas útiles para el trabajo
    ### Funciones

    ### Clases
from models.rut import rut as ruts
from models.carrera import carrera as carreras

### Variables globales estaticas
finalname = "Puntajes.xlsx"
finalmime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class wsSoap(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, _returns = Iterable(Unicode))
    def calculadorPuntajePsu(ctx,filename,mimetype,content):
        
        finalcontent = "S"
        yield(finalname)
        yield(finalmime)
        yield(finalcontent)


application = Application( [wsSoap ],tns = 'soap.psu.calculator',in_protocol = Soap11(),out_protocol = Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('127.0.0.1', 8000, wsgi_app)
    print("\nServer Online")
    server.serve_forever()