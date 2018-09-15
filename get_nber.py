"""
Scrape the weekly papers archives of the NBER

Todo:
-----
* Include dates, citation author, pdf_url
* Account for missing pages (e.g. w7443)
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(format='%(asctime)s %(message)s',
                    filename='get_nber.log',
                    level=logging.DEBUG,
                    filemode='w')


def get_contents(index):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(f'http://www.nber.org/papers/w{index}')

    # Get html of webage and title
    html_src = driver.page_source
    title = driver.title

    # Close webdriver when finished
    driver.close()

    return html_src, title


def get_abstract(html):
    # Find only paragraphs with specific attributes
    soup = BeautifulSoup(html)
    p_attrib = {"style": "margin-left: 40px; margin-right: 40px; text-align: justify"}
    results = soup.findAll('p', p_attrib)
    return results[0].text


def get_meta(html):
    soup = BeautifulSoup(html)
    all_meta = soup.find_all('meta')
    return all_meta


if __name__ == '__main__':
    # beg = 6453
    # end = 25025

    beg = 9999
    end = 10000

    save_path = "/Users/s6215054/Desktop/play/get_nber/nber_data.json"

    with open(save_path, 'w') as f_save:

        for i in range(beg, end):

            data = {}

            data["index"] = i

            try:
                html_src, title = get_contents(i)
                abstract = get_abstract(html_src)
                data["abstract"] = abstract
                data["title"] = title
                logging.info(f"Got data for {i}")

                meta = get_meta(html_src)

                # TODO: SAVE THIS IN data dict !!!

                print(meta)

                author_list = [name.get("content") for name in meta
                               if name.get("name") == "citation_author"]
                date = [date.get("content") for date in meta
                        if date.get("name") == "citation_date"]

                pdf_url = [url.get("content") for url in meta
                           if url.get("name") == "citation_pdf_url"]

                print(author_list, date, pdf_url, sep='\n')

            except Exception as e:
                logging.warning(f'Failed to get data for {i}')
                print(e, f"An error occurred---last index processed {i-1}")
                break

            # Save json
            # json.dump(data, f_save)
            # f_save.write('\n')
