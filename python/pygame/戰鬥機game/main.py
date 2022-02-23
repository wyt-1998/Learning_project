import pygame
import random
import os

FPS = 60  # frame per second:每秒顯示幀(ㄓㄥˋ)數
WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# 常數皆大寫 

# 遊戲初始化 and 創建視窗
pygame.init()   # 幫pygame的東東都做初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))    # 設定遊戲畫面(視窗)寬、高
pygame.display.set_caption("小遊戲")  # 視窗名稱
clock = pygame.time.Clock() # 創建管理與操控時間的物件


# 載入圖片--在載入圖片前，一定要先將pygame初始化，否則會出錯
# os.path : 檔案當前路徑(位置) -->較可以避免在不同作業系統時出錯
background_img = pygame.image.load(os.path.join("img", "background.png")).convert() 
# .convert():將圖片轉換成pygame較容易讀取的格式, 之後在畫到畫面上(畫面顯示 ↓↓)
player_img = pygame.image.load(os.path.join("img", "player.png")).convert() 
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert() 
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert() 


# Sprite:pygame內建的類別，可用來表示畫面上顯示的所有東西
# 玩家sprite:Player
class Player(pygame.sprite.Sprite):  # 創建類別Player，Player繼承類別Sprite
    def __init__(self):  # Player初始函式設定
        pygame.sprite.Sprite.__init__(self)  # copy類別Sprite的初始函式
        # 有兩個屬性:image和rect
        # image:表示顯示的圖片
        # rect:定位image
        '''
        # eg. 先不放圖片，自己製造一個綠色image ↓↓↓
        self.image = pygame.Surface((50, 40))  # 創建一個平面(surface), 寬:50、高:40
        self.image.fill(GREEN) # 將此平面填滿綠色 
        '''
        # 放入png檔    self.image = player_img
        # 調整圖片大小
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)  # set_colorkey((R, G, B))，將(R, G, B)變為透明
        self.rect = self.image.get_rect() # 定位image:將image(綠色平面)框起來
        self.radius = 23
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #用來檢查圈起來的範圍
        # 設定image的位置，(x, y)是以框框的左上角(topleft)點座標<--(因為python的原點(0, 0)在左上角)
        #self.rect.x = 200 
        #self.rect.y = 200
        #self.rect.center = (WIDTH/2, HEIGHT/2)  # 將image放在畫面正中央     
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 8  # 新增控制速度的屬性

    def update(self):
        """      
        self.rect.x += 2  # 讓物件向右移動
        if self.rect.left > WIDTH:  # 當物件左邊的座標值大於寬度(=物件完全離開畫面)
            self.rect.right = 0  # 物件的右邊座標設為0 => 物件的右邊回到畫面最左邊 
        # 因為迴圈繼續跑, x座標持續加2=> 物件從畫面左邊冒出來
        """
        key_pressed = pygame.key.get_pressed()  # 回傳一串Boolean值, 判斷鍵盤上按了哪些按鍵(按:TRUE, 沒按:FALSE)
        if key_pressed[pygame.K_RIGHT]:  # 是否按了右鍵  也可設定按d:key_pressed[pygame.K_d]
            self.rect.x += self.speed_x
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        # 不讓物件跑出畫面 ↓↓↓
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0        

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)  # 創建子彈(bullet)
        all_sprites.add(bullet)  # 將子彈(bullet)放進大群組(all_sprites)
        bullets.add(bullet)  # 將子彈(bullet)放進子彈群組(bullets)
