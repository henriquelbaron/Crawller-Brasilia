from Connection import Connection


class DaoService(object):
    _con = Connection('localhost', 'imob', 'postgres', 'P2a3u0l9')

    def __init__(self, mhost, db, usr, pwd):
        self._con = Connection('localhost', 'imob', 'postgres', 'P2a3u0l9')

    def persistirPlanilha(self,imovels):
        sqlImovel = 'Insert into imovel values({})'
        sqlParametro = 'INSERT INTO parametro (codigoImovel,id_imovel,id_imobiliaria) values ({},{},1)'
