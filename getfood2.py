#This program generates random recipes by webscraping from allrecipes.com
#3/10/22

from bs4 import BeautifulSoup
import requests
import random
import sys
import os
import textwrap

#ask user if they want anything specific
def pick_interest():
    print('What sounds good?\nTry "pasta" or just press enter for a random recipe.')
    search_term = input('> ')
    return search_term

#generate 2 search terms for recipe search
def generate_search(food):
    keyword_list = ['mexican', 'italian', 'chinese', 'japanese', 'american', 'spanish', 'greek']
    ingredients_list = ['chicken', 'pasta', 'potato', 'cheese', 'fish', 'green+chile', 'bacon', 'asparagus', 'mushrooms', 'spinach', 'cabbage', 'red+pepper+flakes', 'turkey', 'bread', 'garlic', 'bell+pepper', 'salsa', 'teriyaki']
    search_terms = []
    keyword = random.choice(keyword_list)
    ingredient = random.choice(ingredients_list)

    #append food if user inputs, else append keyword
    if food:
        search_terms.append(food)
    else:
        search_terms.append(keyword)

    #include 1 random ingredient
    search_terms.append(ingredient)

    return search_terms

#check if user wants to quit
def check_quit(inp):
    if inp == 'quit':
        sys.exit(0)

#retrieve recipes from allrecipes.com
#runs until user says quit
while(True):
    os.system('clear')
    terms = generate_search(pick_interest())
    print(f'\nFinding recipes for {terms[0]} and {terms[1]}...')
    
    html_text = requests.get('https://www.allrecipes.com/search/results/?search=' + terms[0] + '&IngIncl=' + terms[1]).text
    soup = BeautifulSoup(html_text, 'lxml')
    foods = soup.find_all('div', class_='component card card__recipe card__facetedSearchResult')

    #how many search results to return
    desired_results = 3

    #count of how many recipes are to be printed (initialized to 0)
    recipe_count = 0

    #count of how many recipes get deleted/not printed (initialized to 0)
    deleted = 0

    #minimum number of ratings a result should have
    ratings_filter = 500

    #only runs if there is at least 1 in the list
    if (len(foods) >= 1):
        for stuff in foods:  
            recipe = stuff.find('a', class_='card__titleLink manual-link-behavior elementFont__titleLink margin-8-bottom')['title']
            
            #some recipe attributes can be none so if else prevents errors
            rating = None
            if(stuff.find('span', class_='review-star-text visually-hidden')):
                rating = stuff.find('span', class_='review-star-text visually-hidden').text.replace('Rating: ', '')
            
            rating_count = None
            if(stuff.find('span', class_='ratings-count elementFont__details')):
                rating_count = stuff.find('span', class_='ratings-count elementFont__details').text.strip() 
            
            if rating_count == None:
                deleted += 1
                continue

            if int(rating_count) < ratings_filter:
                deleted += 1
                continue

            description = None
            if(stuff.find('div', class_='card__summary elementFont__details--paragraphWithin margin-8-tb')):
                description = stuff.find('div', class_='card__summary elementFont__details--paragraphWithin margin-8-tb').text.strip()

            link = stuff.find('a', class_='card__titleLink manual-link-behavior elementFont__titleLink margin-8-bottom')['href']

            wrapper = textwrap.TextWrapper(width=75, initial_indent='\t', subsequent_indent='\t\t')
            print(f'\nRecipe:\t\t{recipe}\nRating:\t\t{rating}\nRating Count:\t{rating_count}\nDescription:{wrapper.fill(description)}\n\nLink:\t{wrapper.fill(link)}\n\n-----------------------------------------------------------------------------------------')

            recipe_count +=1
            if recipe_count == desired_results:
                break
    
    if (recipe_count == 0 and deleted >= 1):
        print(f'No results. (filtered {deleted} for {ratings_filter} ratings)')
    
    elif (recipe_count == 0):
        print('No results.')

    print("\nNeed another? Press enter or type 'quit' to exit program.")
    check_quit(input('> '))