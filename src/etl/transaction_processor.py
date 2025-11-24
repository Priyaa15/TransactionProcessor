import csv
import logging
from datetime import datetime

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

    #2. Clean and validate the data 

    def clean_data(self):
        """Clean and validate transaction data"""
        cleaned = []

        for tx in self.transactions:
            try:
                # convert amount into float
                tx['amount'] = float(tx['amount'])

                # validate timestamp format
                datetime.strptime(tx['timestamp'], '%y-%m-%d %H:%M:%S')

                #Validate transaction type
                if tx['transaction_type'] not in ['debit', 'credit']:
                    raise ValueError(f"Invalid transaction type: {tx['transaction_type']}")
                
                #Validate status
                if tx['status'] not in ['posted', 'failed', 'refunded']:
                    raise ValueError(f"Invalid status {tx['status']}")
                
                cleaned.append(tx)
            except ValueError as e:
                logger.error(f"invalid transaction: {tx['transaction_id']}{e}")
                self.error_records.append({
                    'transaction_id': tx['transaction_id'],
                    'error': str(e)
                })
            
            self.transactions = cleaned
            logger.info(f"Successfully cleaned transactions: {len(cleaned)} transactions")


        
