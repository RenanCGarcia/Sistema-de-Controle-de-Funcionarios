import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3

class BancoDeDados:
    def conectarBanco(self):
        self.banco = sqlite3.connect("Sistema de Controle de Funcionários/data.db")
        self.root = self.banco.cursor()
        self.root.execute("CREATE TABLE IF NOT EXISTS usuarios (id_user INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT UNIQUE NOT NULL, senha TEXT NOT NULL, root BOOLEAN NOT NULL)")
        self.root.execute("CREATE TABLE IF NOT EXISTS funcionarios (cpf INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT NOT NULL, nascimento DATE NOT NULL, funcao TEXT NOT NULL, data_inicio DATE NOT NULL)")
        self.root.execute("CREATE TABLE IF NOT EXISTS punicao (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, tipo TEXT NOT NULL, motivo TEXT NOT NULL, data DATE NOT NULL, cpf INTEGER NOT NULL, FOREIGN KEY(cpf) REFERENCES funcionarios(cpf))")

    def cadastrar_Funcionario(self, cpf, nome, nascimento, funcao, data_inicio):
        cpfBanco = cpf.replace(".","").replace("-","")[:11]
        self.root.execute("INSERT INTO funcionarios (cpf, nome, nascimento, funcao, data_inicio) VALUES ('"+cpfBanco+"', '"+nome.title()+"', '"+nascimento+"', '"+funcao+"', '"+data_inicio+"')")
        self.banco.commit()
    
    def btns_Funcionarios(self):
        self.root.execute("SELECT nome FROM funcionarios")
        funcionarios = self.root.fetchall()
        return funcionarios
    
    def mostrar_Funcionario(self, nome):
        self.root.execute("SELECT nome, cpf, nascimento, funcao, data_inicio FROM funcionarios WHERE nome = '"+nome+"'")
        func = self.root.fetchall()
        return func[0]
    
    def add_Falta(self, motivo, data, cpf):
        # ALTERANDO FORMATO DA DATA
        dataBanco = Funcionalidades.inverterData(self, datainvert=data.get())   
        # ADICIONANDO FALTA NO BANCO DE DADOS
        self.root.execute("INSERT INTO punicao (tipo, motivo, data, cpf) VALUES ('FALTA', '"+motivo.get()+"', '"+dataBanco+"', '"+cpf+"')")
        print(f"FALTA + {motivo.get()} + {dataBanco} + {cpf}")
        self.banco.commit()

    def add_Advertencia(self, motivo, data, cpf):
        # ALTERANDO FORMATO DA DATA
        dataBanco = Funcionalidades.inverterData(self, datainvert=data.get())
        # ADICIONANDO ADVERTÊNCIA NO BANCO DE DADOS
        self.root.execute("INSERT INTO punicao (tipo, motivo, data, cpf) VALUES ('ADVERTÊNCIA', '"+motivo.get()+"', '"+dataBanco+"', '"+cpf+"')")
        print(f"ADVERTÊNCIA + {motivo.get()} + {dataBanco} + {cpf}")
        self.banco.commit()

    def add_Suspensao(self, motivo, data, cpf):
        # ALTERANDO FORMATO DA DATA
        dataBanco = Funcionalidades.inverterData(self, datainvert=data.get())
        # ADICIONANDO SUSPENSÃO NO BANCO DE DADOS
        self.root.execute("INSERT INTO punicao (tipo, motivo, data, cpf) VALUES ('SUSPENSÃO', '"+motivo.get()+"', '"+dataBanco+"', '"+cpf+"')")
        print(f"SUSPENSÃO + {motivo.get()} + {dataBanco} + {cpf}")
        self.banco.commit()

    def contFaltas(self, cpf):
        self.root.execute("SELECT COUNT(tipo) FROM punicao WHERE cpf = '"+cpf+"' AND tipo = 'FALTA'")
        contador = self.root.fetchall()
        return contador
    
    def contAdvertencias(self, cpf):
        self.root.execute("SELECT COUNT(tipo) FROM punicao WHERE cpf = '"+cpf+"' AND tipo = 'ADVERTÊNCIA'")
        contador = self.root.fetchall()
        return contador

    def contSuspensao(self, cpf):
        self.root.execute("SELECT COUNT(tipo) FROM punicao WHERE cpf = '"+cpf+"' AND tipo = 'SUSPENSÃO'")
        contador = self.root.fetchall()
        return contador        

    def entrar(self, usuario, senha):
        self.conectarBanco(self=BancoDeDados)
        self.root.execute("SELECT nome, senha, root FROM usuarios WHERE nome = '"+usuario.get()+"'")
        try:
            id = self.root.fetchall()[0]
            if (id[0] == usuario.get()) and (id[1] == senha.get()):
                global adm, current_user
                current_user = id[0]
                adm = id[2]
                print("Login efetuado com sucesso!")
                return True
            elif id[1] != senha.get():
                print("Senha Incorreta.")
                return False
        except IndexError:
            return False

    def delFuncionario(self, funcionario):
        if adm == 1:
            self.root.execute("DELETE FROM funcionarios WHERE cpf = '"+funcionario+"'")
            self.banco.commit()
            return True
        else:
            tk.messagebox.showinfo(title="Aviso", message="Você não tem permissão para fazer isso.")
            return False

