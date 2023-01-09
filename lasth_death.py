import requests
from bs4 import BeautifulSoup
from measure_time import measure_time

# Script responsavel por buscar lasth deaths sem aol == buscando bps vazias

# Classe que vai orientar o manuseio das informacoes de cada player
class Player_dead:
    def __init__(self,name,data,killer,bless,url) -> None:
        self.name = name
        self.data = data
        self.killer = killer
        self.bless = bless
        self.url = url
        pass

    def __hash__(self):
        return hash(('name', self.name,
                     'data', self.data))

    def __eq__(self, other):
        return self.name==other.name\
           and self.data==other.data

# Funcao que busca a pagina `last deaths` e retorna uma lista com objetos que sao os players mortos, onde cada objeto contem um self. name,data,killer,bless e url.
@measure_time
def check_last_death():
    hook = requests.get('https://nostalrius.com.br/deaths')
    bshook = BeautifulSoup(hook.content, 'html.parser')
    last_deaths = bshook.find('table', attrs={'class':'table'})
    alltr = last_deaths.find_all('tr')

    PLAYERS_DEAD = []

    for tr in alltr:
        tds = tr.find_all('td')
        nome = str(tds[0].text)
        data = str(tds[1].text)
        killer = str(tds[2].text)
        bless = str(tds[3].text)

        nome_td = tds[0]
        url = nome_td.find('a')['href']
        nome = nome.split(":")
        nome = nome[1].strip()
        killer = killer.strip()
        bless = bless.strip()

        player_dead = Player_dead(nome,data,killer,bless,url)

        PLAYERS_DEAD.append(player_dead)

    return PLAYERS_DEAD


# Funcao que checa se um player morreu e está sem sua bp, ou seja, morreu sem aol e retorna False caso o jogador esteja com bp e caso esteja sem bp retorna uma lista com seus itens
@measure_time
def check_death_aol(player):
    hook = requests.get(player.url)
    bshook = BeautifulSoup(hook.content, 'html.parser')
    inventory = bshook.find('table', attrs={'class':'table'})
    alltr = inventory.find_all('tr')
    itens = []
    itens_with_class = []  # Nova lista para armazenar itens com a classe 'item-opacity'
    for tr in alltr:
        for td in tr.select('td.inventory-item'):
            img = td.select_one('img')
            if img:
                itens.append(img['src'])
                # Verifica se o atributo 'class' existe e se a classe 'item-opacity' está presente
                if 'class' in img.attrs and 'item-opacity' in img['class']:
                    itens_with_class.append(img['src'])  # Adiciona o item à lista itens_with_class

    without_bp = False
    try:
        for item in itens_with_class:

            if item == 'https://nostalrius.com.br/assets/images/inventory/3.gif':
                without_bp = True

        if without_bp:
            return [without_bp,itens]
        else:
            return False

    except Exception as e:
        return False

FIRST_HOOK = check_last_death()