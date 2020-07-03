# SOAP-Python
## Asignatura: Computación paralela y distribuida

Servicio web soap para el consumo de puntajes psu y su organización en diversas carreras según ciertos criterios de ordenamiento

### Linux-Ubuntu pre-Requeriments

`sudo apt install python3-venv python3-pip unixodbc-dev`

### Requirements

* Python **3.7.5**
* **pip - PyPi**
* Packages
    * **Spyne** to Soap Connection `pip install spyne` on linux-ubuntu use `pip3 install spyne`
    * **lxml** to xml elements `pip install lxml` on linux-ubuntu use `pip3 install lxml`
    * **openpyxl** to excel management `pip install openpyxl` on linux-ubuntu use `pip3 install openpyxl`
    * **pyodbc** to db management `pip install pyodbc` on linux-ubuntu use `pip3 install pyodbc`

**WSDL definition:** http://localhost:8000/wssoap/calculadorpuntajepsu.wsdl