# 石頭sprite:Rock
class Rock(pygame.sprite.Sprite):  # 創建類別Rock，Rock繼承類別Sprite
    def __init__(self):  # Rock初始函式設定
        pygame.sprite.Sprite.__init__(self)  # copy類別Sprite的初始函式
        # 有兩個屬性:image和rect
        # image:表示顯示的圖片
        # rect:定位image
        '''
        # eg. 先不放圖片，自己製造一個紅色image ↓↓↓
        self.image = pygame.Surface((30, 40))  # 創建一個平面(surface), 寬:30、高:40
        self.image.fill(RED) # 將此平面填滿紅色
        ''' # 放圖片 ↓↓↓ 
        ''' 
        self.image = rock_img
        self.image.set_colorkey(BLACK) # 將圖片中的黑色變為透明
        ''' # 為了解決旋轉後失真問題 ↓↓↓ 
        self.image_ori = rock_img  # 原始圖片(拿來旋轉)
        self.image_ori.set_colorkey(BLACK) # 去黑
        self.image = self.image_ori.copy() # 旋轉後圖片
        self.rect = self.image.get_rect() # 定位image:將image框起來
        self.radius = self.rect.width * 0.85 / 2
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # 用來檢查圈起來的範圍
        # 設定image的位置，(x, y)是以框框的左上角(topleft)點座標<--(因為python的原點(0, 0)在左上角)
        # 石頭是在頂部的隨機位置出現 ↓↓↓           self.rect.width:物件(石頭)的寬度
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) # randrange(a, b):隨機回傳a~b之間的值
        self.rect.y = random.randrange(-100, -40)
        #self.speed_y = 2  # 石頭掉落的垂直速度的屬性
        self.speed_y = random.randrange(2, 10)
        self.speed_x = random.randrange(-3, 3)  # 石頭掉落的水平速度的屬性
        self.total_degree = 0  # 物件旋轉角度
        self.rot_degree = random.randrange(-3, 3)  # 每次旋轉角度

    def rotate(self):  # 建立旋轉函式
        '''self.image = pygame.transform.rotate(self.image, self.rot_degree)
        # pygame內建的旋轉函式transform.rotate(要旋轉的物件, 旋轉角度) 
        '''  # 此函式每次旋轉後會失真，解決失真方式--新增屬性self.image_ori(↑↑)， ↓↓↓
        self.total_degree += self.rot_degree  # 物件每次旋轉3度
        self.total_degree %= 360  # 確保旋轉角度不會超過360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # 每次轉動都要重新定位，不然轉動會受限於原始定位 ↓↓↓
        center = self.rect.center  # 原中心位
        self.rect = self.image.get_rect()  # 重新定位
        self.rect.center = center  # 中心位不變

    def update(self):  # 因為FPS = 60，所以每秒update 60次
        self.rotate() # 在上方新增旋轉函式(↑↑)，並在此呼叫，每次更新時轉動石頭
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        """ 法一:自己寫得
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        """
        # 法二: 一碰到邊就重新跑random
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) # randrange(a, b):隨機回傳a~b之間的值
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(2, 10)  # 石頭掉落的垂直速度
            self.speed_x = random.randrange(-3, 3)  # 石頭掉落的水平速度
# 子彈sprite:Bullet
class Bullet(pygame.sprite.Sprite):  # 創建類別Bullet，Bullet繼承類別Sprite
    def __init__(self, x, y):  # Bullet初始函式設定     (x, y)是飛船(player玩家)的位置!!!!
        pygame.sprite.Sprite.__init__(self)  # copy類別Sprite的初始函式
        '''
        self.image = pygame.Surface((10, 20))  # 創建一個平面(surface), 寬:10、高:20
        self.image.fill(YELLOW) # 將此平面填滿黃色
        '''
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # 定位image:將image(黃色平面)框起來
        # 子彈的位置是在飛船頂部中間 ↓↓↓
        self.rect.centerx = x  # 子彈的中心x <- 傳進來的x
        self.rect.bottom = y  # 子彈的底部 <- 傳進來的y
        self.speed_y = -10  # 子彈向上發射的速度
        

    def update(self):
        self.rect.y += self.speed_y
        # 當子彈超出視窗時，將子彈刪除 ↓↓↓
        if self.rect.bottom < 0: 
            self.kill()  # Sprite中的函式，將此物件從所有含此物件的sprite群組中刪掉
        
