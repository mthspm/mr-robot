#Script que deve buscar todos players online, checar sua pagina html e ver se o mesmo possui aol e itens vip.

import nostalrius_requests
import requests
from bs4 import BeautifulSoup
from measure_time import measure_time

dict_itens = {
    'AOL':'https://nostalrius.com.br/assets/images/inventory_items/3057.gif',
    'NOST SHIELD':'https://nostalrius.com.br/assets/images/inventory_items/3442.gif',
    'NOST RING':'https://nostalrius.com.br/assets/images/inventory_items/9191.gif',
    'NOST BOOTS':'https://nostalrius.com.br/assets/images/inventory_items/6160.gif',
    'BOOTS OF HASTE':'https://nostalrius.com.br/assets/images/inventory_items/3079.gif',
    'ROYAL HELMET':'https://nostalrius.com.br/assets/images/inventory_items/3392.gif',
    'NOST ARMOR':'https://nostalrius.com.br/assets/images/inventory_items/9185.gif',
    'NOST LEGS':'https://nostalrius.com.br/assets/images/inventory_items/9186.gif',
    'ANCIENT HELMET':'https://nostalrius.com.br/assets/images/inventory_items/3229.gif',
    'ANCIENT HELMET ENCANTADO':'https://nostalrius.com.br/assets/images/inventory_items/3230.gif',
    'BOTA DE GELO':'https://nostalrius.com.br/assets/images/inventory_items/5498.gif',

        }

@measure_time
def search_victims():

    cache = nostalrius_requests.get_online()

    # Itera sobre todos objetos dos players online para
    for player in cache:

        # hook guarda o valor do request da pagina url do primeiro jogador da iteracao 'for player in cache[0]==playersonline'
        hook = requests.get(player.url)

        # bshook eh um produto da funcao bs, que passa como argumento o conteudo do request e o novo formato do pacote de informacoes
        bshook = BeautifulSoup(hook.content, 'html.parser')

        # primeiro filtro de informacoes
        container_inv = bshook.find('table',attrs={'class' : 'table'})

        # lista que contera todas urls dos itens encontrados no player
        imgs = []
        lvl = player.lvl
        url = player.url
        voc = player.voc
        target_itens = []

        # iterando cada url no ultimo pacote de informacoes 'container_inv'
        for URL in container_inv.find_all('img'):
            imgs.append(str(URL['src']))

        # para cada busca na lista de urls

        try:
            for search in dict_itens.values():

                # se a busca estiver na lista de itens do player e a primeira imagem nao for AOL
                if search in imgs and imgs[0] != dict_itens['AOL']:

                    # obtendo a key do item == nome do item.. item = list[index] onde search = url do item
                    item = list(dict_itens.keys())[list(dict_itens.values()).index(search)]

                    #checa para nao retornar uma lista vazia
                    if len(item) > 0:

                        target_itens.append(item)
                    
            #checa se algum item foi preenchido no target, se sim retorna o pacote para quem chama
            if len(target_itens) > 0:
                return [player.name,url,lvl,voc,target_itens]       
            

        except Exception as e:
            print(e)
            return ('LOG: Nao foram encontrados players sem aol e itens valiosos')