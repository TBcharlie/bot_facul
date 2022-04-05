from cgitb import text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Requerimento:
    def __init__(self, Tipo, Protocolo, Status):
        self.Tipo = Tipo
        self.Status = Status
        self.Protocolo = Protocolo


class Portal:

    def __init__(self):
        self.Login = ""
        self.Senha = ""
        self.requerimentos = []

        chrome_options = Options()
        ## faz com que o browser não abra durante o processo
        chrome_options.add_argument("--headless") 
        ## caminho para o seu webdriver
        caminho = "C:" 
        self.driver = webdriver.Chrome(caminho +'\chromedriver.exe', options=chrome_options)
        self.driver.implicitly_wait(10)

    def PegarLogin(self,login):
        self.Login = login

    def PegarSenha(self,Senha):
        self.Senha = Senha

    def Logar(self):

        self.driver.get('http://177.69.195.4/FrameHTML/WEB/APP/EDU/PORTALEDUCACIONAL/login/')

        time.sleep(5)

        print("Preparando para o login")

        elementForm = self.driver.find_element(By.NAME,"controller.formLogin")
        elementUser = self.driver.find_element(By.ID,"User")
        elementPass = self.driver.find_element(By.ID,"Pass")

        elementUser.send_keys(self.Login) 
        elementPass.send_keys(self.Senha)

        elementForm.submit()
        self.driver.implicitly_wait(10)

        time.sleep(10)
        elemenMenu = self.driver.find_element(By.ID,"show-menu")
        print("Logado")

    def AbrirAbaRequerimentos(self):

        print("Tentando abrir o menu secretaria")

        elemenMenu = self.driver.find_element(By.ID,"show-menu")
        elemenMenu.click()

        time.sleep(5)

        elementLiMenuSecretaria = self.driver.find_element(By.ID,"EDU_PORTAL_ACADEMICO_SECRETARIA")
        elementLiMenuSecretaria.click()
        time.sleep(5)
        print("finalizado, abriu o menu secretaria")

    def BuscarTodosRequementosFeito(self):
        self.AbrirAbaRequerimentos()
        print("Tentando abrir a aba requirimento")
        # elementSpanSecretaria = elementLiMenuSecretaria.find_element(By.XPATH,".//span[@class='menu-item-text']")
        # elementSpanSecretaria.click()
        time.sleep(5)

        elementPage =  self.driver.find_element(By.CLASS_NAME,"page-details")

        elementLiRequerimento = elementPage.find_elements(By.XPATH,".//li")
        elementLiRequerimentoSolicitados = elementLiRequerimento[1]
        elementA= elementLiRequerimentoSolicitados.find_element(By.XPATH,".//a")

        elementA.click()

        time.sleep(5)

        print("Finalizado, abriu a aba requirimento")


        elementsRequerimentos = self.driver.find_elements_by_css_selector(".tag-2.list-item.ng-scope.ng-isolate-scope")

        self.requerimentos = []

        for requerimento in elementsRequerimentos:
            tipo = requerimento.find_element_by_css_selector(".title.link.ng-binding").text

            detalhe = requerimento.find_element_by_css_selector(".item-info.ng-scope")

            itemDetalhe = detalhe.find_elements_by_css_selector(".col-lg-6.col-md-6.col-sm-12.col-xs-12.ng-scope.ng-isolate-scope")

            protocolo = itemDetalhe[0].find_elements_by_css_selector(".ng-binding.ng-scope")[1].text

            status = itemDetalhe[2].find_elements_by_css_selector(".ng-binding.ng-scope")[1].text

            requerimento = Requerimento(tipo, protocolo, status)

            self.requerimentos.append(requerimento)

    def RequerimentoMaisRecente(self):

        return(f"requerimento mais novo esta com o protocolo {self.requerimentos[0].Protocolo }º com status: {self.requerimentos[0].Status}")

    def TotalDeRequerimentos(self):
        total = len(self.requerimentos)
        return(f"total De Requerimentos: { total}")

    def MostrarTodosRequerimentos(self):
        texto = ""

        requerimentos = self.requerimentos

        for requerimento in requerimentos:
            texto += f"Protocolo: {requerimento.Protocolo} - Status: {requerimento.Status} - Tipo: {requerimento.Tipo} \n"
            texto += "---------------------------------------\n\n"

        return texto


