import turtle

wn = turtle.Screen()
wn.title("Pong by czx")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# score
Score_A = 0
Score_B = 0

# Paddle A
paddle_A = turtle.Turtle()
paddle_A.speed(0)
paddle_A.shape("square")
paddle_A.color("white")
paddle_A.shapesize(stretch_wid=5, stretch_len=1)
paddle_A.penup()
paddle_A.goto(-350, 0)

# Paddle B
paddle_B = turtle.Turtle()
paddle_B.speed(0)
paddle_B.shape("square")
paddle_B.color("white")
paddle_B.shapesize(stretch_wid=5, stretch_len=1)
paddle_B.penup()
paddle_B.goto(350, 0)

# Ball
Ball = turtle.Turtle()
Ball.speed(0)
Ball.shape("square")
Ball.color("white")
Ball.penup()
Ball.goto(0, 0)
# Ball movement
Ball.dx = 0.2
Ball.dy = 0.2

# Pen
Pen = turtle.Turtle()
Pen.speed(0)
Pen.color("white")
Pen.penup()
Pen.hideturtle()
Pen.goto(0, 260)
Pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))


# function
def paddle_A_up():
    if paddle_A.ycor() < 250:
        y = paddle_A.ycor()
        y += 25
        paddle_A.sety(y)


def paddle_A_down():
    if paddle_A.ycor() > -250:
        y = paddle_A.ycor()
        y -= 25
        paddle_A.sety(y)

def paddle_B_up():
    if paddle_B.ycor() < 250:
        y = paddle_B.ycor()
        y += 25
        paddle_B.sety(y)

def paddle_B_down():
    if paddle_B.ycor() > -250:
        y = paddle_B.ycor()
        y -= 25
        paddle_B.sety(y)

# keyboard binding
wn.listen()
wn.onkeypress(paddle_A_up, "w")
wn.onkeypress(paddle_A_down, "s")
wn.onkeypress(paddle_B_up, "Up")
wn.onkeypress(paddle_B_down, "Down")

#main game loop
while True:
    wn.update()

    # move the ball
    Ball.setx(Ball.xcor() + Ball.dx)
    Ball.sety(Ball.ycor() + Ball.dy)

    # border checking
    if Ball.ycor() > 290:
        Ball.sety(290)
        Ball.dy *= -1

    if Ball.ycor() < -290:
        Ball.sety(-290)
        Ball.dy *= -1

    if Ball.xcor() > 390:
        Ball.goto(0, 0)
        Ball.dx *= -1
        Score_A += 1
        Pen.clear()
        Pen.write("Player A: {}  Player B: {}".format(Score_A, Score_B), align="center", font=("Courier", 24, "normal"))

    if Ball.xcor() < -390:
        Ball.goto(0, 0)
        Ball.dx *= -1
        Score_B += 1
        Pen.clear()
        Pen.write("Player A: {}  Player B: {}".format(Score_A, Score_B), align="center", font=("Courier", 24, "normal"))

    # paddle and ball collision
    if (Ball.xcor() > 340 and Ball.xcor() < 350) and (Ball.ycor() < paddle_B.ycor() + 50 and Ball.ycor() > paddle_B.ycor() - 50):
        Ball.setx(340)
        Ball.dx *= -1

    if (Ball.xcor() < -340 and Ball.xcor() > -350) and (Ball.ycor() < paddle_A.ycor() + 50 and Ball.ycor() > paddle_A.ycor() - 50):
        Ball.setx(-340)
        Ball.dx *= -1