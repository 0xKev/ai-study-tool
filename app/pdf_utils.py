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
        self.extracted_text = ''

        with pdfplumber.open(self.file_path) as pdf:
            self.totalPages = len(pdf.pages)
          

    def NumPages(self) -> int:
        return self.totalPages
        
    
    def getPages(self, page_num: int = None, end_page: int = None) -> str:
        '''
        returns text from user requested page or range of pages
        '''
        extracted_text = ''
        
        with pdfplumber.open(self.file_path) as pdf:
            if page_num is None:
                if end_page is None:
                    page_num = 0                    # for 0 based indexing
                    end_page = self.totalPages      # to include last page + 1
            else:                                   # if page_num then set end_page 
                end_page = page_num + 1             # to include last page

            # input validation if pages are specified
            if page_num < 0 or page_num > self.totalPages:
                raise ValueError("Invalid page number.")
            
            elif end_page > self.totalPages or end_page < page_num:
                raise ValueError("Invalid end page.")
            
            print(f"start page: {page_num}")
            print(f"end page {end_page}")

            for page in range(page_num, end_page):
                extracted_text += pdf.pages[page].extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
                #extracted_text += f"\n{'--' * 30}\n"
        
            return extracted_text
    
    
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

if __name__ == "__main__":

    the_happy_prince = PdfProcessor("..\pdf_files\The_Happy_Prince by Oscar Wilde.pdf")
    print(the_happy_prince.getPages(1))
    #print(the_happy_prince.getAll)