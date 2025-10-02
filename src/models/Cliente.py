import pandas as pd
from src.connection import Conexao


class Cliente ():
    '''Classe responsavel pela interacao dos objetos clientes'''

    def __init__(self, codCliente = '' ):

        self.codCliente = codCliente


    def get_clientes(self):
        '''Metodo publico que obtem as informacoes dos clientes '''


        SQL = """
        select
            "CNPJ/CPF" ,
            codcliente,
            "nomeCliente" ,
            situacao,
            "DataCadastro"
        from
            clientes c
        """

        conn = conexao.conexaoEngine()
        consulta = pd.read_sql(SQL,conn)

        return consulta

    def post_cliente(self):
        """Metodo publico que cadastra um cliente no erp"""


    def put_cliente(self):
        """Metodo publico que atualiza informacoes de um cliente """

    def get_cliente_especifico(self):
        """Metodo publico que obtem informacoes de um cliente em espercifico"""

        SQL = f"""
        select
            "CNPJ/CPF" ,
            codcliente,
            "nomeCliente" ,
            situacao,
            "DataCadastro"
        from
            clientes c
        WHERE
            codcliente = '{str(self.codCliente)}'
        """

        conn = conexao.conexaoEngine()
        consulta = pd.read_sql(SQL, conn)

        return consulta



    def delete_cliente_especifico(self):
        """Metodo que exclui o cliente do erp , se ele nao tiver movimentacoes em outras tabelas"""

