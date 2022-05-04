# Manual del programador

Este documento tiene la finalidad de explicar el funcionamiento de los distintos paquetes de funciones que se crearon para llevar a cabo la solución de la problemática planteada por Fundación Teletón.

El documento se dividirá en 6 apartados: Una breve introducción y explicación de la solución general planteada, estructura de la solución, estructura de la base de datos, preparación del equipo, explicación de las funciones y un ejemplo del funcionamiento.

## Explicación general de la solución planteada

El archivo **`main.py`** sería el código principal. Éste contiene la interfaz del usuario y manda a llamar a los archivos **`DataBaseConection.py`** y **`CertificateFunctions.py`** para poder utilizar las funciones que estos dos archivos contienen. Existen funciones que deben ser manejadas exclusivamente por un administrador, por ejemplo: la creación de certificados e insertar usuarios nuevos a la base de datos. Por ello, estos códigos fueron brindados de manera separada a la solución y deberán ser ejecutados con una persona con el permiso de hacerlo (administrador).

Al utilizar este código, se asume que, tanto el servidor (en este caso fue creado localmente) como la base de datos fueron debidamente inicializados y se cuenta con al menos un usuario dentro de la misma. Una vez que se tiene al servidor, se pueden ejecutar el siguiente código para crear la base de datos y conectarla (o sólo conectarla) con la aplicación proporcionada:

```py
# Se cargan las librerías necesarias
import hashlib
import DataBaseConection
from CertificateFunctions import cert_gen, check_associate_cert_with_private_key, VerificarVigencia, Hash_document, VerificarPassword

database = DataBaseConection.DataBase(user = "Usuario", password = "Contraseña", db = "Nombre de la base de datos")
```

En caso de que no se cuente con algún usuario activo en la base de datos se puede correr las siguientes líneas de código para introducir un nuevo usuario:

```py
nombre_1 = "Nombre1"
password_1 = "Contrasena1"
nomina_1 = "ID"
email_1 = "Correo electronico1"

cert_gen(emailAddress=email_1,
    commonName=nomina_1,
    countryName="MX",
    localityName="Municipio donde se expide",
    stateOrProvinceName="Estado donde se expide",
    organizationName="Nombre de la organizacion",
    organizationUnitName="Nombre unitario de la organizacion",
    serialNumber= 0,
    validityStartInSeconds = 0,
    validityEndInSeconds = 1*365*24*60*60, #UN AÑO
    KEY_FILE = 'Nombre del archivo de la clave privada.key'
                #Sugerido: "Ejemplo/private"+nomina_1.replace(" ","_")+".key",
    CERT_FILE='Nombre del archivo del certificado.crt'
                #Sugerido: "Ejemplo/Certificado"+nomina_1.replace(" ","_")+".crt")

print("Firma generada")
print("Guarde su llave privada en un lugar aparte")
print("-------------------\n")
print("Subiendo certificado a la base de datos")

database.insert_users(nomina = nomina_1,
                #Contraseña se subirá encriptada
                password=hashlib.sha256(bytes(password_1, encoding="utf-8")).hexdigest(),
                nombre = nombre_1,
                puesto = "Puesto",
                tags = "Informacion relevante (ejemplo: Becario)",
                certificado = 'Nombre del archivo certificado.crt'
                            #Sugerido: f"Ejemplo/Certificado{nomina_1}.crt",
                estatus = "Activo")
```

## Estructura de la solución

![Estructura de la solución](.\Interfaz2\Capturas\DiagramaPrincipal.png)

## Estructura de la base de datos

![Estructura de la base de datos](.\Interfaz2\Capturas\strucDB.jpeg)

## Levantamiento del servidor 

Para verificar el correcto funcionamiento de la solución se instaló el paquete de MySQL que contiene el MySQL Server y MySQL Workbench, para después conectar la aplicación de MySQL Workbench con el servidor. Ahora se puede observar y administrar la base de datos de una manera más gráfica y cómoda para el usuario. 

Para la comodidad de la fundación, se planea que se asigne un equipo de cómputo de escritorio (o algún servidor que maneje Teletón) como servidor que esté simpre encendido o, en su defecto, que se encuentre encendido durante las horas laborales. En esta máquina se encontrará la base de datos y la aplicación diseñada. La idea es que los empleados se conecten por Internet, desde su navegador ingresar la IP del equipo (servidor) siguido por dos puntos y el puerto de `streamlit` que es el 8501.