class Validadores:
    def formatCPF(self, event= None):
        cpf = self.cpf.get().replace(".","").replace("-","")[:11]
        cpf_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(cpf)):
            if not cpf[num] in "0123456789":
                continue
            if num in [2, 5]: 
                cpf_formatado += cpf[num] + "."
            elif num == 8:
                cpf_formatado += cpf[num] + "-"
            else:
                cpf_formatado += cpf[num]

        self.cpf.delete(0, "end")
        self.cpf.insert(0, cpf_formatado)

    def formatNASC(self, event= None):
        nasc = self.nascimento.get().replace("/","")[:8]
        nasc_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(nasc)):
            if not nasc[num] in "0123456789":
                continue
            if num in [1, 3]:
                nasc_formatado += nasc[num] + "/"
            else:
                nasc_formatado += nasc[num]

        self.nascimento.delete(0, "end")
        self.nascimento.insert(0, nasc_formatado)

    def formatDataInicio(self, event= None):
        DataInicio = self.data_inicio.get().replace("/","")[:8]
        DataInicio_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(DataInicio)):
            if not DataInicio[num] in "0123456789":
                continue
            if num in [1, 3]:
                DataInicio_formatado += DataInicio[num] + "/"
            else:
                DataInicio_formatado += DataInicio[num]

        self.data_inicio.delete(0, "end")
        self.data_inicio.insert(0, DataInicio_formatado)

