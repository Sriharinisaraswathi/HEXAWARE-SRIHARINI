from configparser import ConfigParser

def get_connection_string(file_name):
    config = ConfigParser()
    config.read(file_name)
    
    driver = config['database']['driver']
    server = config['database']['server']
    database = config['database']['database']
    trusted_connection = config['database']['trusted_connection']

    return f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};"
