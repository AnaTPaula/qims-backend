from passlib.handlers.pbkdf2 import pbkdf2_sha256
from config import database

class UsuarioHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'tipo': item.get('tipo'),
            'senha': item.get('senha'),
            'dataCadastro': item.get('data_cadastro')
        }


def query_all():
    query = f" SELECT * from usuario "
    return database.select_all(query=query)


def query_one(usuario_id: str):
    query = f" SELECT * from usuario WHERE id = {usuario_id} "
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO usuario (id, tipo, senha, data_cadastro) VALUES " \
            f" ('{item['tipo']}', '{item['senha']}', '{item['dataCadastro']}'); "
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE usuario SET tipo = '{item['tipo']}', senha = '{item['senha']}' " \
            f" WHERE id = '{item['id']}'"
    database.execute(query=query)


def execute_delete(usuario_id):
    query = f" DELETE FROM usuario WHERE id = '{usuario_id}' "
    database.execute(query=query)


def verify_password(item: dict, senha_sem_hash: str):
    try:
        return pbkdf2_sha256.verify(senha_sem_hash, item['senha'])
    except ValueError:
        return False


def set_hash_password(item: dict, senha_nova: str):
    item['senha'] = pbkdf2_sha256.hash(senha_nova)
