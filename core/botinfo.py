import ConfigParser, json
#"ed" : EventDispatcher, "nick" : "", "hostmask" : "", "channels" : []
bot_info = dict()

def read_config(config_name):
	config = ConfigParser.ConfigParser()
	config.read(config_name)
	for section in config.sections():
		bot_info[section] = get_config(config, section)
	return bot_info[config_name]
	
def read_config_section(config_name, section):
	config = ConfigParser.ConfigParser()
	config.read(config_name)
	bot_info[section] = get_config_section(config, section)
	return bot_info[section]

def get_config_section(config, section):
	option_dict = dict()
	for option in config.options(section):
		try:
			option_dict[option] = json.loads(config.get(section, option))
		except:
			option_dict[option] = None
	return option_dict