Para más información relacionada a ``streamlit`` favor de consultar su [documentación](https://docs.streamlit.io/library/advanced-features/configuration).

Es necesario correr el archivo ``main.py`` para activar ``streamlit`` así como todas las funciones y la implementación general del proyecto. Se recomienda implementar el servidor, base de datos y aplicación en un equipo que pueda estar prendido todo el día o a menos en horario laboral, para evitar tener que estar ejecutando el código cada vez que alguien quiera acceder al sistema.

Los usuarios deberían ser capaces de abrir un navegador (Microsoft Edge) e ingresar:

```
localhost:8501
```

En caso de que existan problemas al momento de conectarse, favor de revisar la configuración del equipo o del Firewall del mismo.

## Explicación de las funciones

### Documento **`DataBaseConection.py`** 

| Funciones  |  Entradas  |  Salidas |  Descripción  |  
|---|---|---|---|
| __init__  | - Usuario de la base de datos. <br> - Contraseña <br> - Nombre de la base de datos| - Mensaje | Función de inicialización de la clase. Se conecta y, en caso de no encontrar la base de datos especificada, crea la base de datos con los parámetros proporcionados. |
| insert_users  | - ID de la persona <br> - Constraseña creada por la persona <br> - Nombre completo de la persona <br> - Puesto de la persona <br> - Tags: información adicional de la persona <br> -Archivo certificado de la persona <br> - Estatus: Activo/Inactivo  |- Mensaje | Función para insertar usuarios nuevos a la base de datos en la tabla llamada 'users'. Debe ser manejada por administrador  |   
|  insert_documentos | - Hash del documento a firmar <br> - Tipo de documento <br> - Nombre del archivo <br> - Descripción <br> - IDs de las personas que firmarán (puede ser más de una, separados por un punto-coma ';') <br> - Estatus: Activo/Inactivo  | - Mensaje  | Función para insertar documentos nuevos a la base de datos en la tabla llamada 'dcumentos'. Se manda a llamar por la aplicación cuando se selecciona la opción de 'Solicitar firma' |  
| insert_firma  |  - Documento de firma de documento <br> - Hash del documento que se firmó <br> - ID de la persona que firma |  | Función que sube a la tabla 'firmas' el archivo con la firma digital para el documento identificado con su hash, quién lo firma y la fecha y hora de cuando esto ocurre. Se tiene la intención que esta tabla sirva como *logs* para saber y llevar un control de las firmas. <br> Esta función se llama cuando se escoge la opción de 'Firmar' en la aplicación. |   

A continuación se presentan funciones de comandos típicos de una base de datos MySQL:

| Funciones  |  Entradas  |  Salidas |  Descripción  |  
|---|---|---|---|
| select  |  - Nombre de la tabla <br> - La variable a regresar <br> - Variable independiente <br> - Valor de la variable independiente <br> *Opcional:* <br> - Segunda variable independiente <br> - Valor de la segunda variable independiente | - *list*: Todos los valores de la variable dependiente donde se cumple las condiciones de las variables independientes.  |  Función regresa todos los valores de una variable (columna) donde se cumple las condiciones impuestas por las variables independientes. |   
| update  |  - Nombre de la tabla <br> - La variable a actualizar <br> - Valor de la variable a actualizar <br> - Variable independiente <br> - Valor de la variable independiente |  - Mensaje | Función que actualiza un valor de una variable dentro de la base de datos. Esta actualización está sujeta a las condiciones de la variable independiente y su valor. |  
|  delete | - Nombre de la tabla <br> - La variable independiente <br> - Valor de la variable independiente  | - Mensaje  |  Función que elimina toda una fila donde se cumple la condición impuesta. <br> Esta función debe ser manejada por un administrador. | 
| create  | - Nombre de usuario para la base de datos <br> - Contraseña para acceder a la base de datos <br> - Nombre de la base de datos |   | Función que crea la base de datos considerando los parámetros ingresados. <br> La función debe ser ejecutada por un administrador. |

### Documento **`CertificateFunctions.py`** 

| Funciones  |  Entradas  |  Salidas |  Descripción  |  
|---|---|---|---|
| cert_gen  |  - Correo electrónico del empleado <br> - Nombre completo del empleado <br> - País donde se expide <br> - Municipio donde se expide <br> - Nombre de la organización que expide el certificado <br> - Nombre unitario de la organización <br> - Nombre de serie <br> - Nombre unitario de la organización <br> - Tiempo de vigencia (*default:* un año) <br> - Ubicación y nombre del archivo donde se creará la clave privada <br> - Ubicación y nombre del archivo donde se creará el certificado |   |  Función que crea los certificados para los empleados o los futuros usuarios de la aplicación de firmas. <br> Deberá ser usada por un administrador. |   
| check_associate_cert_with_private_key  |  - Certificado <br> - Archivo de la clave privada  |  - Mensaje | Esta función verifica si la clave privada ingresada está asociada al certificado ingresado. |  
| Hash_document | - Dirección del archivo  | - Hash del documento ingresado  |  Función que genera el *hash* del documento ingresado.| 
| VerificarVigencia  | - Archivo del certificado | - Mensaje <br> - True/False| Función que verifica si el certificado es aún vigente |
| VerificarPassword  | - ID del empleado <br> - Contraseña del empleado <br> - Objeto de la clase DataBase   | - True/False| Función que verifica si la contrasela ingresada corresponde a la contraseña del usuario. Se aplica para permitirle (o no) el acceso a alguien a la plataforma. |

### Documento **`signVerify.py`** 

| Funciones  |  Entradas  |  Salidas |  Descripción  |  
|---|---|---|---|
| gen_signature  |  - Clave privada de la persona que firma <br> - Hash del documento <br> - Nombre del documento a firmar <br> - ID de la persona que firma | - Archivo binario con la firma <br>  |  Esta función sirve para generar la firma del documento que se necesite. Se usa la función hash SHA-512. |   
| verify  |  - Certificado <br> - Hash del documento que se quiera verificar <br> - Archivo binario que contiene la firma digital del documento <br> - ``` load = True``` (Saber si lo tiene que leer del disco)  |  - True/False | Esta función verifica si la firma ingresada corresponde a una firma para el documento ingresado. | 

### Documento **`login.py`** 

| Funciones  |  Entradas  |  Salidas |  Descripción  |  
|---|---|---|---|
| main_to_options <br> potions_to_main <br> options_to_sign <br> options_to_verify <br> options_to_request_signature <br> sign_to_options <br> verify_to_options <br> request_signature_to_options  |  |   |  Funciones que sirven para cerrar ventanas emergentes de la aplicación. Sirve para no cerrarlas manualmente. Se usan dentro del código de la interfaz.|   
| main_window  |  |   | Función que contiene a la ventana principal de la aplicación (Ventana de ingreso a la plataforma). |  
| validateLogin | - Nombre de usuario ingresado <br> - Contraseña ingresada| - Mensaje  |  Función que verifica si el usuario y la contraseña corresponden a algún usuario en la base de datos. <br> 
Esta función se encuentra dentro de la función de main_window() y usa a la función VerificaPassword().| 
| options_window  |  |  | Contiene el código de la ventana de la interfaz relacionada con las opciones de 'Solicitar firma', 'Firmar' y 'Verificar'. |
| sign_window  |   | | Función que contiene lo relacionado a la opción de 'Firmar'. |
| select_file <br> select_privateKey <br> select_publicKey |  | - Mensaje  |  Funciones que permiten seleccionar un archivo del dispositivo local. |   
| sign_file |  | - Mensaje  | Función que toma la clave privada y el documento a firmar. Verifica si la clave privada corresponde al certificado del usuario conectado y verifica la vigencia de este certificado. Si no hubo error, se ejecuta la función ```signVerify.gen_signature()```. |  
| check_permit |  | - Mensaje  |  Función que verifica si la persona que intenta firmmar tiene permiso para hacer; es decir, si su ID se encuentra en los *tags* de ese documento.| 
| verify_window  |  |  | Función que contiene el código relacionado a la opción de 'Verificar'. |
| verify_file  |   | | Función que toma el certificado (se extrae la clave pública), el archivo con la firma digital y el documento a verificar. Verifica si el archivo de la firma digital corresponde a el documento ingresado, se usa la función  ```signVerify.verify()```.|
| request_signature_window |  |  |  Función que contiene el código relacionado a la opción de 'Solicitar firma'.| 
| nominas | - IDs de los empleados que se solicita que firmen <br> - Tipo de documento <br> - Descripción |  | Función que usa la función ```DataBase.insert_documentos()``` para cargar a la base de datos un nuevo documento con sus variables. |

## Ejemplo de aplicación
Revisar el ejemplo del [archivo](ejemploAplicado.ipynb).
