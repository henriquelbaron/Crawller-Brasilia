import psycopg2


class Connection(object):
    _db = None

    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(host=mhost, database=db, user=usr, password=pwd)

    def manipular(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close();
            self._db.commit()
        except:
            return False;
        return True;

    def consultar(self, sql):
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall();
        except:
            return None
        return rs

    def proximaPK(self, tabela, chave):
        sql = 'select max(' + chave + ') from ' + tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk + 1

    def fechar(self):
        self._db.close()

    def insertParametro(self,imovel,imob):
        sqlImovel = """INSERT INTO imovel (inscricao)VALUES (%s) RETURNING id;"""
        sqlParametro= """INSERT INTO parametro (codigoImovel,id_imovel, id_imobiliaria) VALUES(%s,%s,%s)"""
        sqlFatura = """"INSERT INTO  consulta """
        id_imovel = None
        try:
            cur = self._db.cursor()
            cur.execute(sqlImovel, (imovel['inscricao'],))
            id_imovel = cur.fetchone()[0]
            cur.execute(sqlParametro, (imovel['codImovel'],id_imovel,1))
            self._db.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self._db.rollback()
            print(error)
        return id_imovel
