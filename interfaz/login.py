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
    
def open_file():
    nombrearch=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("pdf files","*.pdf"),("todos los archivos","*.*")))
    print(nombrearch)
    return nombrearch

## FUNCIONES DE VENTANAS

# VENTANA PRINCIPAL
def main_window():
    
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

    # Variables
    username = StringVar()
    password = StringVar()
    validateLogin = partial(validateLogin, username, password)
    
    # Entradas
    entrada_name = Entry(main, textvariable=username, width=37, relief="flat", bg=black_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_name.place(x=36,y=264)
    entrada_name.focus_set()

    entrada_pwd = Entry(main, textvariable=password, width=37, relief="flat", bg=black_color, bd=20, fg=white_color, insertbackground=white_color, show="*")
    entrada_pwd.place(x=36,y=375)
    entrada_pwd.focus_set()
    
    # Botones
    boton = Button(main, text="log in", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=validateLogin)
    boton.place(x=34, y=472)
    
    #Visualizar main
    main.mainloop()

# VENTANA DE OPCIONES
def options_window():
    global options
    options = Toplevel(main)
    options.title("Options")
    options.geometry("414x896+800+50")
    options.resizable(width=False, height=True)
    fondo = PhotoImage(file="options.png")
    fondo1 = Label(options, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
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
    
    options.mainloop()

# VENTANA PARA FIRMAR DOCUMENTOS
def sign_window():
    global sign
    sign = Toplevel(options)
    sign.title("Sign")
    sign.geometry("414x896+800+50")
    sign.resizable(width=False, height=False)
    fondo = PhotoImage(file="sign.png")
    fondo1 = Label(sign, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    #Boton de Home
    btn_home = Button(sign, cursor="hand2", bg=yellow_color, width=1, relief="flat", padx=8, pady=1, activebackground=yellow_color, command=sign_to_options)
    btn_home.place(x=191, y=127)
    
    #Boton de document
    btn_Document = Button(sign, text="Document", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_Document.place(x=34, y=246)
    #Boton de private key
    btn_PrivateKey = Button(sign, text="Private Key", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_PrivateKey.place(x=34, y=358)
    #Boton de firmar
    btn_Sign = Button(sign, text="Sign", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_Sign.place(x=34, y=469)
    
    sign.mainloop()

# FUNCION PARA VERIFICAR DOCUMENTOS
def verify_window():
    global verify
    verify = Toplevel(options)
    verify.title("Verify")
    verify.geometry("414x896+800+50")
    verify.resizable(width=False, height=False)
    fondo = PhotoImage(file="verify.png")
    fondo1 = Label(verify, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    #Boton de Home
    btn_home = Button(verify, cursor="hand2", bg=yellow_color, width=1, relief="flat", padx=8, pady=1, activebackground=yellow_color, command=verify_to_options)
    btn_home.place(x=191, y=127)
    
    #Boton de document
    btn_Document = Button(verify, text="Document", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_Document.place(x=34, y=246)
    #Boton de private key
    btn_PrivateKey = Button(verify, text="Private Key", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_PrivateKey.place(x=34, y=358)
    #Boton de Verificar
    btn_Verify = Button(verify, text="Verify", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_Verify.place(x=34, y=469)
    
    verify.mainloop()

# FUNCION PARA SOLICITAR FIRMAR
def request_signature_window():
    global request_signature
    request_signature = Toplevel(options)
    request_signature.title("Request Signature")
    request_signature.geometry("414x896+800+50")
    request_signature.resizable(width=False, height=False)
    fondo = PhotoImage(file="request.png")
    fondo1 = Label(request_signature, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    
    #Variables
    tagNominas = StringVar()
    
    #Boton de Home
    btn_home = Button(request_signature, cursor="hand2", bg=yellow_color, width=1, relief="flat", padx=8, pady=1, activebackground=yellow_color, command=request_signature_to_options)
    btn_home.place(x=191, y=127)
    
    #Boton de document
    btn_Document = Button(request_signature, text="Document", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                      font=("Poppins Light", 14, "bold"), padx=85, pady=10, command=open_file)
    btn_Document.place(x=34, y=246)
    #Boton de private key
    '''btn_Tags = Button(request_signature, text="Tags", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_Tags.place(x=34, y=358)'''
    #Boton para entrada de nominas que deben firmar
    entrada_tags = Entry(request_signature, font=("Poppins", 12, "italic"), textvariable=tagNominas, width=28, relief="flat", bg=purple_color, bd=20, fg=white_color, insertbackground=white_color)
    entrada_tags.place(x=34,y=358)
    entrada_tags.insert(0, "write payrolls here...")
    entrada_tags.focus_set()
    
    def placeholder(event):
        entrada_tags.configure(state = NORMAL)
        entrada_tags.configure(font=("Poppins", 12, "bold"))
        entrada_tags.delete(0, END)

        entrada_tags.unbind('<Button-1>', click)

    click = entrada_tags.bind('<Button-1>', placeholder)
    
    #Boton de Verificar
    btn_Request_Signature = Button(request_signature, text="Request Signature", cursor="hand2", bg=purple_color, fg=white_color, width=12, relief="flat",
                    font=("Poppins Light", 14, "bold"), padx=85, pady=10)
    btn_Request_Signature.place(x=34, y=469)
    
    request_signature.mainloop()
    
main_window()
