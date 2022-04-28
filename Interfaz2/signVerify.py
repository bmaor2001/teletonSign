## Sign Algorithm (parameters: **document, priv_key)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from OpenSSL import crypto        
from datetime import datetime

## Sign Algorithm
def gen_signature(priv_key, document, nombreDoc, nomina,):
    """
    :type priv_key: str (dirección del documento)
    :type document: bytes (El hash pasarlo a str y eso a bytes)
    :type nombreDoc: str (nombre del archivo a firmar, solo como referencia)
    :type nomina: str (nomina de quien firma)
    :rtype: str (nombre del archivo firmado)
    """
    '''Receives the HASH of the documentPDF and the private key,
    returns a binary file with the signature.
    This will be uploaded to the logs section FIRMAS'''

    #Read private_key from other file
    with open(priv_key, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    signature = private_key.sign(
        document,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),     
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )   

    #Format: aaaammdd_hhmmss
    date = str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '_')[:-7]

    #write the binary signature file
    name = f"{nombreDoc}_{nomina}_{date}.sign"
    f = open(name, "wb")
    f.write(signature)
    f.close()

    #Returns the sign binary file, will be uploaded to DB
    return name


## Verifying Algorithm
def verify(cert, document, sigfile, load = True):
    """
    :type cert: str (dirección del documento)
    :type document: bytes (El hash pasarlo a str y eso a bytes)
    :type sigfile: str (Dirección del archivo firmado)
    :type load: bool (Saber si lo tiene que leer del disco [True] o se le pasará un archivo en bytes)
    :rtype: str (nombre del archivo firmado)
    """
    '''Receives the certificate with public key, the
    document and the signaturefile to see if said signatures
    corresponds to that document. And its hasn't been 
    altered or something else was signed. '''

    #Get public_key from certificate
    
    
    if load:
        f = open(sigfile, 'rb')
        sigfile = f.read()
        crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert).read())
    else:
        crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
        
    pub_key = crtObj.get_pubkey()
    pub_key = pub_key.to_cryptography_key()

    try: 
        pub_key.verify(
        sigfile,
        document,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
        )
        return True

    except: 
        return False

