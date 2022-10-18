from config import database
from model.usuario import UsuarioHelper


class EmpresaHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            'situacaoConta': item.get('situacao_conta'),
            'tipoArmazenagem': item.get('tipo_armazenagem'),
            'aceiteTermosUso': item.get('aceite_termos_de_uso'),
            'razaoSocial': item.get('razao_social'),
            **UsuarioHelper.serialize(item)
        }


def query_all_empresa(nome: str = None):
    query = "SELECT e.nome_usuario, e.situacao_conta, e.tipo_armazenagem, e.aceite_termos_de_uso, e.razao_social," \
            " u.id, u.tipo, u.senha, u.data_cadastro from empresa e JOIN usuario u ON e.usuario_fk = u.id"
    if nome:
        query += " WHERE nome_usuario = %s "
    query += " order by e.razao_social "
    return database.select_all(query=query, params=(nome,))


def query_one_empresa(usuario_id: int):
    query = "SELECT e.nome_usuario, e.situacao_conta, e.tipo_armazenagem, e.aceite_termos_de_uso, e.razao_social," \
            " u.id, u.tipo, u.data_cadastro from empresa e JOIN usuario u ON e.usuario_fk = u.id " \
            "WHERE e.usuario_fk = %s"
    return database.select_one(query=query, params=(usuario_id,))


def execute_create_empresa(item: dict):
    query = "INSERT INTO empresa (nome_usuario, situacao_conta, tipo_armazenagem, aceite_termos_de_uso, " \
            "usuario_fk, razao_social) VALUES (%s, %s, %s, %s, %s, %s); "
    database.execute(query=query, params=(
        item['nomeUsuario'], item['situacaoConta'], item['tipoArmazenagem'], item['aceiteTermosUso'], item['id'],
        item['razaoSocial'],))


def execute_update_empresa(item: dict):
    query = "UPDATE empresa SET nome_usuario = %s, situacao_conta = %s, aceite_termos_de_uso = %s, " \
            " razao_social = %s  WHERE usuario_fk = %s "
    database.execute(query=query, params=(
        item['nomeUsuario'], item['situacaoConta'], item['aceiteTermosUso'], item['razaoSocial'], item['id']))


def execute_delete_empresa(usuario_id: int):
    query = "DELETE FROM empresa WHERE usuario_fk = %s"
    database.execute(query=query, params=(usuario_id,))
