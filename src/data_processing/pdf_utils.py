# will unpack the pdf to text
import pdfplumber 
import time



'''
user uploads pdf
feeds it to pdf class
pdf class features:
- translates entire pdf to txt
- fetches txt for any page user requests

''' 

class PdfProcessor:
    '''
    class to process pdf files into text
    '''
    #constructor
    def __init__(self, pdf_file: str, uploaded_by: str = 'test'): # uploaded by type can be UserAccount instead so the pdf's are linked to user ID
        self.file_path = pdf_file
        self.uploaded_by = uploaded_by
        self.extracted_text = ''

        try:

            with pdfplumber.open(self.file_path) as pdf:
                self.totalPages = len(pdf.pages)

        except TypeError as type_error:
            
            print(f"Invalid file type: {type_error}")

        except FileNotFoundError as invalid_file_path:

            print(f"File not found: {invalid_file_path}")
        

    def NumPages(self) -> int:
        return self.totalPages
        
    
    def getPages(self, page_num: int = None, end_page: int = None) -> str:
        '''
        returns text from user requested page or range of pages
        '''
        extracted_text = ''
        
        with pdfplumber.open(self.file_path) as pdf:
            if page_num is None and end_page is None:
                page_num = 1                    # for 0 based indexing
                end_page = self.totalPages      # self.totalPages is 1 based indexing so no need to add 1
            elif end_page is None:                                   # if page_num then set end_page 
                end_page = page_num             # to compensate for 0 based indexing below

            # input validation if pages are specified
            if page_num <= 0 or page_num > self.totalPages:
                raise ValueError(f"Invalid page number. Make sure it's within the range 1 to {self.totalPages}.")
            
            elif end_page > self.totalPages or end_page < page_num:
                raise ValueError(f"Invalid end page. Did you mean page {self.totalPages}?")
            
            '''print(f"start page: {page_num}")
            print(f"end page {end_page}")'''

            for page in range(page_num - 1, end_page):  # for 0 based indexing
                extracted_text += pdf.pages[page].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
                #extracted_text += f"\n{'--' * 30}\n"
        
            return extracted_text
    
    def getPagesInChunks(): # if big pdf, then process every 5 pages, serve info, and repeat
        pass
    
    def getAll(self) -> str:
        '''
        returns every page from pdf
        '''
        extracted_text = self.getPages()
        
        return extracted_text
    



if __name__ == "__main__":
    pass