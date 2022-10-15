import logging
from connexion import App
from connexion.resolver import RestyResolver
from config import get_config
from service.administrador import find, create

config = get_config()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=config.logging_level)

options = {'swagger_url': '/'}
application = App(__name__, specification_dir='swagger/', options=options)
application.add_api('v1.yaml', resolver=RestyResolver('controller'), strict_validation=False)
application.secret_key = config.secret
application.debug = config.debug

if __name__ == '__main__':
    config.create_table()
    admins = find()
    if not admins:
        create(body={
            'nomeUsuario': 'admin',
            'senha': '123@123'
        })
    application.run(debug=False)