class Funcionalidades:
    def centralizar_tela(self, tela, h, w):
        largura = h
        altura = w

        largura_tela = tela.winfo_screenwidth()
        altura_tela = tela.winfo_screenheight()

        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        posicao = f"{largura}x{altura}+{x}+{y}"
        print(posicao)
        tela.geometry(posicao)

    def inverterData(self, datainvert):
        dataNaOrdem = datainvert
        dia = dataNaOrdem[:2]
        mes = dataNaOrdem[3:5]
        ano = dataNaOrdem[6:]
        dataBanco = ano + "-" + mes + "-" + dia
        return dataBanco
    
    def formatCPFFalta(self, event= None):
        cpf = self.cpfFunc.get().replace(".","").replace("-","")[:11]
        cpf_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(cpf)):
            if not cpf[num] in "0123456789":
                continue
            if num in [2, 5]: 
                cpf_formatado += cpf[num] + "."
            elif num == 8:
                cpf_formatado += cpf[num] + "-"
            else:
                cpf_formatado += cpf[num]

        self.cpfFunc.delete(0, "end")
        self.cpfFunc.insert(0, cpf_formatado)

    def formatDataFalta(self, event= None):
        faltaData = self.dataFalta.get().replace("/","")[:8]
        faltaData_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(faltaData)):
            if not faltaData[num] in "0123456789":
                continue
            if num in [1, 3]:
                faltaData_formatado += faltaData[num] + "/"
            else:
                faltaData_formatado += faltaData[num]

        self.dataFalta.delete(0, "end")
        self.dataFalta.insert(0, faltaData_formatado)

    def formatDataAdvertencia(self, event= None):
        AdvertenciaData = self.dataAdvertencia.get().replace("/","")[:8]
        AdvertenciaData_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(AdvertenciaData)):
            if not AdvertenciaData[num] in "0123456789":
                continue
            if num in [1, 3]:
                AdvertenciaData_formatado += AdvertenciaData[num] + "/"
            else:
                AdvertenciaData_formatado += AdvertenciaData[num]

        self.dataAdvertencia.delete(0, "end")
        self.dataAdvertencia.insert(0, AdvertenciaData_formatado)

    def formatDataSuspensao(self, event= None):
        SuspensaoData = self.dataSuspensao.get().replace("/","")[:8]
        SuspensaoData_formatado = ""

        if event.keysym.lower() == "backspace" : return

        for num in range(len(SuspensaoData)):
            if not SuspensaoData[num] in "0123456789":
                continue
            if num in [1, 3]:
                SuspensaoData_formatado += SuspensaoData[num] + "/"
            else:
                SuspensaoData_formatado += SuspensaoData[num]

        self.dataSuspensao.delete(0, "end")
        self.dataSuspensao.insert(0, SuspensaoData_formatado)

    def funcBtnCadastrar(self):
        try:
            self.cadastrar_Funcionario(self.cpf.get(), self.nome.get().title(), self.nascimento.get(), self.funcao.get(), self.data_inicio.get())
            tk.messagebox.showinfo(title="Aviso", message="Cadastro efetuado com sucesso!")
        except:
            tk.messagebox.showinfo(title="Aviso", message="Seu cadastro não foi efetuado, tente novamente.")

    def funcBtnAddFalta(self):
        self.telaAddFalta = ctk.CTkToplevel()
        # Propriedades da janela de AddFalta
        self.telaAddFalta.title("Adicionar Nova Falta")
        self.telaAddFalta.geometry("800x300")
        self.telaAddFalta.resizable(width=False, height=False)
        self.telaAddFalta.attributes("-topmost", True)
        #ENTRADAS
        textFalta = ctk.CTkLabel(master=self.telaAddFalta, text="CADASTRAR FALTA", font=("Helvetica", 18))
        textFalta.place(relx=0.1, rely=0.03, relheight=0.15)
        motivo = ctk.CTkEntry(master=self.telaAddFalta, placeholder_text="Motivo: ")
        motivo.place(relx=0.1, rely=0.19, relwidth=0.8, relheight=0.15)
        self.dataFalta = ctk.CTkEntry(master=self.telaAddFalta, placeholder_text="Data da Falta: ")
        self.dataFalta.bind("<KeyRelease>", self.formatDataFalta)
        self.dataFalta.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.15)
        self.atestado = tk.StringVar(value="off") # usar o .get() ao usar o valor da checkbox
        self.checkAtestado = ctk.CTkCheckBox(master=self.telaAddFalta, text="ATESTADO/DECLARAÇÃO ",variable=self.atestado, onvalue="on", offvalue="off")
        self.checkAtestado.place(relx=0.1, rely=0.51, relwidth=0.8, relheight=0.15)
        # BOTAO DE CADASTRAR FALTA
        btnCadastrFalta = ctk.CTkButton(master=self.telaAddFalta,text="CADASTRAR", command=lambda motivo=motivo, data=self.dataFalta, cpf=self.cpfFuncionario : (self.add_Falta(motivo, data, cpf), self.telaAddFalta.destroy()))
        btnCadastrFalta.place(relx=0.1, rely=0.73, relwidth=0.8, relheight=0.15)
        
    def funcBtnAddAdvertencia(self):
        self.telaAddAdvertencia = ctk.CTkToplevel()
        # Propriedades da janela de AddAdvertencia
        self.telaAddAdvertencia.title("Adicionar Nova Advertência")
        self.telaAddAdvertencia.geometry("800x300")
        self.telaAddAdvertencia.resizable(width=False, height=False)
        self.telaAddAdvertencia.attributes("-topmost", True)
        #ENTRADAS
        textAdvertencia = ctk.CTkLabel(master=self.telaAddAdvertencia, text="CADASTRAR ADVERTÊNCIA", font=("Helvetica", 18))
        textAdvertencia.place(relx=0.1, rely=0.03, relheight=0.15)
        motivo = ctk.CTkEntry(master=self.telaAddAdvertencia, placeholder_text="Motivo: ")
        motivo.place(relx=0.1, rely=0.19, relwidth=0.8, relheight=0.15)
        self.dataAdvertencia = ctk.CTkEntry(master=self.telaAddAdvertencia, placeholder_text="Data da Advertência: ")
        self.dataAdvertencia.bind("<KeyRelease>", self.formatDataAdvertencia)
        self.dataAdvertencia.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.15)
        # BOTAO DE CADASTRAR ADVERTÊNCIA
        btnCadastrAdvertencia = ctk.CTkButton(master=self.telaAddAdvertencia,text="CADASTRAR", command=lambda motivo=motivo, data=self.dataAdvertencia, cpf=self.cpfFuncionario : (self.add_Advertencia(motivo, data, cpf), self.telaAddAdvertencia.destroy()))
        btnCadastrAdvertencia.place(relx=0.1, rely=0.73, relwidth=0.8, relheight=0.15)

    def funcBtnAddSuspensao(self):
        self.telaAddSuspensao = ctk.CTkToplevel()
        # Propriedades da janela de AddSuspensão
        self.telaAddSuspensao.title("Adicionar Nova Suspensão")
        self.telaAddSuspensao.geometry("800x300")
        self.telaAddSuspensao.resizable(width=False, height=False)
        self.telaAddSuspensao.attributes("-topmost", True)
        #ENTRADAS
        textSuspensao = ctk.CTkLabel(master=self.telaAddSuspensao, text="CADASTRAR SUSPENSÃO", font=("Helvetica", 18))
        textSuspensao.place(relx=0.1, rely=0.03, relheight=0.15)
        motivo = ctk.CTkEntry(master=self.telaAddSuspensao, placeholder_text="Motivo: ")
        motivo.place(relx=0.1, rely=0.19, relwidth=0.8, relheight=0.15)
        self.dataSuspensao = ctk.CTkEntry(master=self.telaAddSuspensao, placeholder_text="Data da Suspensão: ")
        self.dataSuspensao.bind("<KeyRelease>", self.formatDataSuspensao)
        self.dataSuspensao.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.15)
        # BOTAO DE CADASTRAR SUSPENSÃO
        btnCadastrSuspensao = ctk.CTkButton(master=self.telaAddSuspensao,text="CADASTRAR", command=lambda motivo=motivo, data=self.dataSuspensao, cpf=self.cpfFuncionario : (self.add_Suspensao(motivo, data, cpf), self.telaAddSuspensao.destroy()))
        btnCadastrSuspensao.place(relx=0.1, rely=0.73, relwidth=0.8, relheight=0.15)
        
    def funcBtnLogin(self, user, senha):
        login = BancoDeDados.entrar(self=BancoDeDados,usuario=user, senha=senha)
        if login == True:
            self.telaLogin.destroy()
            tk.messagebox.showinfo(title="Aviso", message=f"Bem vindo {current_user}!")
            app = App()
            app.run()
        elif login == False:
            tk.messagebox.showinfo(title="Aviso", message="Usuário ou senha incorretas, tente novamente.")
         
    def funcBtnDelFuncionario(self, resp):
        # Função de deletar
        if resp == True:
            delete = BancoDeDados.delFuncionario(self=BancoDeDados, funcionario=self.cpfFuncionario)
            if delete == True:
                tk.messagebox.showinfo(title="Aviso", message="Esse funcionário foi deletado permanentemente.")
            elif delete == False:
                tk.messagebox.showinfo(title="Aviso", message="Esse funcionário não deletado corretamente.")
        elif resp == False:
            tk.messagebox.showinfo(title="Aviso", message="Esse funcionário NÃO foi deletado.")

