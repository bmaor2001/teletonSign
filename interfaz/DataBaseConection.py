
import pymysql

class DataBase:
    def __init__(self, user, password, db):
        try:
            self.connection = pymysql.connect(
                host = "localhost",
                user = user,
                password = password,
                db = db,
                autocommit=True
            )
            self.cursor = self.connection.cursor()

            print("Conexión exitosa")
        except:
            self.create(user, password, "teleton")
            
    
    def insert_users(self, nomina, password, nombre, puesto, tags, certificado, estatus):
            certificado = open(certificado, "rb").read()
            sql = """INSERT INTO users (`Nomina`,`Password`, `Nombre`, `Puesto`, `Tags`, `Certificado`, `Estatus`) VALUES (%s, %s,%s,%s,%s,%s,%s)"""
            try:
                self.cursor.execute(sql, (nomina,password, nombre, puesto, tags, certificado, estatus))
                print(f"{nombre} ha sido añadido a la base de datos.")
            except Exception as e:
                print(e)
                
    def insert_documentos(self, Hash, Tipo, Nombre, Descripcion, Tags, Estatus):
            sql = f"INSERT INTO documentos (`Hash`, `Tipo`, `Nombre`, `Descripcion`, `Tags`, `Estatus`) VALUES ('{Hash}', '{Tipo}', '{Nombre}', '{Descripcion}', '{Tags}', '{Estatus}')"
            try:
                self.cursor.execute(sql)
                print(f"{Nombre} ha sido añadido a la base de datos.")
            except Exception as e:
                print(e)
                
    ## Changes in these two functions
    '''
    def insert_firma(self, Hash, Nomina, Doc_signed): 
            Doc_signed = open(Doc_signed, "rb").read()
            sql = """ INSERT INTO firmas  (Hash, Nomina, Doc_signed) VALUES (%s,%s,%s)"""
            try:
                self.cursor.execute(sql, (Hash, Nomina, Doc_signed))
                print(f"{Hash} ha sido añadido a la base de datos.")
            except Exception as e:
                print(e)
    
    def cargar_firma(self, Doc_signed, Hash, Nomina):
        Doc_signed = open(Doc_signed, "rb").read()
        sql = """ UPDATE firmas SET Doc_signed = %s WHERE (Hash, Nomina) = (%s, %s)"""
        #sql = """ INSERT INTO firmas SET Doc_signed = %s WHERE (Hash, Nomina) = (%s, %s)"""
        self.cursor.execute(sql, (Doc_signed, Hash, Nomina))
    '''
    def insert_firma(self, Doc_signed, Hash, Nomina):
        Doc_signed = open(Doc_signed, "rb").read()
        #sql = """ UPDATE firmas SET Doc_signed = %s WHERE (Hash, Nomina) = (%s, %s)"""
        sql = """ INSERT INTO firmas  (Doc_signed, Hash, Nomina) VALUES (%s,%s,%s)"""
        self.cursor.execute(sql, (Doc_signed, Hash, Nomina))
    ## End of changes
                
    def select(self, tabla, what, where, value, where_2 = "", value_2 = ""):
        if what == "*":
            sql = f"SELECT {what} FROM {tabla}"
        elif where_2 != "":
            sql = f"SELECT {what} FROM {tabla} where {where} = '{value}' AND {where_2} = '{value_2}'"
            
        else:
            sql = f"SELECT {what} FROM {tabla} where {where} = '{value}'"
        self.cursor.execute(sql)
        val = self.cursor.fetchall()
        return val
        
    def update(self, tabla, what, value, where_col, where_val):
        sql = f"UPDATE {tabla} set {what} = '{value}' where {where_col} = '{where_val}'"
        self.cursor.execute(sql)
        print("Actualización exitosa")
        
    def delete(self, tabla, where, value):
        sql = f"DELETE FROM {tabla} where {where} = '{value}'"
        self.cursor.execute(sql)
        print("Eliminación exitosa")
        
    def create(self, user, password, database):
                Users_table = "CREATE TABLE `users` (`Nomina` varchar(10) NOT NULL,`Password` varchar(100) NOT NULL,`Nombre` varchar(100) NOT NULL,`Puesto` varchar(50) NOT NULL,`Tags` text NOT NULL,  `Certificado` blob,`Estatus` varchar(20) NOT NULL,PRIMARY KEY (`Nomina`))"
                Documentos_table = "CREATE TABLE `documentos` (`Hash` varchar(80) NOT NULL,`Tipo` varchar(100) NOT NULL,`Nombre` varchar(100) NOT NULL,`Descripcion` text NOT NULL,`Tags` varchar(100) NOT NULL,`Estatus` varchar(10) NOT NULL,`TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`Hash`))"
                Firmas_table = "CREATE TABLE `firmas` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Hash` varchar(100) NOT NULL,`Doc_signed` blob,`Nomina` varchar(50) NOT NULL,`TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`ID`))"
                connection = pymysql.connect(
                        host = "localhost",
                        user = user,
                        password = password,
                        db = "sys"
                    )
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE {database}")
                cursor.close()

                connection = pymysql.connect(
                            host = "localhost",
                            user = user,
                            password = password,
                            db = database
                        )
                cursor = connection.cursor()
                cursor.execute(Firmas_table)
                cursor.execute(Documentos_table)
                cursor.execute(Users_table)
                self.cursor = connection.cursor()

