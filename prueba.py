import pygame
import random
import numpy
import math

# Siempre se pone esto al inicio
pygame.init()

# Ventana
screenwidth = 1200
screenheight = 650
# La pantalla de mi computador es 1360*765
win = pygame.display.set_mode((screenwidth, screenheight))
# win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# icon = pygame.image.load('Pixel art gali 1.png')
# pygame.display.set_icon(icon)
# Nombre de la ventana
pygame.display.set_caption("Frog")

# Cargar las imágenes
fondoNoche = pygame.image.load('imagenes/fondo noche.png').convert()

imgLuna = pygame.image.load('imagenes/luna.png').convert()
imgLuna.set_colorkey((51, 25, 149))

imgBanca = pygame.image.load('imagenes/banca.png').convert()
imgBanca.set_colorkey((51, 25, 149))

imgNubes = [pygame.image.load('imagenes/Nubes/Nube 1.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 2.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 3.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 4.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 5.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 6.png').convert()]

for nube in imgNubes:
    nube.set_colorkey((254, 254, 254))

imgHistoria1 = [pygame.image.load('imagenes/historias/historia1/historia1-1.png').convert(),
                pygame.image.load('imagenes/historias/historia1/historia1-2.png').convert()]

imgEstrellaPequena = pygame.image.load('imagenes/estrella pequeña.png').convert()
imgEstrellaMediana = pygame.image.load('imagenes/estrella mediana.png').convert()

imgAvion = pygame.image.load('imagenes/avion.png').convert()
imgAvion.set_colorkey((51, 25, 149))
imgAvion = pygame.transform.scale(imgAvion, (64, 64))

boundaries = 10