class TelaLogin(BancoDeDados, Validadores, Funcionalidades):
    def __init__(self):
        self.conectarBanco()
        self.telaLogin = ctk.CTk()
        self.propriedadesTelaLogin()
        self.elementosTelaLogin()

    def propriedadesTelaLogin(self):
        self.telaLogin.title("Login")
        #self.telaLogin.geometry("400x200")
        self.telaLogin.resizable(width=False, height=False)
        self.telaLogin._set_appearance_mode("dark")
        self.centralizar_tela(self.telaLogin, 400, 200)

    def elementosTelaLogin(self):
        # TEXTO: Login
        textLogin = ctk.CTkLabel(master=self.telaLogin, text="Login",font=("Helvetica", 24))
        textLogin.place(relx=0.445, rely=0.05)
        # Entrada de usuário
        textUser = ctk.CTkLabel(master=self.telaLogin, text="Usuário:",font=("Helvetica", 15))
        textUser.place(relx=0.15, rely=0.25)
        user = ctk.CTkEntry(master=self.telaLogin, placeholder_text="Insira seu usuário", width=220)
        user.place(relx=0.30, rely=0.25)
        # Entrada de senha
        textPass = ctk.CTkLabel(master=self.telaLogin, text="Senha:",font=("Helvetica", 15))
        textPass.place(relx=0.17, rely=0.41)
        password = ctk.CTkEntry(master=self.telaLogin, placeholder_text="Insira sua senha", show="*",width=220)
        password.place(relx=0.30, rely=0.41)
        # Botão de Login
        btnLog = ctk.CTkButton(master=self.telaLogin, text="LOGIN", height=35,width=150, command= lambda usuario=user, senha=password:(self.funcBtnLogin(usuario, senha)))
        btnLog.place(relx=0.325, rely=0.63)

    def run(self):
        self.telaLogin.mainloop()

