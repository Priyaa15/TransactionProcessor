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
            logger.info(f"Successfully cleaned transactions: {len(cleaned)} transactions. Found {len(self.error_records)}")

        #3. Calculate daily Transaction summary

        def calc_daily_trasaction_summary(Self):
            """calculate daily transaction summaries"""
            daily_totals = {} #empty dict
            
            for tx in self.transactions:
                date = datetime.strptime(tx['timestamp', '%y-%m-%d %H:%M:%S']).date
                date_iso = date.isoformat() # extract date into iso format

                if date_iso not in daily_totals: # if date doesn't exist, then add the following schema
                    daily_totals[date_iso] = {
                        'total_debit' :0,
                        'total_credit':0,
                        'successful_tx':0,
                        'failed_tx':0,
                        'total_tx':0,
                        'avg_tx':0
                    }
                    #update daily debit/credit

                    if tx['transaction_type'] == 'debit':
                        daily_totals[date_iso]['total_debit'] += tx['amount']
                    else:
                        daily_totals[date_iso]['total_credit'] += tx['amount']

                    if tx['status'] == 'posted':
                        daily_totals[date_iso]['successful_tx'] += 1
                    else:
                        daily_totals[date_iso]['failed_tx'] += 1
                    
                    daily_totals[date_iso]["total_tx"] += 1 # ALL TOTALS

                    #calc avg
                    for date in daily_totals:
                        total_value = daily_totals[date]['total_debit'] + daily_totals[date]['total_credit']
                        total_tx = daily_totals[date['total_tx']]
                        daily_totals[date]['avg_transactions'] = round (total_value/total_tx)

                    return daily_totals




        
