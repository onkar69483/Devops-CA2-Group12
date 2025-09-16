import uvicorn
from app.configs.logging_config import setup_logger
from config.config_manager import ConfigurationManager

# Setup logger
logger = setup_logger()

# Initialize Configuration Manager
config_manager = ConfigurationManager()
config_manager.load_config()

try:
    # Read server settings with error handling
    HOST = config_manager.get("server","host", "127.0.0.0").strip()
    PORT = int(config_manager.get("server","port", "9001"))
    RELOAD = bool(config_manager.get("server","reload", "true"))
    LOGLEVEL = config_manager.get("server","loglevel", "info").strip()

except (ValueError, KeyError) as config_error:
    logger.critical(f"Error reading configuration: {str(config_error)}", exc_info=True)

def main():
    try:
        logger.info(f"Starting FastAPI app on {HOST}:{PORT} (reload={RELOAD})")
        uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD, log_level=LOGLEVEL)
    except Exception as e:
        logger.critical(f"Failed to start the FastAPI app: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
