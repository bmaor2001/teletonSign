#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from OpenSSL import crypto, SSL
from datetime import datetime
import OpenSSL.crypto 
import sys
import hashlib


#Función para generar el certificado digital y la llave privada
def cert_gen(
    emailAddress="emailAddress",
    commonName="commonName",
    countryName="NT",
    localityName="localityName",
    stateOrProvinceName="stateOrProvinceName",
    organizationName="organizationName",
    organizationUnitName="organizationUnitName",
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60,
    KEY_FILE = "private.key",
    CERT_FILE="selfsigned.crt"):
    #can look at generated file using openssl:
    #openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
        

def check_associate_cert_with_private_key(cert, private_key):
    """
    :type cert: str
    :type private_key: str
    :rtype: bool
    """
    try:
        private_key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(private_key).read())
    except OpenSSL.crypto.Error:
        raise Exception('private key is not correct: %s' % private_key)

    try:
        cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        #cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(cert).read())
    except OpenSSL.crypto.Error:
        raise Exception('certificate is not correct: %s' % cert)

    context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
    context.use_privatekey(private_key_obj)
    context.use_certificate(cert_obj)
    try:
        context.check_privatekey()
        return True
    except OpenSSL.SSL.Error:
        return False
    
def Hash_document(file):
    """
    :type file: str (dirección del archivo)
    :rtype: _hashlib.HASH
    Utilice Hash_document(file).hexdigest() para obtener la representación del SHA en string.
    """
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha256()
    #hashlib.sha512

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)

    #print("MD5: {0}".format(md5.hexdigest()))
    #print("SHA1: {0}".format(sha1.hexdigest()))
    return sha1

#Verificando si todavía es vigente
def VerificarVigencia(Certificado_1):
    """
    :type Certificado_1: str (dirección del archivo)
    :rtype: bool
    """
    try:
        cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, Certificado_1)
        #cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(cert).read())
    except OpenSSL.crypto.Error:
        raise Exception('certificate is not correct: %s' % cert)

    fecha = cert_obj.get_notAfter().decode()
    anio = int(fecha[:4])
    mes = int(fecha[4:6])
    dia = int(fecha[6:8])

    if datetime(anio, mes, dia) >= datetime.now():
        print("Certificado vigente")
        return True
    else:
        print("Certificado no vigente, no puede firmar")
        return False
