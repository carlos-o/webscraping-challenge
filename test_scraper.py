import pytest
import scraper
from bs4 import BeautifulSoup


@pytest.mark.parametrize("arg1,result",  [
    ("http://books.toscrape.com/", BeautifulSoup),
    ("https://www.google.cl/", BeautifulSoup),
    ("http://www.techk.cl/", BeautifulSoup)
])
def test_index_page(arg1, result):
    assert type(scraper.get_index_page(arg1)) == result


def test_export_cvs():
    data_frame = {
        "Title": ["example1", "example2"],
        "Price": ["533", "123"],
        "Stock": [22, 30],
        "Category": ["mystery", "romance"],
        "Cover": ["http://www.techk.cl/wp-content/uploads/2017/01/equipo-techk0001.png",
                  "http://www.techk.cl/wp-content/uploads/2017/01/equipo-techk02-1.png"],
        "UPC": ["adasd1231", "asdalksdblka"],
        "Product Type": ["book", "documentation"],
        "Price (excl. tax)": ["533.2", "123.3"],
        "Price (incl. tax)": ["533.3", "123.4"],
        "Tax": [0, 0],
        "Availability": [22, 30],
        "Number of reviews": [50, 20]
    }
    assert scraper.export_cvs(data_frame)


@pytest.mark.parametrize("data,result",  [
    ("http://books.toscrape.com/catalogue/frankenstein_20/index.html",
     {'Price': '38.00', 'Price (incl. tax)': '38.00', 'Tax': '0.00', 'Title': 'Frankenstein', 'UPC': 'a492f49a3e2b6a71',
      'Price (excl. tax)': '38.00', 'Availability': '1', 'Stock': '1', 'Category': 'Default', 'Product Type': 'Books',
      'Cover': 'http://books.toscrape.com/media/cache/f7/22/f722c24607ddc8013476ca8e84639ba7.jpg',
      'Number of reviews': '0'} ),
    ("http://books.toscrape.com/catalogue/forever-rockers-the-rocker-12_19/index.html",
     {'Category': 'Music', 'Cover': 'http://books.toscrape.com/media/cache/a2/fc/a2fc91793502f5c10b5826ad606de435.jpg',
      'Tax': '0.00', 'Title': 'Forever Rockers (The Rocker #12)', 'Availability': '1', 'Price (incl. tax)': '28.80',
      'Product Type': 'Books', 'Stock': '1', 'Price (excl. tax)': '28.80', 'UPC': 'e564c3f1a93ccf2e', 'Price': '28.80',
      'Number of reviews': '0'}),
])
def test_get_book_data(data, result):
    data = scraper.get_book_data(scraper.get_index_page(data))
    assert data.get('Title') == result.get('Title')
    assert data.get('Price') == result.get('Price')
    assert data.get('Stock') == result.get('Stock')
    assert data.get('Category') == result.get('Category')
    assert data.get('Cover') == result.get('Cover')
    assert data.get('UPC') == result.get('UPC')
    assert data.get('Product Type') == result.get('Product Type')
    assert data.get('Price (excl. tax)') == result.get('Price (excl. tax)')
    assert data.get('Price (incl. tax)') == result.get('Price (incl. tax)')
    assert data.get('Tax') == result.get('Tax')
    assert data.get('Availability') == result.get('Availability')
    assert data.get('Number of reviews') == result.get('Number of reviews')
