from config import get_config
from model.model import Almoxarifado

session = get_config().get_session()


def find(conta: str):
    items = session.query(Almoxarifado).filter_by(conta=conta).all()
    return [item.serialize for item in items]
