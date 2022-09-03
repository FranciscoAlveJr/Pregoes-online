from time import sleep
from tkinter import ttk
import requests as rq
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from tkinter import *
from tkinter import scrolledtext
from subprocess import CREATE_NO_WINDOW
from sys import exit

url_ini = 'http://aquisicoes.seplag.mt.gov.br/sgc/faces/priv/comum/PrincipalAreaLicitante.jsp'

n = '0400168/2020'

l = 'michelmab'
s = 'Mic@1979'


class Pregao():

    def acesso(self):

        login = vlogin.get()
        senha = vsenha.get()
        codigo=vcodigo.get()
        janela.destroy()

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        service.creationflags = CREATE_NO_WINDOW
        self.driver = Chrome(service=service, options=options)
        

        self.driver.get(url_ini)

        wa = WebDriverWait(self.driver, 60)
        wa.until(EC.presence_of_all_elements_located((By.ID, 'loginForm:usuarioText')))

        write_login = self.driver.find_element(By.ID, 'loginForm:usuarioText')
        write_login.send_keys(login)

        write_senha = self.driver.find_element(By.ID, 'loginForm:senhaText')
        write_senha.send_keys(senha)

        btn_entrar = self.driver.find_element(By.ID, 'loginForm:loginButton')
        btn_entrar.click()

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[6]/div[1]/span')))
        proto_entr = self.driver.find_element(By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[6]/div[1]/span')
        proto_entr.click()

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[6]/div[2]/ul/li/a/span')))
        meus_proto = self.driver.find_element(By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[6]/div[2]/ul/li/a/span')
        meus_proto.click()

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/form/section[2]/div/div/fieldset/span/table/tbody/tr/td[1]/table/tbody/tr[2]/td/input')))
        por_processo = self.driver.find_element(By.XPATH, '/html/body/form/section[2]/div/div/fieldset/span/table/tbody/tr/td[1]/table/tbody/tr[2]/td/input')
        por_processo.click()

        sleep(1)

        info_proc = self.driver.find_element(By.XPATH, '/html/body/form/section[2]/div/div/fieldset/span/table/tbody/tr/td[2]/input')
        info_proc.send_keys(codigo)

        pesquisar_lo = self.driver.find_element(By.NAME, 'formMeusProtocolosPageList:pesquisarButton')
        pesquisar_lo.click()

        sleep(1)

        html = self.driver.page_source
        soup = bs(html, 'html.parser')
  
        self.pro_lotes = []
        self.lote_lista = soup.find('table', {'class': 'TabDadosFundo'}).find_all('tbody')[1].find_all('tr')
        for tr in self.lote_lista:
            lote = tr.find_all('td')[2]
            situacao = tr.find_all('td')[7]
            if situacao.text != 'Cancelado':
                self.pro_lotes.append(lote.text)
        
        print(self.pro_lotes)

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[4]/div[1]')))

        btn_pregoes = self.driver.find_element(By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[4]/div[1]')
        btn_pregoes.click()

        btn_participar = self.driver.find_element(By.XPATH, '/html/body/form/nav/div[1]/div[1]/div[4]/div[2]/ul/li[4]/a/span')
        btn_participar.click()

        btn_processo = self.driver.find_element(By.XPATH, '/html/body/form/section[2]/div/div/fieldset/table/tbody/tr[3]/td[2]/input')
        btn_processo.send_keys(codigo)

        btn_pesquisar = self.driver.find_element(By.NAME, 'formPregaoDiaPageList:pesquisarButton')
        btn_pesquisar.click()

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/form/section[2]/div/div/div[4]/table/tbody/tr/td[7]/a')))
        btn_visualizar = self.driver.find_element(By.XPATH, '/html/body/form/section[2]/div/div/div[4]/table/tbody/tr/td[7]/a')
        btn_visualizar.click()

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/fieldset[2]/div/table/tbody')))

        html = self.driver.page_source
        soup = bs(html, 'html.parser')

        self.des_lotes = []
        lista_lotes = soup.find('tbody', {'id':'listaLotesTbody'})
        self.tag_lotes = lista_lotes.find_all('a', {'class':'link'})
        for lo in self.tag_lotes:
            self.des_lotes.append(lo.text)

        wa.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/ul/li[3]/a')))
        aba_lances = self.driver.find_element(By.XPATH, '/html/body/ul/li[3]/a')
        aba_lances.click()

        # btn_parar.config(state=NORMAL)

        self.run = True

        self.tags = []
        for i in range(len(self.des_lotes)):
            if self.des_lotes[i] in self.pro_lotes:
                self.tags.append(self.tag_lotes[i])
        
        
        self.janela2()

    def lances(self):

        if self.run:
            self.btn_iniciar.after(1500, self.lances)
  
            html = self.driver.page_source
            soup = bs(html, 'html.parser')
            
            lance_off = 'labelLanceDesativado'
            lance_on = 'labelFormLance'

            random = soup.find_all('label', {'class':'labelFormRandAtivado'})

            html = self.driver.page_source
            soup = bs(html, 'html.parser')

            print(self.des_lotes)
            print(self.pro_lotes)
            print(self.tags)

            for i in range(len(self.pro_lotes)):
                try:
                    id = self.tags[i]['id'][self.tags[i]['id'].find('e')+1:]
                    print(id)
                    
                    sub = self.debitos[i].get()
                    sub = float(sub)
                    valor_minimo = self.minimos[i].get()
                    valor_minimo = float(valor_minimo)

                    tag_first = soup.find('label', {'id':f'primeiroMelhorColocado{id}'})
                    t_first = tag_first.text.split('.')
                    first = float(''.join(t_first).replace(',', '.'))

                    self.tag_lance = soup.find('label', {'id':f'meuLanceLicitante{id}'})
                    t_lance = self.tag_lance.text.split('.')
                    meulanceatual = float(''.join(t_lance).replace(',', '.'))

                    # lote = soup.find('label', {'id': f'labelLote{id}'})
                    # print(lote.text)

                    sleep(1)

                    'randomico = label, id:lbDoulheId{id}'

                    if first < meulanceatual and meulanceatual > valor_minimo:

                        sleep(0.5)

                        novolance = first-sub
                        if novolance < valor_minimo:
                            novolance = valor_minimo

                        if novolance >= valor_minimo:
                            lance = self.driver.find_element(By.ID, f'txtLance{id}')
                            lance.clear()
                            lance.send_keys(f'{novolance}'.replace('.', ','))

                            env_lance = self.driver.find_element(By.ID, f'btLance{id}')
                            env_lance.click()
                            sleep(1)
                            lance.clear()
                            
                except Exception as e:
                    print(e)
                    continue                
                
    def iniciar(self):

        self.run = True

        self.btn_iniciar.config(state=DISABLED)
        self.btn_parar.config(state=NORMAL)

        for i in range(len(self.minimos)):
            self.minimos[i].config(state=DISABLED)
            self.debitos[i].config(state=DISABLED)

        self.lances()

    def parar(self):

        self.btn_parar.config(state=DISABLED)
        self.btn_iniciar.config(state=NORMAL)

        for i in range(len(self.minimos)):
            self.minimos[i].config(state=NORMAL)
            self.debitos[i].config(state=NORMAL)
        
        self.run = False

    def lancar(self):

        if self.run:
            self.janela.after(3000, self.lancar)
            self.d_lotes = ['LT 1', 'LT 2', 'LT 3', 'LT 4', 'LT 5']
            ids = []

            for i in range(len(self.d_lotes)):
                if self.d_lotes[i] in self.lotes:
                    ids.append(self.d_lotes[i])
            
            for i in range(len(ids)):
                    if self.minimos[i].get() == '':
                        minimo = 0
                    else:
                        minimo = float(self.minimos[i].get())

                    if self.val[i] > minimo:
                        print(ids[i])
                        if self.debitos[i].get() == '':
                            sub = 0
                        else:
                            sub = float(self.debitos[i].get())
                        self.val[i]-=sub
                        print(self.val[i])
    
                    if self.val[i] < minimo:
                        self.val[i] = minimo
                        print(ids[i])
                        print(self.val[i])

    def janela2(self):
        self.janela = Tk()
        self.janela.title('SIAG BOT')
        self.janela.resizable(False, True)
        self.janela.iconbitmap('ico.ico')
        # janela.geometry('540x520')

        main_frame = Frame(self.janela)
        main_frame.pack(fill=BOTH, expand=True)

        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _bind_to_mousewheel(event):
            my_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_from_mousewheel(event):
            my_canvas.unbind_all("<MouseWheel>")

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
        my_canvas.bind('<Enter>', _bind_to_mousewheel)
        my_canvas.bind('<Leave>', _unbind_from_mousewheel)

        second_frame = Frame(my_canvas)

        my_canvas.create_window((0,0), window=second_frame, anchor='nw')

        self.run = True

        self.val = [1000, 10000, 20000]
        self.lotes = self.tags
        # self.lotes = ['LT 1','LT 2','LT 5']

        nlote = 0
        self.minimos = []
        self.debitos = []
        self.runner = []

        f_frame = LabelFrame(second_frame, text=' LOTES ', padx=5, pady=5)
        f_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        s_frame = LabelFrame(self.janela, padx=5, pady=5)
        s_frame.pack(padx=10, pady=10)

        for i in range(len(self.lotes)):

            frame = LabelFrame(f_frame, padx=5, pady=5)
            frame.pack(padx=10, pady=10)

            Label(frame, text=self.lotes[i].text).grid(column=0, row=0)
            Label(frame, text='Valor mínimo: R$').grid(column=0, row=1, padx=10)
            self.vminimo = Entry(frame, width=30)
            self.vminimo.grid(column=1, row=1, padx=10)
            self.minimos.append(self.vminimo)

            Label(frame, text='Valor à debitar: R$').grid(column=0, row=2)
            self.vdim = Entry(frame, width=30)
            self.vdim.grid(column=1, row=2, pady=10, padx=10)
            self.debitos.append(self.vdim)
            
        self.btn_iniciar = Button(s_frame, text='Iniciar', width=10, command=self.iniciar)
        self.btn_iniciar.grid(column=0, row=1, padx=50, pady=10)

        self.btn_parar = Button(s_frame, text='Parar', width=10, command=self.parar, state=DISABLED)
        self.btn_parar.grid(column=1, row=1, padx=50, pady=10)

        # self.runner.append(self.run)

            # nlote+=4
            

        self.janela.mainloop()



pregao = Pregao()

janela = Tk()
janela.title('SIAG BOT')
janela.resizable(False, False)
janela.iconbitmap('ico.ico')
janela.geometry('300x170')

Label(janela, text='Login:').grid(column=0, row=0, pady=10, columnspan=3)
vlogin = Entry(janela, width=25)
vlogin.place(x=130, y=12)

Label(janela, text='Senha:').grid(column=0, row=2, pady=10)
vsenha = Entry(janela, width=25)
vsenha.place(x=130, y=53)

Label(janela, text='Código do processo:').grid(column=0, row=3, pady=10, padx=10)
vcodigo = Entry(janela, width=25)
vcodigo.place(x=130, y=95)

btn_entrar = Button(janela, text='Entrar', width=30, command=pregao.acesso)
btn_entrar.place(x=40, y=130)

janela.mainloop()

try:
    pregao.driver.quit()
except:
    pass