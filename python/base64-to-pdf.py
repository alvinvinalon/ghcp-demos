#!/usr/bin/env python
"""
Base64 to PDF Converter

A simple utility to convert Base64 encoded strings back to PDF files.
"""

import base64
import argparse
import os
import sys
from pathlib import Path


def convert_base64_to_pdf(base64_string, output_path):
    """
    Convert a Base64 encoded string back to a PDF file.
    
    Args:
        base64_string (str): Base64 encoded string of PDF data
        output_path (str): Path where to save the PDF file
        
    Raises:
        ValueError: If the base64 string is invalid
    """
    try:
        # Decode the base64 string to binary data
        pdf_data = base64.b64decode(base64_string)
        
        # Write binary data to file
        output_path = Path(output_path)
        with open(output_path, 'wb') as file:
            file.write(pdf_data)
            
        return output_path
    except base64.binascii.Error:
        raise ValueError("Invalid base64 string provided")


def create_sample_base64(output_file=None):
    """
    Create a sample base64 encoded PDF for demonstration purposes.
    This creates a minimal valid PDF file.
    
    Args:
        output_file (str, optional): Path to save the base64 string
    
    Returns:
        str: A sample base64 string representing a minimal PDF
    """
    # This is a minimal valid PDF file in binary
    minimal_pdf = (
        b'%PDF-1.0\n'
        b'1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n'
        b'2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n'
        b'3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n'
        b'xref\n'
        b'0 4\n'
        b'0000000000 65535 f\n'
        b'0000000010 00000 n\n'
        b'0000000053 00000 n\n'
        b'0000000102 00000 n\n'
        b'trailer<</Size 4/Root 1 0 R>>\n'
        b'startxref\n'
        b'178\n'
        b'%%EOF\n'
    )
    
    # Convert to base64
    base64_string = base64.b64encode(minimal_pdf).decode('utf-8')
    
    if output_file:
        with open(output_file, 'w') as file:
            file.write(base64_string)
            
    return base64_string


def main():
    """Main function to handle command-line arguments and convert base64 to PDF."""
    parser = argparse.ArgumentParser(description='Convert Base64 encoded string back to a PDF file.')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-s', '--string', help='Base64 encoded string')
    input_group.add_argument('-f', '--file', help='File containing the Base64 encoded string')
    input_group.add_argument('--sample', action='store_true', help='Create a sample base64 string for demo purposes')
    
    parser.add_argument('-o', '--output', required=True, help='Output path for the PDF file')
    
    args = parser.parse_args()
    
    try:
        if args.sample:
            print("Creating a sample base64 encoded PDF...")
            base64_string = create_sample_base64()
        elif args.file:
            with open(args.file, 'r') as file:
                base64_string = file.read().strip()
        else:
            base64_string = args.string
        
        output_path = convert_base64_to_pdf(base64_string, args.output)
        print(f"PDF file successfully saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()