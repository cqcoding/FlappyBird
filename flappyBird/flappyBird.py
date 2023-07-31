import pygame
import os
import random

TelaLarg= 500
TelaAlt = 800

ImagemCano= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs\imgs', 'pipe.png')))
ImagemChao= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs\imgs', 'base.png')))
ImagemBG= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs\imgs', 'bg.png')))
ImagensPassaro= [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs\imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs\imgs', 'bird2.png'))),   
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs\imgs', 'bird3.png'))),
]


pygame.font.init()
FontePontos= pygame.font.SysFont('arial', 50)

class Passaro:
    Imagens = ImagensPassaro
    RotacaoMax= 25
    VelocRotacao = 20
    TempoAnimacao = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.veloc = 0
        self.altura = self.y
        self.tempo = 0
        self.contagemImg = 0
        self.imagem = self.Imagens[0]
        
    def pular(self):
        self.veloc = -10.5
        self.tempo = 0
        self.altura = self.y
        
        
    def mover(self):
        self.tempo += 1
        deslocamento = 1.5*(self.tempo**2) + self.veloc*self.tempo
        
        if deslocamento > 16 :
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
            
        self.y += deslocamento
        
        if deslocamento<0 or self.y< (self.altura + 50):
            if self.angulo < self.RotacaoMax:
                self.angulo = self.RotacaoMax
        else:
            if self.angulo> -90:
                self.angulo -= self.VelocRotacao
        
    
    def desenhar(self, tela):
        self.contagemImg += 1
        
        if self.contagemImg < self.TempoAnimacao:
            self.imagem = self.Imagens[0]
        elif self.contagemImg< self.TempoAnimacao*2:
            self.imagem = self.Imagens[1]
        elif self.contagemImg < self.TempoAnimacao*3:
            self.imagem = self.Imagens[2]
        elif self.contagemImg < self.TempoAnimacao*4:
            self.imagem = self.Imagens[1]
        elif self.contagemImg >= self.TempoAnimacao*4 +1: 
            self.imagem = self.Imagens[0]
            self.contagemImg = 0
            
        
        if self.angulo <= -80:
            self.imagem = self.Imagens[1]
            self.contagemImg = self.TempoAnimacao*2
            
        imagemRot = pygame.transform.rotate(self.imagem, self.angulo)
        retangulo = imagemRot.get_rect(center =(self.x, self.y))
        tela.blit(imagemRot, retangulo.topleft)
               

    def get_mask(self):
       return pygame.mask.from_surface(self.imagem)
        
        
class Cano:
    Distancia= 270
    Velocidade= 5
    
    def __init__ (self, x):
        self.x = x
        self.altura = 0
        self.posicTopo = 0
        self.posicBase = 0
        self.canoTopo= pygame.transform.flip(ImagemCano, False, True)
        self.canoBase= ImagemCano
        self.passou = False
        self.definirAlt()
        
    def definirAlt(self):
        self.altura = random.randrange(50, 450)
        self.posicTopo = self.altura - self.canoTopo.get_height()
        self.posicBase= self.altura + self.Distancia
        
    def mover(self):
        self.x -= self.Velocidade
        
    def desenhar(self, tela):
        tela.blit(self.canoTopo, (self.x, self.posicTopo))
        tela.blit(self.canoBase, (self.x, self.posicBase))
        
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask. from_surface(self.canoTopo)
        base_mask = pygame.mask. from_surface(self.canoBase)
        
        distanciaTopo =(self.x - passaro.x, self.posicTopo - int(passaro.y))
        distanciaBase =(self.x - passaro.x, self.posicBase - int(passaro.y))
        
        topoPonto = passaro_mask.overlap(topo_mask, distanciaTopo)
        basePonto = passaro_mask.overlap(base_mask, distanciaBase)
        
        if basePonto or topoPonto:
            return True
        else:
            return False
        
        

class Chao:
    Velocidade = 5
    Largura = ImagemChao.get_width()
    Imagem = ImagemChao
    
    def __init__(self, y):
        self. y= y
        self.x0 = 0
        self.x1 = self.Largura
        
    def mover(self):
        self.x0 -= self.Velocidade
        self.x1 -= self.Velocidade
        
        if self.x0 + self.Largura < 0:
            self.x0 = self.x1 + self.Largura
        if self.x1 + self.Largura < 0:
            self.x1 = self.x0 + self.Largura
            
    def desenhar(self, tela):
        tela.blit(self.Imagem, (self.x0, self.y))
        tela.blit(self.Imagem, (self.x1, self.y))    
        
        
        
def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(ImagemBG, (0,0))
    
    for passaro in passaros:
        passaro.desenhar(tela)
        
    for cano in canos:
        cano.desenhar(tela)
        
    texto = FontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TelaLarg- 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()
    
    
