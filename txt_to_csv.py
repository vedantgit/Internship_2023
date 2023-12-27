# import csv
# import re
# import os

# # def clean_text(text):
# #     chars_to_remove = r'[,"!  ]'  # Example: commas, double quotes, exclamation marks
# #     cleaned_text = re.sub(chars_to_remove, '', text)
# #     return cleaned_text

# def clean_text(text, is_email=False):
#     chars_to_remove = r'[,"\']'  # Remove double quotes and single quotes
#     if is_email:
#         return re.sub(chars_to_remove, '', text.strip())
#     else:
#         return text.replace(',', '')  # Remove commas from Name column




# def extract_data_from_text(text_content):
#     data = []
#     emails = text_content.split('\n\n')  # Split by empty lines as each email entry is separated by empty lines
#     for email in emails:
#         email_data = {'TO': '', 'Name': ''}
#         lines = email.split('\n')
#         for line in lines:
#             if line.startswith('TO :'):
#                 email_data['TO'] = line.replace('TO :','').strip()
#             elif line.startswith('Dear'):
#                 email_data['Name'] = line.replace('Dear','').strip()

#         # email_data['TO'] = clean_text(email_data['TO'])
#         # email_data['Name'] = clean_text(email_data['Name'])
#         email_data['TO'] = clean_text(email_data['TO'], is_email=True)
#         email_data['Name'] = clean_text(email_data['Name'])

#         data.append(email_data)
#     return data

# folder_path = '/Users/vedant/Downloads/untitled folder/'  # Replace this placeholder with the folder path
# output_csv_path = '/Users/vedant/Downloads/Testing_script/output_data.csv'

# # Open the CSV file in 'append' mode to add data for each file
# with open(output_csv_path, 'a', newline='') as csvfile:
#     fieldnames = ['Name', 'Email']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # Write header only if the file is empty
#     if os.path.getsize(output_csv_path) == 0:
#         writer.writeheader()

#     # Iterate through files in the folder
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.txt'):  # Process only text files
#             file_path = os.path.join(folder_path, filename)
            
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     text_content = file.read()
#             except UnicodeDecodeError:
#                 # Try reading the file with a different encoding (e.g., 'latin-1')
#                 try:
#                     with open(file_path, 'r', encoding='latin-1') as file:
#                         text_content = file.read()
#                 except Exception as e:
#                     print(f"Error reading file {filename}: {e}")
#                     continue

#             # Extract 'TO' value and text after 'Dear' from the text content
#             extracted_data = extract_data_from_text(text_content)

#             # Write extracted data to the CSV file
#             for email_data in extracted_data:
#                 writer.writerow({'Email': email_data['TO'], 'Name': email_data['Name']})

# print(f"Data extracted from files in {folder_path} and saved to {output_csv_path}.")


#___________________________________________________________________________________________________________________________


import csv
import re
import os

def clean_text(text, is_email=False):
    chars_to_remove = r'[,"\']'  # Remove double quotes and single quotes
    if is_email:
        return re.sub(chars_to_remove, '', text.strip())
    else:
        return text.replace(',', '')  # Remove commas from Name column

def extract_data_from_text(text_content):
    data = []
    emails = text_content.split('\n\n')  # Split by empty lines as each email entry is separated by empty lines
    for email in emails:
        email_data = {'Name': '', 'Emails': []}  # Initialize empty list for emails
        lines = email.split('\n')
        for line in lines:
            if line.startswith('TO :'):
                to_value = line.replace('TO :', '').strip()
                email_data['Emails'] = [clean_text(email.strip(), is_email=True) for email in to_value.split(',')]
            elif line.startswith('Dear'):
                email_data['Name'] = clean_text(line.replace('Dear', '').strip())
        
        data.append(email_data)
    return data

folder_path = '/Users/vedant/Downloads/untitled folder/'  # Replace this placeholder with the folder path
output_csv_path = '/Users/vedant/Downloads/Testing_script/output_data.csv'  # Replace this placeholder with the output file path

# Open the CSV file in 'append' mode to add data for each file
with open(output_csv_path, 'a', newline='') as csvfile:
    fieldnames = ['Name', 'Email_1', 'Email_2', 'Email_3', 'Email_4', 'Email_5','Email_6','Email_7','Email_8','Email_9','Email_10']  # Assuming maximum 10 email columns
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header only if the file is empty
    if os.path.getsize(output_csv_path) == 0:
        writer.writeheader()

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # Process only text files
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
            except UnicodeDecodeError:
                # Try reading the file with a different encoding (e.g., 'latin-1')
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        text_content = file.read()
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                    continue

            # Extract email data from the text content
            extracted_data = extract_data_from_text(text_content)

            # Write extracted data to the CSV file
            for email_data in extracted_data:
                row = {'Name': email_data['Name']}
                for i, email in enumerate(email_data['Emails'], start=1):
                    row[f'Email_{i}'] = email
                writer.writerow(row)

print(f"Data extracted from files in {folder_path} and saved to {output_csv_path}.")