import logging

from config import get_config
from model.model import Empresa, Usuario, Funcionario
from controller.api_helper import ApiError


def find(nome: str):
    session = get_config().get_session()
    try:
        if nome:
            items = session.query(Empresa).filter_by(nome_usuario=nome).all()
        else:
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
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
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
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    session = get_config().get_session()
    try:
        item = session.query(Empresa).filter_by(usuario_fk=body['id']).first()
        item.nome_usuario = body['nomeUsuario']
        item.lingua = body['lingua']
        if body.get('situacaoConta'):
            item.situacao_conta = body['situacaoConta']
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
            funcionarios = session.query(Funcionario).filter_by(empresa_fk=item.id)
            for funcionario in funcionarios:
                funcionario = session.query(Usuario).filter_by(id=funcionario.usuario_fk).first()
                session.delete(funcionario)
            session.commit()
            session.delete(item)
            session.commit()
        return item
    except Exception as ex:
        logging.error(ex)
        session.rollback()
    finally:
        session.close()


def is_unique(body: dict):
    session = get_config().get_session()
    try:
        item = session.query(Empresa).filter_by(nome_usuario=body['nomeUsuario']).first()
        if body.get('id'):
            return False if item and int(body.get('id')) != item.usuario_fk else True
        else:
            return False if item else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    finally:
        session.close()
