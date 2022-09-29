import logging
from datetime import datetime, timedelta

import jwt

from config import get_config
from controller.api_helper import ApiError
from model.administrador import AdministradorHelper, query_all_adm
from model.empresa import EmpresaHelper, query_all_empresa
from model.operador import OperadorHelper, query_all_operador
from model.usuario import UsuarioHelper

config = get_config()


def validate_access(body: dict):
    try:
        usuario = get_usuario(body=body)
        if UsuarioHelper.verify_password(item=usuario, senha_sem_hash=body['senha']):
            return {
                'token': generate_auth_token(usuario),
                'usuario': serialize_usuario(usuario)
            }
        else:
            ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')
    except Exception as ex:
        logging.error(ex)
        raise ex


def serialize_usuario(usuario: dict):
    if usuario.get('tipo') == 'operador':
        return OperadorHelper.serialize(usuario)
    elif usuario.get('tipo') == 'empresa':
        return EmpresaHelper.serialize(usuario)
    elif usuario.get('tipo') == 'administrador':
        return AdministradorHelper.serialize(usuario)


def generate_auth_token(usuario: dict, exp=60):
    date_time = datetime.utcnow() + timedelta(minutes=exp)
    payload_data = {
        'id': usuario.get('id'),
        'exp': int(date_time.timestamp()),
        'tipo': usuario.get('tipo')
    }
    if usuario.get('tipo') == 'operador':
        payload_data['empresa'] = usuario.get('empresa_fk')
        payload_data['acesso'] = usuario.get('tipo_acesso')
    if usuario.get('tipo') == 'empresa':
        payload_data['situacao'] = usuario.get('situacao_conta')
    token = jwt.encode(payload_data, config.secret, algorithm='HS256')
    return token


def get_usuario(body: dict):
    tipo = body['tipo']
    usuario = None
    if tipo == 'empresa':
        items = query_all_empresa(nome=body['nomeUsuario'])
        usuario = items[0] if items else None
    elif tipo == 'operador':
        items = query_all_empresa(nome=body['nomeEmpresa'])
        empresa = items[0] if items else None
        if not empresa:
            ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')
        items = query_all_operador(empresa_id=empresa.get('id'), nome=body['nomeUsuario'])
        usuario = items[0] if items else None
    elif tipo == 'administrador':
        items = query_all_adm(nome=body['nomeUsuario'])
        usuario = items[0] if items else None
    else:
        ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')
    if not usuario:
        ApiError(error_code=401, error_message='Senha ou nome de usuário inválidos.')
    return usuario
