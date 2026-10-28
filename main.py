import pygame
import random
from pathlib import Path
import math


from codigo.mapa import Mapa
from codigo.personagem import Personagem
from codigo.camera import Camera
from codigo.zumbi import Zumbi
from codigo.hud import HUD
from codigo.item import Item
from codigo.fundo_menu import FundoMenu
from codigo.arma import Arma
from codigo.projetil import Projetil

pygame.init()

LARGURA = 1280
ALTURA = 720
pasta_sons = Path(__file__).resolve().parent / "sons"
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Zumbi")
fundo_menu = FundoMenu(LARGURA, ALTURA)
clock = pygame.time.Clock()

som_chuva = pygame.mixer.Sound(str(pasta_sons / "chuva.wav"))
som_vento = pygame.mixer.Sound(str(pasta_sons / "vento.wav"))
som_clique = pygame.mixer.Sound(str(pasta_sons / "click_no_botao.wav"))
som_transicao = pygame.mixer.Sound(str(pasta_sons / "transicao.wav"))

som_chuva.set_volume(0.25)
som_vento.set_volume(0.15)
som_clique.set_volume(0.50)
som_transicao.set_volume(0.40)

canal_chuva = pygame.mixer.Channel(0)
canal_vento = pygame.mixer.Channel(1)
canal_clique = pygame.mixer.Channel(2)
canal_transicao = pygame.mixer.Channel(3)

posicoes_spawn = [
    (500, 370),
    (800, 250),
    (300, 250),
    (1000, 370),
    (700, 100),
    (300, 500),
    (900, 500),
    (1100, 200)
]

ultimo_spawn = 0
inter_spawn = 3000
max_zumbis = 5
zumbis_vivos = 0
camera = Camera()
mapa = Mapa(tela, camera)
personagem = Personagem(tela, mapa)
arma_chao = Arma("Pistola", str(Path(__file__).resolve().parent / "imagens" / "armas" / "pistola.png" ), 130, 120)
taco_chao = Item(tela, mapa, "taco", 100, 80)
medicamento_chao = Item(tela, mapa, "medicamento", 200, 120)
itens_mapa = [taco_chao, medicamento_chao]
largura_mapa =  mapa.tamanho_tile * len(mapa.mapa[0])
altura_mapa = mapa.tamanho_tile * len(mapa.mapa)

zumbis = []
projeteis = []

camera.seguir(personagem)

fonte = pygame.font.SysFont("comicsans", 30)

fonte_do_titulo = pygame.font.SysFont(
    "arial",
    60,
    bold=True
)

fonte_botao = pygame.font.SysFont(
    "arial",
    40,
    bold=True
)

botao_jogar = pygame.Rect(490, 280, 300, 70)
botao_sair = pygame.Rect(490, 400, 300, 70)

rodando = True

hud = HUD(LARGURA, ALTURA)

tela_atual = "menu"

inventario_aberto = False
game_over = False

for i in range(max_zumbis):
    x = posicoes_spawn[i][0]
    y = posicoes_spawn[i][1]

    zumbi = Zumbi(tela, mapa, x, y)

    zumbis.append(zumbi)

    zumbi.seguir(personagem)

canal_chuva.play(som_chuva, loops=-1, fade_ms=1000)
canal_vento.play(som_vento, loops=-1, fade_ms=1000)

