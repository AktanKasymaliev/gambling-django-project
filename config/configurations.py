
from configparser import ConfigParser, NoOptionError, NoSectionError
import os

def load_config(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError) as e:
        output = default
    return output

def config() -> None:
    config_parse = ConfigParser()
    config_parse.read("settings.ini")
    DATABASE = "DATABASE"
    SYSTEM = "SYSTEM"

    #DATABASE
    os.environ.setdefault("DATABASE_NAME", load_config(config_parse, DATABASE, "DATABASE_NAME"))
    os.environ.setdefault("DATABASE_USER", load_config(config_parse, DATABASE, "DATABASE_USER"))
    os.environ.setdefault("DATABASE_PASSWORD", load_config(config_parse, DATABASE, "DATABASE_PASSWORD"))
    os.environ.setdefault("DATABASE_HOST", load_config(config_parse, DATABASE, "DATABASE_HOST"))
    os.environ.setdefault("DATABASE_PORT", load_config(config_parse, DATABASE, "DATABASE_PORT"))
    
    #SYSTEM
    os.environ.setdefault("DJANGO_DEBUG", load_config(config_parse, SYSTEM, "DJANGO_DEBUG", "False"))
    os.environ.setdefault("DJANGO_KEY", load_config(config_parse, SYSTEM, "DJANGO_KEY", "super_secret_key"))