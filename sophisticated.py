import csv
import re
import os
import logging

# Configure logging
logging.basicConfig(filename='data_extraction.log', level=logging.INFO)

def clean_text(text):
    return re.sub(r'[,"\']', '', text.strip())

def extract_data_from_text(text_content):
    data = []
    emails = text_content.split('From:')
    for email in emails:
        email_data = {'Name': '', 'Emails': []}
        lines = email.split('\n')
        for line in lines:
            if line.startswith('To:'):
                to_value = line.replace('To:', '').strip()
                email_data['Emails'] = [email.strip() for email in to_value.split(',')]
            elif line.startswith('Dear'):
                name_match = line.split('Dear', 1)[-1].strip()
                if name_match:
                    email_data['Name'] = clean_text(name_match)
        data.append(email_data)
    return data

folder_path = 
output_csv_path = 


# Open the CSV file in 'write' mode
with open(output_csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Name'] + [f'Email_{i}' for i in range(1, 11)]  # Assuming a maximum of 10 emails
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)

            try:
                with open(file_path, 'r') as file:
                    text_content = file.read()
                    logging.info("Processing file: %s", filename)
                    
                    # Check if the file is empty
                    if not text_content.strip():
                        logging.warning("File %s is empty.", filename)
                        continue
            except Exception as e:
                logging.warning(f"Error reading file {filename}: {e}")
                continue

            # Extract email data from the text content
            try:
                extracted_data = extract_data_from_text(text_content)
            except Exception as e:
                logging.warning(f"Error extracting data from file {filename}: {e}")
                continue

            # Write extracted data to the CSV file
            for row in extracted_data:
                if any(row['Emails']):  # Check if there are any emails in the row
                    writer.writerow({**{'Name': row['Name']}, **{f'Email_{i}': email for i, email in enumerate(row['Emails'], start=1)}})