# Sprite群組--一個sprite群組, 可以放很多sprite物件
all_sprites = pygame.sprite.Group()  # 創建一個sprite的大群組, 放所有sprite物件
rocks = pygame.sprite.Group()  # 放rock的群組
bullets = pygame.sprite.Group()  # 放bullet的群組

player = Player()  # 創建一個sprite物件:player
all_sprites.add(player)  # 將player放進sprite群組中-->去畫面顯示(↓↓)中畫出來
#rock = Rock() # 創建一顆石頭(sprite物件)
#all_sprites.add(rock)  # 將rock放進sprite群組中-->去畫面顯示(↓↓)中畫出來
for i in range(8): # 隨機產生8顆石頭
    r = Rock()
    all_sprites.add(r)
    rocks.add(r) # 將石頭(r)放進石頭群組(rocks)


# 遊戲迴圈
running = True
while running: 
    clock.tick(FPS)  # 一秒內最多只能被執行(FPS)次, 提高遊戲體驗的公平性(避免因電腦狀況好壞而一秒內多跑、少跑了幾次while迴圈)
    # 取得輸入
    for event in pygame.event.get():    # pygame.event.get():回傳包含所有現在發生的事件的list  (ex.滑鼠滑到哪, 鍵盤按了甚麼按鍵)
        # 用for迴圈將列表中的事件逐個檢查
        if event.type == pygame.QUIT:   # 若事件類型是滑鼠點叉叉(關閉遊戲)
            running = False # 跳出while迴圈--> 迴圈外寫pygame.quit(),遊戲結束
        elif event.type == pygame.KEYDOWN:  # 若事件類型是按鍵盤鍵
                if event.key == pygame.K_SPACE:  # 若按空白建(space)
                    player.shoot()  # 射擊子彈 : 呼叫飛船的函式(↑↑)  <-- 在class Player中新增shoot函式



    # 更新遊戲
    # 讓image動起來 ↓↓↓
    all_sprites.update()  # 執行大群組(all_sprites)中每個物件的update函式-->在類別(↑↑)中新增update()函式
# 更新完所有物件後
# (1)判斷石頭和子彈是否碰撞: 若碰撞，子彈和石頭一起消失
    # pygame.sprite.groupcollide(群組a, 群組b, 若a和b碰撞,群組a之碰撞物件是否刪除, 若a和b碰撞,群組b之碰撞物件是否刪除)
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)  # 此函數會回傳一個字典(dic)
    # 石頭和子彈碰撞後消失，不同時新增的話，石頭會不夠，為了永遠保持8顆，每碰撞一次就要新增一個石頭
    for hit in hits:
        # 新增石頭
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
 # (2)判斷石頭和飛船是否碰撞: 若碰撞，遊戲結束
    # pygame.sprite.spritecollide(物件a, 群組b, 若a和b之物件碰撞,群組b之碰撞物件是否刪除)
    ''' hits = pygame.sprite.spritecollide(player, rocks, False) ''' # 回傳一個列表(list)
    # 但spritecollide碰撞判斷預設為為矩形碰撞判斷，因此判斷較不精準，有時物件本身看起來並未相撞(是框住物件的矩形互撞了)
    # 因此改為圓形碰撞判斷較精準，但圓形碰撞判斷的缺點是運算較複雜--較耗時
    # 修改為圓形碰撞判斷:spritecollide的第四個參數 ↓↓↓
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle) 
    # 因為改為圓形，所以要給player類別和rock類別新增radius屬性 (↑↑)
    # pygame.sprite.collide_circle:以物件中心點, 半徑(self.radius)畫一個圓框起物件
    if hits:
        running = False
        


    # 畫面顯示
    screen.fill(BLACK)  # 遊戲視窗填滿白色, (R, G, B):每個元素range:0~255
    screen.blit(background_img, (0, 0)) # 畫圖:screen.blit(要畫的圖, 畫圖的起始座標:圖的topleft)
    all_sprites.draw(screen) # 將群組內的物件都畫到視窗中
    pygame.display.update()  # 更新畫面，才會顯示


pygame.quit()
