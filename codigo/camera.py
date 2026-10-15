class Camera:

    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0

    def seguir(self, personagem):
        self.personagem = personagem

    def atualizar(self):

        self.camera_x = self.personagem.retangulo.centerx - 640
        self.camera_y = self.personagem.retangulo.centery - 360

        # Limite esquerdo e superior
        if self.camera_x < 0:
            self.camera_x = 0

        if self.camera_y < 0:
            self.camera_y = 0

        # Tamanho do mapa
        largura_mapa = 32 * 40
        altura_mapa = 18 * 40

        # Limite direito
        limite_x = largura_mapa - 1280

        if self.camera_x > limite_x:
            self.camera_x = limite_x

        # Limite inferior
        limite_y = altura_mapa - 720

        if self.camera_y > limite_y:
            self.camera_y = limite_y