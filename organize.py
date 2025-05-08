import os
import shutil

# Define the target structure
structure = {
    'fraud_signature_detection/models': ['compare.py'],  # Put logic here
    'fraud_signature_detection/database': ['database.py', 'signatures.db'],
    'fraud_signature_detection/templates': ['index.html', 'dashboard.html'],
    'fraud_signature_detection/static/uploads': ['signature1.png'],
}

# Create folders
for path in structure:
    os.makedirs(path, exist_ok=True)

# Mapping current files to new names/locations
file_renames = {
    'signature_compare.py': 'compare.py',
    'fraud_signatures.py': 'database.py',
    'fraud_signatures.db': 'signatures.db',
}

# Move and rename files
for old_name, new_name in file_renames.items():
    if os.path.exists(old_name):
        for target_path in structure:
            if new_name in structure[target_path]:
                shutil.move(old_name, os.path.join(target_path, new_name))

# Move HTML files if present
html_files = ['index.html', 'dashboard.html']
for file in html_files:
    if os.path.exists(file):
        shutil.move(file, os.path.join('fraud_signature_detection/templates', file))

# Move the image file
if os.path.exists('signature1.png'):
    shutil.move('signature1.png', 'fraud_signature_detection/static/uploads/signature1.png')

# Move main file
if os.path.exists('main.py'):
    shutil.move('main.py', 'fraud_signature_detection/app.py')
elif os.path.exists('signature_compare.py'):
    shutil.move('signature_compare.py', 'fraud_signature_detection/app.py')

# Move requirements.txt if exists
if os.path.exists('requirements.txt'):
    shutil.move('requirements.txt', 'fraud_signature_detection/requirements.txt')

print("Files organized successfully.")