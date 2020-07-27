<?php
/**
 * Paquetes necesarios:
 * sudo apt-get install php-cli php-soap php-xml
 */
class calculadorPuntajePsu {

    public $filename= null;
    public $mimetype= null;
    public $content= null;

    public function __construct($filename,$mimetype,$content) {
        $this->filename=$filename;
        $this->mimetype=$mimetype;
        $this->content=$content;
    }

}

/**
 * Se lee el archivo con los puntajes
 */
$pathInputContent = "/media/compartida/puntajes2.csv"; //Ingresar la ruta del archivo 
$filename = "puntajes2.csv"; //Nombre del archivo
$mimetype ="text/csv";
$host = "localhost:8000";
$pathDeSalida = "/media/compartida/testthreads.xlsx"; //Debe terminar el .xlsx

$file = fopen($pathInputContent,"rb");
$content = "";

while(!feof($file)){
    $line = fgets($file);
    $content = $content.$line;
}
fclose($file);
/**
 * Endpoint del servicio soap
 */

$url = "http://".$host."/wssoap/calculadorapuntajepsu.wsdl";
$client = new SoapClient($url);
/**
 * Datos iniciales
 */

$content = base64_encode($content);

$datos = new calculadorPuntajePsu($filename,$mimetype,$content);
ini_set('default_socket_timeout',9999999999);
try {
    $resultado = $client->calculadorPuntajePsu($datos);
    $data = base64_decode($resultado->calculadorPuntajePsuResult->string[2]);
    $archivo = fopen($pathDeSalida, "w");
    fwrite($archivo, $data);
    fclose($archivo);

} catch (Exception $e) {
    echo "{$e->getMessage()}";
}
?>