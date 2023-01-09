# Carrega o arquivo dos hunteds e retorna uma lista com esses nomes
def load():

    hunted = []

    # Abrindo o arquivo em modo de leitura
    with open('hunted_list.txt', 'r') as f:
        # Lendo o conteúdo do arquivo como uma lista de linhas
        lines = f.readlines()

    # Adicionado cada linha para uma lista 'hunted'
    for line in lines:
        hunted.append(line)

    # Limpando a lista com o metodo strip para cada iteracao da lista hunted
    hunted = [line.strip() for line in hunted]
    
    f.close()

    return hunted

def show(list):

    const = (f'*Hunted List*: {len(list)}\n')
    const = 'Hunted List:\n'
    # Carregando a lista de hunteds do modulo hunted.py
    for name in list:
        const += (f'{name}\n')

    if len(list) < 1:
        return 'Nao ha hunteds'

    return const

# Checa se um hunted pertence a lista e se sim retorna True, se nao ... False
def check(hunted,list):

    if hunted in list:
        return True

    return False

def add(target):
  try:
    with open('hunted_list.txt', 'a') as f:
        f.write(target + "\n")

        f.close()

  except Exception as e:
    print(e)

def remove(target):
    lines = []
    try:
      with open('hunted_list.txt', 'r') as f:
        for l in f:
            if l.strip() != target:
                lines.append(l)
        f.close()
        
    except Exception as e:
      print(e)

    try:
      with open('hunted_list.txt', 'w') as f:
        for l in lines:
            f.write(l)
        f.close()
    except Exception as e:
      print(e)