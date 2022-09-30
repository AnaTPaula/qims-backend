from config import database
from model.usuario import UsuarioHelper


class AdministradorHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            **UsuarioHelper.serialize(item)
        }


def query_all_adm(nome: str = None):
    query = f"SELECT a.nome_usuario, u.id, u.tipo, u.senha, u.data_cadastro from administrador a " \
            f"JOIN usuario u ON a.usuario_fk = u.id"
    if nome:
        query += " WHERE nome_usuario = %s"
    return database.select_all(query=query, params=(nome,))


def query_one_adm(usuario_id: int):
    query = "SELECT a.nome_usuario, u.id, u.tipo, u.senha, u.data_cadastro from administrador a " \
            "JOIN usuario u ON a.usuario_fk = u.id WHERE a.usuario_fk = %s"
    return database.select_one(query=query, params=(usuario_id,))


def execute_create_adm(item: dict):
    query = "INSERT INTO administrador (nome_usuario, usuario_fk) VALUES (%s, %s);"
    database.execute(query=query, params=(item['nomeUsuario'], item['id'],))


def execute_update_adm(item: dict):
    query = "UPDATE administrador SET nome_usuario = %s WHERE usuario_fk = %s;"
    database.execute(query=query, params=(item['nomeUsuario'], item['id'],))


def execute_delete_adm(usuario_fk: int):
    query = "DELETE FROM administrador WHERE usuario_fk = %s"
    database.execute(query=query, params=(usuario_fk,))
