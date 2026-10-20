import pygame
import math


class Zumbi:
    def __init__(self, tela, mapa, x, y):
        self.retangulo = pygame.Rect(x, y, 20, 20)
        self.vida = 100
        self.outros_zumbis = []
        self.vivo = True
        self.dano = 10
        self.ultimo_ataque = 0
        self.tela = tela
        self.mapa = mapa
        self.velocidade_zumbi = 1


    def desenhar(self):
        pygame.draw.rect(
            self.tela,
            (0, 255, 0),
            self.retangulo
        )


    def atualizar(self):

        distancia_x = abs(
            self.retangulo.x - self.seguir_personagem.retangulo.x
        )

        distancia_y = abs(
            self.retangulo.y - self.seguir_personagem.retangulo.y
        )

        distancia = math.sqrt(
            distancia_x ** 2 + distancia_y ** 2
        )


        if self.retangulo.colliderect(self.seguir_personagem.retangulo):
            self.velocidade_zumbi = 0
            tempo_atual = pygame.time.get_ticks()

            if tempo_atual - self.ultimo_ataque >= 1000:
                self.seguir_personagem.vida = self.seguir_personagem.vida - self.dano
                self.ultimo_ataque = tempo_atual
                if self.seguir_personagem.vida <= 0:
                    self.seguir_personagem.vida = 0
                    self.seguir_personagem.vivo = False

        else:
            self.velocidade_zumbi = 1






        coluna = (
            self.retangulo.x
            // self.mapa.tamanho_tile
        )

        linha = (
            self.retangulo.y
            // self.mapa.tamanho_tile
        )


        coluna_jogador = (
            self.seguir_personagem.retangulo.x
            // self.mapa.tamanho_tile
        )

        linha_jogador = (
            self.seguir_personagem.retangulo.y
            // self.mapa.tamanho_tile
        )


        celula_inicial_zumbi = (linha, coluna)

        celula_jogador = (
            linha_jogador,
            coluna_jogador
        )

        if celula_inicial_zumbi == celula_jogador:
            diferenca_x = self.seguir_personagem.retangulo.centerx - self.retangulo.centerx
            diferenca_y = self.seguir_personagem.retangulo.centery - self.retangulo.centery
            movimento_x = 0
            movimento_y = 0
            if diferenca_x > 0:
                movimento_x = 1
            elif diferenca_x < 0:
                movimento_x = -1
            if diferenca_y > 0:
                movimento_y = 1
            elif diferenca_y < 0:
                movimento_y = -1
            novo_retangulo = self.retangulo.copy()
            novo_retangulo.x += movimento_x * self.velocidade_zumbi
            if self.pode_mover(novo_retangulo):
                self.retangulo.x = novo_retangulo.x
            novo_retangulo = self.retangulo.copy()
            novo_retangulo.y += movimento_y * self.velocidade_zumbi
            if self.pode_mover(novo_retangulo):
                self.retangulo.y = novo_retangulo.y
        pais = {}

        fila = [celula_inicial_zumbi]

        visitados = []


        while fila:

            celula_atual = fila.pop(0)


            if celula_atual == celula_jogador:
                break


            visitados.append(celula_atual)


            linha_atual, coluna_atual = celula_atual


            vizinhos = [
                (linha_atual - 1, coluna_atual),
                (linha_atual + 1, coluna_atual),
                (linha_atual, coluna_atual - 1),
                (linha_atual, coluna_atual + 1)
            ]


            for vizinho in vizinhos:

                linha_vizinho, coluna_vizinho = vizinho


                if (
                    0 <= linha_vizinho < len(self.mapa.mapa)
                    and
                    0 <= coluna_vizinho < len(self.mapa.mapa[0])
                ):

                    if self.mapa.mapa[linha_vizinho][coluna_vizinho] == 1:

                        if (
                            vizinho not in visitados
                            and
                            vizinho not in fila
                        ):

                            pais[vizinho] = celula_atual

                            fila.append(vizinho)


        if (
            celula_jogador != celula_inicial_zumbi
            and
            celula_jogador in pais
        ):

            caminho = []

            celula = celula_jogador


            while celula != celula_inicial_zumbi:

                caminho.append(celula)

                celula = pais[celula]


            caminho.reverse()


            proxima_celula = caminho[0]

            linha_proxima_celula = proxima_celula[0]
            coluna_proxima_celula = proxima_celula[1]


            x_alvo = (
                coluna_proxima_celula
                * self.mapa.tamanho_tile
                + self.mapa.tamanho_tile // 2
            )

            y_alvo = (
                linha_proxima_celula
                * self.mapa.tamanho_tile
                + self.mapa.tamanho_tile // 2
            )


            movimento_x = 0
            movimento_y = 0


            if x_alvo > self.retangulo.centerx:
                movimento_x = 1

            elif x_alvo < self.retangulo.centerx:
                movimento_x = -1


            if y_alvo > self.retangulo.centery:
                movimento_y = 1

            elif y_alvo < self.retangulo.centery:
                movimento_y = -1


            novo_retangulo = self.retangulo.copy()

            novo_retangulo.x += (
                movimento_x
                * self.velocidade_zumbi
            )


            if self.pode_mover(novo_retangulo):
                self.retangulo.x = novo_retangulo.x


            novo_retangulo = self.retangulo.copy()

            novo_retangulo.y += (
                movimento_y
                * self.velocidade_zumbi
            )


            if self.pode_mover(novo_retangulo):
                self.retangulo.y = novo_retangulo.y
    def pode_mover(self, novo_retangulo):
        if self.mapa.pode_andar(novo_retangulo) is False:
            return False
        for outro_zumbi in self.outros_zumbis:
            if outro_zumbi is self or not outro_zumbi.vivo:
                continue
            if novo_retangulo.colliderect(outro_zumbi.retangulo):
                return False
        return True



    def seguir(self, personagem):
        self.seguir_personagem = personagem