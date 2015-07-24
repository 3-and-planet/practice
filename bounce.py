from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        
        #6つの数をシャッフルし、取り出す
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3

        #キャンバスの高さを返す
        self.canvas_height = self.canvas.winfo_height()

        #キャンバスの幅を返す
        self.canvas_width = self.canvas.winfo_width()

        #底辺に当たった場合Trueを返す
        self.hit_bottom = False


    def hit_paddle(self, pos):
        paddle_pos =self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos [0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                #ラケットのスピードがボールに反映されるよう調整
                self.x += self.paddle.x
                self.score.hit()
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        #識別IDからキャンバス上の位置をxとyを組み合わせた座標で返す
        #今回は円の左上と右下の座標を返す[x1, y1, x2, y2]
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        #パドルに当たった場合は跳ね返す
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x =3
        if pos[2] >= self.canvas_width:
            self.x = -3


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        
        self.x = 0
        self.canvas_width =self.canvas.winfo_width()
        
        self.started = False

        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.start)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x =2

    def start(self, evt):
        self.started = True

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, fill=color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)



tk = Tk()
tk.title("Game")

#ウインドウサイズの固定
tk.resizable(0,0)

#一番前面に配置
tk.wm_attributes("-topmost", 1)

#bdとhighlightthicknessを0にし、キャンバスの外側線をなくす
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)

#キャンバス表示
canvas.pack()

#アニメーションを表示するために初期化（必須）
tk.update()

score =Score(canvas, 'green')
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

gameover = canvas.create_text(250, 200, text='Game Over!!!', font=('Helvetica',22), fill='red', state='hidden')

while True:
    if paddle.started == True and ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    if ball.hit_bottom == True:
        time.sleep(1)
        canvas.itemconfig(gameover, state='normal')
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)


