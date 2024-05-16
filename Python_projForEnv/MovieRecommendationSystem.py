import requests_with_caching
import json

# Define a class MovieRecommendationSystem
class MovieRecommendationSystem:
    
    # Define a method get_movies_from_tastedive
    # This method should take one input parameter, a string that is the name of a movie or music artist.
    # The function should return the 5 most similar movies or music artists in a list.
    
    def get_movies_from_tastedive(self, title):
        endpoint = 'https://tastedive.com/api/similar'
        param = {'q': title, 'limit': 5, 'type': 'movies'}
        this_page_cache = requests_with_caching.get(endpoint, params=param)
        return json.loads(this_page_cache.text)

    # Define a method extract_movie_titles
    # This method should take one input parameter, a dictionary that contains movie information.
    # The function should extract the movie titles from the dictionary and return them in a list.
    def extract_movie_titles(self, dic):
        movie_titles = []
        for result in dic.get('Similar', {}).get('Results', []):
            movie_titles.append(result['Name'])
        return movie_titles

# Define a method get_related_titles
# This method should take one input parameter, a list of movie titles.
# The function should return a list of related movie titles.    

    def get_related_titles(self, titles_list):
        related_titles = []
        for title in titles_list:
            new_titles = self.extract_movie_titles(self.get_movies_from_tastedive(title))
            for new_title in new_titles:
                if new_title not in related_titles:
                    related_titles.append(new_title)
        print(related_titles)
        return related_titles
# Define a method get_movie_data
# This method should take one input parameter, a string that is the name of a movie.
# The function should return the movie data in a dictionary.

    def get_movie_data(self, title):
        endpoint = 'http://www.omdbapi.com/'
        param = {'t': title, 'r': 'json'}
        this_page_cache = requests_with_caching.get(endpoint, params=param)
        return json.loads(this_page_cache.text)
# Define a method get_movie_rating
# This method should take one input parameter, a dictionary that contains movie information.
# The function should return the Rotten Tomatoes rating of the movie as an integer.
# If there is no Rotten Tomatoes rating, return 0.
    def get_movie_rating(self, data):
        rating = 0
        for rating_source in data.get('Ratings', []):
            if rating_source['Source'] == 'Rotten Tomatoes':
                rating = int(rating_source['Value'][:-1])
        return rating 
# Define a method get_sorted_recommendations
# This method should take one input parameter, a list of movie titles.
# The function should return a list of related movie titles sorted by their Rotten Tomatoes rating, highest to lowest.
# If there is a tie in the rating, the movie titles should be sorted in ascending order.

    def get_sorted_recommendations(self, movie_list):
        related_titles = self.get_related_titles(movie_list)
        ratings_dict = {}
        for title in related_titles:
            rating = self.get_movie_rating(self.get_movie_data(title))
            ratings_dict[title] = rating
        print(ratings_dict)
        return [title[0] for title in sorted(ratings_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]

# Example usage:
if __name__ == "__main__":
    recommendation_system = MovieRecommendationSystem()
    movie_list = ["Inception", "Interstellar", "The Matrix"]
    sorted_recommendations = recommendation_system.get_sorted_recommendations(movie_list)
    print(sorted_recommendations)
