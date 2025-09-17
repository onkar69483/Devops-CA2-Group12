import os
import configparser
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

class ConfigurationManager:
    def __init__(self, config_path=None):
        self.config_path = config_path or "config/config.ini"
        self.config = configparser.ConfigParser()
        self.loaded_config = {}
        logger.info("ConfigurationManager initialized.")

    def load_config(self, sections=None):
        try:
            logger.info(f"Attempting to load configuration from {self.config_path}")

            if not os.path.exists(self.config_path):
                logger.error(f"Config file not found at {self.config_path}. Please create it and try again.")
                raise FileNotFoundError(f"Config file not found at {self.config_path}.")

            self.config.read(self.config_path)

            # Load all sections or specific sections as requested
            if sections is None:
                self.loaded_config = {section: dict(self.config[section]) for section in self.config.sections()}
            else:
                for section in sections:
                    if section in self.config:
                        self.loaded_config[section] = dict(self.config[section])
                    else:
                        logger.warning(f"Section '{section}' not found in the configuration file.")

            logger.info("Configuration loaded successfully.")

        except Exception as e:
            logger.error(f"Configuration error: {str(e)}")
            raise

    def save_config(self):
        try:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

    def update_config_value(self, section: str, key: str, value: str):
        try:
            self.config.read(self.config_path)

            if not self.config.has_section(section):
                raise KeyError(f"Section [{section}] not found in config.")

            self.config.set(section, key, value)

            with open(self.config_path, "w") as configfile:
                self.config.write(configfile)

            logger.info(f"Updated [{section}] {key} = {value} in config.")
            
        except KeyError as ke:
            logger.error(str(ke))
            raise
        except Exception as e:
            logger.error(f"Failed to update config: {e}")
            raise

    def get(self, section, key, default=None):
        try:
            self.load_config() 
            return self.loaded_config.get(section, {}).get(key, default)
        except KeyError:
            logger.warning(f"Key '{key}' not found in section '{section}'. Using default value: {default}")
            return default
