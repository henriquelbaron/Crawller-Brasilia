import os
import re
from PyPDF2 import PdfFileReader, PdfFileWriter


class SplitPdfs():
    caminho_pdfs = '/home/henrique/Downloads/Boletos/'
    output_file = '/home/henrique/Downloads/'

    def __init__(self):
        for path, dir, arquivos in os.walk(self.caminho_pdfs):
            print('Encontrado {} pdfs'.format(len(arquivos)))
            for arquivo in arquivos:
                print('Extraindo informações do {} de {} pdfs'.format(arquivos.index(arquivo), len(arquivos)))
                # dados_imovel =  self.find('(.+?)_UNICA',arquivo,1)

                dados_imovel = arquivo.split('_')
                pdf = PdfFileReader(path + arquivo)
                for page in range(pdf.getNumPages()):
                    page_obj = pdf.getPage(page)
                    pdf_writer = PdfFileWriter()
                    pdf_writer.addPage(page_obj)
                    texto = page_obj.extractText()
                    parcela = self.find('Valor(.+?)RGR', texto, 1).replace('/', '-')
                    tributo = self.find('IMPOSTO TERRITORIAL URBANO', texto, 0)
                    if tributo is None:
                        tributo = 'TCRS'
                    else:
                        tributo = 'IPTU'
                    output_filename = '{}_{}_{}_{}.pdf'.format(dados_imovel[0], dados_imovel[1], parcela, tributo)
                    output_save = self.create_file(self.output_file + parcela) + '/' + output_filename
                    with open(output_save, 'wb') as out:
                        pdf_writer.write(out)

    def create_file(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)
            print('Pasta {} criada'.format(path))
        return os.path.abspath(path)

    def find(self, regex, text, group, flag=0):
        search = re.search(regex, text, flag)
        try:
            return search.group(group)
        except Exception as e:
            return None


start = SplitPdfs()
