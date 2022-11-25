import logging

from flask import make_response
from xhtml2pdf import pisa
from io import StringIO, BytesIO

from config import get_config
from controller.api_helper import handler_exception, token_required, create_response_pdf, create_response_csv
from service.relatorio import saida_produto, entrada_produto, estoque_quantidade, produto_quantidade

config = get_config()


@handler_exception
@token_required(tipos=['empresa', 'operador'], acessos=['total'], validate_empresa=True)
def search(empresa_id: int, body: dict):
    logging.info('Getting informações do relatorio')
    response = []
    body['empresaId'] = empresa_id
    if body['tipo'] == 'saida_produto':
        response = saida_produto(body=body)
    elif body['tipo'] == 'entrada_produto':
        response = entrada_produto(body=body)
    elif body['tipo'] == 'estoque_quantidade':
        response = estoque_quantidade(body=body)
    elif body['tipo'] == 'produto_quantidade':
        response = produto_quantidade(body=body)

    if body['arquivo'] == 'csv':
        return create_response_csv(response=response.to_csv(), status=200)
    else:
        html = response.to_html().replace('<td>', '<td align="center">')
        pdf = BytesIO()
        pisa.CreatePDF(StringIO(html),pdf)
        resp = pdf.getvalue()
        pdf.close()
        return create_response_pdf(resp, status=200)


def options_id(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response
