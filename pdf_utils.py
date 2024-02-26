# will unpack the pdf to text
import pdfplumber

'''
user uploads pdf
feeds it to pdf class
pdf class features:
- translates entire pdf to txt
- fetches txt for any page user requests

'''


class PdfProcessor:
    #constructor
    def __init__(self, pdf_file: str, uploaded_by: str = 'test'): # uploaded by type can be UserAccount instead so the pdf's are linked to user ID
        self.file_path = pdf_file
        self.uploaded_by = uploaded_by
        self.extracted_text = None

        with pdfplumber.open(self.file_path) as pdf:
            self.totalPages = len(pdf.pages)
          

    def NumPages(self) -> int:
        return self.totalPages
        
    
    def getPages(self, page_num: int, end_page : int) -> str:
        '''
        returns text from user requested page or range of pages
        '''
        extracted_text = None
        page_num -= 1 # bc page starts from 0 and must compensate

        
        with pdfplumber.open(self.file_path) as pdf:
            if end_page > page_num and end_page <= self.totalPages:
                for page in range(page_num, end_page):
                    extracted_text += pdf.pages[page].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
            
                return extracted_text
      
            return pdf.pages[page_num].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
    
    def getPagesInChunks(): # if big pdf, then process every 5 pages, serve info, and repeat
        pass
    
    def getAll(self) -> str:
        '''
        returns every page from pdf
        '''
        extracted_text = self.getPages(1, self.totalPages)
        
        return extracted_text
class NoteSummarizer:
    pass

'''reader = PdfReader("pdf_files\The_Happy_Prince by Oscar Wilde.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()'''

the_happy_prince = PdfProcessor("pdf_files\The_Happy_Prince by Oscar Wilde.pdf")
#print(the_happy_prince.getPages(1))
print(the_happy_prince.getAll)