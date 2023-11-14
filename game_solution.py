from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk


# Define the class paddle
class Paddle:
	#initialise object
	def __init__(self, paddle_id, paddle_image):
		self.id = paddle_id
		self.image = paddle_image
		self.speed = 30


#define functions that move paddle left and right
def move_paddle_left(event,speed):
	print("moving left")
	canvas.move(paddle_id, -speed, 0)

def move_paddle_right(event, speed):
	print("moving right")
	canvas.move(paddle_id, speed, 0)


print("running")

window = Tk()
WIDTH = 1280
HEIGHT=720

window.geometry(f"{WIDTH}x{HEIGHT}")
window.title("Classic Brick Breaker")

canvas = Canvas(window,bg="black",width=WIDTH,height=HEIGHT)
canvas.pack()

paddle_image = Image.open("paddle.png")
paddle_image = paddle_image.resize((int(600/5), int(151/5)))
paddle_image = ImageTk.PhotoImage(paddle_image)
paddle_id = canvas.create_image(int(WIDTH/2),int(HEIGHT-paddle_image.height()), anchor="nw", image=paddle_image)
paddle = Paddle(paddle_id,paddle_image)

window.bind("<Left>", lambda event: move_paddle_left(event, paddle.speed))
window.bind("<Right>", lambda event: move_paddle_right(event, paddle.speed))




window.mainloop()