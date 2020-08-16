import requests
import re
from bs4 import BeautifulSoup
import traceback

from cfg import config
from logger import logger


def get_top_movies():
    """
    This function scrapes top movies from IMDB top movies page
    :return: list of movie dicts
    """

    # This list will contain the final output i.e. list of movie dicts
    top_movies_list = []

    headers = {
        'User-Agent': config['user_agent'],
    }

    # Get the IMDB top movies page HTML
    try:
        logger.debug("Making HTTP GET request: " + config['top_movies_url'])
        r = requests.get(config['top_movies_url'], headers=headers)
        res = r.text
        logger.debug("Got HTML source, content length = " + str(len(res)))
    except:
        logger.exception("Failed to get HTML source from " + config['top_movies_url'])
        traceback.print_exc()

        # Returns empty array as there was an error in getting HTML
        return top_movies_list

    logger.debug("Extracting top movies info from the HTML")

    # Use the HTML to create a soup object
    soup = BeautifulSoup(res, 'html.parser')

    # Extract the tbody with class='lister-list'
    tbody = soup.find('tbody', class_="lister-list")

    # Extract table rows
    trs = tbody.find_all('tr')

    # Loop over table rows to extract each movie info
    for row in trs:
        # This is the second column in the row
        td1 = row.find('td', class_="titleColumn")

        # The tag that contains the name of the movie
        a_tag = td1.find('a')

        # Extract movie name
        movie_name = a_tag.get_text()

        # Extract the IMDB link of this movie
        link = a_tag['href']

        # Extract the year
        year = td1.find('span', class_="secondaryInfo").get_text()

        # Year contains ( and ) symbols for ex. (2012)
        try:
            nums = re.findall(r'\d+', year)
            if len(nums) > 0:
                year = int(nums[0])
        except:
            # Ignore this error
            pass

        # Extract IMDB rating from the third column
        td2 = row.find('td', class_="imdbRating")
        rating = td2.find('strong').get_text()

        # Converting rating string into float
        try:
            rating = float(rating)
        except:
            # Rating is not a valid float number
            rating = 0.0

        # Put all the extract information into a dict
        movie = {
            'name': movie_name,
            'year': year,
            'rating': rating,
            'link': link,
        }

        # Append the dict to the list that will be returned
        top_movies_list.append(movie)

    # Once all table rows have been processed, return the list
    return top_movies_list


if __name__ == "__main__":
    logger.debug('Starting process')

    top_movies_list = get_top_movies()

    logger.debug("Extracted " + str(len(top_movies_list)) + " top movies info from the HTML")

    logger.debug('Printing movies list')

    i = 0
    for movie in top_movies_list:
        i += 1
        print(str(i) + '. ' + movie['name'] + ' (' + str(movie['year'])
              + ') - Rating ' + str(movie['rating']) + '')

    logger.debug('Process complete')
