# -*- coding:utf-8 -*-

from tkinter import *
import random
import time


#座標を記録するクラス
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
#横方向の衝突を調べる
def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2)\
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2)\
            or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
        return True
    else:
        return False

#縦方向の衝突を調べる
def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2)\
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2)\
            or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else:
        return False


#衝突検出
def collided_left(co1, co2):
     if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
              return True
        return False

def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        #床から落ちることもあるためこれから床と衝突するかをチェックする
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False


#ゲームの親クラスを定義する
class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    #特に何もしない関数を定義することでSpriteを親に持つクラスはエラーなくmove関数を呼べる
    def move(self):
        pass
    def coords(self):
        return self.coordinates

#床のクラスを定義する
class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

#スティックマンを定義する
class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        #画像をあらかじめ読み込んでおくことで、都度読み込みを不要とする
        self.images_left = [
            PhotoImage(file="figure-L1.gif"),
            PhotoImage(file="figure-L2.gif"),
            PhotoImage(file="figure-L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="figure-R1.gif"),
            PhotoImage(file="figure-R2.gif"),
            PhotoImage(file="figure-R3.gif")
        ]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')

        #スティックマンを動かす時に使う変数
        self.x = -2
        self.y = 0

        #スティックマン画像のインデックス値
        self.current_image = 0
        self.current_image_add = 1

        #ジャンプ中に使うカウンター
        self.jump_count = 0

        #最後に画像を変更した時刻
        self.last_time = time.time()
        
        #Coordsクラスのオブジェクトを初期化状態でセット
        self.coordinates = Coords()

        #キーが押されたときの挙動
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    #ジャンプしていなければ方向を変更する
    #evtオブジェクトは今回使用しないが、引数で渡さないとエラーになるため記載
    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            #永久に上へ移動することを禁止するためにカウントを0へ
            self.jump_count = 0


    #動きに応じて画像を変更する
    def animate(self):
        if self.x != 0 and self.y ==0 :
            #画像を切り替えるタイミングを調節
            if time.time() - self.last_time >0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1        
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y !=0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    
    #スティックマンの現在位置を示す
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0]+27
        self.coordinates.y2 = xy[1]+30
        return self.coordinates

    #スティックマンを動かす
    def move(self):
        self.animate()
        #yが負ならジャンプ中
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1

        #位置のチェックと変数初期化
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        #キャンバス左端および右端の衝突チェック
        #これ以上チェックする必要がなければFalseをセット
        if self.y > 0 and co.y2 >=self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y <0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        #1つずつ他のスプライトとの衝突チェック
        for sprite in self.game.sprites:
            #自分自身との衝突はチェックしない
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y <0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                #床の上部に着地するために落下するピクセル数
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y =0
                bottom = False
                top = False
            if bottom and falling and self.y == 0\
                    and co.y2 < self.game.canvas_height\
                    and collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.end(sprite)
            if right and self.x >0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.end(sprite)

        #衝突が検出されず、キャンバスの底辺より上にいる場合落下させる
        if falling and bottom and self.y ==0 \
                and co.y2 < self.game.canvas_height:
            self.y = 4
        #xとyに基づいて画像を動かす
        self.game.canvas.move(self.image, self.x, self.y)

    def end(self, sprite):
        self.game.running = False
        sprite.opendoor()
        time.sleep(1)
        #スティックマンを消す
        self.game.canvas.itemconfig(self.image, state='hidden')
        sprite.closedoor()


class DoorSprite(Sprite):
    def __init__(self, game, x, y, width, height):
        Sprite.__init__(self, game)
        self.closed_door = PhotoImage(file="door1.gif")
        self.opened_door = PhotoImage(file="door2.gif")
        self.image = game.canvas.create_image(x, y, image=self.closed_door, anchor='nw')
        #ドアの正面でスティックマンを止まらせるためにx2座標は幅の半分とする
        self.coordinates = Coords(x, y, x + (width /2), y + height)
        #スティックマンがドアにたどり着いたらゲーム終了
        self.endgame = True

    def opendoor(self):
        self.game.canvas.itemconfig(self.image, image=self.opened_door)
        self.game.tk.update_idletasks()

    def closedoor(self):
        self.game.canvas.itemconfig(self.image, image=self.closed_door)
        self.game.tk.update_idletasks()

class Game:
    def __init__(self):

        self.tk = Tk()
        self.tk.title("Stick Man Races for the Exit")
        #ウインドウサイズ固定
        self.tk.resizable(0,0)
        #ウインドウが手前に来るように指定
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500

        self.bg1 = PhotoImage(file="background1.gif")
        self.bg2 = PhotoImage(file="background2.gif")
        #self.bg_shelf = PhotoImage(file="shelf.gif")
        #self.bg_lamp = PhotoImage(file="lamp.gif")
        w = self.bg1.width()
        h = self.bg1.height()
        draw_bg = 0
        #count = 0
        #100ピクセルの画像で背景を埋める
        for x in range(0, 5):
            for y in range(0, 5):
                if draw_bg == 1:
                    self.canvas.create_image(x*w, y*h, image=self.bg1, anchor='nw')
                    draw_bg = 0
                else:
                    #count = count +1
                    #if count == 5:
                    #    self.canvas.create_image(x*w, y*h, image=self.bg_shelf, anchor='nw')
                    #elif coount == 9:
                    #    self.canvas.create_image(x*w, y*h, image=self.bg_lamp, anchor='nw')
                    #else:
                    self.canvas.create_image(x*w, y*h, image=self.bg2, anchor='nw')
                    draw_bg = 1

        self.sprites = []
        self.running = True
        self.you_win_text = self.canvas.create_text(250,250,text='YOU WIN!!!!', state='hidden')

    def mainloop(self):
        #ウインドウが閉じるまでwhileループ
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            else:
                time.sleep(1)
                self.canvas.itemconfig(self.you_win_text, state = 'normal')
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


g = Game()
platform1 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 175, 350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 45, 60, 100, 10)
platform9 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 230, 200, 32, 10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

door = DoorSprite(g, 45, 30, 40, 35)
g.sprites.append(door)

sf = StickFigureSprite(g)
g.sprites.append(sf)

g.mainloop()

