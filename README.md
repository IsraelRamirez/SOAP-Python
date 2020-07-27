# SOAP-Python
***
#### Participantes:
* Israel Ramirez
* Humberto Román
* Victor Araya
***
## Asignatura: Computación paralela y distribuida

Servicio web soap para el consumo de puntajes psu y su organización en diversas carreras según ciertos criterios de ordenamiento
=======
***

#### Asignatura: Computación paralela y distribuida

Servicio web soap para el consumo de puntajes psu y su organización en diversas carreras según ciertos criterios de ordenamiento.

Requiere el uso de base de datos PostgreSQL, el archivo para la creación de las tablas se encuentra en la carpeta `DataBase`. Se debe cambiar los valores para la conexión a la base de datos dentro del archivo `.../SOAP-Python/func/utils.py`.

### Linux-Ubuntu pre-Requeriments

`sudo apt install python3-venv python3-pip`

### Requirements

* Python **3.7.5**
* **pip - PyPi**
* Packages
    * **Spyne** to Soap Connection `pip install spyne` on linux-ubuntu use `pip3 install spyne`
    * **lxml** to xml elements `pip install lxml` on linux-ubuntu use `pip3 install lxml`
    * **openpyxl** to excel management `pip install openpyxl` on linux-ubuntu use `pip3 install openpyxl`
    * **pygresql** to postrgresql db management `pip install pygresql` on linux-ubuntu use `pip3 install pygresql`

**WSDL definition:** http://localhost:8000/wssoap/calculadorpuntajepsu.wsdl
***
