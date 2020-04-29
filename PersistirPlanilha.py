import xlrd

from dao.Connection import Connection


class PersistirPlanilha():
    workbook = xlrd.open_workbook(
        '/home/henrique/Planilhas/fazendaBrasilia2.xls')
    worksheet = workbook.sheet_by_index(0)
    imovels = []
    con = Connection('localhost', 'imob', 'postgres', 'P2a3u0l9')
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = str(cell.value).replace('.0', '')
        con.insertParametro(row_data)
        imovels.append(row_data)


start = PersistirPlanilha()