class personaje(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.yinicial = y
        self.yinicialoriginal = y
        self.yreal = y
        self.height = height
        self.width = width
        # El self.jumpcount puede actuar como "gravedad", controla el tiempo que dura el salto
        self.jumpCount = 47
        self.moduloJump = -0.006
        self.jumpCountInicial = self.jumpCount
        self.vel = 5
        self.debesaltar = False
        self.subiendo = False
        self.moverse = True

    def draw(self, win):

        # Hitbox

        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def moverseIzquierda(self):
        if self.x >= 10:
            self.x -= self.vel

    def moverseDerecha(self):
        if self.x <= screenwidth - self.width - 10:
            self.x += self.vel

    def saltar(self):
        if self.debesaltar:
            if self.jumpCount > 0:
                self.subiendo = True
                if self.moverse:
                    self.y += (self.jumpCount ** 2) * self.moduloJump
                self.jumpCount -= 1

            elif self.jumpCount <= 0:
                self.subiendo = False
                self.y -= (self.jumpCount ** 2) * self.moduloJump
                self.jumpCount -= 1

            if self.y >= self.yinicialoriginal:
                self.jumpCount = self.jumpCountInicial


class plataforma(object):
    def __init__(self, x, y, width, vel):
        self.x = x
        self.y = y
        self.yOriginal = y
        self.vel = vel
        self.width = width
        self.height = 20

        self.tocando = False
        self.vecesTocado = 0
        self.contacto = False

    def draw(self, win):
        # Hitbox
        self.y = self.yOriginal - camaraDeRana.cambio
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def movimiento(self):
        self.y = self.yOriginal - camaraDeRana.cambio
        self.x += self.vel
        if self.x <= boundaries or self.x >= screenwidth - self.width - boundaries:
            self.vel = self.vel * -1

    def contactoArriba(self):
        self.y = self.yOriginal - camaraDeRana.cambio
        # Esta parte controla el contacto con la rana
        if rana.x + rana.width >= self.x and self.x + self.width >= rana.x:

            # Caso en el que está por encima
            if self.y - self.height - (rana.y + rana.width) <= 10 and self.y - self.height - (
                    rana.y + rana.width) >= -10 and not rana.subiendo:

                self.contacto = True
                rana.jumpCount = rana.jumpCountInicial
                self.tocando = True
                if rana.debesaltar:
                    self.vecesTocado += 1

                if self.vecesTocado >= 3:
                    self.x = 10000
                    self.vel = 0

            else:
                self.contacto = False
        else:
            self.contacto = False
            self.y = self.yOriginal - camaraDeRana.cambio


class montonDePlataformas(object):
    def __init__(self, PlataformasACrear):
        self.platforms = []
        self.altura = 400
        self.nroDePlataforma = 0
        self.PlataformasACrear = PlataformasACrear
        self.distanciaEntrePlataformas = 200
        self.x = random.randint(150, 150)
        self.velF = 3
        self.velI = 1
        self.anchoInicial = 100
        self.anchoFinal = 200
        self.menosAnchoInicial = 0
        self.menosAnchoFinal = 0
        self.masVelInicial = 0
        self.masVelFinal = 0
        self.i = 1
        self.subirDificultad = 0
        self.velocidadMaximaFinal = 5
        self.velocidadInicialFinal = 3
        self.anchoMaximoFinal = 100
        self.anchoMinimoFinal = 50

        for i in range(4):
            self.platforms.append((plataforma(random.randint(50, screenheight - 250), self.altura,
                                              random.randint(self.anchoInicial - self.menosAnchoInicial,
                                                             self.anchoFinal - self.menosAnchoFinal),
                                              random.choice([-1, 1]) * random.randint(
                                                  self.velI + self.masVelInicial,
                                                  self.velF + self.masVelFinal)),
                                   self.nroDePlataforma))
            self.altura -= self.distanciaEntrePlataformas
            self.nroDePlataforma += 1

    def draw(self, win):

        for platform in self.platforms:

            platform[0].draw(win)
            platform[0].movimiento()
            platform[0].contactoArriba()
            if platform[0].vecesTocado >= 3 or platform[0].y >= 700:
                self.platforms.remove(platform)
                if self.nroDePlataforma < self.PlataformasACrear:
                    self.platforms.append((plataforma(random.randint(50, screenheight - 250), self.altura,
                                                      random.randint(self.anchoInicial - self.menosAnchoInicial,
                                                                     self.anchoFinal - self.menosAnchoFinal),
                                                      random.choice([-1, 1]) * random.randint(
                                                          self.velI + self.masVelInicial,
                                                          self.velF + self.masVelFinal)),
                                           self.nroDePlataforma))
                    self.altura -= self.distanciaEntrePlataformas
                    self.nroDePlataforma += 1
                    if self.nroDePlataforma == 10 * self.i:
                        print("Velocidad iniicial:", self.velI + self.masVelInicial,
                              "Velocidad final: ", self.velF + self.masVelFinal,
                              "Ancho inicial: ", self.anchoInicial - self.menosAnchoInicial,
                              "Ancho final: ", self.anchoFinal - self.menosAnchoFinal)
                        self.subirDificultad += 1
                        if self.subirDificultad == 1 and self.masVelFinal + self.velF < self.velocidadMaximaFinal:
                            self.masVelFinal += 1
                        elif self.subirDificultad == 2 and self.anchoFinal - self.menosAnchoFinal - 50 >= self.anchoMaximoFinal:
                            self.menosAnchoFinal += 50
                        elif self.subirDificultad == 3:
                            if self.masVelInicial + self.velI < self.velocidadInicialFinal:
                                self.masVelInicial += 1
                            if 100 - self.menosAnchoInicial - 25 >= self.anchoMinimoFinal:
                                self.menosAnchoInicial += 25
                            self.subirDificultad = 0
                        self.i += 1

            if platform[0].contacto and platform[1] == self.PlataformasACrear - 1:
                print('ganaste')



class historia(object):
    def __init__(self, imagenes, nroImagenes):
        self.mostrando = True
        self.imagenes = imagenes
        self.i = 0
        self.numero = nroImagenes
        self.desaparecer = False
        self.j = 255

    def draw(self, win):
        win.blit(self.imagenes[self.i], (0, 0))

    def pasarimagen(self):
        if not self.desaparecer:
            self.i += 1

        if self.i == self.numero:
            self.desaparecer = True
            self.mostrando = False

    def desapareciendo(self, win):
        # .set_alpha sirve para controlar la opacidad de la imagen
        if self.desaparecer:
            self.imagenes[self.numero - 1].set_alpha(self.j)  # 0 is fully transparent and 255 fully opaque.
            self.j -= 10
            if self.j <= 0:
                self.desaparecer = False
                animacion1.mostrando = True

            win.blit(self.imagenes[self.numero - 1], (0, 0))


class animacion(object):
    def __init__(self, x):
        self.x = x
        self.mostrando = False
        self.i = 100

    def mostrar(self):
        if rana.x < self.x:
            rana.x += rana.vel
        elif rana.x >= self.x:
            self.i += 1
            if self.i >= 100:
                self.mostrando = False
                rana.debesaltar = True


class estrellas(object):

    def __init__(self, Img, numEstrellas, y2):
        self.numEstrellas = numEstrellas
        self.estrellasImg = Img
        self.estrellasX = []
        self.estrellasY = []
        self.dibujarlas = False
        self.vel = 4000
        self.desdeDonde = 0
        self.hastaDonde = y2
        # 0 si no aparece, 1 si aparece
        self.aparecerEstrella = []
        for i in range(self.numEstrellas):
            self.aparecerEstrella.append(0)

        for i in range(self.numEstrellas):
            self.estrellasX.append(random.randint(1, 1200))
            self.estrellasY.append(random.randint(-20000 - camaraDeRana.cambio, 600 - camaraDeRana.cambio))

        self.sumatoriaparaestrellas = 0

    def draw(self, win, desdecuando):
        # AQUI SE DEFINE DESDE CUANDO APARECEN
        if camaraDeRana.cambio <= -desdecuando:
            self.dibujarlas = True
        if self.dibujarlas:
            for i in range(self.numEstrellas):
                if self.sumatoriaparaestrellas // self.vel == i:
                    self.aparecerEstrella[i] = 1
                    if i < (self.numEstrellas):
                        self.aparecerEstrella[i + 1] = 1
                    if i < self.numEstrellas - 1:
                        self.aparecerEstrella[i + 2] = 1
                    if i < self.numEstrellas - 2:
                        self.aparecerEstrella[i + 3] = 1

                if self.aparecerEstrella[i] == 1:
                    win.blit(self.estrellasImg, (self.estrellasX[i], self.estrellasY[i] - camaraDeRana.cambio / 2))
                else:
                    self.sumatoriaparaestrellas += 1
                if self.estrellasY[i] >= screenheight:
                    del self.estrellasX[i]
                    del self.estrellasY[i]


class estrellaFugaz(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagenes = []
        self.coordenadas = []
        self.coordenadasADibujar = []
        self.i = 0
        self.j = 0
        self.total = 0
        self.limite = 45
        self.bajada = 0
        self.ultimoY = y

        while self.i < self.limite:
            self.coordenadas.append((self.x, self.y))
            self.y += (self.i ** 2) * rana.moduloJump
            self.i += 1

    def dibujar(self, win):

        self.j += 1

        if self.j % 6 == 0 and self.coordenadas:
            self.coordenadasADibujar.append(self.coordenadas[-1])
            del self.coordenadas[-1]

        for coordenada in self.coordenadasADibujar:
            win.blit(imgEstrellaPequena, (coordenada[0], coordenada[1] - self.bajada - camaraDeRana.cambio / 2))
            self.ultimoY = coordenada[1] - self.bajada - camaraDeRana.cambio / 2

        self.bajada -= 0.1


class montonEstrellasFugaces(object):
    def __init__(self, nro, y):
        self.estrellasFugaces = []
        self.nro = nro
        self.dibujarEstrellasFugaces = False
        # self.y define cuándo comienzan las estrellas
        self.y = y
        self.sd = 1000

        for i in range(self.nro):
            # Para el range de y se tiene que hacer la siguiente ecuación: ? + camaraDeRana/2 = -y que se quiere -> ? = -(y+camaraDeRana/2)
            self.estrellasFugaces.append(estrellaFugaz(random.randint(0, 1200),
                                                       numpy.random.normal(-self.sd * 3.3,
                                                                           self.sd)))

            # En vez de random randint se puede poner una distribución normal numpy.random.normal(-self.y+1100+camaraDeRana.cambio/2, 1100, size=None)
            # Random random.randint(-self.y + camaraDeRana.cambio / 2,-self.y + 2200 + camaraDeRana.cambio / 2)))

    def draw(self, win):
        if -camaraDeRana.cambio > -self.y:
            self.dibujarEstrellasFugaces = True
        elif -camaraDeRana.cambio > self.y + 1000:
            self.dibujarEstrellasFugaces = False

        if self.dibujarEstrellasFugaces:
            for fugaz in self.estrellasFugaces:
                fugaz.dibujar(win)


class objetosEnElCIelo(object):
    def __init__(self):
        self.avionDibujar = False
        self.avionY = -200
        self.avionAparecer = 1000
        self.avionCamara = 0
        self.xAvion = 500
        self.yOvni = 2000
        self.yNubes = 500

    def draw(self, win):
        if -camaraDeRana.cambio > self.avionAparecer and self.xAvion <= 1200 and not self.avionDibujar:
            self.avionDibujar = True
            self.avionCamara = camaraDeRana.cambio
        elif self.avionDibujar and self.xAvion <= 1250:
            win.blit(imgAvion, (self.xAvion, self.avionY - (camaraDeRana.cambio - self.avionCamara) / 2))
            self.xAvion += 0.5


class camara(object):
    def __init__(self):
        self.ydeCambio = 150

        # Es 120 con rana.jumpcoiunt = 50
        self.cambio = 0
        self.limite = 22000

    def movimientoCamara(self):
        if rana.y <= self.ydeCambio and rana.subiendo and -self.cambio < self.limite:
            rana.moverse = False
            self.cambio += (rana.jumpCount ** 2) * rana.moduloJump
            rana.yinicialoriginal = rana.yreal - self.cambio

        else:

            rana.moverse = True


rana = personaje(185, screenheight - 40 - 40, 24, 40)
camaraDeRana = camara()

# estrellas(imagenestrella, numero de estrellas)
estrellapequeña = estrellas(imgEstrellaPequena, 10000, -20000)
estrellamediana = estrellas(imgEstrellaMediana, 400, -20000)
estrellasFugaces = montonEstrellasFugaces(100, -2000)

# plataforma(self, x, y, width, vel)
generarPlataformas = montonDePlataformas(200)
# Se crea la instacnia de objetos
objetos = objetosEnElCIelo()
historia1 = historia(imgHistoria1, 2)
animacion1 = animacion(700)


# Función que dibuja todos los objetos, personajes, etc en cada momento
def redrawGameWindow():
    global altura
    global nroDePlataforma
    if not historia1.mostrando:
        camaraDeRana.movimientoCamara()
        win.blit(fondoNoche, (0, screenheight - 22000 - camaraDeRana.cambio/2))
        win.blit(imgNubes[5], (100, 200 - camaraDeRana.cambio))
        # Luna

        estrellapequeña.draw(win, 100)
        estrellamediana.draw(win, 100)
        estrellasFugaces.draw(win)
        objetos.draw(win)

        win.blit(imgLuna, (200, -1000 - camaraDeRana.cambio / 2))
        # plataforma, dibujo y movimiento
        if not animacion1.mostrando and not historia1.desaparecer:
            generarPlataformas.draw(win)

        rana.draw(win)
        rana.saltar()
        win.blit(imgBanca, (677, 582 - camaraDeRana.cambio))

        # Este se pone al final para que la imagen de la historia se fade out
        if historia1.desaparecer:
            historia1.desapareciendo(win)

    elif historia1.mostrando:

        historia1.draw(win)


# mainloop
run = True
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
while run:
    print(-camaraDeRana.cambio)
    clock.tick(60)
    keys = pygame.key.get_pressed()

    # Dentro de este for vienen las acciones que se deben apretar solo 1 vez y se reinician cuando se apretan de nuevo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if historia1.mostrando:
            if keys[pygame.K_SPACE]:
                historia1.pasarimagen()

    if keys[pygame.K_d]:
        rana.jumpCount = 44.5

    if keys[pygame.K_LEFT]:
        if not historia1.desaparecer and not historia1.mostrando and not animacion1.mostrando:
            rana.moverseIzquierda()

    if keys[pygame.K_RIGHT]:
        if not historia1.desaparecer and not historia1.mostrando and not animacion1.mostrando:
            rana.moverseDerecha()

    if keys[pygame.K_1]:
        run = False

    if animacion1.mostrando:
        animacion1.mostrar()

    redrawGameWindow()
    pygame.display.update()

pygame.quit()
