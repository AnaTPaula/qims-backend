from config import database

class EmpresaHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            'situacaoConta': item.get('situacao_conta'),
            'tipoArmazenagem': item.get('tipo_armazenagem'),
            'aceiteTermosUso': item.get('aceite_termos_uso'),
            'usuarioId': item.get('usuario_fk'),
            'razaoSocial': item.get('razao_social')
        }


def query_all(usuario_id: str, nome: str = None):
    query = f"SELECT * from empresa WHERE usuario_fk = {usuario_id}"
    if nome:
        query += f" AND nome_usuario = '{nome}'"
    return database.select_all(query=query)


def query_one(usuario_fk: str):
    query = f"SELECT * from empresa WHERE usuario_fk = {usuario_fk}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO empresa (nome_usuario, situacao_conta, lingua, tipo_armazenagem," \
            f" aceite_termos_uso, usuario_fk)VALUES " \
            f" ('{item['nomeUsuario']}', '{item['situacaoConta']}', '{item['tipoArmazenagem']}', " \
            f" ('{item['aceiteTermosUso']}', '{item['usuarioId']}', '{item['razaoSocial']}'); "
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE empresa SET nome_usuario = '{item['nomeUsuario']}', situacao_conta = '{item['situacaoConta']}', " \
            f" tipo_armazenagem = '{item['tipoArmazenagem']}' " \
            f" WHERE usuario_fk = '{item['usuarioID']}' "
    database.execute(query=query)


def execute_delete(usuario_fk: str):
    query = f"DELETE FROM empresa WHERE usuario_fk = '{usuario_fk}'"
    database.execute(query=query)
