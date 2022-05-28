from config import get_config
from model.model import Funcionario, Usuario

session = get_config().get_session()


def find(empresa_id: str):
    items = session.query(Funcionario).filter_by(empresa_fk=empresa_id).all()
    return [item.serialize for item in items]


def get_item(empresa_id: str, funcionario_id: int):
    item = session.query(Funcionario).filter_by(empresa_fk=empresa_id, usuario_fk=funcionario_id).first()
    return item.serialize if item else {}


def create(body: dict):
    usuario = Usuario(tipo='funcionario', senha=body['senha'])
    session.add(usuario)
    session.commit()
    item = Funcionario(usuario_fk=usuario.id,
                       nome_usuario=body['nome_usuario'],
                       acesso=body['acesso'],
                       empresa_fk=body['empresa_id'])
    session.add(item)
    session.commit()
    return item.serialize


def update(body: dict):
    item = session.query(Funcionario).filter_by(empresa_fk=body['empresa_id'], usuario_fk=body['id']).first()
    item.nome_usuario = body['nome_usuario']
    item.acesso = body['acesso']
    item.usuario.senha = body['senha']
    session.add(item)
    session.commit()
    return item.serialize


def remove(empresa_id: str, funcionario_id: int):
    item = session.query(Funcionario).filter_by(empresa_fk=empresa_id, usuario_fk=funcionario_id).first()
    usuario = session.query(Usuario).filter_by(id=funcionario_id).first()
    if item and usuario:
        session.delete(usuario)
        session.commit()
    return item
