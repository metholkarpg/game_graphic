import pygame
import os
from pygame import mouse
from pygame.locals import *
from sys import exit
from tinydb import TinyDB, Query

import shop_interface
import char
import items

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Inicialização do PyGame
pygame.init()
pygame.font.init()
pygame.display.set_caption('Metholka RPG')

# player data
ch = None
name_to_load = None
db = None

# Definições iniciais do PyGame (Fonte, Tela, Cores)
font_name = pygame.font.get_default_font()
start_menu_font = pygame.font.Font('data/fonts/coders_crux.ttf', 40)
game_font = pygame.font.SysFont(font_name, 25)
screen_width = 512
screen_height = 480
black = (0, 0, 0)
red = (255, 0, 0)
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
clock = pygame.time.Clock()
FPS = 60

# Definição do mapa do jogo
# O vetor LEVEL é criado baseado na imagem criada para o mapa
# 'W' representa "paredes" onde o player nao consegue avançar
# 'O' representa onde o player pode andar
walls = []
level = [
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "WWWWWWWWWWWWWWWW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WWWWWWWOOWWWWWWW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOWWOOWWOOOOW",
    "WWWWWWWWWWWWWWWW"
]

# Definições para utilização do cursor do mouse no pygame
DEFAULT_CURSOR = mouse.get_cursor()

_HAND_CURSOR = (
    "     XX         ",
    "    X..X        ",
    "    X..X        ",
    "    X..X        ",
    "    X..XXXXX    ",
    "    X..X..X.XX  ",
    " XX X..X..X.X.X ",
    "X..XX.........X ",
    "X...X.........X ",
    " X.....X.X.X..X ",
    "  X....X.X.X..X ",
    "  X....X.X.X.X  ",
    "   X...X.X.X.X  ",
    "    X.......X   ",
    "     X....X.X   ",
    "     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

# Dicionarios referentes aos caminhos das imagens utilizadas no mapa
dict_map_images = {
    'chao': 'resources/camadaChao.png',
    'chao2': 'resources/camadaChao2.png',
    'casa': 'resources/camadaCasa.png',
    'placas': 'resources/camadaPlacas.png'
}

# Dicionarios referentes aos caminhos das imagens utilizadas no player
dict_player_images = {
    'front': 'resources/playerFront.png',
    'back': 'resources/playerBack.png',
    'left': 'resources/playerLeft.png',
    'right': 'resources/playerRight.png'
}

# Inicializa variaveis que armazenam as imagens convertidas
background_start_menu = pygame.image.load('resources/start_menu.png').convert_alpha()
camada_chao = pygame.image.load(dict_map_images['chao']).convert()
camada_chao2 = pygame.image.load(dict_map_images['chao2']).convert_alpha()
camada_casa = pygame.image.load(dict_map_images['casa']).convert_alpha()
camada_placa = pygame.image.load(dict_map_images['placas']).convert_alpha()


class Player(object):
    # Inicialização do player.
    # Criamos um "retangulo" para representar o objeto fisico do player
    def __init__(self):
        self.rect = pygame.Rect(256, 256, 32, 32)
        self.sprite = pygame.image.load(dict_player_images['back']).convert_alpha()

    # Função que trata o movimento do player ao andar
    def move(self, dx, dy):
        if dx != 0:
            self.rect.x += dx
        if dy != 0:
            self.rect.y += dy

        # Checa as colisões que o player faz com a parede
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    # Troca a sprite dependendo da direção que o player está andando
    def change_sprite(self, side):
        if side == 1:
            self.sprite = pygame.image.load(dict_player_images['back']).convert_alpha()
        elif side == 2:
            self.sprite = pygame.image.load(dict_player_images['front']).convert_alpha()
        elif side == 3:
            self.sprite = pygame.image.load(dict_player_images['left']).convert_alpha()
        elif side == 4:
            self.sprite = pygame.image.load(dict_player_images['right']).convert_alpha()


class Wall(object):
    # Inicializa os objetos fisico das paredes
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


# CRIANDO A LISTA DE ITEMS DA LOJA WEAPON
def create_shop_list_weapon():

    lista = ["Dagger 30", "Short Sword 80", "Long Sword 90", "Divine Sword 150", "Bow 45", "War Hammer 95", "Knife 25"]

    shop_list = list()

    for item in lista:
        novo = item.split()

        # FAZENDO O TRATAMENTO QUANDO A WEAPON CONTEM DUAS PALAVRAS
        if len(novo) == 3:
            temp = " ".join(novo[0:2])
            novo[0] = temp
            novo[1] = novo[2]

        shop_list.append(items.Weapon(novo[0], novo[1]))

    return shop_list


# CRIANDO A LISTA DE ITEMS DA LOJA ARMOR
def create_shop_list_armor():

    lista = ["Tunic 30", "Chain Armor 80", "Silver Armor 90", "Diamond Armor 150", "Boots 45", "Iron Shield 95",
             "Pants 25"]

    shop_list = list()

    for item in lista:
        novo = item.split()

        # FAZENDO O TRATAMENTO QUANDO A ARMOR CONTEM DUAS PALAVRAS
        if len(novo) == 3:
            temp = " ".join(novo[0:2])
            novo[0] = temp
            novo[1] = novo[2]

        shop_list.append(items.Armor(novo[0], novo[1]))

    return shop_list


# CRIANDO A LISTA DE ITEMS DA LOJA POTION
def create_shop_list_potion():

    lista = ["Minus Health 15", "Medium Health 30", "Big Health 70", "Full Restore 150"]

    shop_list = list()

    for item in lista:
        novo = item.split()

        # FAZENDO O TRATAMENTO QUANDO A POTION CONTEM DUAS PALAVRAS
        if len(novo) == 3:
            temp = " ".join(novo[0:2])
            novo[0] = temp
            novo[1] = novo[2]

        shop_list.append(items.Potion(novo[0], novo[1]))

    return shop_list


# Realiza a verificação da posição do player em relação ao cenário
# Utiliza o conceito dos retangulos criados para verificar se ele está em tal posição da tela
# Dependendo da posição, ele identifica que está em frente a uma loja e habilita a opção de acessá-la
def check_pos(p_centerx, p_centery):
    if 123 >= p_centerx >= 56 and p_centery <= 224:
        show_text('PRESS (E)')
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_e]:
            # ultimo parametro é o callback que a janela terá que chamar caso queira salvar os dados do jogador
            st = shop_interface.StoreWindow(ch, create_shop_list_weapon(), "Weapon Store", save_char)
            st.start_window()

    if 296 >= p_centerx >= 230 and p_centery <= 224:
        show_text('PRESS (E)')
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_e]:
            # ultimo parametro é o callback que a janela terá que chamar caso queira salvar os dados do jogador
            st = shop_interface.StoreWindow(ch, create_shop_list_armor(), "Armor Store", save_char)
            st.start_window()
    if 445 >= p_centerx >= 380 and p_centery <= 224:
        show_text('PRESS (E)')
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_e]:
            # ultimo parametro é o callback que a janela terá que chamar caso queira salvar os dados do jogador
            st = shop_interface.StoreWindow(ch, create_shop_list_potion(), "Potion Store", save_char)
            st.start_window()


