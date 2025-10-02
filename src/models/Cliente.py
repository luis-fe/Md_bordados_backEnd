import pandas as pd
from src.connection import Conexao


class Cliente ():
    '''Classe responsavel pela interacao dos objetos clientes'''

    def __init__(self, codCliente = '', cnpj_cpf = '', nomeCliente = '', situacaoCliente = '', DataCadastro = '' ):

        self.codCliente = codCliente
        self.cnpj_cpf = cnpj_cpf
        self.nomeCliente = nomeCliente
        self.situacaoCliente = situacaoCliente
        self.DataCadastro = DataCadastro



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

        conn = Conexao.conexaoEngine()
        consulta = pd.read_sql(SQL,conn)

        return consulta

    def post_cliente(self):
        """Metodo publico que cadastra um cliente no erp"""

        insert = """
        insert into clientes (
            "CNPJ/CPF" ,
            codcliente,
            "nomeCliente" ,
            situacao,
            "DataCadastro"
        )
        values ( %s, %s, %s, %s, %s ) 
        """
        verifica_cpf = self.__verificanco_dupliccao_cpf()
        verifica_codCliente = self.get_cliente_especifico()

        if verifica_cpf == False:

            return pd.DataFrame([{'Mensagem': 'CPF/CNPJ JA EXISTE PARA OUTRO CLIENTE !', 'status': False}])

        else:

            if not verifica_codCliente.empty:
                return pd.DataFrame([{'Mensagem': 'cliente ja possue cadastro !', 'status': False}])


            else:
                    with Conexao.conexao() as conn:
                        with conn.cursor() as curr:
                            curr.execute(insert,(self.cnpj_cpf, self.codCliente, self.nomeCliente, self.situacaoCliente, self.DataCadastro))
                            conn.commit()
                    return pd.DataFrame([{'Mensagem':'Usuario incluido com sucesso !','status':True}])



    def put_cliente(self):
        """Metodo publico que atualiza informacoes de um cliente """

        update = f"""
        update from 
            clientes
        set 
            "nomeCliente" = %s,
            "situacao" = %s,
            "CNPJ/CPF" = %s
        where  
            codcliente = '{str(self.codCliente)}'
        """

        verifica_cpf = self.__verificanco_dupliccao_cpf()
        verifica_codCliente = self.get_cliente_especifico()

        if verifica_cpf == False:
            return pd.DataFrame([{'Mensagem': 'CPF/CNPJ JA EXISTE PARA OUTRO CLIENTE !', 'status': False}])
        else:

            if  verifica_codCliente.empty:
                return pd.DataFrame([{'Mensagem': 'cliente nao possue cadastro !', 'status': False}])

            else:
                    with Conexao.conexao() as conn:
                        with conn.cursor() as curr:
                            curr.execute(update,( self.nomeCliente, self.situacaoCliente, self.cnpj_cpf))
                            conn.commit()
                    return pd.DataFrame([{'Mensagem':'Usuario alterado com sucesso !','status':True}])


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

        conn = Conexao.conexaoEngine()
        consulta = pd.read_sql(SQL, conn)

        return consulta



    def delete_cliente_especifico(self):
        """Metodo que exclui o cliente do erp , se ele nao tiver movimentacoes em outras tabelas"""

        delete = f"""
        delete from 
        clientes 
        where 
        codcliente = '{str(self.codCliente)}'
        """

        with Conexao.conexao() as conn:
            with conn.cursor() as curr:
                curr.execute(delete)
                conn.commit()
        return pd.DataFrame([{'Mensagem': 'Usuario alterado com sucesso !', 'status': True}])

    def __verificanco_dupliccao_cpf(self):
        """Metodo privado que valida o cpf e cnpj do cliente """


        SQL = f"""
        select
            "CNPJ/CPF"
        WHERE
            "CNPJ/CPF" = '{str(self.cnpj_cpf)}'
        """

        conn = Conexao.conexaoEngine()
        consulta = pd.read_sql(SQL, conn)

        if consulta.empty:
            return True
        else:
            return False



