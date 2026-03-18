from ea.logger.app_logger import setup_logger


def main():
    logger = setup_logger()

    logger.debug("Debug message")
    logger.info("Info message")
    logger.error("Something went wrong")
    
    
if __name__ == "__main__":
    main()
