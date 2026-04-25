from playwright.sync_api import sync_playwright
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import font
import os
import subprocess


class RoboProcedures():
    
    def __init__(self, master):
        self.pw = ''
        self.navegador = ''
        self.contexto = ''
        self.pagina = ''

        self.manual_procedures = []
        self.pacote_procedures = []
        self.xl = 0
        self.itens = ""

        self.master = master
        self.senha_usuario_protheus = tk.Entry(master, show="*")
        self.senha_usuario_protheus.grid(row=3, column=1) 

        self.entrada_usuario_protheus = tk.Entry(master)
        self.entrada_usuario_protheus.grid(row=2, column=1, padx=1)

        self.entrada_usuario_portal = tk.Entry(master)
        self.entrada_usuario_portal.grid(row=5, column=1, padx=1)

        self.senha_usuario_portal = tk.Entry(master, show="*") 
        self.senha_usuario_portal.grid(row=6, column=1)

        self.entrada_pasta = tk.Entry(master) 
        self.entrada_pasta.grid(row=8, column=0)


    def verifica_campos(self):
        try:
            if self.entrada_pasta.get() != "" and self.senha_usuario_portal.get() != "" and self.entrada_usuario_portal.get() != "" and self.entrada_usuario_protheus.get() != "" and self.senha_usuario_protheus.get() != "":
                self.abrir_webagent()
                self.login()
                self.navegar_procedures()
                time.sleep(1)
                self.consultando_procedures()
                time.sleep(0.5)
                self.mov_direita_botao()
                time.sleep(0.5)
                self.consultando_procedures()
                if self.validar_seleciona():
                    self.seleciona_procedures()
                    time.sleep(1)
                    self.mov_esquerda_botao()
                    time.sleep(1)
                    self.seleciona_procedures()
                    time.sleep(1)
                    self.mov_esquerda_botao()
                    time.sleep(1)
                    self.seleciona_procedures()
                    self.instalando_procedures()
                else:
                    label_procedures = tk.Label(text="Finalizado!", font=fonte_subtitulos)
                    label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
                    self.navegador.close()
                    self.pw.stop()
            else:
                label_procedures = tk.Label(text="Preencha todos os campos!", font=fonte_subtitulos)
                label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
        except:    
            label_procedures = tk.Label(text="Ocorreu um Erro Interno.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            raise
        

    def selecionar_pasta(self):
        try:
            pasta = filedialog.askdirectory(title="Selecione onde será salvo os Pacotes de Atualização")
            if pasta:
                self.entrada_pasta.delete(0, tk.END)
                self.entrada_pasta.insert(0, pasta)
        except:
            raise



    def login(self):
        try:
            self.pw = sync_playwright().start()
            self.navegador = self.pw.chromium.launch(
            headless=False,
            channel="msedge",
            args=["--start-maximized"])
            self.contexto = self.navegador.new_context(no_viewport=True)
            self.pagina = self.contexto.new_page()
        
            self.pagina.goto("https://172.16.11.41:11000/webapp/")
            self.pagina.get_by_role("group", name="Programa Inicial").get_by_role("textbox").fill("SIGACFG")
            self.pagina.get_by_role("button", name="Ok").click()



            self.pagina.frame_locator("iframe") \
            .get_by_role("textbox", name="Insira seu usuário") \
            .fill(self.entrada_usuario_protheus.get())

            self.pagina.frame_locator("iframe") \
            .get_by_role("textbox", name="Insira sua senha")\
            .fill(self.senha_usuario_protheus.get())

            self.pagina.frame_locator("iframe") \
            .get_by_role("button", name="Entrar").click()\
            
            time.sleep(4)

            self.pagina.frame_locator("iframe") \
            .get_by_role("button", name="Entrar").click()\
            
            self._fechar_alertas()
            time.sleep(1)
            self._fechar_alertas()
        except:
            label_procedures = tk.Label(text="Erro no Login! Verificar Credenciais.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise
            


    def navegar_procedures(self):
        try:
            self.pagina.get_by_text("Base de Dados (4)").click()
            time.sleep(2)
            self.pagina.get_by_text("Dicionário (10)").click()
            time.sleep(2)
            self.pagina.get_by_text("Stored Procedure").click()
            self._fechar_alertas()
        except:
            label_procedures = tk.Label(text="Ocorreu um Erro.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise
            

    def esperar_itens(self):
        try:
            self.itens = self.pagina.locator("table tbody tr:has(td:nth-child(4))")
            while self.itens.count() == 0:
                time.sleep(1)
                self.itens = self.pagina.locator("table tbody tr:has(td:nth-child(4))")
            return
        except:
            self.navegador.close()
            self.pw.stop()
            raise

    def consultando_procedures(self):
        try:
            self.esperar_itens()

            for i in range(self.itens.count()):
                linha = self.itens.nth(i)
                texto = linha.inner_text()

                if "Não instalado" in texto or "Desatualizado" in texto:
                    texto_tratado = texto.split("\n")[-1].strip()
                    time.sleep(0.5)
                    linha.get_by_text(texto_tratado).dblclick()

                    while (self.pagina.get_by_role("button", name="Cancelar").count()) == 0:
                        time.sleep(0.5) #Esperar abrir o grid com a visualização das atualizações
                    
                    botao = self.pagina.locator("wa-button[caption='Buscar atualização']:not([disabled])")
                    botao = botao.nth(0)


                    if botao.count() > 0 and "Não instalado" in texto: ##--> 1 - Nesse ponto eu tenho que ver como vou fazer o processo de abrir e salvar numa pasta o arquivo da procedure em questão

                        botao.click()
                        time.sleep(0.5)
                        self.pagina.locator("input").last.wait_for()
                        time.sleep(0.5)
                        valor = self.pagina.locator("input").last.input_value()
                        time.sleep(1)

                        if 'https://' in valor:
                            
                            pagina2 = self.contexto.new_page()
                            pagina2.goto(valor, timeout=60000)

                            
                            if self.xl == 0:
                                pagina2.get_by_role("textbox", name="Você está em um campo para login").fill(self.entrada_usuario_portal.get())
                                pagina2.get_by_role("textbox", name="Você está em um campo para senha").fill(self.senha_usuario_portal.get())
                                pagina2.get_by_role("button", name="Botão para confirmação das").click()

                            with pagina2.expect_download() as download_info:
                                pagina2.get_by_role("button", name="Fazer Download").click()

                            download = download_info.value
                            download.save_as(f"{self.entrada_pasta.get()}/{download.suggested_filename}")
                    
                            pagina2.close()
                            time.sleep(1)
                            fechar = self.pagina.get_by_role("button", name="fechar")
                            if fechar.count() > 0:
                                fechar.click()
                            time.sleep(3)
                            self.pagina.get_by_role("button", name="Cancelar").click()
                            self.xl += 1
                            self.pacote_procedures.append(texto_tratado)
                        else:
                            fechar = self.pagina.get_by_role("button", name="fechar")
                            if fechar.count() > 0:
                                fechar.click()
                            self.pagina.get_by_role("button", name="Cancelar").click()

                    elif "Desatualizado" in texto:
                        self.manual_procedures.append(texto_tratado)
                        self.pagina.get_by_role("button", name="Cancelar").click()
                    else:
                        self.pagina.get_by_role("button", name="Cancelar").click()
        except:
            label_procedures = tk.Label(text="Erro no Login! Verificar Credenciais.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise

    def mov_direita_botao(self):
        try:
            self.pagina.locator("#COMP6152 > button").click()
            time.sleep(1)
        except:
            label_procedures = tk.Label(text="Ocorreu um Erro. Entrar em Contato com o Desenvolvedor.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise

    def validar_seleciona(self):
        try:
            if len(self.manual_procedures) != 0:
                return True
            else:
                return False
        except:
            self.navegador.close()
            self.pw.stop()
            raise
    
    def seleciona_procedures(self):
            try:  
                grid = self.pagina.locator('#COMP6135')
                labels = grid.locator('table tbody tr td div > label')
                for i in range(labels.count()):
                    label = labels.nth(i)
                    texto = label.inner_text()
                    if (texto.strip()) in self.manual_procedures:
                        tr = label.locator("xpath=ancestor::tr")
                        time.sleep(0.5)
                        primeiro_td = tr.locator("td:nth-child(1)")
                        time.sleep(0.5)
                        primeiro_td.click()
                        time.sleep(1)
                        primeiro_td.dblclick()
            except:
                label_procedures = tk.Label(text="Ocorreu um Erro. Entrar em Contato com o Desenvolvedor.", font=fonte_subtitulos)
                label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
                self.navegador.close()
                self.pw.stop()
                raise


    def mov_esquerda_botao(self):
        try:
            self.pagina.locator("#COMP6133 > button").click()
        except:    
            label_procedures = tk.Label(text="Ocorreu um Erro. Entrar em Contato com o Desenvolvedor.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise

    def instalando_procedures(self):
        try:
            #Desinstalando todas efetivamente
            self.pagina.locator(".image-cell").first.click()
            self.pagina.locator(".image-cell").first.dblclick()
            time.sleep(0.5)
            self.pagina.locator("#COMP6061 > button").dblclick()
            time.sleep(0.5)
            self.pagina.get_by_role("button", name="Sim").click()
            time.sleep(0.5)
            self.pagina.get_by_role("button", name="Fechar").click()
            time.sleep(0.5)
            self.pagina.locator("#COMP6060 > button").dblclick()
            time.sleep(0.5)
            self.pagina.get_by_role("button", name="Sim").click()
            time.sleep(0.5)
            self.pagina.get_by_role("button", name="Fechar").click()
            self.navegador.close()
            self.pw.stop()
            label_procedures = tk.Label(text="Finalizado!", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
        except:
            label_procedures = tk.Label(text="Ocorreu um Erro. Entrar em Contato com o Desenvolvedor.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise

    def _fechar_alertas(self):
        try:
            for i in range(5):
                if self.pagina.get_by_role("button", name="Cancelar").count() > 0:
                    self.pagina.get_by_role("button", name="Cancelar").click()
                    return
                elif self.pagina.get_by_role("button", name="Fechar").count() > 0:
                    self.pagina.get_by_role("button", name="Fechar").click()
                    return
                time.sleep(1)
            return
        except:
            label_procedures = tk.Label(text="Ocorreu um Erro. Entrar em Contato com o Desenvolvedor.", font=fonte_subtitulos)
            label_procedures.grid(row=10, column=0, pady = 5, sticky="nswe", columnspan=2)
            self.navegador.close()
            self.pw.stop()
            raise

    def abrir_webagent(self):
        caminhos = [
            r"C:\TOTVS",
            r"C:\Arquivos de Programas",
            r"C:\Arquivos de Programas (x86)",
            os.environ.get("LOCALAPPDATA") ##local padrao
        ]

        for base in caminhos:
            if not base or not os.path.exists(base):
                continue

            for pasta_atual, diretorios, arquivos in os.walk(base):
                for arquivo in arquivos:
                    if arquivo.lower() == "web-agent.exe":
                        caminho_agent = os.path.join(pasta_atual, arquivo)
                        os.startfile(caminho_agent)
                        return
        return
    



janela = tk.Tk()
robo_procedures = RoboProcedures(janela)


fonte_titulo = font.Font(family="Arial", size=11, weight="bold")
fonte_subtitulos = font.Font(family="Arial", size=9)

janela.title("Ferramenta de Automacao Procedures")

label_procedures = tk.Label(text="Atualização Procedures", borderwidth=2, font=fonte_titulo)
label_procedures.grid(row=0, column=0, padx=15, pady=15, sticky="nswe", columnspan=2)

label_procedures = tk.Label(text="Acesso Protheus", font=fonte_subtitulos)
label_procedures.grid(row=1, column=0, pady = 7, sticky="nswe", columnspan=2)

label_procedures = tk.Label(text="Usuário/ID")
label_procedures.grid(row=2, column=0, sticky="nswe", columnspan=1)


label_procedures = tk.Label(text="Senha") 
label_procedures.grid(row=3, column=0, sticky="nswe") 

label_procedures = tk.Label(text="Acesso Portal Totvs", font=fonte_subtitulos)
label_procedures.grid(row=4, column=0, pady = 7, sticky="nswe", columnspan=2)

label_procedures = tk.Label(text="E-mail")
label_procedures.grid(row=5, column=0, sticky="nswe", columnspan=1)


label_procedures = tk.Label(text="Senha") 
label_procedures.grid(row=6, column=0, sticky="nswe") 


label_procedures = tk.Label(text="Selecione Downloads", font=fonte_subtitulos)
label_procedures.grid(row=7, column=0, pady = 7, sticky="nswe", columnspan=2)


botao_pasta = tk.Button(text="Selecionar Pasta", command=robo_procedures.selecionar_pasta)
botao_pasta.grid(row=8, column=1, pady=5)

botao_executar = tk.Button(text="Executar", height=2, command=robo_procedures.verifica_campos)
botao_executar.grid(row=9, column=0, columnspan=2, padx=10, pady=20, sticky="nswe")

janela.mainloop()