import pdfplumber

with pdfplumber.open("pdf_files\The_Happy_Prince by Oscar Wilde.pdf") as pdf:
    allPages = len(pdf.pages)

    for page in range(allPages):
        print(pdf.pages[page].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13))