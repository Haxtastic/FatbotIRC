import ConfigParser, json, os

bot_info = dict()

def read_config(config_dir, config_name):
    #global bot_info
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_dir, config_name)
    configReader = ConfigParser.ConfigParser()
    configReader.read(config_path)
    config = dict()
    for section in configReader.sections():
        config[section] = get_config_section(configReader, section)
    #print bot_info
    return config
    
def read_config_section(config_path, section):
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    return get_config_section(config, section)

def get_config_section(config, section):
    option_dict = dict()
    for option in config.options(section):
        try:
            option_dict[option] = json.loads(config.get(section, option))
        except:
            option_dict[option] = None
    return option_dict
