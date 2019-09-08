from bs4 import BeautifulSoup
import logging
import requests

logger = logging.getLogger('scrapper')

# BASE URL
URL = "http://books.toscrape.com/"


def get_index_page(url: str) -> BeautifulSoup:
    """
        Obtain the parsing of a specific web page

        :param url: website to realize the parsing
        :type url: str
        :return: parser content
        :raise: ConnectionError
    """
    logger.info("Obtain html content from {} to scraper them".format(url))
    try:
        content = requests.get(url)
    except Exception as e:
        logger.error("Request Problem %s" % str(e))
        raise ConnectionError(str(e))
    logger.info("")
    return BeautifulSoup(content.text, 'html.parser')


def get_total_pages(data: BeautifulSoup) -> int:
    """
        Obtain the number total of pages to realise scraper the of all book for page

        :param data: parser of the website
        :type data: BeautifulSoup
        :return: total of pages
    """
    page_content = data.select_one(".pager .current").get_text(strip=True)
    total_pages = int(page_content[-2:])
    return total_pages


def get_book_data(scraper: BeautifulSoup) -> dict:
    """
        Obtain all information of the books

        :param scraper: parser of the website
        :type scraper: BeautifulSoup
        :return: dictionary with all book data
    """
    book_data = {"Title": "", "Price": "", "Stock": "", "Category": "", "Cover": "", "UPC": "", "Product Type": "",
                 "Price (excl. tax)": "", "Price (incl. tax)": "", "Tax": "", "Availability": "",
                 "Number of reviews": ""}
    logger.info("Obtain the title")
    book_data['Title'] = scraper.select_one('.product_main h1').get_text(strip=True).\
        encode('ascii', 'ignore').decode('ascii')
    logger.info("Obtain the price")
    book_data['Price'] = scraper.find('p', class_='price_color').text.encode('ascii', 'ignore').decode('ascii')
    logger.info("Obtain the stock")
    pre_stock = scraper.select_one('.availability').get_text(strip=True)
    book_data['Stock'] = "".join(filter(str.isdigit, pre_stock))
    logger.info("Obtain the category")
    book_data['Category'] = scraper.find('ul', class_="breadcrumb").findAll('li')[2].select_one('a').get_text(strip=True)
    logger.info("Obtain the cover")
    pre_cover = scraper.select_one(".thumbnail .carousel-inner .item img")['src'].strip()
    book_data['Cover'] = URL + "/".join(pre_cover.split('/')[2:])
    logger.info("Obtain additional information (upc, tax, product type, etc)")
    product_information = []
    for row in scraper.select('.product_page table td'):
        product_information.append(row.text.encode('ascii', 'ignore').decode('ascii'))
    book_data['UPC'] = product_information[0]
    book_data['Product Type'] = product_information[1]
    book_data['Price (excl. tax)'] = product_information[2]
    book_data['Price (incl. tax)'] = product_information[3]
    book_data['Tax'] = product_information[4]
    book_data['Availability'] = book_data.get('Stock')
    book_data['Number of reviews'] = product_information[6]
    return book_data


def init_scraper() -> bool:
    """
        Start the process of obtaining the information on the website
        and then obtain the data in a cvs file
    """
    logger.info("Start scraping")
    scraper = get_index_page(URL)
    logger.info("Obtain total number of pages")
    last_number_page = get_total_pages(scraper)
    data_frame = {"Title": [], "Price": [], "Stock": [], "Category": [], "Cover": [], "UPC": [], "Product Type": [],
                  "Price (excl. tax)": [], "Price (incl. tax)": [], "Tax": [], "Availability": [],
                  "Number of reviews": []}
    logger.info("Scraper data page by page")
    for number in range(1, last_number_page + 1):
        logger.info("Get the information the page number {}".format(number))
        current_page = get_index_page(URL + 'catalogue/page-{}.html'.format(number))
        for product in current_page.select('.product_pod'):
            book_page = get_index_page(URL + "/catalogue/" + product.select_one('a')['href'].strip())
            logger.info("Start the book scraper")
            book_data = get_book_data(book_page)
            data_frame["Title"].append(book_data.get('Title'))
            data_frame["Price"].append(book_data.get('Price'))
            data_frame["Stock"].append(book_data.get('Stock'))
            data_frame["Category"].append(book_data.get('Category'))
            data_frame["Cover"].append(book_data.get('Cover'))
            data_frame["UPC"].append(book_data.get('UPC'))
            data_frame["Product Type"].append(book_data.get('Product Type'))
            data_frame["Price (excl. tax)"].append(book_data.get('Price (excl. tax)'))
            data_frame["Price (incl. tax)"].append(book_data.get('Price (incl. tax)'))
            data_frame["Tax"].append(book_data.get('Tax'))
            data_frame["Availability"].append(book_data.get('Availability'))
            data_frame["Number of reviews"].append(book_data.get('Number of reviews'))
            logger.info("The book {} has been stored".format(book_data.get('Title')))
        logger.info("Finished the scrape of the page {}".format(number))
    print(data_frame)
    return True