while rodando:
    dt = clock.tick(60) / 1000.0

    eventos = pygame.event.get()

    for evento in eventos:

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if personagem.vivo and evento.key == pygame.K_r and tela_atual == "jogar" and not game_over:
                if personagem.item_equipado == "Pistola" and personagem.arma is not None:
                    print("reserva:", personagem.arma.reserva)
                    print("municao:", personagem.arma.municao)
                    personagem.arma.recarregar()
                    print("reserva:", personagem.arma.reserva)
                    print("municao:", personagem.arma.municao)

            if evento.key == pygame.K_i and personagem.vivo and not game_over:
                inventario_aberto = not inventario_aberto

            if evento.key == pygame.K_r and game_over:

                personagem = Personagem(tela, mapa)

                zumbis = []

                for i in range(max_zumbis):

                    x = posicoes_spawn[i][0]
                    y = posicoes_spawn[i][1]

                    zumbi = Zumbi(tela, mapa, x, y)

                    zumbis.append(zumbi)

                    zumbi.seguir(personagem)

                camera.seguir(personagem)

                inventario_aberto = False
                game_over = False
                ultimo_spawn = pygame.time.get_ticks()
                for item in itens_mapa:
                    item.coletado = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1 and tela_atual == "menu":
                if botao_jogar.collidepoint(evento.pos):
                    tela_atual = "jogar"
                    canal_clique.play(som_clique)
                    canal_transicao.play(som_transicao)
                    canal_chuva.fadeout(800)
                    canal_vento.fadeout(800)

                elif botao_sair.collidepoint(evento.pos):
                    canal_clique.play(som_clique)
                    rodando = False
            elif evento.button == 1 and tela_atual == "jogar":
                if personagem.item_equipado == "Pistola" and personagem.arma is not None:
                    if personagem.arma.municao > 0:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mouse_mapa_x = mouse_x + camera.camera_x
                        mouse_mapa_y = mouse_y + camera.camera_y

                        dirx = mouse_mapa_x - personagem.retangulo.centerx
                        diry = mouse_mapa_y - personagem.retangulo.centery

                        comprimento = math.sqrt(dirx ** 2 + diry ** 2)
                        if comprimento > 0:
                            dirx = dirx / comprimento
                            diry = diry / comprimento
                            if ((personagem.direcao == "direita" and dirx > 0) or (personagem.direcao == "esquerda" and dirx < 0)
                                or (personagem.direcao == "cima" and diry < 0) or (personagem.direcao == "baixo" and diry > 0)):
                                bala = Projetil(tela, personagem.retangulo.centerx - 3, personagem.retangulo.centery - 3, 6, 6, 10, dirx, diry)
                                projeteis.append(bala)
                                personagem.arma.municao -= 1
                                print("Disparo detectado")
                                print("municao restante " + str(personagem.arma.municao))


    if tela_atual == "menu":
        fundo_menu.atualizar(dt)
        fundo_menu.desenhar(tela)

        titulo = fonte_do_titulo.render(
            "Zoio e os zumbis",
            True,
            (255, 255, 255)
        )

        texto_jogar = fonte_botao.render(
            "Jogar",
            True,
            (255, 255, 255)
        )

        texto_sair = fonte_botao.render(
            "Sair",
            True,
            (255, 255, 255)
        )

        pygame.draw.rect(
            tela,
            (45, 120, 45),
            botao_jogar,
            border_radius=20
        )

        pygame.draw.rect(
            tela,
            (150, 40, 40),
            botao_sair,
            border_radius=20
        )

        tela.blit(
            titulo,
            titulo.get_rect(
                center=(LARGURA // 2, 170)
            )
        )

        tela.blit(
            texto_jogar,
            texto_jogar.get_rect(
                center=botao_jogar.center
            )
        )

        tela.blit(
            texto_sair,
            texto_sair.get_rect(
                center=botao_sair.center
            )
        )

    elif tela_atual == "jogar":
        hud.atualizar(eventos)
        if hud.slot_selecionado < len(personagem.inventario.itens):
            item_selecionado = personagem.inventario.itens[hud.slot_selecionado]
        else:
            item_selecionado = None
        personagem.item_equipado = item_selecionado

        if personagem.item_equipado == "Pistola" and personagem.arma is not None:
            pass

        if personagem.vivo and not game_over:
            personagem.atualizar()
        for item in itens_mapa:
            if personagem.retangulo.colliderect(item.retangulo) and not item.coletado:
                if pygame.key.get_pressed()[pygame.K_e]:
                    personagem.inventario.adicionar(item.nome)
                    item.coletado = True



        if personagem.vida <= 0:

            personagem.vida = 0
            personagem.vivo = False
            game_over = True
            inventario_aberto = False

        camera.atualizar()

        mapa.desenhar()
        if arma_chao is not None:
            arma_chao.desenhar_chao(tela, camera)

        if arma_chao is not None:
            if arma_chao.esta_perto(personagem):
                if pygame.key.get_pressed()[pygame.K_e]:
                    personagem.inventario.adicionar(arma_chao.nome)
                    personagem.arma = arma_chao
                    arma_chao = None


        for item in itens_mapa:
            if not item.coletado:
                item.desenhar()

        if personagem.vivo:
            personagem.desenhar()

        if personagem.vivo and not game_over:

            for zumbi in zumbis:

                if zumbi.vivo:

                    if personagem.area_ataque is not None:

                        if personagem.area_ataque.colliderect(
                            zumbi.retangulo
                        ):

                            if pygame.time.get_ticks() - personagem.ultimo_ataque >= 500:

                                personagem.ultimo_ataque = pygame.time.get_ticks()

                                zumbi.vida -= 500

                            if zumbi.vida <= 0:

                                zumbi.vida = 0
                                zumbi.vivo = False

        zumbis_vivos = 0

        for zumbi in zumbis:

            if zumbi.vivo:
                zumbis_vivos += 1

        tempo = pygame.time.get_ticks()

        if (
            not game_over
            and personagem.vivo
            and zumbis_vivos < max_zumbis
            and tempo - ultimo_spawn > inter_spawn
        ):

            posicao_spawn_aleat = random.choice(posicoes_spawn)

            zumbi = Zumbi(
                tela,
                mapa,
                posicao_spawn_aleat[0],
                posicao_spawn_aleat[1]
            )

            zumbis.append(zumbi)

            zumbi.seguir(personagem)

            ultimo_spawn = tempo

        for zumbi in zumbis:
            zumbi.outros_zumbis = zumbis
            if personagem.vivo and not game_over and zumbi.vivo:
                zumbi.atualizar()

            if zumbi.vivo:
                zumbi.desenhar()

        projeteis_remover = []
        for projetil in projeteis:
            projetil.atualizar()
            if ((projetil.retangulo.left > largura_mapa) or (projetil.retangulo.right < 0) or
                (projetil.retangulo.bottom < 0) or (projetil.retangulo.top > altura_mapa)):
                projeteis_remover.append(projetil)
                continue
            if mapa.pode_andar(projetil.retangulo) is False:
                projeteis_remover.append(projetil)
                continue
            projetil.desenhar(camera)
            for zumbi in zumbis:
                if zumbi.vivo and projetil.retangulo.colliderect(zumbi.retangulo):
                    zumbi.vida -= 25
                    projeteis_remover.append(projetil)
                    if zumbi.vida <= 0:
                        zumbi.vivo = False
                    break

        for projetil in projeteis_remover:
            projeteis.remove(projetil)


        if personagem.vivo and not game_over:

            hud.desenhar(
                tela,
                personagem.vida,
                personagem.vida_maxima,
                personagem.inventario.itens
            )

        if inventario_aberto and personagem.vivo and not game_over:
            personagem.inventario.desenhar(tela)

        if game_over:

            camada = pygame.Surface(
                (LARGURA, ALTURA)
            )

            camada.set_alpha(150)
            camada.fill((0, 0, 0))

            tela.blit(
                camada,
                (0, 0)
            )

            texto_game_over = fonte_do_titulo.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            texto_reiniciar = fonte_botao.render(
                "Pressione R para reiniciar",
                True,
                (255, 255, 255)
            )

            tela.blit(
                texto_game_over,
                texto_game_over.get_rect(
                    center=(
                        LARGURA // 2,
                        ALTURA // 2 - 50
                    )
                )
            )

            tela.blit(
                texto_reiniciar,
                texto_reiniciar.get_rect(
                    center=(
                        LARGURA // 2,
                        ALTURA // 2 + 50
                    )
                )
            )

    pygame.display.update()


pygame.quit()