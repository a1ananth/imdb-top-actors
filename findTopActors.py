from cfg import config
from logger import logger
from getActorsInMovie import get_actors_in_movie
from getTopMovies import get_top_movies

if __name__ == "__main__":
    logger.debug('Starting process')

    # Get the top movies list
    top_movies_list = get_top_movies()

    # We will store actor names and their number of movies in this dict
    actor_movie_counts = {}

    logger.debug("Extracted " + str(len(top_movies_list)) + " top movies info")

    # For testing purposes use only top 15 movies
    # Remove this line below to run the algorithm on all 250 movies
    top_movies_list = top_movies_list[:15]

    for movie in top_movies_list:
        movie_name = movie['name']
        movie_link = movie['link']

        # domain name is missing from the movie link, so append manually
        full_movie_link = config['host_name'] + movie_link

        actor_names = get_actors_in_movie(full_movie_link)

        logger.debug("Extracted " + str(len(actor_names)) + " actor names in movie " + movie_name)

        for actor_name in actor_names:
            # If actor name is already in dict, then increment the count
            if actor_name in actor_movie_counts:
                actor_movie_counts[actor_name] += 1
            # If actor name is not in dict, this is the first time we're seeing this actor name
            else:
                actor_movie_counts[actor_name] = 1

    # Sort the dictionary by movie count
    actor_movie_counts_sorted = sorted(actor_movie_counts, key=actor_movie_counts.get, reverse=True)

    logger.info('Here are the top 20 actors')

    # Print top 10 elements in the sorted dictionary
    i = 0
    for actor_name in actor_movie_counts_sorted:
        count = actor_movie_counts[actor_name]
        logger.info('#' + str(i) + ' actor is ' + actor_name + ' with ' + str(count) + ' movies')

        i += 1

        if i >= 20:
            break

    logger.debug('Process complete')
