import csv
import logging

# Set up logger
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transaction_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
class transaction_processor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.transactions = []
        self.error_records = []


    #1. read method from the sample csv
    
    def read_transactions(self):
        """Read Transactions from the input file"""
    try:
        with open(self.inputfile, 'r') as f:
            reader = csv.DictReader(f)
            self.transactions = list(reader)
            logging.info(f"Successfully read len{self.transactions} transactions")
    except Exception as e:
        logger.info(f"Error Reading transactions: {e}")
        raise


        
