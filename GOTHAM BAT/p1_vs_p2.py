import pygame
import neat
import time
import os
import random
pygame.font.init() 
WIN_WIDTH=500
WIN_HEIGHT=800

BIRD_IMGS1=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs2","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs2","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs2","bird3.png")))]
BIRD_IMGS2=[(pygame.image.load(os.path.join("imgs2","bbird2.png"))),(pygame.image.load(os.path.join("imgs2","bbird2.png"))),(pygame.image.load(os.path.join("imgs2","bbird2.png")))]
PIPE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs2","pipe.png")))
BASE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs2","base.png")))
BG_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs2","bg.png")))
STAT_FONT=pygame.font.SysFont('comicsans',50)

class Bird:
    IMGS=BIRD_IMGS1
    MAX_ROTATION=25
    ROT_VEL=20
    ANIMATION_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMGS[0]
    def jump(self):
        self.vel=-7.5
        self.tick_count=0
        self.height=self.y
    def move(self):
        self.tick_count+=1
        d=self.vel*self.tick_count+1.5*self.tick_count**2
        if d>=16:
            d=16
        if d<0:
            d-=2
        self.y=self.y+d
        if d<0 or self.y<self.height+50:
            if self.tilt<self.MAX_ROTATION:
                self.tilt=self.MAX_ROTATION
        else:
            if self.tilt>-90:
                self.tilt-=self.ROT_VEL
    def draw(self,win,num):
        if num==1:
            self.IMGS=BIRD_IMGS1
        else:
            self.IMGS=BIRD_IMGS2
        self.img_count+=1
        if self.img_count<self.ANIMATION_TIME:
            self.img=self.IMGS[0]
        elif self.img_count<self.ANIMATION_TIME*2:
            self.img=self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*3:
            self.img=self.IMGS[2]
        elif self.img_count<self.ANIMATION_TIME*4:
            self.img=self.IMGS[1]
        elif self.img_count==self.ANIMATION_TIME*4+1:
            self.img=self.IMGS[0]
            self.img_count=0
        if self.tilt<=-80:
            self.img=self.IMGS[1]
            self.img_count=self.ANIMATION_TIME*2
        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP=250
    VEL=5
    def __init__(self,x):
        self.x=x
        self.height=0
        self.gap=100
        self.top=0
        self.bottom=0
        self.PIPE_TOP=pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM=PIPE_IMG
        self.passed=False
        self.set_height()
    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.bottom=self.height+self.GAP
    def move(self):
        self.x-=self.VEL
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
    def collide(self,bird):
        bird_mask=bird.get_mask()
        top_mask=pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask=pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset=(self.x-bird.x,self.top-round(bird.y))
        bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))
        b_point=bird_mask.overlap(bottom_mask,bottom_offset)
        t_point=bird_mask.overlap(top_mask,top_offset)
        if t_point or b_point:
            return True
        return False

class Base:
    VEL=5
    WIDTH=BASE_IMG.get_width()
    IMG=BASE_IMG
    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.WIDTH
    def move(self):
        self.x1-=self.VEL
        self.x2-=self.VEL
        if self.x1+self.WIDTH<0:
            self.x1=self.x2+self.WIDTH
        if self.x2+self.WIDTH<0:
            self.x2=self.x1+self.WIDTH
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))


def draw_window(win,bird1,bird2,pipes,base,score1,score2):
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    font=pygame.font.SysFont('comicsans',25)
    text_y=font.render("Press 'SPACE' for Yellow to Jump",1,(255,255,255))
    win.blit(text_y,(10,10))
    text_b=font.render("Press 'UP' for Blue to Jump",1,(255,255,255))
    win.blit(text_b,(10,10+text_y.get_height()))
    font2=pygame.font.SysFont('comicsans',40)
    text=font2.render("Yellow: "+str(score1),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
    text1=font2.render("Blue: "+str(score2),1,(255,255,255))
    win.blit(text1,(WIN_WIDTH-10-text1.get_width(),20+text.get_height()))
    base.draw(win) 
    bird1.draw(win,1)
    bird2.draw(win,2)
    pygame.display.update()
    
def main():
    bird1=Bird(230,350)
    bird2=Bird(230,350)
    base=Base(730)
    pipes=[Pipe(600)]
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock=pygame.time.Clock()
    score1=0
    score2=0
    run1=True
    run2=True
    while run1 or run2:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        bird1.move()
        bird2.move()
        add_pipe=False
        rem=[]
        for pipe in pipes:
            if pipe.collide(bird1):
                run1=False
            if pipe.collide(bird2):
                run2=False
            if pipe.x+pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)
            if not pipe.passed:
                if pipe.x<bird1.x and run1:
                    pipe.passed=True
                    add_pipe=True
                    score1+=1
                if pipe.x<bird2.x and run2:
                    pipe.passed=True
                    add_pipe=True
                    score2+=1
            pipe.move()
        if add_pipe:
            pipes.append(Pipe(600))
        for r in rem:
            pipes.remove(r)
        if bird1.y+bird1.img.get_height()>=730:
            run1=False
        if bird2.y+bird2.img.get_height()>=730:
            run2=False


        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and run1:
            bird1.jump()
        if keys[pygame.K_UP] and run2:
            bird2.jump()

            
        base.move()
        draw_window(win,bird1,bird2,pipes,base,score1,score2)

    wins=""
    if score1>score2:
        wins="Yellow wins"
    elif score2>score1:
        wins="Blue wins"
    else:
        wins="Draw"
    pygame.draw.rect(win,(0,0,0),(WIN_WIDTH/2-100,WIN_HEIGHT/2-50,200,100))
    text3=STAT_FONT.render("Game Over",1,(255,255,255))
    win.blit(text3,(WIN_WIDTH/2-text3.get_width()/2,WIN_HEIGHT/2-text3.get_height()/2))
    text4=STAT_FONT.render(wins,1,(255,255,255))
    win.blit(text4,(WIN_WIDTH/2-text4.get_width()/2,WIN_HEIGHT/2+text3.get_height()-text3.get_height()/2))
    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
    
main()
