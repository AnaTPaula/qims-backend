from config import database
from model.usuario import UsuarioHelper


class OperadorHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            'tipoAcesso': item.get('tipo_acesso'),
            'empresaId': item.get('empresa_fk'),
            'tipoArmazenagem': item.get('tipoArmazenagem'),
            **UsuarioHelper.serialize(item)
        }


def query_all_operador(empresa_id: int, nome: str = None):
    query = "SELECT o.nome_usuario, o.tipo_acesso, o.empresa_fk, u.id, u.tipo, u.senha, u.data_cadastro " \
            "from operador o JOIN usuario u ON o.usuario_fk = u.id WHERE empresa_fk = %s "
    if nome:
        query += " AND nome_usuario = %s"
    query += " order by o.nome_usuario asc "
    params = (empresa_id, nome,) if nome else (empresa_id,)
    return database.select_all(query=query, params=params)


def query_one_operador(empresa_id: int, usuario_id: int):
    query = "SELECT o.nome_usuario, o.tipo_acesso, o.empresa_fk, u.id, u.tipo, u.senha, u.data_cadastro " \
            "from operador o JOIN usuario u ON o.usuario_fk = u.id WHERE empresa_fk = %s AND usuario_fk = %s"
    return database.select_one(query=query, params=(empresa_id, usuario_id,))


def execute_create_operador(item: dict):
    query = " INSERT INTO operador (nome_usuario, tipo_acesso, empresa_fk, usuario_fk) VALUES " \
            " (%s, %s, %s, %s);"
    database.execute(query=query, params=(item['nomeUsuario'], item['tipoAcesso'], item['empresaId'], item['id'],))


def execute_update_operador(item: dict):
    query = " UPDATE operador SET nome_usuario = %s, tipo_acesso = %s WHERE usuario_fk = %s AND empresa_fk = %s;"
    database.execute(query=query, params=(item['nomeUsuario'], item['tipoAcesso'], item['id'], item['empresaId']))


def execute_delete_operador(usuario_id: int, empresa_id: int):
    query = f"DELETE FROM operador WHERE usuario_fk = %s AND empresa_fk = %s"
    database.execute(query=query, params=(usuario_id, empresa_id))
