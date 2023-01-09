import discord
import os
import platform
from decouple import config
import nostalrius_requests
import hunted
import asyncio
import victims
from itertools import cycle
from discord.ext import tasks
import lasth_death

def init1(): 

    intents = discord.Intents.default() 
    intents.message_content = True
    client = discord.Client(intents=intents)
    prefix = '!'    #prefix usado para comandos 
    status = cycle(["type '!online' to check online players on nostalrius", "check the hunted list with '!hunted'", "you also can add or remove hunteds ex: '!hunted add player'", "ver.1.0_hellofriend.mov"])
    
    async def find_hunted_post(channel_id):

        hunted_list = hunted.load()
        players = nostalrius_requests.get_online()
        processed_players = set()

        for player in players:

            if player.name in hunted_list:

                name = player.name
                url = player.url
                lvl = player.lvl
                voc = player.voc

                if name not in processed_players:
                    channel = client.get_channel(1058500722678845480)
                    await channel.send(f'```diff\n- Hunted ON: {name} {lvl} {voc}\n```{name} url -> {url}')
                    print(f'LOG: Hunted-Player {name} is online! {lvl} {voc} {url}')
                    processed_players.add(name)
                else:
                    pass

            else:
                pass

    async def find_victim_post(channel_id):

        # Call hook chama a funcao search victim do modulo victms importado... retorna uma string com os achados
        hook = victims.search_victims()
        newcheck = False

        if hook is not None:
            for check in hook:
                if check is not None:
                    player = hook[0]
                    url = hook[1]
                    lvl = hook[2]
                    voc = hook[3]
                    item = hook[4]
                    newcheck = True

        if newcheck:
            channel = client.get_channel(1058500722678845480)
            await channel.send(f'```diff\n- Player: {player} {voc} {lvl} SEM AOL COM:{item}\n```{player} url -> {url}')
            print(f'LOG: Encontrei {player} {voc} {lvl} sem AOL e com : {item}')
        else:
            pass

    async def find_death(channel_id):

        hook = lasth_death.check_last_death()

        players_to_check = []
        first_call = lasth_death.FIRST_HOOK
        check = []

        if hook != first_call:
            
            print('LOG: Um ou mais players morreram')
            set1 = set(hook)
            set2 = set(first_call)
            players_to_check = list(set1-set2)
            print(len(players_to_check))
            lasth_death.FIRST_HOOK.clear()
            lasth_death.FIRST_HOOK = hook.copy()

            for newplayer in players_to_check:
                print(f'{newplayer.name}')

                check = lasth_death.check_death_aol(newplayer)

                if type(check) is list and check[0] is True:

                    channel = client.get_channel(1058500722678845480)
                    await channel.send(f'```diff\n+ Player: {newplayer.name} morreu sem aol pra {newplayer.killer} na data {newplayer.data} bless = {newplayer.bless} \n```')
                    print(f'LOG: Player: {newplayer.name} morreu sem aol pra {newplayer.killer} na data {newplayer.data} bless = {newplayer.bless}')
                else:
                    pass
        else:
            print('LOG: Nenhum Player Morreu')
            pass
    
    @tasks.loop(seconds=10)
    async def change_status():
        await client.change_presence(activity=discord.Game(next(status)))

    @client.event #Retorna um feedback ao iniciar
    async def on_ready():
        print(client.users)
        print("-------------------")
        print(f"Logged in as {client.user.name}")
        print(f"discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")

        client.loop.create_task(check_lists_periodically(1058500722678845480))
        client.loop.create_task(check_victims_periodically(1058500722678845480))
        client.loop.create_task(check_deaths_periodically(1058500722678845480))
        change_status.start()

    async def check_lists_periodically(channel_id):
        await client.wait_until_ready()
        while not client.is_closed():
            await find_hunted_post(channel_id)
            # Espera por um tempo t ate checar a lista novamente
            await asyncio.sleep(20)

    async def check_victims_periodically(channel_id):
        await client.wait_until_ready()
        while not client.is_closed():
            await find_victim_post(channel_id)
            # Espera por um tempo t ate checar a lista novamente
            await asyncio.sleep(30)

    async def check_deaths_periodically(channel_id):
        await client.wait_until_ready()
        while not client.is_closed():
            await find_death(channel_id)
            # Espera por um tempo t ate checar a lista novamente
            await asyncio.sleep(10)


    @client.event # Funcao de ler todas msgs do discord
    async def on_message(message: discord.Message):
        # Ignora mensagens enviadas pelo próprio bot
        if message.author == client.user:
                return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')

        command = ''

        # Verifica se a mensagem começa com o prefixo do comando
        if message.content.startswith(prefix):
        # Remove o prefixo da mensagem
            command = message.content[len(prefix):]

        # Verifica o comando e executa a ação correspondente
        if command == 'online':
            # Obtem a string de ate 2k caracteres de nostal_requests
            resultado = nostalrius_requests.show_online()

            # Pega cada parte do resultado e divide ele para poder postar no discord
            for parte in [resultado[i:i+1900] for i in range(0, len(resultado), 1900)]:
                await message.channel.send(f'```diff\n{parte}\n```')

        # Verifica o comando e executa a ação correspondente
        if command == 'hunted':
            # Carregando a lista de hunteds do modulo hunted.py
            hunted_list = hunted.load()

            feedback = hunted.show(hunted_list)

            await message.channel.send(f'```diff\n{feedback}\n```')

        if command[0:10] == 'hunted add':

            size = len(command)
            target = command[11:size]

            hunted.add(target)

            await message.channel.send(f'```diff\n{username} Voce adicionou {target} a lista de hunteds\n```')

        if command[0:13] == 'hunted remove':

            size = len(command)
            target = command[14:size]
            
            hunted.remove(target)

            await message.channel.send(f'```diff\n{username} Voce removeu {target} da hunted list\n```')

                                                  
    TOKEN = config("TOKEN")
    client.run(TOKEN)