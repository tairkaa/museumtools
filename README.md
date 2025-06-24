# museumtools
Tools for cpu museum
# 1. extract_pdf_images.py
Requirements:
'''
pip install pymupdf pillow
'''

Input: pdf files with N pages
Output: small and big photos in dirs by pdf name
Example:
>input
L12345.pdf with 2 pages (each page contain 1 photo)
<output
small/L12345/0.jpg
small/L12345/1.jpg
big/L12345/0.jpg
big/L12345/1.jpg

