import csv
import re
import os
import logging
import chardet

# Configure logging
logging.basicConfig(filename='data_extraction.log', level=logging.INFO)

def clean_text(text, is_email=False):
    chars_to_remove = r'[,"\']'  # Remove double quotes and single quotes
    if is_email:
        return re.sub(chars_to_remove, '', text.strip())
    else:
        return text.replace(',', '')  # Remove commas from Name column

def extract_data_from_text(text_content):
    data = []

    # Handle empty lines within email entries (Option 1)
    emails = text_content.split('\n\n')
    for i in range(len(emails) - 1):
        if not emails[i] and not emails[i+1]:  # Check for consecutive empty lines
            emails[i] = emails[i] + '\n' + emails[i+1]  # Join them

    # Alternatively, use more robust email entry separators (Option 2)
    # emails = re.split(r'\n\n(?=\S)', text_content)  # Split only before non-whitespace lines

    for email in emails:
        email_data = {'Name': '', 'Emails': []}
        lines = email.split('\n')
        for line in lines:
            if line.startswith('TO :'):
                to_value = line.replace('TO :', '').strip()
                email_data['Emails'] = to_value.split(',')  # Store all emails without immediate cleaning
            elif line.startswith('Dear'):
                email_data['Name'] = clean_text(line.replace('Dear', '').strip())

        # Check for missing data and log warnings
        if not email_data['Name']:
            logging.warning("Missing Name in email: %s", email)
        if not email_data['Emails']:
            logging.warning("Missing Email addresses in email: %s", email)

        data.append(email_data)
    return data

folder_path = '/Users/vedant/Downloads/untitled folder/'  # Replace with your folder path
output_csv_path = '/Users/vedant/Downloads/Testing_script/output_data2.csv'  # Replace with your output file path

# Open the CSV file in 'append' mode to add data for each file
with open(output_csv_path, 'a', newline='') as csvfile:
    fieldnames = ['Name', 'Email_1', 'Email_2', 'Email_3', 'Email_4', 'Email_5','Email_6','Email_7','Email_8','Email_9','Email_10']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header only if the file is empty
    if os.path.getsize(output_csv_path) == 0:
        writer.writeheader()

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # Process only text files
            file_path = os.path.join(folder_path, filename)

            try:
                # Enhanced encoding handling
                
                with open(file_path, 'rb') as file:
                    rawdata = file.read()
                    result = chardet.detect(rawdata)
                    encoding = result['encoding']
                with open(file_path, 'r', encoding=encoding) as file:
                    text_content = file.read()
                    logging.info("Processing file: %s", filename)
            except UnicodeDecodeError:
                try:
                    # Fallback to 'latin-1' encoding
                    with open(file_path, 'r', encoding='latin-1') as file:
                        text_content = file.read()
                        logging.warning("Fallback encoding used for file: %s", filename)
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                    logging.error("Error reading file: %s", filename, exc_info=True)
                    continue

            # Extract email data and write to CSV
            extracted_data = extract_data_from_text(text_content)
            for email_data in extracted_data:
                emails = email_data['Emails']
                row = {'Name': email_data['Name'], 'Email_1': emails[0]}  # Add more email columns as needed
                for i in range(1, len(emails)):
                    row[f'Email_{i+1}'] = emails[i]  # Dynamically create columns for additional emails
                writer.writerow(row)


