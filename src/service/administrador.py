import logging

from config import get_config
from model.model import Administrador, Usuario
from controller.api_helper import ApiError


def find():
    session = get_config().get_session()
    try:
        items = session.query(Administrador).all()
        return [item.serialize for item in items]
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
        usuario = Usuario(tipo='administrador')
        usuario.set_hash_password(senha=body['senha'])
        session.add(usuario)
        session.commit()
    except Exception as ex:
        logging.error(ex)
        session.rollback()
        session.close()
        raise ApiError()

    try:
        item = Administrador(
            usuario_fk=usuario.id,
            nome_usuario=body['nomeUsuario'])
        session.add(item)
        session.commit()
        return item.serialize
    except Exception as ex:
        logging.error(ex)
        session.rollback()
        session.delete(usuario)
        session.commit()

        raise ApiError()
    finally:
        session.close()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    session = get_config().get_session()
    try:
        item = session.query(Administrador).filter_by(usuario_fk=body['id']).first()
        item.nome_usuario = body['nomeUsuario']
        if body.get('senha'):
            item.usuario.set_hash_password(senha=body['senha'])

        session.add(item)
        session.commit()
        return item.serialize
    except Exception as ex:
        logging.error(ex)
        session.rollback()
    finally:
        session.close()


def is_unique(body: dict):
    session = get_config().get_session()
    try:
        item = session.query(Administrador).filter_by(nome_usuario=body['nomeUsuario']).first()
        if body.get('id'):
            return False if item and int(body.get('id')) != item.usuario_fk else True
        else:
            return False if item else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()
