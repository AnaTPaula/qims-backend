import logging

from config import get_config, config_application
from service.administrador import find, create

if __name__ == '__main__':
    config = get_config()
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=config.logging_level)

    # config.create_table()
    admins = find()
    if not admins:
        create(body={
            'nomeUsuario': 'admin',
            'senha': '123@123'
        })
    app = config_application(config=config)
    app.run(port=config.port_host)
