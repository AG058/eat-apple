import sys , pygame
from pygame.locals import *
from farmer import *
from apple import *

pygame.init()
pygame.mixer.init()

# 创建屏幕
screen_size = (800 , 600)
active_size = (800 , 555)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('吃苹果')

clock = pygame.time.Clock()

# 导入背景
background_image = pygame.image.load('images/background.png').convert_alpha()

# 导入胜利图
you_win_image = pygame.image.load('images/you_win.png').convert_alpha()
you_win_image_rect = you_win_image.get_rect()
you_win_image_rect.center = screen_size[0] // 2 , screen_size[1] // 2

# 导入音效
eat_apple_sound = pygame.mixer.Sound('musics/eat_apple.wav')
eat_apple_sound.set_volume(0.2)
win_sound = pygame.mixer.Sound('musics/win.wav')
win_sound.set_volume(0.5)

# 创建组
player_group = pygame.sprite.Group() # 序列图需要用组draw方法更新帧
apple_group = pygame.sprite.Group() 

# 创建字体
score_font = pygame.font.Font('font/font.ttf' , 20)

# 创建苹果
for i in range(50):
    apple = Apple('images/apple.png' , active_size )
    apple_group.add(apple)

# 创建玩家（农民）	
player = Farmer('images/farmer walk.png' , 96 , 96 , 8 , active_size )
# 将玩家序列图添加进组
player_group.add(player)

# 判断游戏是否结束
running = True
game_over = False

while running:
    clock.tick(30)

    # 获取当前时间
    ticks = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == QUIT :
            sys.exit()
            
    keys = pygame.key.get_pressed()
    if keys[K_UP] or keys[K_w]:
        player.move(0 , -1) # move()第一个参数为x的方向 1 为正，-1为负
    elif keys[K_DOWN] or keys[K_s]:
        player.move(0 , 1)
    elif keys[K_LEFT] or keys[K_a]:
        player.move(-1 , 0)
    elif keys[K_RIGHT] or keys[K_d]:
        player.move(1 , 0)
    else:
        # 如果未产生移动，则保持最后一帧不变
        player.frame = player.first_frame = player.last_frame 

    # 碰撞检测
    collide_list = pygame.sprite.spritecollide(player , apple_group ,\
                                                 True , pygame.sprite.collide_mask) # 碰撞则删除苹果组中的苹果
    if collide_list : # 计算能量/得分
        eat_apple_sound.play()
        player.energy += len(collide_list) * 2
        
    # 画背景
    screen.blit(background_image , (0 , 0))
    # 画苹果
    for each in apple_group:
            screen.blit(each.image, each.rect)

    # 让人物按照帧的位置更新        
    player_group.update(ticks , 50)
    player_group.draw(screen)
        
    # 画血条
    pygame.draw.rect(screen , (0 , 0 , 0) , \
                     (10 , 570 , 100 , 15) , 3 )
    energy_remain = player.energy / 100
    pygame.draw.rect(screen , (0 , 255 , 0) ,\
                     (10 , 570 , player.energy , 15))

    # 画分数
    score_text_image = score_font.render('Your Score : ' + str(player.energy) , True , (255 , 255 , 255))
    screen.blit(score_text_image , (640 , 570))

     # 判断得分是否足够，足够则结束游戏
    if player.energy == 100:
        win_sound.play()
        game_over = True
        running = False
        break
    
    pygame.display.update()
    
while game_over:
    for event in pygame.event.get():
        if event.type == QUIT :
            sys.exit()
        
    screen.blit(you_win_image , you_win_image_rect)
    running = False
    pygame.display.update()
    
