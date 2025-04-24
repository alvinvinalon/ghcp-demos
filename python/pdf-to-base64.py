#!/usr/bin/env python
"""
PDF to Base64 Converter

A simple utility to convert PDF files to Base64 encoded strings.
"""

import base64
import argparse
import os
import sys
from pathlib import Path


def convert_pdf_to_base64(file_path):
    """
    Convert a PDF file to a Base64 encoded string.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Base64 encoded string of the PDF file
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is not a PDF file
    """
    file_path = Path(file_path)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Check if it's a PDF file
    if file_path.suffix.lower() != '.pdf':
        raise ValueError(f"The file {file_path} is not a PDF file.")
    
    # Read the file in binary mode and encode it
    with open(file_path, 'rb') as file:
        pdf_data = file.read()
        base64_data = base64.b64encode(pdf_data).decode('utf-8')
        
    return base64_data


def main():
    """Main function to handle command-line arguments and convert PDFs to base64."""
    parser = argparse.ArgumentParser(description='Convert a PDF file to Base64 encoded string.')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output file to save base64 string (optional)')
    
    args = parser.parse_args()
    
    try:
        base64_string = convert_pdf_to_base64(args.pdf_path)
        
        if args.output:
            # Save to output file
            with open(args.output, 'w') as output_file:
                output_file.write(base64_string)
            print(f"Base64 string saved to {args.output}")
        else:
            # Print to console
            print("Base64 string (copy and paste from below):")
            print("-" * 40)
            print(base64_string)
            print("-" * 40)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()