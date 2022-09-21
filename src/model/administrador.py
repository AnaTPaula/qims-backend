from config import database

class AdministradorHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            'usuario_id': item.get('usuario_fk'),
        }


def query_all():
    query = f"SELECT * from administrador"
    return database.select_all(query=query)


def query_one(usuario_id: str):
    query = f"SELECT * from administrador WHERE usuario_fk = {usuario_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO (nome_usuario, usuario_fk VALUES" \
            f" ('{item['nomeUsuario']}', '{item['usuarioFk']}'"
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE administrador SET nome_usuario = '{item['nomeUsuario']}',"\
            f" WHERE usuario_fk = '{item['usuarioID']}'"
    database.execute(query=query)


def execute_delete(usuario_fk: str):
    query = f"DELETE FROM administrador WHERE usuario_fk = '{usuario_fk}'"
    database.execute(query=query)