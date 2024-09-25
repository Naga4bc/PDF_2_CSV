# -*- coding: utf-8 -*-
"""
@Authour: Nagaraj 
@guidance:Prabir

Original file is located at
    https://colab.research.google.com/drive/1ZvwP3_WqvLdezZQIagkTonNcz0-Z7Ew-
"""

#pip install pdfplumber

import os
import pdfplumber
import pandas as pd
import re

# extract tables and columns from a PDF
def extract_tables_columns(pdf_file, page_number):
    extracted_data = []
    with pdfplumber.open(pdf_file) as pdf:
        tables = pdf.pages[page_number - 1].extract_tables()

        for table in tables:
            extracted_table = [[row[0].strip(), row[3].strip()] for row in table if len(row) >= 4]
            extracted_data.append(extracted_table)
    return extracted_data

# save data to a CSV file
def save_to_csv(data, pdf_filename):
    csv_filename = os.path.splitext(pdf_filename)[0] + ".csv"
    pd.DataFrame(data, columns=["Depth of Coverage", "Target Coverage at or Above Indicated Depth of Coverage"]).to_csv(csv_filename, index=False)
    print(f"Table saved as {csv_filename}")

#remove non-numeric characters from a string
def remove_non_numeric(s):
    return re.sub(r'\D', '', str(s))

#clean table data and convert it to DataFrame
def clean_table(table):
    df = pd.DataFrame(table, columns=["Depth of Coverage", "Target Coverage at or Above Indicated Depth of Coverage"])
    df = df.applymap(remove_non_numeric)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    df['Depth of Coverage'] = df['Depth of Coverage'].astype(str).str.replace('\.0', 'X')
    df['Target Coverage at or Above Indicated Depth of Coverage'] = (df['Target Coverage at or Above Indicated Depth of Coverage'] / 100).astype(str) + '%'
    return df

#input: all the pdf files in input_directory
def main():
    input_directory = "D:\Git\PDF_2_CSV"

    for filename in os.listdir(input_directory):
        if filename.endswith(".pdf"):
            pdf_file = os.path.join(input_directory, filename)
            tables_columns = extract_tables_columns(pdf_file, page_number=5)
            df = pd.concat([clean_table(table) for table in tables_columns], ignore_index=True)
            save_to_csv(df, pdf_file)

if __name__ == "__main__":
    main()