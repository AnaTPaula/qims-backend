from datetime import datetime, timedelta

import jwt

from config import get_config
from controller.api_helper import ApiError
from model.model import Administrador, Empresa, Funcionario

config = get_config()


def validate_access(body: dict):
    usuario = get_usuario(body=body)
    if usuario.verify_password(senha_sem_hash=body['senha']):
        return {
            'token': generate_auth_token(usuario),
            'usuario': usuario.serialize
        }
    else:
        ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')


def generate_auth_token(usuario, exp=60):
    date_time = datetime.utcnow() + timedelta(minutes=exp)
    payload_data = {
        'id': usuario.usuario_fk,
        'exp': int(date_time.timestamp()),
        'tipo': usuario.usuario.tipo
    }
    if usuario.usuario.tipo == 'funcionario':
        payload_data['empresa'] = usuario.empresa_fk
        payload_data['acesso'] = usuario.acesso
    token = jwt.encode(payload_data, config.secret, algorithm='HS256')
    return token


def get_usuario(body: dict):
    session = get_config().get_session()
    tipo = body['tipo']
    usuario = None
    if tipo == 'empresa':
        usuario = session.query(Empresa).filter_by(nome_usuario=body['nomeUsuario']).first()
    elif tipo == 'funcionario':
        empresa = session.query(Empresa).filter_by(nome_usuario=body['nomeEmpresa']).first()
        if not empresa:
            session.close()
            ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')

        usuario = session.query(Funcionario).filter_by(nome_usuario=body['nomeUsuario'],
                                                       empresa_fk=empresa.usuario_fk).first()
    elif tipo == 'administrador':
        usuario = session.query(Administrador).filter_by(nome_usuario=body['nomeUsuario']).first()
    else:
        session.close()
        ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')
    if not usuario:
        session.close()
        ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')
    session.close()
    return usuario
