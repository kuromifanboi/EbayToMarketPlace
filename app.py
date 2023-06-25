import csv
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the index page with a file upload form.
    """
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """
    Handles the file upload and conversion process.
    """
    ebay_csv_file = request.files['file']
    
    if ebay_csv_file:
        # Save the uploaded file temporarily
        file_path = 'temp.csv'
        ebay_csv_file.save(file_path)

        # Convert the file
        facebook_csv_file = 'converted.csv'
        convert_ebay_to_facebook(file_path, facebook_csv_file)

        # Remove the temporary file
        os.remove(file_path)

        # Send the converted file as a download
        return send_file(facebook_csv_file, as_attachment=True, attachment_filename='converted.csv')
    
    return 'Error: No file provided.'

def convert_ebay_to_facebook(ebay_csv_file, facebook_csv_file):
    """
    Converts the eBay CSV file to Facebook-compatible CSV format.

    Args:
        ebay_csv_file (str): Path to the eBay CSV file.
        facebook_csv_file (str): Path to save the converted Facebook CSV file.
    """
    with open(ebay_csv_file, 'r') as ebay_file:
        ebay_reader = csv.DictReader(ebay_file)
        with open(facebook_csv_file, 'w', newline='') as facebook_file:
            fieldnames = ['Title', 'Description', 'Price', 'Condition', 'Image URL']
            facebook_writer = csv.DictWriter(facebook_file, fieldnames=fieldnames)
            facebook_writer.writeheader()
            for row in ebay_reader:
                title = row['Title']
                description = row['Description']
                price = row['Price']
                condition = row['Condition']
                image_url = row['Image URL']
                facebook_writer.writerow({
                    'Title': title,
                    'Description': description,
                    'Price': price,
                    'Condition': condition,
                    'Image URL': image_url
                })

if __name__ == '__main__':
    app.run()
