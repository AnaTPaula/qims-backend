from config import database

class FuncionarioHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            'usuario_id': item.get('usuario_fk'),
        }


# def query_all(usuario_id: str, nome: str = None):
#     query = f"SELECT * from empresa WHERE usuario_fk = {usuario_id}"
#     if nome:
#         query += f" AND nome_usuario = '{nome}'"
#     return database.select_all(query=query)
#
#
# def query_one(empresa_id: str, almoxarifado_id: int):
#     query = f"SELECT * from almoxarifado WHERE empresa_fk = {empresa_id} AND id = {almoxarifado_id}"
#     return database.select_one(query=query)


# def execute_create(item: dict):
#     query = f" INSERT INTO (nome_usuario, situacao_conta, lingua, tipo_armazenagem," \
#             f" aceite_termos_uso, usuario_fk)VALUES " \
#             f" ('{item['nomeUsuario']}', '{item['situacaoConta']}', '{item['lingua']}', '{item['tipoArmazenagem']}', " \
#             f" ('{item['aceiteTermosUso']}', '{item['usuarioId']}'); "
#     database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE administrador SET nome_usuario = '{item['nomeUsuario']}',"\
            f" WHERE usuario_fk = '{item['usuarioID']}' "
    database.execute(query=query)


# def execute_delete(usuario_fk: str):
#     query = f"DELETE FROM empresa WHERE usuario_fk = '{usuario_fk}'"
#     database.execute(query=query)