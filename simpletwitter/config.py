import configparser


def read_config(key_file):
    config = configparser.ConfigParser()
    config.read(key_file)
    return config.get("twitter", "api_key"), config.get("twitter", "api_secret")
