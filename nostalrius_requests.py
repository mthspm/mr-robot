import requests
from bs4 import BeautifulSoup
from measure_time import measure_time

PLAYERS = []

class Player:
    def __init__(self, name,url,lvl,voc) -> None:

        self.name = name
        self.url = url
        self.lvl = lvl
        self.voc = voc

        pass

# Limpa as informacoes guardads nas listas da classe Player ---> Necessario a cada get_online() para nao concatenar informacoes repetidas.
def clean_cache():

    PLAYERS.clear()

# Main funcao que faz requests e filtra os dados da pagina buscada
@measure_time
def get_online():

    # Criando request
    online = requests.get('https://nostalrius.com.br/online/list')

    # Transformando o pacote de informacoes do request em html.parser
    BSonline = BeautifulSoup(online.content, 'html.parser')

    # Comeco da filtracao, busncando a table de class 'table'
    site = BSonline.find('table', attrs={'class' : 'table'})

    # Itera o proximo tbofy
    site2 = site.find('tbody')

    # Call de todos tr. Compartimento onde estao as infos dos jogadores online
    players = site2.findAll('tr')

    # Itera sobre as tags 'tr' e extrai os dados
    for tr in players:
        # Encontra a primeira tag 'td'
        td1 = tr.find("td")
        # Obtém o texto da tag 'td'
        name = td1.text
        # Obtém o atributo 'href' da tag 'a' dentro da tag 'td'
        link = td1.find("a")["href"]
    
        # Encontra a segunda tag 'td'
        td2 = tr.findAll("td")[1]
        # Obtém o texto da tag 'td'
        lvl = td2.text

        # Encontra a terceira tag 'td'
        td3 = tr.findAll("td")[2]
        # Obtém o texto da tag 'td'
        voc = td3.text

        # Cria um objeto da classe Player, chamado player que ira guardar o nome,link,lvl,voc
        player = Player(name,link,lvl,voc) 

        #remove os \n do nome
        player.name = player.name.replace('\n', '')

        PLAYERS.append(player)

    # Retorna uma lista que contem todos objetos da classe Player, ou seja, os players online
    return PLAYERS

@measure_time
def show_online():

    clean_cache()

    # Faz a chamada dos players online a partir da funcao criada acima
    call = get_online()
    players_online = len(call)

    string = (f'Players Online: {players_online}\n')

    # Para cada jogador online adiciona suas informacoes na string que sera retornada
    for player in call:
        try:
            if len(string) < 2000:

                newstring = (f'NAME: {player.name:<20} LVL: {player.lvl:<10} VOC: {player.voc:<10} URL: {player.url}\n')

                if len(string+newstring) <= 2000:

                    string += newstring
        except Exception as e:
            print(e)
            pass
            
    return string