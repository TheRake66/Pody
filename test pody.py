


import logging
from Pody.configuration import Configuration
from Pody.connection import Connection
from Pody.factory.repository.generator import Generator
from global_tables.tf_pro_agents import Tf_pro_agents



logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)



Connection(Configuration('global_tables', 'root', '', 'localhost', '3306'))
Generator().generate()

agent = Tf_pro_agents('PBfttfr15515').many()

# TODO
# count, size, etc...

pass