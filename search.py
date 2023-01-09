import requests
from bs4 import BeautifulSoup

def search_player(player):
  # Send a GET request to the URL
  response = requests.get('https://nostalrius.com.br/character')

  # Create a BeautifulSoup object from the HTML
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the form element
  input_field = soup.find('input', attrs={'name' : 'character', 'autocomplete' : 'off'})

  print()


search_player('Mathlokz')