import requests
from bs4 import BeautifulSoup
import traceback

from cfg import config
from logger import logger


def get_actors_in_movie(url):
    """
    This function scrapes the names of actors listed in a IMDB movie page
    :return: list of actor names
    """

    # This list will contain the final output i.e. list of actor names
    actor_names = []

    headers = {
        'User-Agent': config['user_agent'],
    }

    # Get the IMDB movie page HTML
    try:
        logger.debug("Making HTTP GET request: " + url)
        r = requests.get(url, headers=headers)
        res = r.text
        logger.debug("Got HTML source, content length = " + str(len(res)))
    except:
        logger.exception("Failed to get HTML source from " + url)
        traceback.print_exc()

        # Returns empty array as there was an error in getting HTML
        return actor_names

    # Use the HTML to create a soup object
    soup = BeautifulSoup(res, 'html.parser')

    # Extract the Cast list table
    cast_list_table = soup.find('table', class_="cast_list")

    # Extract the table rows that contain actor names
    trs = cast_list_table.find_all('tr', class_=["odd", "even"])

    # Loop over these table rows to extract each actor name
    for row in trs:
        # Actor name is in the second column in each row
        tds = row.find_all('td')
        actor_td = tds[1]

        # Actor name is inside an <a> tag in the second column
        a_tag = actor_td.find('a')
        actor_name = a_tag.get_text()

        # Actor name contains a trailing space in the source
        actor_name = actor_name.strip()

        # Append the actor name to the list that will be returned
        actor_names.append(actor_name)

    return actor_names


if __name__ == "__main__":
    logger.debug('Starting process')

    """
        In this file, we are writing logic for
        extracting actor names of a single movie
    """

    imdb_url = 'https://www.imdb.com/title/tt1205489/?pf_rd_m=' \
               'A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf' \
               '_rd_r=9PYDEDDNAQ8EYVD4PTYV&pf_rd_s=center-1&pf_rd_t=15506&pf' \
               '_rd_i=top&ref_=chttp_tt_180'

    actor_names = get_actors_in_movie(imdb_url)
    logger.debug('Extracted actor names from the IMDB url')

    logger.debug('Printing actor names')

    print('Actors in the movie are:')

    i = 0
    for actor_name in actor_names:
        i += 1
        print(str(i) + '. ' + actor_name)

    logger.debug('Process complete')