class App(BancoDeDados, Validadores, Funcionalidades):
    def __init__(self):
        self.conectarBanco()
        self.janela = ctk.CTk()
        self.propriedadesJanela()
        self.framePrincipal()
        self.user()
        self.abas()
        self.frameBotoesFuncionarios()
        self.frameSelecioneFuncionario()
        self.abaCadastrarFuncionários()
        self.abaOcorrencias()

    def propriedadesJanela(self):
        self.janela.title("Sistema")
        #self.janela.geometry("1280x720")
        self.janela.resizable(width=False, height=False)
        self.janela._set_appearance_mode("dark")
        self.centralizar_tela(self.janela, 1280, 720)

    def framePrincipal(self):
        self.framePrincipal = ctk.CTkFrame(master=self.janela, width=1280, height=720)
        self.framePrincipal.place(relx=0, rely=0, relheight=1, relwidth=1)

    def user(self):
        textUser = ctk.CTkLabel(master=self.framePrincipal, text= f"Usuário: {current_user}", font=("Helvetica", 15))
        textUser.place(relx=0.005, rely=0.0)

    def abas(self):
        self.abas = ctk.CTkTabview(master=self.framePrincipal, width=1280, height=900)
        self.abas.place(relx=0, rely=0.03)
        self.abas.add("Funcionários")
        self.abas.add("Cadastrar Funcionários")
        self.abas.add("Ocorrências")

    def frameBotoesFuncionarios(self):
        # Frame dos Botões de funcionários
        self.frameFuncionarios = ctk.CTkFrame(master=self.abas.tab("Funcionários"))
        self.frameFuncionarios.place(relx=0, rely=0, relwidth=0.30, relheight=0.79)
        # Tela c/ Scroll com os botões dos funcionários
        self.telaFuncionarios = ctk.CTkScrollableFrame(master=self.frameFuncionarios)
        self.telaFuncionarios.place(relx=0, rely=0, relwidth=1, relheight=0.98)

        # Botões dos funcionários
        for func in self.btns_Funcionarios():
            botaoFunc = ctk.CTkButton(
                master=self.telaFuncionarios,
                text=str(func[0]), 
                height=35, width=350, 
                command=lambda nome=str(func[0]): (self.selecionarFuncionario(nome), self.frameInfos.destroy()))
            botaoFunc.pack()
    
    def frameSelecioneFuncionario(self):
        self.frameInfos = ctk.CTkFrame(master=self.abas.tab("Funcionários"), height=800, width=900)
        self.frameInfos.place(relx=0.32, rely=0, relwidth=0.67, relheight= 0.765)
        # Texto no frame
        self.texto = ctk.CTkLabel(master=self.frameInfos, text="Selecione um funcionário", anchor="center", font=("Helvetica", 32))
        self.texto.pack(expand=True, fill="both", padx=10, pady=10)

    def frameInfosFuncionarios(self):
        # Frame das informações dos funcionários
        self.frameInfos = ctk.CTkFrame(master=self.abas.tab("Funcionários"), height=800, width=900)
        self.frameInfos.place(relx=0.32, rely=0.02, relwidth=0.67, relheight= 0.97)

    def abaCadastrarFuncionários(self):
        # Entrada do CPF
        self.cpf = ctk.CTkEntry(master=self.abas.tab("Cadastrar Funcionários"), placeholder_text="CPF: 000.000.000-00", width=400, height=35)
        self.cpf.bind("<KeyRelease>", self.formatCPF)
        self.cpf.pack(pady=2)
        # Entrada do nome
        self.nome = ctk.CTkEntry(master=self.abas.tab("Cadastrar Funcionários"), placeholder_text="Nome do Funcionário: ", width=400, height=35)
        self.nome.pack(pady=2)
        # Entrada da data de nascimento
        self.nascimento = ctk.CTkEntry(master=self.abas.tab("Cadastrar Funcionários"), placeholder_text="Data de nascimento:", width=400, height=35)
        self.nascimento.bind("<KeyRelease>", self.formatNASC)
        self.nascimento.pack(pady=2)
        # Entrada da função do funcionário
        self.funcao = tk.StringVar(value='')
        self.funcao_btn = ctk.CTkComboBox(master=self.abas.tab("Cadastrar Funcionários"), values=["Estagiário 6h30", "Estagiário 7h", "CLT", "Backoffice", "TI", "ADM"],
                                      variable=self.funcao, width=400, height=35, state='readonly')
        self.funcao_btn.pack(pady=2)
        # Entrada da data de inicio do funcionário
        self.data_inicio = ctk.CTkEntry(master=self.abas.tab("Cadastrar Funcionários"), placeholder_text="Data de contratação:", width=400, height=35)
        self.data_inicio.bind("<KeyRelease>", self.formatDataInicio)
        self.data_inicio.pack(pady=2)
        # Botão de cadastrar
        self.botao_Cadastro = ctk.CTkButton(master=self.abas.tab("Cadastrar Funcionários"), text="CADASTRAR", width=250, height=35, command=self.funcBtnCadastrar)
        self.botao_Cadastro.pack(pady=2)

    def selecionarFuncionario(self, funcionario):
        infos = self.mostrar_Funcionario(funcionario)
        print(infos, type(infos))
        self.frameFuncs = ctk.CTkFrame(master=self.abas.tab("Funcionários"), height=800, width=900)
        self.frameFuncs.place(relx=0.32, rely=0, relwidth=0.65, relheight=0.35)
        # Informações dos funcionários
        self.nomeFuncionario = str(infos[0])
        self.cpfFuncionario = str(infos[1])
        self.nascimentoFuncionario = str(infos[2])
        self.funcaoFuncionario = str(infos[3])
        self.dataInicioFuncionario = str(infos[4])
        # NOME
        textNome = ctk.CTkLabel(master=self.frameFuncs, text= "Nome: ", width=150, anchor="w")
        textNome.grid(row=0, column=0, sticky="w", padx=10)
        name = ctk.CTkLabel(master=self.frameFuncs, text=self.nomeFuncionario)
        name.grid(row=0, column=1, sticky="w")
        # CPF
        textCPF = ctk.CTkLabel(master=self.frameFuncs, text= "CPF: ", width=150, anchor="w")
        textCPF.grid(row=1, column=0, sticky="w", padx=10)
        cpf = ctk.CTkLabel(master=self.frameFuncs, text=self.cpfFuncionario)
        cpf.grid(row=1, column=1, sticky="w")
        # DATA DE NASCIMENTO
        textNascimento = ctk.CTkLabel(master=self.frameFuncs, text= "Data de nascimento: ", width=150, anchor="w")
        textNascimento.grid(row=2, column=0, sticky="w", padx=10)
        nascimento =  ctk.CTkLabel(master=self.frameFuncs, text=self.nascimentoFuncionario)
        nascimento.grid(row=2, column=1, sticky="w")
        # FUNÇÃO DA PESSOA NA EMPRESA
        textFuncao = ctk.CTkLabel(master=self.frameFuncs, text= "Função: ", width=150, anchor="w")
        textFuncao.grid(row=3, column=0, sticky="w", padx=10)
        funcao = ctk.CTkLabel(master=self.frameFuncs, text=self.funcaoFuncionario)
        funcao.grid(row=3, column=1, sticky="w")
        # DATA DE INÍCIO DA PESSOA NA EMPRESA
        textDataInicio = ctk.CTkLabel(master=self.frameFuncs, text= "Data de Início: ", width=150, anchor="w")
        textDataInicio.grid(row=4, column=0, sticky="w", padx=10)
        DataInicio = ctk.CTkLabel(master=self.frameFuncs, text=self.dataInicioFuncionario)
        DataInicio.grid(row=4, column=1, sticky="w")
        # CONTADOR DE FALTAS E ADVERTÊNCIAS
        textFaltas = ctk.CTkLabel(master=self.frameFuncs, text="Faltas: ", width=150, anchor="w")
        textFaltas.grid(row=5, column=0, sticky="w", padx=10)
        contadorFaltas = ctk.CTkLabel(master=self.frameFuncs, text=self.contFaltas(self.cpfFuncionario), width=150, anchor="w")
        contadorFaltas.grid(row=5, column=1, sticky="w")
        textAdvertencias = ctk.CTkLabel(master=self.frameFuncs, text="Advertências: ", width=150, anchor="w")
        textAdvertencias.grid(row=6, column=0, sticky="w", padx=10)
        contadorAdvertencias = ctk.CTkLabel(master=self.frameFuncs, text=self.contAdvertencias(self.cpfFuncionario), width=150, anchor="w")
        contadorAdvertencias.grid(row=6, column=1, sticky="w")
        textSuspensao = ctk.CTkLabel(master=self.frameFuncs, text="Suspensões: ", width=150, anchor="w")
        textSuspensao.grid(row=7, column=0, sticky="w", padx=10)
        contadorSuspensao = ctk.CTkLabel(master=self.frameFuncs, text=self.contSuspensao(self.cpfFuncionario), width=150, anchor="w")
        contadorSuspensao.grid(row=7, column=1, sticky="w")
        # Botão de deletar funcionários
        self.btnDelFuncionarios = ctk.CTkButton(master=self.frameFuncs, text="Deletar Funcionário", command=self.telaConfDelFuncionario)
        self.btnDelFuncionarios.place(relx=0.80, rely=0.73, relwidth=0.19)
        # ABAS DE PUNIÇÃO
        self.punicaoFuncionarios()

    def punicaoFuncionarios(self):
        # Frame com as abas de punição
        self.framePunicao = ctk.CTkFrame(master=self.abas.tab("Funcionários"))
        self.framePunicao.place(relx=0.32, rely=0.30, relwidth=0.65, relheight=0.455)
        # Adicionando abas de Falta e Advertencias
        self.abaPunicao = ctk.CTkTabview(master=self.framePunicao, height=468, width=900)
        self.abaPunicao.place(relx=0, rely=0)
        self.abaPunicao.add("Faltas")
        self.abaPunicao.add("Advertências")
        self.abaPunicao.add("Suspensões")
        self.abaFaltas()
        self.abaAdvertencias()
        self.abaSuspensoes()

    def telaConfDelFuncionario(self):
        self.telaConfDel = ctk.CTkToplevel()
        # Propriedades da Tela de Confirmação
        self.telaConfDel.title("Confirmar")
        #self.telaConfDel.geometry("400x150")
        self.telaConfDel.resizable(width=False, height=False)
        self.telaConfDel.attributes("-topmost", True)
        self.centralizar_tela(self.telaConfDel, 400, 150)
        # Elementos da tela de confirmação
        textConf = ctk.CTkLabel(master=self.telaConfDel, text=f"Tem certeza que deseja deletar {self.nomeFuncionario}?")
        textConf.place(relx=0.17, rely=0.10, relwidth=0.66)
        btnNao = ctk.CTkButton(master=self.telaConfDel, text="NÃO", command=lambda resp=False:(self.telaConfDel.destroy(), self.funcBtnDelFuncionario(resp) ))
        btnNao.place(relx=0.10, rely=0.45)
        btnSim = ctk.CTkButton(master=self.telaConfDel, text="SIM", command=lambda resp=True:(self.telaConfDel.destroy(), self.funcBtnDelFuncionario(resp)))
        btnSim.place(relx=0.55, rely=0.45)

    def abaOcorrencias(self):
        # Frame de Ocorrencias
        self.textOcorrencias = ctk.CTkLabel(master=self.abas.tab("Ocorrências"), text="OCORRÊNCIAS:", font=("Helvetica", 32))
        self.textOcorrencias.place(relx=0.024, rely=0.01)
        self.frameOcorrencias = ctk.CTkFrame(master=self.abas.tab("Ocorrências"), height=800, width=600)
        self.frameOcorrencias.place(relx=0.025, rely=0.05, relwidth=0.945, relheight=0.675)
        # Lista Ocorrencias
        self.listaOcorrencias = ttk.Treeview(master=self.abas.tab("Ocorrências"), height=19, column=("col1", "col2", "col3", "col4"))
        self.listaOcorrencias.place(relx=0.025, rely=0.05, relwidth=0.945, relheight=0.675)
        # CONFIGURAÇÃO DAS COLUNAS
        self.listaOcorrencias.heading("#0", text="")
        self.listaOcorrencias.heading("#1", text="TIPO")
        self.listaOcorrencias.heading("#2", text="DATA")
        self.listaOcorrencias.heading("#3", text="MOTIVO")
        self.listaOcorrencias.heading("#4", text="FUNCIONÁRIO")
        self.listaOcorrencias.column("#0", width=0)
        self.listaOcorrencias.column("#1", width=100)
        self.listaOcorrencias.column("#2", width=100)
        self.listaOcorrencias.column("#3", width=300)
        self.listaOcorrencias.column("#3", width=200)
        # MOSTRAR OCORRÊNCIAS NA TREEVIEW
        self.root.execute("SELECT tipo, motivo, data, cpf FROM punicao ORDER BY data DESC")
        ocorrencias = self.root.fetchall()
        for ocorr in ocorrencias:
            self.listaOcorrencias.insert("", "end", values=ocorr)

    def abaFaltas(self):
        # BOTÃO DE ADICIONAR FALTAS
        self.btnAddFaltas = ctk.CTkButton(master=self.abaPunicao.tab("Faltas"), text="Adicionar Falta", command=self.funcBtnAddFalta)
        self.btnAddFaltas.place(relx=0.01, rely=0, relwidth=0.3, relheight=0.06)
        # TREEVIEW QUE MOSTRA AS FALTAS
        self.listaFaltas = ttk.Treeview(master=self.abaPunicao.tab("Faltas"), height=19, column=("col1", "col2", "col3", "col4"))
        self.listaFaltas.place(relx=0.01, rely=0.07, relwidth=0.959, relheight=0.97)
        # CONFIGURAÇÃO DAS COLUNAS
        self.listaFaltas.heading("#0", text="")
        self.listaFaltas.heading("#1", text="TIPO")
        self.listaFaltas.heading("#2", text="DATA")
        self.listaFaltas.heading("#3", text="MOTIVO")
        self.listaFaltas.heading("#4", text="FUNCIONÁRIO")
        self.listaFaltas.column("#0", width=0)
        self.listaFaltas.column("#1", width=100)
        self.listaFaltas.column("#2", width=100)
        self.listaFaltas.column("#3", width=300)
        self.listaFaltas.column("#3", width=200)
        # SCROLL DA TREEVIEW DAS FALTAS
        self.scrollFaltas = tk.Scrollbar(master=self.abaPunicao.tab("Faltas"), orient="vertical")
        self.listaFaltas.configure(yscrollcommand=self.scrollFaltas.set)
        self.scrollFaltas.place(relx=0.96, rely=0.07, relwidth=0.03, relheight=0.97)
        # MOSTRAR FALTAS NA TREEVIEW
        tipo = "FALTA"
        self.root.execute("SELECT tipo, motivo, data, cpf FROM punicao WHERE tipo = '"+tipo+"' AND cpf = '"+self.cpfFuncionario+"' ORDER BY data")
        faltas = self.root.fetchall()
        for falta in faltas:
            self.listaFaltas.insert("", "end", values=falta)

    def abaAdvertencias(self):
        # BOTÃO DE ADICIONAR ADVERTÊNCIAS
        self.btnAddAdvertencias = ctk.CTkButton(master=self.abaPunicao.tab("Advertências"), text="Adicionar Advertência", command=self.funcBtnAddAdvertencia)
        self.btnAddAdvertencias.place(relx=0.01, rely=0, relwidth=0.3, relheight=0.06)
        # TREEVIEW QUE MOSTRA AS ADVERTÊNCIAS
        self.listaAdvertencias = ttk.Treeview(master=self.abaPunicao.tab("Advertências"), height=19, column=("col1", "col2", "col3", "col4"))
        self.listaAdvertencias.place(relx=0.01, rely=0.07, relwidth=0.959, relheight=0.97)
        # CONFIGURAÇÃO DAS COLUNAS
        self.listaAdvertencias.heading("#0", text="")
        self.listaAdvertencias.heading("#1", text="TIPO")
        self.listaAdvertencias.heading("#2", text="DATA")
        self.listaAdvertencias.heading("#3", text="MOTIVO")
        self.listaAdvertencias.heading("#4", text="FUNCIONÁRIO")
        self.listaAdvertencias.column("#0", width=0)
        self.listaAdvertencias.column("#1", width=100)
        self.listaAdvertencias.column("#2", width=100)
        self.listaAdvertencias.column("#3", width=300)
        self.listaAdvertencias.column("#3", width=200)
        # SCROLL DA TREEVIEW DAS ADVERTÊNCIAS
        self.scrollAdvertencias = tk.Scrollbar(master=self.abaPunicao.tab("Advertências"), orient="vertical")
        self.listaAdvertencias.configure(yscrollcommand=self.scrollAdvertencias.set)
        self.scrollAdvertencias.place(relx=0.96, rely=0.07, relwidth=0.03, relheight=0.97)
        # MOSTRAR ADVERTÊNCIAS NA TREEVIEW
        tipo = "ADVERTÊNCIA"
        self.root.execute("SELECT tipo, motivo, data, cpf FROM punicao WHERE tipo = '"+tipo+"' AND cpf = '"+self.cpfFuncionario+"'")
        advertencias = self.root.fetchall()
        for adv in advertencias:
            self.listaAdvertencias.insert("", "end", values=adv)

    def abaSuspensoes(self):
        # BOTÃO DE ADICIONAR SUSPENSÕES
        self.btnAddSuspensoes = ctk.CTkButton(master=self.abaPunicao.tab("Suspensões"), text="Adicionar Suspensão", command=self.funcBtnAddSuspensao)
        self.btnAddSuspensoes.place(relx=0.01, rely=0, relwidth=0.3, relheight=0.06)
        # TREEVIEW QUE MOSTRA AS SUSPENSÕES
        self.listaSuspensoes = ttk.Treeview(master=self.abaPunicao.tab("Suspensões"), height=19, column=("col1", "col2", "col3", "col4"))
        self.listaSuspensoes.place(relx=0.01, rely=0.07, relwidth=0.959, relheight=0.97)
        # CONFIGURAÇÃO DAS COLUNAS
        self.listaSuspensoes.heading("#0", text="")
        self.listaSuspensoes.heading("#1", text="TIPO")
        self.listaSuspensoes.heading("#2", text="DATA")
        self.listaSuspensoes.heading("#3", text="MOTIVO")
        self.listaSuspensoes.heading("#4", text="FUNCIONÁRIO")
        self.listaSuspensoes.column("#0", width=0)
        self.listaSuspensoes.column("#1", width=100)
        self.listaSuspensoes.column("#2", width=100)
        self.listaSuspensoes.column("#3", width=300)
        self.listaSuspensoes.column("#3", width=200)
        # SCROLL DA TREEVIEW DAS SUSPENSÕES
        self.scrollSuspensoes = tk.Scrollbar(master=self.abaPunicao.tab("Suspensões"), orient="vertical")
        self.listaSuspensoes.configure(yscrollcommand=self.scrollSuspensoes.set)
        self.scrollSuspensoes.place(relx=0.96, rely=0.07, relwidth=0.03, relheight=0.97)
        # MOSTRAR SUSPENSÕES NA TREEVIEW
        tipo = "SUSPENSÃO"
        self.root.execute("SELECT tipo, motivo, data, cpf FROM punicao WHERE tipo = '"+tipo+"' AND cpf = '"+self.cpfFuncionario+"'")
        suspensoes = self.root.fetchall()
        for susp in suspensoes:
            self.listaSuspensoes.insert("", "end", values=susp)

    def run(self):
        self.janela.mainloop()

log = TelaLogin()
log.run()
