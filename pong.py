import turtle
import os
import winsound
import sys

wn = turtle.Screen()

canvas = wn.getcanvas()
root = canvas.winfo_toplevel()

wn.title("Pong Game")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Game coords
paddle_edge_y_top = 260
paddle_edge_y_bottom = -260
ball_edge_y_top = 290
ball_edge_y_bottom = -290
ball_edge_x_left = 390
ball_edge_x_right = -390
ball_edge_on_paddle_x_left = 330
ball_edge_on_paddle_x_right = -330

# Sounds
pong_blip = "pong_blip.wav"
pong_blip_for_linux = "aplay pong_blip.wav&"
pong_blip_for_mac = "afplay pong_blip.wav&"

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("blue")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("red")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = 0.1

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: {}  Player B: {}".format(score_a, score_b),
          align="center", font=("Courier", 24, "normal"))

# Functions

# Move paddles up and down the board
def paddle_a_up():
    if paddle_a.ycor() < paddle_edge_y_top:
        paddle_a.sety(paddle_a.ycor() + 20)


def paddle_a_down():
    if paddle_a.ycor() > paddle_edge_y_bottom:
        paddle_a.sety(paddle_a.ycor() - 20)


def paddle_b_up():
    if paddle_b.ycor() < paddle_edge_y_top:
        paddle_b.sety(paddle_b.ycor() + 20)


def paddle_b_down():
    if paddle_b.ycor() > paddle_edge_y_bottom:
        paddle_b.sety(paddle_b.ycor() - 20)


# Play sound based on OS
def play_pong_blip():
    if sys.platform.startswith("win32"):
        winsound.PlaySound(pong_blip, winsound.SND_ASYNC)
    if sys.platform.startswith('linux'):
        os.system(pong_blip_for_linux)
    if sys.platform.startswith('darwin'):
        os.system(pong_blip_for_mac)

# Game loop
def game_loop():
    global score_a, score_b

    # Move the ball
    ball.setposition(ball.xcor() + ball.dx, ball.ycor() + ball.dy)

    # Border checking

    # Board is 800x and 600y. Ball is 20x and 20y.
    if ball.ycor() > ball_edge_y_top:
        ball.sety(ball_edge_y_top)
        ball.dy *= -1
        play_pong_blip()

    if ball.ycor() < ball_edge_y_bottom:
        ball.sety(ball_edge_y_bottom)
        ball.dy *= -1
        play_pong_blip()

    if ball.xcor() > ball_edge_x_left or ball.xcor() < ball_edge_x_right:
        if ball.xcor() > ball_edge_x_left:
            score_a += 1
        if ball.xcor() < ball_edge_x_right:
            score_b += 1
        ball.goto(0, 0)
        ball.dx *= -1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b),
                  align="center", font=("Courier", 24, "normal"))

    # Paddle and ball collisions
    if ball.xcor() > ball_edge_on_paddle_x_left and ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40:
        ball.setx(ball_edge_on_paddle_x_left)
        ball.dx *= -1
        play_pong_blip()

    if ball.xcor() < ball_edge_on_paddle_x_right and ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40:
        ball.setx(ball_edge_on_paddle_x_right)
        ball.dx *= -1
        play_pong_blip()

    wn.update()

    wn.ontimer(game_loop)


# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

game_loop()

wn.mainloop()
