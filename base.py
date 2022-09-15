

import logging
from Pody.configuration import Configuration
from Pody.connection import Connection
from Pody.factory.repository.generator import Generator



logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

config = Configuration('test', 'root', '', 'localhost', '3306')
Connection(config)
Generator().generate()


pass