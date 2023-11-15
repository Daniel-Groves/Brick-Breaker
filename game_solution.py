from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk


# Define the class paddle
class Paddle:
	#initialise object
	def __init__(self, paddle_id, paddle_image):
		self.id = paddle_id
		self.image = paddle_image
		self.speed = 30

#Define the brick class
class Brick:
	#initialise object
	def __init__(self, x, y, image, cracked_image):
		self.image = image
		self.cracked_image = cracked_image	
		self.id = canvas.create_image(x,y, anchor="nw", image=self.image)

	def crack(self):
		#Turns brick into cracked version
		canvas.itemconfig(self.id, image=self.cracked_image)

#Child class for grey brick
class GreyBrick(Brick):
	def __init__(self, x, y):
		super().__init__(x, y, grey_brick_image, grey_brick_cracked_image)
		self.image = grey_brick_image 
		self.cracked_image = grey_brick_cracked_image		

#define functions that move paddle left and right
def move_paddle_left(event,speed):
	print("moving left")
	canvas.move(paddle_id, -speed, 0)

def move_paddle_right(event, speed):
	print("moving right")
	canvas.move(paddle_id, speed, 0)

#Initialise window
window = Tk()

#Change desired width and height here
WIDTH = 1280
HEIGHT=720


window.geometry(f"{WIDTH}x{HEIGHT}")
window.title("Classic Brick Breaker")

#Create canvas on window
canvas = Canvas(window,bg="black",width=WIDTH,height=HEIGHT)
canvas.pack()

#Load paddle image and resize using PIL
paddle_image = Image.open("paddle.png")
paddle_image = paddle_image.resize((int(600/5), int(151/5)))
paddle_image = ImageTk.PhotoImage(paddle_image)
paddle_id = canvas.create_image(int(WIDTH/2),int(HEIGHT-paddle_image.height()), anchor="nw", image=paddle_image)
paddle = Paddle(paddle_id,paddle_image)


BRICKS_PER_ROW = 10
BRICK_WIDTH = WIDTH // BRICKS_PER_ROW
BRICK_HEIGHT = int(BRICK_WIDTH * (57 / 170))

NUMBER_OF_ROWS = 5

#Load and resize grey_brick_image
grey_brick_image = Image.open("grey_brick.png")
grey_brick_image = grey_brick_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
grey_brick_image = ImageTk.PhotoImage(grey_brick_image)

#Load and resize grey_brick_cracked_image
grey_brick_cracked_image = Image.open("grey_brick_cracked.png")
grey_brick_cracked_image = grey_brick_cracked_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
grey_brick_cracked_image = ImageTk.PhotoImage(grey_brick_cracked_image)

bricks = []

#Loop to place bricks
for row in range(NUMBER_OF_ROWS):
	for brick in range(BRICKS_PER_ROW):
		new_brick = GreyBrick(brick*BRICK_WIDTH,row*BRICK_HEIGHT)
		bricks.append(new_brick)


# grey_brick_id = canvas.create_image(0,0, anchor="nw", image=grey_brick_image)

#Bind left and right keys to move paddle
window.bind("<Left>", lambda event: move_paddle_left(event, paddle.speed))
window.bind("<Right>", lambda event: move_paddle_right(event, paddle.speed))




window.mainloop()