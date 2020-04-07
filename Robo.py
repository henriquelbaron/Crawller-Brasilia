import logging
import os
import re
import time
from datetime import datetime
from io import BytesIO

import xlrd
import xlwt
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait


class RoboBrasilia():
    path = '/home/files/BRASILIA/{}/{}/'.format(datetime.now().strftime('%d_%m_%y'),
                                                datetime.now().strftime('%H%M%S%f'))
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='brasilia.log',
                        level=logging.INFO)

    def __init__(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        workbook = xlrd.open_workbook(
            '/home/henrique/Planilhas/fazendaBrasilia2.xls')
        worksheet = workbook.sheet_by_index(0)
        imovels = []

        keys = [v.value for v in worksheet.row(0)]
        for row_number in range(worksheet.nrows):
            if row_number == 0:
                continue
            row_data = {}
            for col_number, cell in enumerate(worksheet.row(row_number)):
                row_data[keys[col_number]] = str(cell.value).replace('.0', '')
            imovels.append(row_data)
        quantidade_imovels = len(imovels)
        logging.info(str(quantidade_imovels) + " Imoveis para processamento")
        try:
            contador = 1
            for imovel in imovels:
                self.create_file(self.path + "/boletos")
                try:
                    logging.info('Processando {} {} de {}'.format(imovel, contador, quantidade_imovels))
                    if self.efetuar_login(driver, imovel['inscricao']):
                        imovel['faturas'] = []
                        imovel['status'] = 'COM DÉBITO'
                        wait = WebDriverWait(driver, 10)
                        wait.until(
                            cond.element_to_be_clickable((By.XPATH, '//button/span[contains(text()," Imprimir ")]')))
                        while True:
                            btns_imprimir = driver.find_elements_by_xpath(
                                "//button/span[contains(text(),' Imprimir ')]")
                            aba_atual = driver.window_handles[0]
                            for btn_imprimir in btns_imprimir:
                                try:
                                    btn_imprimir.click()
                                    if len(driver.find_elements_by_xpath("//*[contains(@id,'cdk-overlay-')]")) >= 1:
                                        driver.find_element_by_xpath("//button[text()='Confirmar']").click()
                                    wait.until(cond.new_window_is_opened)
                                    driver.switch_to.window(driver.window_handles[1])
                                    wait.until(
                                        cond.text_to_be_present_in_element(
                                            (By.XPATH, '//*[@id="htmlDar"]/div/button/strong'),
                                            'Imprimir'), cond.text_to_be_present_in_element(
                                            (By.XPATH, '//*[@id="htmlDar"]/div/button/strong'),
                                            'Imprimir'))
                                    self.extrair_dados(driver, imovel)
                                finally:
                                    driver.close()
                                    driver.switch_to.window(aba_atual)
                            btn_next = driver.find_element_by_xpath(
                                "//button[contains(@class,'mat-paginator-navigation-next')]")
                            if btn_next.is_enabled():
                                btn_next.click()
                            else:
                                break
                    else:
                        imovel['status'] = 'NUMERO DA INSCRICAO DE IMOVEL INCORRETO'
                except Exception as py_ex:
                    imovel['status'] = 'REPROCESSAR'
                    logging.error(py_ex)
                    logging.error(py_ex.args)
                logging.info(imovel)
                contador += 1
        except Exception as py_ex:
            logging.error(py_ex)
            logging.error(py_ex.args)
        finally:
            driver.quit()
            fildnames = ['codImovel', 'inscricao', 'status']
            for imovel in imovels:
                try:
                    for field in [*imovel['faturas'][0]]:
                        fildnames.append(field)
                    break
                except:
                    pass
            try:
                workbook = xlwt.Workbook()
                worksheet = workbook.add_sheet(u'Resultado')
                worksheet.write(0, 0, 'codImovel')
                worksheet.write(0, 1, 'inscricao')
                worksheet.write(0, 2, 'status')
                worksheet.write(0, 3, 'Nome ou Razão Social')
                worksheet.write(0, 4, 'CPF/CNPJ')
                worksheet.write(0, 5, 'Endereço')
                worksheet.write(0, 6, 'Vencimento')
                worksheet.write(0, 7, 'Cod. Barras')
                worksheet.write(0, 8, 'Cod Receita')
                worksheet.write(0, 9, 'Cota ou Refer')
                worksheet.write(0, 10, 'Exercício')
                worksheet.write(0, 11, 'Valor')
                worksheet.write(0, 12, 'Multa')
                worksheet.write(0, 13, 'Juros')
                worksheet.write(0, 14, 'Outros')
                worksheet.write(0, 15, 'Valor Total')
                worksheet.write(0, 16, 'Tributo')
                novaLinha = 1;
                for imovel in imovels:
                    if imovel['faturas'] is None:
                        worksheet.write(novaLinha, 0, imovel['codImovel'])
                        worksheet.write(novaLinha, 2, imovel['inscricao'])
                        worksheet.write(novaLinha, 3, imovel['status'])
                        novaLinha += 1
                    else:
                        for fatura in imovel['faturas']:
                            worksheet.write(novaLinha, 0, imovel['codImovel'])
                            worksheet.write(novaLinha, 1, imovel['inscricao'])
                            worksheet.write(novaLinha, 2, imovel['status'])
                            worksheet.write(novaLinha, 3, fatura['Nome ou Razão Social'])
                            worksheet.write(novaLinha, 4, fatura['CPF/CNPJ'])
                            worksheet.write(novaLinha, 5, fatura['Endereço'])
                            worksheet.write(novaLinha, 6, fatura['Vencimento'])
                            worksheet.write(novaLinha, 7, fatura['Cod. Barras'])
                            worksheet.write(novaLinha, 8, fatura['Cod Receita'])
                            worksheet.write(novaLinha, 9, fatura['Cota ou Refer'])
                            worksheet.write(novaLinha, 10, fatura['Exercício'])
                            worksheet.write(novaLinha, 11, fatura['Valor'])
                            worksheet.write(novaLinha, 12, fatura['Multa'])
                            worksheet.write(novaLinha, 13, fatura['Juros'])
                            worksheet.write(novaLinha, 14, fatura['Outros'])
                            worksheet.write(novaLinha, 15, fatura['Valor Total'])
                            worksheet.write(novaLinha, 16,
                                            '/'.join([*fatura['Tributo']]))
                            novaLinha += 1
                workbook.save(self.path + '/resultado.xls')
            except IOError:
                print("I/O error")

    def extrair_dados(self, driver, imovel):
        time.sleep(0.5)
        fatura = {}
        text = driver.find_element_by_xpath("//body").text
        fatura['Cod Receita'] = self.find('Cod Receita (.+?)\\n', text, 1)
        fatura['Cota ou Refer'] = self.find('Refer. (.+?)\\n', text, 1)
        fatura['Vencimento'] = self.find('Vencimento. (.+?)\\n', text, 1)
        fatura['Exercício'] = self.find('Exercício. (.+?)\\n', text, 1)
        fatura['CPF/CNPJ'] = self.find('CPF/CNPJ (.+?)\\n', text, 1)
        fatura['Valor'] = self.find('Principal - R\\$ (.+?)\\n', text, 1)
        fatura['Multa'] = self.find('Multa - R\\$ (.+?)\\n', text, 1)
        fatura['Juros'] = self.find('Juros - R\\$ (.+?)\\n', text, 1)
        fatura['Outros'] = self.find('Outros - R\\$ (.+?)\\n', text, 1)
        fatura['Valor Total'] = self.find('Valor Total - R\\$ (.+?)\\n', text, 1)
        fatura['Cod. Barras'] = self.find('\\n(.+?)\\n01.CF/DF', text, 1)
        fatura['Nome ou Razão Social'] = self.find('Razão Social\\n(.+?)\\n', text, 1)
        fatura['Endereço'] = self.find('Endereço\n(.+?)\\n', text, 1)
        tributos = {}
        if self.find('VLR IPTU: (.+?)\\n', text, 1) != None:
            tributos['IPTU'] = self.find('VLR IPTU: (.+?)\\n', text, 1)
        if self.find('VLR TLP : (.+?)\\n', text, 1) != None:
            tributos['LIXO'] = self.find('VLR TLP : (.+?)\\n', text, 1)

        fatura['Tributo'] = tributos
        file_name = '{}_{}_{}.pdf'.format(imovel['codImovel'], imovel['inscricao'],
                                          fatura['Cota ou Refer'])
        file_name = re.sub(r"/", "-", file_name)
        self.gera_pdf(driver, file_name)
        imovel['faturas'].append(fatura)
        return imovel

    def gera_pdf(self, driver, file_name):
        img = Image.open(BytesIO(driver.find_element_by_tag_name('body').screenshot_as_png))
        rgb = Image.new('RGB', img.size, (255, 255, 255))
        rgb.paste(img, mask=img.split()[3])
        rgb.save(self.path + "/boletos/" + file_name, "PDF", quality=100)

    def efetuar_login(self, driver, inscicao):
        driver.get("https://ww1.receita.fazenda.df.gov.br/emissao-segunda-via/iptu")
        inscricao_input = driver.find_element_by_id('mat-input-0')
        inscricao_input.send_keys(inscicao)
        consultar_btn = driver.find_element_by_xpath("//button[@color='primary']")
        consultar_btn.click()
        try:
            driver.find_element_by_xpath('//*[contains(@class ,"alert-info")]')
            return False
        except:
            return True

    def create_file(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)
            print('Pasta criada')

    def find(self, regex, text, group, flag=0):
        search = re.search(regex, text, flag)
        try:
            return search.group(group)
        except Exception as e:
            return None


robo = RoboBrasilia()
