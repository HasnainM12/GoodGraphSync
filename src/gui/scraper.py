import requests
from bs4 import BeautifulSoup

class GoodreadsScraper:
    def __init__(self, user_id):
        self.user_id = user_id  # '177602267-hasnain'
        self.want_to_read_url = f'https://www.goodreads.com/review/list/{user_id}?shelf=to-read'
    
    def get_books(self):
        try:
            print("Fetching 'Want to Read' books...")
            response = requests.get(self.want_to_read_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            books = []
            # Find the table containing the books
            table = soup.find('table', {'id': 'books'})
            
            if table:
                for row in table.find_all('tr', {'class': 'bookalike'}):
                    title_cell = row.find('td', {'class': 'field title'})
                    author_cell = row.find('td', {'class': 'field author'})
                    
                    if title_cell and author_cell:
                        title = title_cell.find('a', {'class': 'bookTitle'}).text.strip()
                        author = author_cell.find('a', {'class': 'authorName'}).text.strip()
                        print(f"Found book: {title} by {author}")  # Debug print
                        books.append({
                            'title': title,
                            'author': author,
                            'status': 'Want to Read',
                            'platform': 'Goodreads'
                        })
            else:
                print("No table found")  # Debug print
            
            return books
            
        except Exception as e:
            print(f"Error getting books: {e}")
            return []

# Test the scraper
if __name__ == "__main__":
    scraper = GoodreadsScraper('177602267-hasnain')
    books = scraper.get_books()
    
    print("\nBooks found:")
    for book in books:
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print("Status: Want to Read")
        print("-" * 30)