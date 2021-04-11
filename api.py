from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup


class Chrome:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.drive_path = "chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=Perfil')
        self.chrome = webdriver.Chrome(
            self.drive_path,
            options=self.options
        )
        self.matricula = [[], [], []]
        self.horario = [["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"], [[], [], [], [], [], [], []]]
        self.att = []
        self.desc = []

    def acess(self):
        self.chrome.get("https://sigaa.ufma.br/sigaa/verTelaLogin.do")

    def exit(self):
        self.chrome.quit()

    def getHour(self):
        try:
            input_user = self.chrome.find_element_by_id('usuarioLogin')
            input_pass = self.chrome.find_element_by_id('senhaLogin')
            btn_login = self.chrome.find_element_by_class_name('botao-entrar')

            input_user.send_keys(self.user)
            input_pass.send_keys(self.password)
            btn_login.click()

            btn_skip1 = self.chrome.find_element_by_name('j_id_jsp_712183460_1:j_id_jsp_712183460_2')
            btn_skip1.click()
            sleep(8)

            btn_skip1 = self.chrome.find_element_by_name('j_id_jsp_712183460_1:j_id_jsp_712183460_2')
            btn_skip1.click()
            sleep(5)

            btn_show_menu = self.chrome.find_element_by_id('menu:formensino:menuensino')
            btn_show_menu.click()

            btn_matricula = self.chrome.find_element_by_id('menu:formensino:atestadoMatricula')
            btn_matricula.click()

            """PEGANDO OS DADOS DA TABELA MATRICULA"""
            table = self.chrome.find_element_by_id('matriculas')
            data = table.get_attribute('innerHTML')
            html = BeautifulSoup(data, 'html.parser')

            """PEGANDO O CODIGO DAS MATERIAS"""
            info_codigo = html.select('.codigo')
            for i in info_codigo:
                self.matricula[0].append(i.text)

            """PEGANDO O NOME DAS MATERIAS"""
            info_name = html.select('.componente')
            for i in info_name:
                self.matricula[1].append(i.text)

            """PEGANDO O DOCENTE DA MATERIA"""
            info_doc = html.select('.docente')
            for i in info_doc:
                self.matricula[2].append(i.text)

            """PEGANDO OS DADOS DA TABELA HORARIO"""
            table1 = self.chrome.find_element_by_id('horario')
            data1 = table1.get_attribute('innerHTML')
            html1 = BeautifulSoup(data1, 'html.parser')

            """PEGANDO OS HORARIOS"""
            a = 1
            b = 1
            while a <= 7:
                while b <= 6:
                    value = f'{a}_{b}'
                    info_hour = html1.findAll(id=value)
                    self.horario[1][a-1].append(info_hour[0].text)
                    b += 1
                b = 1
                a += 1

            print(self.horario)
            self.chrome.get("https://sigaa.ufma.br/sigaa/portais/discente/discente.jsf")

        except Exception as error:
            print(error)

    def getAtv(self):
        path_att = self.chrome.find_elements_by_xpath("//td[@headers='atividades_data']")
        path_desc_att = self.chrome.find_elements_by_xpath("//td[@headers='descricao-atividade']")
        for i in path_att:
            a = BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser').text.rsplit('\t')
            a = ''.join(a)
            b = a.rsplit('\n')
            b = ''.join(b)
            self.att.append(b)
        for i in path_desc_att:
            a = BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser').text.rsplit('\t')
            a = ''.join(a)
            b = a.rsplit('\n')
            b = ''.join(b)
            self.desc.append(b)
        print(self.att)
        print(self.desc)


if __name__ == "__main__":
    chrome = Chrome('nome.sobrenome', 'senha')
    chrome.acess()
    chrome.getHour()
    chrome.getAtv()