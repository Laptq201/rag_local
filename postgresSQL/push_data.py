import argparse
from test_database import connect_db
from test_database import add_dummy_data
from test_database import delete_data_in_postgres
import extract_text as extract_text
from chunk_text import text_chunk

# Set up argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Process PDF file and push data.")
    parser.add_argument('-d', '--pdf', type=str, required=True, help="Path to the PDF file.")
    return parser.parse_args()

# Main script execution
def main():
    # Parse arguments
    args = parse_arguments()

    # Connect to the database and delete existing data
    pdf_path = args.pdf
    pdf_text = extract_text.text_extract(pdf_path)

    dummy_data = text_chunk(pdf_text, max_length=1000)

    dummy_data = [{'title': f"Document {i+1}", 'content': chunk} for i, chunk in enumerate(dummy_data)]
    print(dummy_data[0])  # Print the first chunk of data

    # delete_data_in_postgres()  # Uncomment if you want to delete existing data first
    add_dummy_data(dummy_data)

if __name__ == "__main__":
    main()
