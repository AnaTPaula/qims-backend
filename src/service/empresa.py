from config import get_config
from model.model import Empresa, Usuario

session = get_config().get_session()


def find():
    items = session.query(Empresa).filter_by().all()
    return [item.serialize for item in items]


def get_item(empresa_id: int):
    item = session.query(Empresa).filter_by(usuario_fk=empresa_id).first()
    return item.serialize if item else {}


def create(body: dict):
    usuario = Usuario(tipo='empresa', senha=body['senha'])
    session.add(usuario)
    session.commit()
    item = Empresa(
        usuario_fk=usuario.id,
        nome_usuario=body['nome_usuario'],
        situacao_conta=body['situacao_conta'],
        lingua=body['lingua'],
        tipo_armazenagem=body['tipo_armazenagem'],
        aceite_termos_uso=body['aceite_termos_uso'])
    session.add(item)
    session.commit()
    return item.serialize


def update(body: dict):
    item = session.query(Empresa).filter_by(usuario_fk=body['id']).first()
    item.nome_usuario = body['nome_usuario']
    item.situacao_conta = body['situacao_conta']
    item.lingua = body['lingua']
    item.aceite_termos_uso = body['aceite_termos_uso']
    item.usuario.senha = body['senha']

    session.add(item)
    session.commit()
    return item.serialize


def remove(empresa_id: int):
    item = session.query(Usuario).filter_by(id=empresa_id).first()
    if item:
        session.delete(item)
        session.commit()
    return item
