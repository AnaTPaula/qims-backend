import logging
from config import get_config
from model.model import Almoxarifado
from controller.api_helper import ApiError


def find(empresa_id: str):
    session = get_config().get_session()
    try:
        items = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id).all()
        return [item.serialize for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()


def get_item(empresa_id: str, almoxarifado_id: int):
    session = get_config().get_session()
    try:
        item = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id, id=almoxarifado_id).first()
        return item.serialize if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()


def create(body: dict):
    session = get_config().get_session()
    try:
        item = Almoxarifado(nome=body['nome'], descricao=body['descricao'], empresa_fk=body['empresa_id'])
        session.add(item)
        session.commit()
        return item.serialize
    except Exception as ex:
        logging.error(ex)
        session.rollback()
        raise ApiError()
    finally:
        session.close()


def update(body: dict):
    session = get_config().get_session()
    try:
        item = session.query(Almoxarifado).filter_by(empresa_fk=body['empresa_id'], id=body['id']).first()
        item.nome = body['nome']
        item.descricao = body['descricao']
        session.add(item)
        session.commit()
        return item.serialize
    except Exception as ex:
        logging.error(ex)
        session.rollback()
        raise ApiError()
    finally:
        session.close()


def remove(empresa_id: str, almoxarifado_id: int):
    session = get_config().get_session()
    try:
        item = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id, id=almoxarifado_id).first()
        if item:
            session.delete(item)
            session.commit()
        return item
    except Exception as ex:
        logging.error(ex)
        session.rollback()
        raise ApiError()
    finally:
        session.close()
