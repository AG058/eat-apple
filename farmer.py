import pygame

class Farmer(pygame.sprite.Sprite):
    def __init__(self , filename , width , height , columns , active_size):
        pygame.sprite.Sprite.__init__(self)
        # 保存序列图
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.master_image_rect = self.master_image.get_rect()
        # group.draw()用，表示相对于屏幕的位置，必须有
        self.rect = pygame.Rect(0 , 0 , width , height)
        # 每一帧的宽度和高度
        self.frame_width = width
        self.frame_height = height
        # 记录行数
        self.columns = columns
        # 纪录上一帧的时间，update中用
        self.last_time = 0
        # 记录最开始方向，人物朝下走，move中用
        self.direction = 0 , 1
        # 人物活动的区域
        self.active_size = active_size
        # 初始化人物的样子是朝下走
        self.first_frame = 4 * self.columns
        self.last_frame = 5 * self.columns - 1
        self.frame = self.first_frame

        # 初始化当前帧的位置，以及帧的遮罩，其中image group.draw()要求必须有，image、mask 碰撞遮罩检测必须有
        frame_x = (self.frame % self.columns) * self.frame_width
        frame_y = (self.frame // self.columns) * self.frame_height
        self.image = self.master_image.subsurface((frame_x , frame_y , self.frame_width ,\
                                                   self.frame_height))
        self.mask = pygame.mask.from_surface(self.image)
        # 初始化能量
        self.energy = 0
        
    def update(self , current_time , rate = 30):
        if current_time > self.last_time +rate:
            self.frame += 1
            if self.frame > self.last_frame :
                self.frame = self.first_frame
            if self.frame < self.first_frame :
                self.frame = self.first_frame
            self.last_time = current_time
            frame_x = (self.frame % self.columns) * self.frame_width # 计算当前帧的左上角位置
            frame_y = (self.frame // self.columns) * self.frame_height
            self.image = self.master_image.subsurface((frame_x , frame_y , self.frame_width ,\
                                                       self.frame_height)) # 位置为相对于序列图的位置
            
            self.mask = pygame.mask.from_surface(self.image)
            
    def move(self , direction_x , direction_y , speed = 5):
        if direction_x == 1:
            self.first_frame = 2 * self.columns
            self.last_frame = 3 * self.columns - 1
            self.rect.left += speed 
        if direction_x == -1 :
            self.first_frame = 6 * self.columns
            self.last_frame = 7 * self.columns - 1
            self.rect.left -= speed
        if direction_y == -1 :
            self.first_frame = 0 * self.columns
            self.last_frame = 1 * self.columns - 1
            self.rect.top -= speed
        if direction_y == 1 :
            self.first_frame = 4 * self.columns
            self.last_frame = 5 * self.columns - 1
            self.rect.top += speed

        # 边缘检测
        if self.rect.left <= 0 -35  :
            self.rect.left = 0 -35
        if self.rect.right>= self.active_size[0] +30  :
            self.rect.right = self.active_size[0] +30
        if self.rect.top <= -16  :
            self.rect.top = -16 
        if self.rect.bottom >= self.active_size[1] + 15 :
            self.rect.bottom = self.active_size[1] + 15

