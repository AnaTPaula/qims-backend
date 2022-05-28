from config import get_config
from model.model import Almoxarifado

session = get_config().get_session()


def find(empresa_id: str):
    items = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id).all()
    return [item.serialize for item in items]


def get_item(empresa_id: str, almoxarifado_id: int):
    item = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id, id=almoxarifado_id).first()
    return item.serialize if item else {}


def create(body: dict):
    item = Almoxarifado(nome=body['nome'], descricao=body['descricao'], empresa_fk=body['empresa_id'])
    session.add(item)
    session.commit()
    return item.serialize


def update(body: dict):
    item = session.query(Almoxarifado).filter_by(empresa_fk=body['empresa_id'], id=body['id']).first()
    item.nome = body['nome']
    item.descricao = body['descricao']
    session.add(item)
    session.commit()
    return item.serialize


def remove(empresa_id: str, almoxarifado_id: int):
    item = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id, id=almoxarifado_id).first()
    if item:
        session.delete(item)
        session.commit()
    return item
