from PyPDF2 import PdfReader
import os
from typing import List 


def text_extract(pdf_path: str) -> str:
    pdf_pages = []

    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pdf_pages.append(text)
    
    pdf_text = "\n".join(pdf_pages)
    return pdf_text