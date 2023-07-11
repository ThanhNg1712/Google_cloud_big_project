#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging
import subprocess

# Configure the logging settings
log_file_path = '/Users/thanhnguyen/Desktop/Data_analysis/DE_k2/project_5/project5_phase2/project5_final/script.log'
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# Example usage of logging statements in your script
def main():
    logging.info('Script execution started.')

    try:
        # Execute the Push_data_mongo2cloud.py script
        python_script_output = subprocess.check_output(['/Users/thanhnguyen/opt/anaconda3/bin/python', '/Users/thanhnguyen/Desktop/Data_analysis/DE_k2/project_5/project5_phase2/project5_final/Push_data_mongo2cloud.py'], stderr=subprocess.STDOUT)
        
        # Log the output of the Python script execution
        logging.info('Python script output:\n{}'.format(python_script_output.decode('utf-8')))
        
        # Example: Log a message when a specific task is completed
        logging.info('Data upload from MongoDB completed.')
        
        # Example: Log an error message if an exception occurs
        logging.error('An error occurred during the execution.')
        
    except Exception as e:
        # Log the exception message
        logging.error('An exception occurred: {}'.format(str(e)))
    
    logging.info('Script execution finished.')

if __name__ == '__main__':
    main()