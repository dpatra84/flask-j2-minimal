from pdfminer.high_level import extract_text
import pandas as pd


def pdf_to_txt(file_path):
    text = extract_text(file_path)
    return text
