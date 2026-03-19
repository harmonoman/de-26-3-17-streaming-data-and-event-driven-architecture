from ea.logger.app_logger import setup_logger
from ea.snowflake_ingestion.load_customers import load_customers


def main():
    setup_logger()

    load_customers("/Users/markbond/Downloads/customers.csv")
    
    
if __name__ == "__main__":
    main()
