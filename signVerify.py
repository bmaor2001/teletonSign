## Sign Algorithm (parameters: **document, priv_key)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime


def gen_signature(priv_key, document):
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

    #write the binary signature file
    f = open('signature' + str(datetime.now()), "wb")
    f.write(signature)
    f.close()

    #Returns the sign binary file, will be uploaded to DB
    return f



def verify(pub_key, document, sigfile):
    '''Receives the public key (certificate), the
    document and the signaturefile to see if said signatures
    corresponds to that document. And its hasn't been 
    altered or something else was signed. '''

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
        print('Verification successful')

    except: 
        print('Verification failed')

