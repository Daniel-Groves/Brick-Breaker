from tkinter import Tk, Canvas, PhotoImage
import math
from PIL import Image, ImageTk


# Define the class paddle
class Paddle:
	#initialise object
	def __init__(self, paddle_id, paddle_image):
		self.id = paddle_id
		self.image = paddle_image
		self.speed = 30

	#Moves paddle left and right with respective button press
	def move_left(self,event):
		if ball.fired:
			canvas.move(paddle_id, -self.speed, 0)

	def move_right(self,event):
		if ball.fired:
			canvas.move(paddle_id, self.speed, 0)



#Define the brick class
class Brick:
	#initialise object
	def __init__(self, x, y, image, cracked_image):
		self.image = image
		self.cracked_image = cracked_image	
		self.id = canvas.create_image(x,y, anchor="nw", image=self.image)
		self.topright = [x,y]

	def crack(self):
		#Turns brick into cracked version
		canvas.itemconfig(self.id, image=self.cracked_image)

	def collision(self, ball):
		# Checks to see if a ball collides with brick
		x_ball_center, y_ball_center = canvas.coords(ball.id)
		x_brick_left, y_brick_top, x_brick_right, y_brick_bottom = canvas.bbox(self.id)

		ball_radius = (ball.image).width() / 2

		# Checks if the ball is within the bounds of the brick
		if (x_brick_left - ball_radius < x_ball_center < x_brick_right + ball_radius) and (y_brick_top - ball_radius < y_ball_center < y_brick_bottom + ball_radius):

			#Works out the overlap of the ball
			x_overlap = min(x_ball_center - (x_brick_left - ball_radius), (x_brick_right + ball_radius) - x_ball_center)
			y_overlap = min(y_ball_center - (y_brick_top - ball_radius), (y_brick_bottom + ball_radius) - y_ball_center)

			#Uses overlap to work out which side of the brick the ball collides with
			if x_overlap < y_overlap:
				if x_ball_center < (x_brick_left + x_brick_right) / 2:
					return "left"
				else:
					return "right"
			else:
				if y_ball_center < (y_brick_top + y_brick_bottom) / 2:
					return "top"
				else:
					return "bottom"

		return None

#Child class for grey brick
class GreyBrick(Brick):
	def __init__(self, x, y):
		super().__init__(x, y, grey_brick_image, grey_brick_cracked_image)
		self.image = grey_brick_image 
		self.cracked_image = grey_brick_cracked_image
		#Creates co-ordinates of top left and bottom right for collision detection purposes
		self.top_left = [x,y]
		self.bottom_right = [x+BRICK_WIDTH,y-BRICK_HEIGHT]	

class Ball:
	def __init__(self, ball_id, ball_image):
		self.id = ball_id
		self.image = ball_image
		self.speed = 3
		self.x_velocity = 0
		self.y_velocity = 0
		self.fired = False

	def fire(self,x,y,):
		if not self.fired:
			#Work out the vectors of the click

			x_vector = canvas.coords(ball.id)[0] - x
			y_vector = canvas.coords(ball.id)[1] - y

			print(canvas.coords(ball.id))
			print(f"fired at {x},{y}")
			print(x_vector,y_vector)
			#Set fired to True as can only fire once
			self.fired = True

			#Work out respective x and y velocities
			
			theta = abs(math.atan(y_vector/x_vector))
			print(theta)

			self.x_velocity = -x_vector
			self.y_velocity = -y_vector

			scale_factor = self.speed**2/(self.x_velocity**2 + self.y_velocity**2)

			self.x_velocity = self.x_velocity * math.sqrt(scale_factor)
			self.y_velocity = self.y_velocity * math.sqrt(scale_factor)

	def move(self):
		#Moves the ball according to the current velocities
		canvas.move(self.id, self.x_velocity, self.y_velocity)

	def update_velocity(self,side):
		#Updates the velocity of the ball depending on collisions
		if side == "top" or side == "bottom":
			self.y_velocity = -self.y_velocity
		else:
			self.x_velocity = -self.x_velocity

	def wall_collisions(self):
		#checks for collisions with walls and updates velocity appropriately
		if canvas.coords(ball.id)[0] < (ball_image.width()/2 + 2) or canvas.coords(ball.id)[0] > (WIDTH - ball_image.width()/2 - 2):
			self.x_velocity = -self.x_velocity
		elif canvas.coords(ball.id)[1] < (ball_image.height()/2 + 2) or canvas.coords(ball.id)[1] > (HEIGHT - ball_image.width()/2 - 2):
			self.y_velocity = -self.y_velocity


def update_game():
	#Updates the game to move the ball
	ball.move()
	for item in balls:
		for brick in bricks:
			side = brick.collision(ball)
			if side != None:
				print(side)
				ball.update_velocity(side)
				break
		ball.wall_collisions()

				


	window.after(2, update_game)

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
paddle_image = paddle_image.resize((154, 41))
paddle_image = ImageTk.PhotoImage(paddle_image)
paddle_id = canvas.create_image(int(WIDTH/2),int(HEIGHT)-5, anchor="s", image=paddle_image)
paddle = Paddle(paddle_id,paddle_image)

ball_image = Image.open("ball.png")
ball_image = ball_image.resize((int(73/1.5), int(72//1.5)))
ball_image = ImageTk.PhotoImage(ball_image)
ball_id = canvas.create_image(int(WIDTH/2),int(HEIGHT-paddle_image.height()-5-(ball_image.width()/2)), anchor="center", image=ball_image)
ball = Ball(ball_id, ball_image)

balls = []
balls.append(ball)

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
window.bind("<Left>", lambda event: paddle.move_left(event))
window.bind("<Right>", lambda event: paddle.move_right(event))

#Bind left click to fire the ball initially
window.bind("<Button-1>", lambda event: ball.fire(event.x,event.y))

update_game()

window.mainloop()