# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:48:01 2022

@author: Jairo Enrique
"""
import pandas as pd
import streamlit as st
import numpy as np

# Se cargan las librerías necesarias
import signVerify
import hashlib
import DataBaseConection
from CertificateFunctions import cert_gen, check_associate_cert_with_private_key, VerificarVigencia, Hash_document, VerificarPassword

if 'permission' not in st.session_state:
    st.session_state.permission = False
if 'database' not in st.session_state:
    st.session_state.database = DataBaseConection.DataBase(user = "root", password = "", db = "teleton")
if 'nomina' not in st.session_state:
    st.session_state.nomina = ""

st.set_page_config(
     page_title="Sistema de firma digital",
     layout="wide",
     page_icon = "🔬",
     initial_sidebar_state="expanded")

st.sidebar.header("Menú")

st.markdown("<h1 style='text-align: center; color: white; font-family: verdana;'>Fundación teleton</h1>", unsafe_allow_html=True)

page = st.sidebar.selectbox("Página:", ["Login", "Registro usuarios","Solicitar firma","Firmar", "Verificar"])
if page == "Login":
    col1, col2, col3 = st.columns([0.3,0.3, 0.3])
    with col2:
        nom = st.text_input("Ingresa tu nómina")
        pass_ = st.text_input("Ingresa tu contraseña")
        if st.button("Ingresar"):
            try:
                if VerificarPassword(nom, pass_, st.session_state.database):
                    st.success("Verificación exitosa")
                    st.session_state.permission = True
                    st.session_state.nomina = nom
                else:
                    st.error("La contraseña no coincide con el usuario")
            except:
                st.error("Usuario no registrado")    
        
if page == "Solicitar firma":
    
    if st.session_state.permission:
        col1, col2= st.columns([0.4, 0.6])
        with col1:
            users = st.session_state.database.select(tabla = "users", 
                            what = "*", 
                            where = "Nomina", 
                            value = "")
            nominas = st.multiselect(
             'Seleccione las nóminas de quién firmará', 
             [u[0] for u in users])
            
            file = st.file_uploader("Elige el PDF a firmar", 
                                              accept_multiple_files=False)
            descripcion = st.text_input("Ingresa la descripción del documento")
            tipo = st.text_input("Ingresa el tipo de documento")
            
            
            if st.button("Cargar"):
                try:
                    st.markdown(nominas)
                    nom = ""
                    for h in nominas:
                        nom+=h+";"
                    st.session_state.database.insert_documentos(Hash = Hash_document(file).hexdigest(), 
                                   Tipo = tipo, 
                                   Nombre = file.name, 
                                   Descripcion = descripcion,
                                   Tags = f"{nom[:-1]}",
                                   Estatus = "Activo")
                    st.success("Archivo cargado correctamente")
                except Exception as e:
                    st.error("El archivo ya se encuentra cargado")
                    st.error(e)
    
                print(file)
            
            with col2:
                users = st.session_state.database.select(tabla = "documentos", 
                what = "*", 
                where = "Nomina", 
                value = "nomina_1")
                
                D = pd.DataFrame([[ u[2], u[3], u[1]] for u in users])
                D.columns = ["Nombre", "Descripción", "Tipo"]
                st.dataframe(D)
    else:
        st.error("Debes de registrarte para acceder a esta página")









if page == "Registro usuarios":
    col1, col2 = st.columns([0.4,0.6])
    if st.session_state.permission:
        with col1:    
            nombre= st.text_input('Ingresa el nombre')
            nomina = st.text_input('Ingresa la nómina')
            pass_ = st.text_input('Ingresa el password')
            email = st.text_input('Ingresa email')
            puesto = st.text_input('Ingresa el puesto')
            vig = st.number_input('Ingresa la vigencia (años)', step=1)
        
            if st.button('Boton de prueba'):
                try:
                    cert_gen(emailAddress=email,
                        commonName=nomina,
                        countryName="MX",
                        localityName="Monterrey",
                        stateOrProvinceName="Nuevo León",
                        organizationName="Tecnológico de Monterrey",
                        organizationUnitName="organizationUnitName",
                        serialNumber = 0,
                        validityStartInSeconds = 0,
                        validityEndInSeconds = int(vig)*365*24*60*60, #UN AÑO
                        KEY_FILE = "private"+nomina.replace(" ","_")+".key",
                        CERT_FILE="Certificado"+nomina.replace(" ","_")+".crt")
                
                    st.session_state.database.insert_users(nomina = nomina,
                        password=hashlib.sha256(bytes(pass_, encoding="utf-8")).hexdigest(),
                        nombre = nombre,
                        puesto = puesto,
                        tags = "IDM",
                        certificado = f"Certificado{nomina}.crt",
                        estatus = "Activo")
                    st.success("Registro exitoso")
                    
                    
                    PK = open("private"+nomina.replace(" ","_")+".key", "rb").read()
                    st.download_button(
                         label = "Descarga tu llave privada",
                         data = PK,
                         file_name="private"+nomina.replace(" ","_")+".key"
                     )
                    st.markdown("Recuerda no compartir tu llave privada y guardarla en un lugar seguro.")
                    
                except Exception as e:
                    st.error("Llena todos los campos")
                    st.markdown(e)
        with col2:
            st.markdown("Usuarios registrados")
            users = st.session_state.database.select(tabla = "users", 
                what = "*", 
                where = "Nomina", 
                value = "nomina_1")
            D = pd.DataFrame([[u[0], u[2], u[3]] for u in users])
            D.columns = ["Nómina", "Nombre", "Puesto"]
            st.dataframe(D)
                    
    else:
        st.error("Debes de registrarte para acceder a esta página")
        
        
        
        
        
        
        
        
        
        
        
if page == "Firmar":
    if st.session_state.permission:
        Certificado_1 = st.session_state.database.select(tabla = "users", 
                    what = "Certificado",
                    where = "Nomina",
                    value = st.session_state.nomina)[0][0]
    
        # Se carga la llave privada del usuario
        
        file_1 = st.file_uploader("Carga el documento a firmar", 
                                                  accept_multiple_files = False)
        private_key_1 = st.file_uploader("Carga la llave privada", 
                                                  accept_multiple_files = False)
        
        
        #Se verifica la vigencia para saber si es posible firmar el documento
        #private_key_2 = private_key_1
        
        if st.button("Firmar"):
            private_key_1  = private_key_1 .read()
            #Le pongo el read porque si le das read dos veces, ocurre un error
            #Solo en este, los demás quesan igual
            # =================================================
        
            if VerificarVigencia(Certificado_1):
                st.success("Certificado vigente")
                if check_associate_cert_with_private_key(Certificado_1, private_key_1):
                    st.success("La llave privada coincide con el certificado")
                    
                    file_name = signVerify.gen_signature(private_key_1, bytes(Hash_document(file_1).hexdigest(), 'utf-8'), file_1.name, st.session_state.nomina)
                    print(f"Archivo firmado en {file_name}")

                    print("\n Cargando la firma a la base de datos")
                    st.session_state.database.insert_firma(Doc_signed = file_name,
                                          Hash = Hash_document(file_1).hexdigest(),
                                          Nomina = st.session_state.nomina)
                    st.success("Documento firmado con éxito y cargado a la base de datos")
                else:
                    st.error("La llave privada no coincide con el certificado, no puede firmar.")
            else:
                st.error("El certificado no es vigente, no puede firmar.\nConsulte a TI.")
            
    else:
        st.error("Debes de registrarte para acceder a esta página")
    
    
        