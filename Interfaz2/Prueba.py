# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:48:01 2022

@author: Jairo Enrique
"""
import streamlit as st
import numpy as np
from streamlit.report_thread import add_report_ctx

# Se cargan las librerías necesarias
import hashlib
import DataBaseConection
from CertificateFunctions import cert_gen, check_associate_cert_with_private_key, VerificarVigencia, Hash_document, VerificarPassword

database = DataBaseConection.DataBase(user = "root", password = "", db = "teleton")

st.set_page_config(
     page_title="Sistema de firma digital",
     layout="wide",
     page_icon = "🔬",
     initial_sidebar_state="expanded"
 )

st.sidebar.header("Menú")

st.markdown("<h1 style='text-align: center; color: white; font-family: verdana;'>Fundación teleton</h1>", unsafe_allow_html=True)
st.markdown("""<pre><p style='text-align: center; color: white; font-family: verdana;'>Aquí irá el texto que describa el funcionamiento y de los por menores del uso, montaje del circuito y 
            todo lo referente al sistema.</p></pre>
            """, unsafe_allow_html = True)
col1, col2, col3 = st.beta_columns([0.3,0.3, 0.3])

page = st.sidebar.selectbox("Página:", ["Login", "Registro usuarios","Solicitar firma","Firmar", "Solicitar"])
if page == "Login":
    
    with col2:
        nom = st.text_input("Ingresa tu nómina")
        pass_ = st.text_input("Ingresa tu contraseña")
        
        

if page == "Solicitar firma":
    users = database.select(tabla = "users", 
                what = "*", 
                where = "Nomina", 
                value = "")
    
    options = st.multiselect(
     'Seleccione las nóminas de quién firmará', 
     [u[0] for u in users])
    
    


if page == "Registro usuarios":
    with col1:    
        nombre= st.text_input('Ingresa el nombre')
        nomina = st.text_input('Ingresa la nómina')
        pass_ = st.text_input('Ingresa el password')
        email = st.text_input('Ingresa email')
        vig = st.number_input('Ingresa la vigencia (años)', step=1)
        if st.button('Boton de prueba 2'):
            st.success("Exito")
        if st.button('Boton de prueba'):
            
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
            
            try:
                database.insert_users(nomina = nomina,
                    password=hashlib.sha256(bytes(pass_, encoding="utf-8")).hexdigest(),
                    nombre = nombre,
                    puesto = "Estudiante",
                    tags = "IDM",
                    certificado = f"Certificado{nomina}.crt",
                    estatus = "Activo")
                st.success("Registro exitoso")
            except Exception as e:
                st.error("Ocurrió un error")
                st.markdown(e)
                
    with col2:    
        st.markdown("""<pre><p style='text-align: center; color: black; font-family: verdana; font-size:12px;'>Fig 2. Descripción 2</p></pre>""", unsafe_allow_html = True)
    st.markdown("""<pre><p style='text-align: center; color: white; font-family: verdana;'>Más texto</p></pre>
                """, unsafe_allow_html = True)
    