# Inicializa o mapa na tela
def load_initial_map():
    screen.blit(camada_chao, (0, 0))
    screen.blit(camada_casa, (0, 0))
    screen.blit(player.sprite, player.rect)
    screen.blit(camada_chao2, (0, 0))
    screen.blit(camada_placa, (0, 0))


# Exibe qualquer texto passado na tela
def show_text(text_display):
    text = game_font.render(text_display, 1, (0, 0, 0))
    screen.blit(text, (32, 450))


# Cria as paredes com suas posições X e Y usando multiplo de 32 (devido ao tamanho de cada "bloco" da imagem)
# Usa a definição do LEVEL como base para saber a posição
def create_walls():
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            x += 32
        y += 32
        x = 0


# Cria o objeto texto
def create_text(text, font, color):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()

    return text_surf, text_rect


# Introdução do game
def game_intro():
    intro = True

    # Inicializa a fonte do menu
    main_text = pygame.font.Font('data/fonts/coders_crux.ttf', 70)
    option_text = pygame.font.Font('data/fonts/coders_crux.ttf', 35)

    # Cria os objetos para estes textos
    start_game_name_surf, start_game_name_rect = create_text('START GAME', option_text, black)
    quit_game_name_surf, quit_game_name_rect = create_text('QUIT', option_text, black)

    while intro:
        mouse_pos = mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_name_surf, game_name_text_rect = create_text('METHOLKA KINGDOM', main_text, black)

        game_name_text_rect.center = ((screen_width / 2), (screen_height / 3))
        start_game_name_rect.center = ((screen_width / 2), (screen_height / 1.8))
        quit_game_name_rect.center = ((screen_width / 2), (screen_height / 1.5))

        # Projeta as imagens e textos na tela
        screen.blit(background_start_menu, (0, 0))
        screen.blit(game_name_surf, game_name_text_rect)
        screen.blit(start_game_name_surf, start_game_name_rect)
        screen.blit(quit_game_name_surf, quit_game_name_rect)

        # Verifica onde está o mouse, para validar o click no START GAME ou QUIT
        if ((start_game_name_rect.right >= mouse_pos[0] >= start_game_name_rect.left) and (
                        start_game_name_rect.bottom >= mouse_pos[1] >= start_game_name_rect.top)) or (
                    (quit_game_name_rect.right >= mouse_pos[0] >= quit_game_name_rect.left) and (
                                quit_game_name_rect.bottom >= mouse_pos[1] >= quit_game_name_rect.top)):
            mouse.set_cursor(*HAND_CURSOR)
            if event.type == MOUSEBUTTONDOWN:
                mouse.set_cursor(*DEFAULT_CURSOR)
                game_loop(player)
        else:
            mouse.set_cursor(*DEFAULT_CURSOR)
        pygame.display.update()
        clock.tick(FPS)


