from selenium import webdriver
from selenium.webdriver.common.by import By
from emails import EnviarEmail
import pickle
import os


class Metropoles:
    def __init__(self):
        self.url = "https://www.metropoles.com/"
        self.caminho_pickle = r'C:\Users\Windows\Downloads\ultima_noticia.pkl'
        self.titulo = ""
        self.link = ""

        try:
            with open(self.caminho_pickle, mode='rb') as ultima_noticia:
                self.titulo, self.link = pickle.load(ultima_noticia)

        except Exception as e:
            print("Exceção no carregamento do arquivo pickle", e)

    def acesso(self):
        # Acesso ao Metropóles sem abertura do navegador
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        driver = webdriver.Chrome(chrome_options=options)
        driver.get(self.url)

        # Coleta da matéria principal com o XPATH normal
        materia = driver.find_element(By.XPATH, '//*[@id="m-main"]/section[1]/div/div/div[1]/article/div[2]/div/h2/a')
        link = materia.get_attribute('href')
        titulo = materia.text

        if titulo == self.titulo:
            print("Permanece a mesma matéria principal! Favor aguardar!")

        else:
            try:
                os.remove(self.caminho_pickle)
                print(titulo)
                print(link)
            except Exception as e:
                print("Exceção na remoção do arquivo", e)

            # Salvando últimos resultados
            with open(self.caminho_pickle, mode='wb') as ultima_noticia:
                pickle.dump([titulo, link], ultima_noticia)

            titulo = "METROPÓLES: " + titulo

            driver.quit()

            # Acessando o contéudo da matéria de capa
            driver1 = webdriver.Chrome(chrome_options=options)
            driver1.get(link)

            textos = driver1.find_elements(By.TAG_NAME, 'p')
            conteudo = ""
            for texto in textos:
                conteudo += texto.text
                conteudo += "\n"

            print(conteudo)

            EnviarEmail(titulo, conteudo)


if __name__ == '__main__':
    metropoles = Metropoles()
    metropoles.acesso()