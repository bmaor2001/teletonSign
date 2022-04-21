from tkinter import *
from tkinter import filedialog as fd
from functools import partial

purple_color = "#651e6e"
black_color = "#000000"
white_color = "#FFFFFF"
yellow_color = "#f5c604"

## FUNCIONES PARA RETIRAR VENTANAS VISUALMENTE

def main_to_options():
    main.state(newstate = "withdraw")
    options_window()

def options_to_main():
    options.state(newstate = "withdraw")
    main.deiconify()
    
def options_to_sign():
    options.state(newstate = "withdraw")
    sign_window()
    
def options_to_verify():
    options.state(newstate = "withdraw")
    verify_window()
    
def options_to_request_signature():
    options.state(newstate = "withdraw")
    request_signature_window()
    
def sign_to_options():
    sign.state(newstate = "withdraw")
    options_window()
    
def verify_to_options():
    verify.state(newstate = "withdraw")
    options_window()
    
def request_signature_to_options():
    request_signature.state(newstate = "withdraw")
    options_window()

## FUNCIONES DE VENTANAS
# ventana principal
def main_window():
    
    # funcion para validar log in
    def validateLogin(username, password):
        print("username entered :", username.get())
        print("password entered :", password.get())
        main_to_options()
        '''if username.get() == nomima and password.get() == pwd:
            main_to_options()
            return
        else:
            '''
    
    global main
    main = Tk()
    main.title("Login")
    main.geometry("414x896+800+50")
    main.resizable(width=False, height=False)
    fondo = PhotoImage(file="login.png")
    fondo1 = Label(main, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)

    # VARIABLES
    username = StringVar()
    password = StringVar()
    validateLogin = partial(validateLogin, username, password)
    
    # ENTRADAS
    entrada_name = Entry(main, textvariable=username, width=37, relief="flat", bg=black_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_name.place(x=36,y=264)
    entrada_name.focus_set()

    entrada_pwd = Entry(main, textvariable=password, width=37, relief="flat", bg=black_color, bd=20, fg=white_color, insertbackground=white_color, show="*")
    entrada_pwd.place(x=36,y=375)
    entrada_pwd.focus_set()
    
    # BOTONES
    boton = Button(main, text="log in", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=validateLogin)
    boton.place(x=34, y=472)
    
    #Visualizar main
    main.mainloop()

# ventana de opciones
def options_window():
    global options
    options = Toplevel(main)
    options.title("Options")
    options.geometry("414x896+800+50")
    options.resizable(width=False, height=True)
    fondo = PhotoImage(file="options.png")
    fondo1 = Label(options, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    # BOTONES
    #Boton de ventana Sign
    btn_Sign = Button(options, text="Sign", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=options_to_sign)
    btn_Sign.place(x=34, y=246)
    #Boton de ventana Verify
    btn_Verify = Button(options, text="Verify", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=options_to_verify)
    btn_Verify.place(x=34, y=358)
    #Boton de ventana Request
    btn_Request = Button(options, text="Request Signature", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=options_to_request_signature)
    btn_Request.place(x=34, y=469)
    #Boton de Exit
    btn_exit = Button(options, text="EXIT", cursor="hand2", bg=yellow_color, fg=black_color, width=8, relief="flat",
                    font=("Poppins Light", 18, "bold"), padx=4, pady=4, command=options_to_main)
    btn_exit.place(x=130, y=580)
    
    # mainloop para visualizacion
    options.mainloop()

# ventana para firma de documentos
def sign_window():
    # funcion para seleccionar archivo a firmar
    def select_file():
        global nombrearch_to_sign
        nombrearch_to_sign=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),("todos los archivos","*.*")))
        print(nombrearch_to_sign)
    # funcion para seleccionar clave privada
    def select_privateKey():
        global privateKey
        privateKey=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),("todos los archivos","*.*")))
        print(privateKey)
    # funcion para firmar archivo
    def sign_file():
        print("File Signed " + "privateKey: " + privateKey + " name: " + nombrearch_to_sign)
        sign_to_options()
    
    global sign
    sign = Toplevel(options)
    sign.title("Sign")
    sign.geometry("414x896+800+50")
    sign.resizable(width=False, height=False)
    fondo = PhotoImage(file="sign.png")
    fondo1 = Label(sign, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    # BOTONES
    #Boton de Home
    btn_home = Button(sign, cursor="hand2", bg=yellow_color, width=1, relief="flat", padx=8, pady=1, activebackground=yellow_color, command=sign_to_options)
    btn_home.place(x=191, y=127)
    
    #Boton de cargar document
    btn_Document = Button(sign, text="Document", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=select_file)
    btn_Document.place(x=34, y=246)
    #Boton de private key
    btn_PrivateKey = Button(sign, text="Private Key", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=select_privateKey)
    btn_PrivateKey.place(x=34, y=358)
    #Boton de firmar
    btn_Sign = Button(sign, text="Sign", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=sign_file)
    btn_Sign.place(x=34, y=469)
    
    # mainloop para visualizar
    sign.mainloop()

# funcion para verificar
def verify_window():
    # funcion para seleccionar archivo a firmar
    def select_file():
        global nombrearch_to_verify
        nombrearch_to_verify=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),("todos los archivos","*.*")))
        print(nombrearch_to_verify)
    # funcion para seleccionar clave publica
    def select_publicKey():
        global publicKey
        publicKey=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),("todos los archivos","*.*")))
        print(publicKey)
    # funcion para verificar archivo
    def verify_file():
        print("File Verified " + "publicKey: " + publicKey + " name: " + nombrearch_to_verify)
        verify_to_options()
    
    global verify
    verify = Toplevel(options)
    verify.title("Verify")
    verify.geometry("414x896+800+50")
    verify.resizable(width=False, height=False)
    fondo = PhotoImage(file="verify.png")
    fondo1 = Label(verify, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    # BOTONES
    #Boton de Home
    btn_home = Button(verify, cursor="hand2", bg=yellow_color, width=1, relief="flat", padx=8, pady=1, activebackground=yellow_color, command=verify_to_options)
    btn_home.place(x=191, y=127)
    
    #Boton de document
    btn_Document = Button(verify, text="Document", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=select_file)
    btn_Document.place(x=34, y=246)
    #Boton de public key
    btn_PrivateKey = Button(verify, text="Public Key", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=select_publicKey)
    btn_PrivateKey.place(x=34, y=358)
    #Boton de Verificar
    btn_Verify = Button(verify, text="Verify", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=verify_file)
    btn_Verify.place(x=34, y=469)
    
    # mainloop para visualizar
    verify.mainloop()

# funcion para solicitar firmas
def request_signature_window():
    # funcion para seleccionar archivo
    def select_file():
        global nombrearch
        nombrearch=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),("todos los archivos","*.*")))
        print(nombrearch)
    # funcion para cargar informacion del archivo
    def nominas(tagNominas, typoDocument, description, tagsDocuments):
        print("Las nominas son: " + tagNominas.get() + ", el typo es: " + typoDocument.get() + ", su descripcion es: " + description.get() + " y sus tags son: " + tagsDocuments.get() + " y la direccion del archivo es: " + nombrearch)
        request_signature_to_options()
    
    global request_signature
    request_signature = Toplevel(options)
    request_signature.title("Request Signature")
    request_signature.geometry("414x896+800+50")
    request_signature.resizable(width=False, height=False)
    fondo = PhotoImage(file="request.png")
    fondo1 = Label(request_signature, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    #VARIABLES
    tagNominas = StringVar()
    typoDocument = StringVar()
    description = StringVar()
    tagsDocument = StringVar()
    nominas = partial(nominas, tagNominas, typoDocument, description, tagsDocument)
    
    # ENTRADAS
    #Entrada para tomar el typo de documento
    entrada_typo = Entry(request_signature, font=("Poppins", 12, "italic"), textvariable=typoDocument, width=28, relief="flat", bg=purple_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_typo.place(x=34,y=320)
    entrada_typo.insert(0, "write typo...")
    
    #Entrada para tomar la descripcion del documento
    entrada_description = Entry(request_signature, font=("Poppins", 12, "italic"), textvariable=description, width=28, relief="flat", bg=purple_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_description.place(x=34,y=395)
    entrada_description.insert(0, "write description...")
    
    #Entrada para tomar los tags del documento
    entrada_tagsDocument = Entry(request_signature, font=("Poppins", 12, "italic"), textvariable=tagsDocument, width=28, relief="flat", bg=purple_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_tagsDocument.place(x=34,y=475)
    entrada_tagsDocument.insert(0, "write document's tags...")
    
    #Entrada para toma de nominas que deben firmar
    entrada_tags = Entry(request_signature, font=("Poppins", 12, "italic"), textvariable=tagNominas, width=28, relief="flat", bg=purple_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_tags.place(x=34,y=590)
    entrada_tags.insert(0, "write payrolls here...")

    #BOTONES
    #Boton de Home
    btn_home = Button(request_signature, cursor="hand2", bg=yellow_color, width=1, relief="flat", padx=8, pady=1, activebackground=yellow_color, command=request_signature_to_options)
    btn_home.place(x=191, y=127)
    
    #Boton de cargar documento
    btn_Document = Button(request_signature, text="Document", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=select_file)
    btn_Document.place(x=34, y=246)
    
    #Boton de Solicitar
    btn_Request_Signature = Button(request_signature, text="Request Signature", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=nominas)
    btn_Request_Signature.place(x=34, y=703)
    
    # mainloop para visualizar
    request_signature.mainloop()
    
main_window()