# Loop do game
def game_loop(player):
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        # Recebe a tecla apertada pelo usuario
        pressed_keys = pygame.key.get_pressed()

        # Faz verificação de qual tecla foi apertada, possibilitando o movimento do player para aquela direção
        if pressed_keys[K_w] or pressed_keys[K_UP]:
            player.move(0, -3)
            player.change_sprite(1)
        elif pressed_keys[K_s] or pressed_keys[K_DOWN]:
            player.move(0, 3)
            player.change_sprite(2)

        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            player.move(-3, 0)
            player.change_sprite(3)
        elif pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            player.move(3, 0)
            player.change_sprite(4)

        load_initial_map()
        check_pos(player.rect.centerx, player.rect.centery)

        pygame.display.update()
        clock.tick(FPS)

# funcao que salva o objeto do jogador no tiny db
def save_char():
    if db is not None: #verifica se o db foi instanciado
        query = Query()

        # criar um dicionario passando o objeto do jogador. O dicionario nao tem o inventario do player ainda
        player_dict = dict(ch)

        # agora uma lista é criada e ganha todos os objetos do inventario do usuario em forma de dicionario
        inventory = []
        for i in ch.inventory:
            inventory.append(dict(ch.inventory[ch.inventory.index(i)]))

        # coloca a lista inventario no dicionario
        player_dict['inventory'] = inventory

        # se o  jogador ja tiver salvo no tiny db entao ele insere o player
        if not db.search(query.name == ch.name):
            db.insert(player_dict)
            print('criado')
        else: # se o  jogador nao tiver salvo no tiny db entao ele atualiza
            db.update(player_dict, query.name == ch.name)
            print('atualizado')

    print('character saved!')


#funcao que carrega o player do tinydb se ele estiver salvo
def load_char_if_saved():
    query = Query()

    if db is not None: #verifica se db esta instanciado
        var = db.search(query.name == name_to_load)
        print('search:')

        # se a consulta ao tiny db retornar algo:
        if var:
            # o tinydb poderia retornar varios usuarios com o nome pesquisado. no caso sempre haverá só um e esse mesmo é o que interessa
            var = var[0]
            #define os atributos do objeto jogador iguais aos do tiny DB
            ch.name = var.get('name')
            ch.coins = var.get('coins')
            inventory = var.get('inventory')
            print(inventory)

            # preenche o inventario do jogador
            player_inventory = []
            for thing in inventory: # para cada objeto no inventario obtido no tinydb, testa-se o seu tipo e dependendo disso se instancia e adiciona o objeto no inventario para o objeto do jogador
                if thing.get('type') == 'item':
                    item = items.Item(thing.get('name'), thing.get('price'))
                    player_inventory.append(item)
                elif thing.get('type') == 'weapon':
                    weap = items.Weapon(thing.get('name'), thing.get('price'), thing.get('damage'))
                    player_inventory.append(weap)
                elif thing.get('type') == 'armor':
                    armor = items.Armor(thing.get('name'), thing.get('price'), thing.get('defense'))
                    player_inventory.append(armor)
                elif thing.get('type') == 'potions':
                    potion = items.Potion(thing.get('name'), thing.get('price'), thing.get('health'))
                    player_inventory.append(potion)

            ch.inventory = player_inventory


if __name__ == "__main__":
    # Carrega database
    db = TinyDB('game_data.json')

    # Cria uma instância do player
    ch = char.Char()
    name_to_load = 'Player01'

    print('coins dps')
    print(ch.coins)

    # obter char se existir
    if not load_char_if_saved():
        save_char()

    print('coins dps')
    print(ch.coins)

    player = Player()
    create_walls()
    game_intro()
    game_loop(player)
