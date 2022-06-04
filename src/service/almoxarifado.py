import logging
from config import get_config
from model.model import Almoxarifado
from controller.api_helper import ApiError


def find(empresa_id: str, nome: str = None):
    session = get_config().get_session()
    try:
        if nome:
            items = session.query(Almoxarifado).filter_by(empresa_fk=empresa_id, nome=nome).all()
        else:
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
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    session = get_config().get_session()
    try:
        item = Almoxarifado(nome=body['nome'], descricao=body.get('descricao'), empresa_fk=body['empresaId'])
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
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    session = get_config().get_session()
    try:
        item = session.query(Almoxarifado).filter_by(empresa_fk=body['empresaId'], id=body['id']).first()
        item.nome = body['nome']
        item.descricao = body.get('descricao', '')
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


def is_unique(body: dict):
    session = get_config().get_session()
    try:
        item = session.query(Almoxarifado).filter_by(empresa_fk=body['empresaId'], nome=body['nome']).first()
        if body.get('id'):
            return False if item and int(body.get('id')) != item.id else True
        else:
            return False if item else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()
