from config import get_config
from model.model import Almoxarifado

session = get_config().get_session()


def find(conta: str):
    items = session.query(Almoxarifado).filter_by(conta=conta).all()
    return [item.serialize for item in items]


def get_item(conta: str, almoxarifado_id: int):
    item = session.query(Almoxarifado).filter_by(conta=conta, id=almoxarifado_id).first()
    return item.serialize if item else {}


def create(body: dict):
    item = Almoxarifado(**body)
    session.add(item)
    session.commit()
    return item.serialize


def update(body: dict):
    item = session.query(Almoxarifado).filter_by(conta=body['conta'], id=body['id']).first()
    item.nome = body['nome']
    item.descricao = body['descricao']
    session.add(item)
    session.commit()
    return item.serialize


def remove(conta: str, almoxarifado_id: int):
    item = session.query(Almoxarifado).filter_by(conta=conta, id=almoxarifado_id).first()
    if item:
        session.delete(item)
        session.commit()
    return item
