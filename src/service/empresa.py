import logging

from config import get_config
from model.model import Empresa, Usuario
from controller.api_helper import ApiError


def find():
    session = get_config().get_session()
    try:
        items = session.query(Empresa).filter_by().all()
        return [item.serialize for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()


def get_item(empresa_id: int):
    session = get_config().get_session()
    try:
        item = session.query(Empresa).filter_by(usuario_fk=empresa_id).first()
        return item.serialize if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()


def create(body: dict):
    session = get_config().get_session()
    try:
        usuario = Usuario(tipo='empresa')
        usuario.set_hash_password(senha=body['senha'])
        session.add(usuario)
        session.commit()
    except Exception as ex:
        logging.error(ex)
        session.rollback()
        session.close()
        raise ApiError()

    try:
        item = Empresa(
            usuario_fk=usuario.id,
            nome_usuario=body['nomeUsuario'],
            situacao_conta='EM_ANALISE',
            lingua=body['lingua'],
            tipo_armazenagem=body['tipoArmazenagem'],
            aceite_termos_uso=body['aceiteTermosUso'])
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
    session = get_config().get_session()
    try:
        item = session.query(Empresa).filter_by(usuario_fk=body['id']).first()
        item.nome_usuario = body['nomeUsuario']
        if body.get('situacaoConta'):
            item.situacao_conta = body['situacaoConta']
        item.lingua = body['lingua']
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


def remove(empresa_id: int):
    session = get_config().get_session()
    try:
        item = session.query(Usuario).filter_by(id=empresa_id).first()
        if item:
            session.delete(item)
            session.commit()
        return item
    except Exception as ex:
        logging.error(ex)
        session.rollback()
    finally:
        session.close()
