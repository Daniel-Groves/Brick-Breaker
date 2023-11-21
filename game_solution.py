from tkinter import Tk, Canvas, PhotoImage, Label, Button, Entry
import math
from PIL import Image, ImageTk


# Define the class paddle
class Paddle:
	#initialise object
	def __init__(self, paddle_id, paddle_image):
		self.id = paddle_id
		self.image = paddle_image
		self.speed = 60

	#Moves paddle left and right with respective button press
	def move_left(self,event):
		if ball.fired:
			game.move(self.id, -self.speed, 0)

	def move_right(self,event):
		if ball.fired:
			game.move(self.id, self.speed, 0)

	def collision(self, ball):
		# Note this code is very similar to the respective method for bricks, so this should be made more concise in the future
		# Checks to see if a ball collides with paddle

		#Gets ball coordinates, if the ball is still present
		if game.coords(ball.id):
			x_ball_center, y_ball_center = game.coords(ball.id)
			x_paddle_left, y_paddle_top, x_paddle_right, y_paddle_bottom = game.bbox(self.id)
			ball_radius = (ball.image).width() / 2

			if (x_paddle_left - ball_radius < x_ball_center < x_paddle_right + ball_radius) and (y_paddle_top - ball_radius < y_ball_center < y_paddle_bottom + ball_radius):

				#Works out the overlap of the ball
				x_overlap = min(x_ball_center - (x_paddle_left - ball_radius), (x_paddle_right + ball_radius) - x_ball_center)
				y_overlap = min(y_ball_center - (y_paddle_top - ball_radius), (y_paddle_bottom + ball_radius) - y_ball_center)

				#Uses overlap to work out which side of the paddle the ball collides with (should mostly be top) but check for all incase of edge cases
				relative_collision_point = None
				if x_overlap < y_overlap:
					if x_ball_center < (x_paddle_left + x_paddle_right) / 2:
						return "left", relative_collision_point
					else:
						return "right", relative_collision_point
				else:
					if y_ball_center < (y_paddle_top + y_paddle_bottom) / 2:

						#Work out the relative position of the ball from the center of the paddle from 0-1
						collision_point = game.coords(ball.id)[0] - game.coords(paddle.id)[0]
						relative_collision_point = collision_point/((x_paddle_left-x_paddle_right)/2)
						print(relative_collision_point)
						return "top", relative_collision_point
					else:
						return "bottom", relative_collision_point
		return None, None
	
	def get_coords(self):
		return game.coords(self.id)

#Define the brick class
class Brick:
	#initialise object
	def __init__(self, x, y, image, cracked_image):
		self.x = x
		self.y = y
		self.image = image
		self.cracked_image = cracked_image	
		self.id = game.create_image(x,y, anchor="nw", image=self.image)
		self.topright = [x,y]
		self.cracked = False

	def crack(self):
		global score
		#Turns brick into cracked version or breaks
		if not self.cracked:
			#If a brick is cracked, add 1 to score
			game.itemconfig(self.id, image=self.cracked_image)
			self.cracked = True
			score += 1

		else:
			#If a brick is broken, add 2 to score
			score += 2
			bricks.remove(self)
			game.delete(self.id)
			del self
			
	def has_brick_on_side(self, side):
		# Check if there is a brick on the specified side
		x, y = self.x, self.y
		if side == "left":
			for brick in bricks:
				if brick != self and brick.x + BRICK_WIDTH == x and brick.y == y:
					return True
		elif side == "right":
			for brick in bricks:
				if brick != self and brick.x - BRICK_WIDTH == x and brick.y == y:
					return True
		elif side == "top":
			for brick in bricks:
				if brick != self and brick.x == x and brick.y + BRICK_HEIGHT == y:
					return True
		elif side == "bottom":
			for brick in bricks:
				if brick != self and brick.x == x and brick.y - BRICK_HEIGHT == y:
					return True
		return False

	def collision(self, ball):
		# Checks to see if a ball collides with brick
		x_ball_center, y_ball_center = game.coords(ball.id)
		x_brick_left, y_brick_top, x_brick_right, y_brick_bottom = game.bbox(self.id)

		ball_radius = (ball.image).width() / 2

		# Checks if the ball is within the bounds of the brick
		if (x_brick_left - ball_radius < x_ball_center < x_brick_right + ball_radius) and (y_brick_top - ball_radius < y_ball_center < y_brick_bottom + ball_radius):

			#Works out the overlap of the ball
			x_overlap = min(x_ball_center - (x_brick_left - ball_radius), (x_brick_right + ball_radius) - x_ball_center)
			y_overlap = min(y_ball_center - (y_brick_top - ball_radius), (y_brick_bottom + ball_radius) - y_ball_center)

			#Uses overlap to work out which side of the brick the ball collides with
			#Don't bother returning anything if a collision is detected on a side where there is already a brick
			#This only happens when the game thinks a ball collides with two bricks and can cause issues
			if x_overlap < y_overlap:
				if x_ball_center < (x_brick_left + x_brick_right) / 2 and not self.has_brick_on_side("left"):
					return "left"
				elif x_ball_center >= (x_brick_left + x_brick_right) / 2 and not self.has_brick_on_side("right"):
					return "right"
			else:
				if y_ball_center < (y_brick_top + y_brick_bottom) / 2 and not self.has_brick_on_side("top"):
					return "top"
				elif y_ball_center >= (y_brick_top + y_brick_bottom) / 2 and not self.has_brick_on_side("bottom"):
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

class BlueBrick(Brick):
	def __init__(self, x, y):
		super().__init__(x, y, blue_brick_image, blue_brick_cracked_image)
		self.image = blue_brick_image 
		self.cracked_image = blue_brick_cracked_image
		#Creates co-ordinates of top left and bottom right for collision detection purposes
		self.top_left = [x,y]
		self.bottom_right = [x+BRICK_WIDTH,y-BRICK_HEIGHT]

class LightBlueBrick(Brick):
	def __init__(self, x, y):
		super().__init__(x, y, light_blue_brick_image, light_blue_brick_cracked_image)
		self.image = light_blue_brick_image 
		self.cracked_image = light_blue_brick_cracked_image
		#Creates co-ordinates of top left and bottom right for collision detection purposes
		self.top_left = [x,y]
		self.bottom_right = [x+BRICK_WIDTH,y-BRICK_HEIGHT]

class UnbreakableBrick(Brick):
	def __init__(self, x, y, color):
		super().__init__(x, y, None, None)  # No images for unbreakable brick
		self.color = color
		self.id = game.create_rectangle(x, y, x + BRICK_WIDTH - 1, y + BRICK_HEIGHT - 1, fill=color)
		# Creates coordinates of top left and bottom right for collision detection purposes
		self.top_left = [x, y]
		self.bottom_right = [x + BRICK_WIDTH, y - BRICK_HEIGHT]
	def crack(self):
		# Unbreakable brick cannot be cracked, so do nothing
		pass
	def collision(self, ball):
		# Checks to see if a ball collides with brick
		x_ball_center, y_ball_center = game.coords(ball.id)
		x_brick_left, y_brick_top, x_brick_right, y_brick_bottom = self.x,self.y,(self.x + BRICK_WIDTH - 1), (self.	y + BRICK_HEIGHT - 1)

		ball_radius = (ball.image).width() / 2

		# Checks if the ball is within the bounds of the brick
		if (x_brick_left - 1 - ball_radius < x_ball_center < x_brick_right + ball_radius + 1) and (y_brick_top - ball_radius < y_ball_center< y_brick_bottom + ball_radius):

			#Works out the overlap of the ball
			x_overlap = min(x_ball_center - (x_brick_left - ball_radius), (x_brick_right + ball_radius) - x_ball_center)
			y_overlap = min(y_ball_center - (y_brick_top - ball_radius), (y_brick_bottom + ball_radius) - y_ball_center)

			#Uses overlap to work out which side of the brick the ball collides with
			#Don't bother returning anything if a collision is detected on a side where there is already a brick
			#This only happens when the game thinks a ball collides with two bricks and can cause issues
			if x_overlap < y_overlap:
				if x_ball_center < (x_brick_left + x_brick_right) / 2 and not self.has_brick_on_side("left"):
					return "left"
				elif x_ball_center >= (x_brick_left + x_brick_right) / 2 and not self.has_brick_on_side("right"):
					return "right"
			else:
				if y_ball_center < (y_brick_top + y_brick_bottom) / 2 and not self.has_brick_on_side("top"):
					return "top"
				elif y_ball_center >= (y_brick_top + y_brick_bottom) / 2 and not self.has_brick_on_side("bottom"):
					return "bottom"

		return None

class Ball:
	def __init__(self, ball_id, ball_image):
		self.id = ball_id
		self.image = ball_image
		self.speed = 9
		self.x_velocity = 0
		self.y_velocity = 0
		self.fired = False

	def fire(self,x,y):
		if not self.fired:
			#Work out the vectors of the click

			x_vector = game.coords(ball.id)[0] - x
			y_vector = game.coords(ball.id)[1] - y

			#Set fired to True as can only fire once
			self.fired = True

			#Work out respective x and y velocities
			self.x_velocity = -x_vector
			self.y_velocity = -y_vector

			scale_factor = self.speed**2/(self.x_velocity**2 + self.y_velocity**2)

			self.x_velocity = self.x_velocity * math.sqrt(scale_factor)
			self.y_velocity = self.y_velocity * math.sqrt(scale_factor)

	def move(self):
		#Moves the ball according to the current velocities
		game.move(self.id, self.x_velocity, self.y_velocity)

	def update_velocity(self,side,relative_collision_point=None):
		#Updates the velocity of the ball depending on collisions
		if relative_collision_point:
			#If there is a relative_collision_point (i.e. we are passing in one, as it is a paddle deflecction)
			if side == "top" or side == "bottom":
				#Turn the relative_collision_point from 0-1 to an angle from 0-60 relative to normal
				deflection_angle = 60 * relative_collision_point
				#Scale the x and y velocity according to that deflection angle
				self.y_velocity = int(-self.speed * math.cos(math.radians(deflection_angle)))
				self.x_velocity = int(-self.speed * math.sin(math.radians(deflection_angle)))
			else:
				self.x_velocity = -self.x_velocity
		else:
			if side == "top" or side == "bottom":
				self.y_velocity = -self.y_velocity
			else:
				self.x_velocity = -self.x_velocity

	def wall_collisions(self, ball):
		#checks for collisions with walls and updates velocity appropriately
		if game.coords(ball.id)[0] < (ball.image.width()/2 + 2) or game.coords(ball.id)[0] > (WIDTH - ball.image.width()/2 - 2):
			self.x_velocity = -self.x_velocity
		elif game.coords(ball.id)[1] < (ball.image.height()/2 + 2):
			self.y_velocity = -self.y_velocity
		elif game.coords(ball.id)[1] > (HEIGHT - ball.image.width()/2):
			balls.remove(self)
			game.delete(self.id)
			del self

def update_game():
	if not paused:
		#Updates the game to move the ball
		ball.move()
		#If there are no bricks or no balls left we know the game is lost or won
		if not balls or not bricks:
			return False
		
		#Code to check for collisions
		for item in balls:
			for brick in bricks:
				side = brick.collision(item)
				if side != None:
					item.update_velocity(side)
					brick.crack()
					ball.move()
					break
			item.wall_collisions(ball)
			print
			side, relative_collision_point = paddle.collision(item)
			if side != None:
				item.update_velocity(side, relative_collision_point)
				ball.move()
				break
		#Update score
		game.itemconfigure(score_label,text=f"Score: {score}")
		# window.after(30, update_game)
	return True

def level_one():
	global balls
	global ball
	global score
	global score_label
	global level_label
	global bricks
	global paddle
	global level

	#Delete anything currently on the canvas so we can replace everything (if game is restarted)
	game.delete('all')
	game.pack()
	level = 1

	#Create the elements
	ball_id, paddle_id, paddle_image, ball_image = create_elements()

	bricks = []
	#Add text to display level
	level_label = game.create_text(3, 3, text=f"Level {level}", font=("Courier New", 28), fill="white", anchor="nw")

	#Add text with score
	score_label = game.create_text(WIDTH/2, 3, text=f"Score: {score}", font=("Courier New", 28), fill="white", anchor="n")

	#Move the paddle to the correct location
	game.coords(paddle, int(WIDTH/2),int(HEIGHT)-5)

	#Loop to place bricks
	for row in range(int(NUMBER_OF_ROWS)):
		for brick in range(BRICKS_PER_ROW):
			new_brick = GreyBrick(brick*BRICK_WIDTH,(row+1)*BRICK_HEIGHT)
			bricks.append(new_brick)

	update = True

	while update:
		update = update_game()
		game.update()

	if balls:
		#If level is completed, hide the ball and paddle
		game.itemconfig(ball.id, state="hidden")
		game.itemconfig(paddle.id, state="hidden")
		game.update_idletasks()
		#If the level is completed, display appropriate message and option to go to next level
		finished_label = Label(game, text=f"Congratulations! \n You have completed Level 1", font=("Courier New", 60), bg="black")
		finished_label.pack()
		finished_label.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")
		level_two_button = Button(game, text="Next Level", command= lambda: level_two(finished_label, level_two_button), font=("Courier New", 60),background="grey")
		level_two_button.pack()
		level_two_button.place(x=WIDTH/2, y=HEIGHT/2 + 120, anchor="center")
	else:
		#If game is lost, display appropriate message and option to play again
		game_over_label = Label(game, text=f"GAME OVER...", font=("Courier New", 60), bg="black")
		game_over_label.pack()
		game_over_label.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")

		play_again_button = Button(game, text="Save & Play Again", command= lambda: play_again(game_over_label,play_again_button),font=("Courier New", 60),background="grey")
		play_again_button.pack()
		play_again_button.place(x=WIDTH/2, y=HEIGHT/2 + 120, anchor="center")
	
def level_two(finished_label=None, level_two_button=None):
	#Start level two
	global balls
	global ball
	global score
	global score_label
	global bricks
	global paddle
	global level
	global level_label
	global saved_score

	#Destory labels from the end of level one if they exist
	try:
		finished_label.destroy()
		level_two_button.destroy()
		game.delete(level_label)
		game.delete(score_label)
	except:
		pass

	#Update score label and save the score from the end of level one
	saved_score = score
	level = 2
	game.pack()
	ball.speed = 12

	#Recreate score and level label
	level_label = game.create_text(3, 3, text=f"Level {level}", font=("Courier New", 28), fill="white", anchor="nw")
	score_label = game.create_text(WIDTH/2, 3, text=f"Score: {score}", font=("Courier New", 28), fill="white", anchor="n")

	#Put the paddle and bal back to the begining
	game.coords(ball.id, int(WIDTH/2), int(HEIGHT-paddle.image.height()-5-(ball.image.width()/2)))
	game.itemconfig(ball.id, state="normal")

	game.coords(paddle.id, int(WIDTH/2),int(HEIGHT)-5)
	game.itemconfig(paddle.id, state="normal")

	bricks = []

	#Update the screen
	game.update_idletasks()

	#Set the ball's velocities back to 0 and allow it to be refired
	ball.x_velocity = 0
	ball.y_velocity = 0
	ball.fired = False

	unbreakable_positions = [[1,5,9],[1,5,9],[3,7],[3,7]]

	#Loop to place bricks
	for row in range(int(NUMBER_OF_ROWS)):
		for brick in range(BRICKS_PER_ROW):
			x = brick * BRICK_WIDTH
			y = (row + 1) * BRICK_HEIGHT
			if brick in unbreakable_positions[row]:  # Every third brick is UnbreakableBrick
				new_brick = UnbreakableBrick(x, y, "grey")
			else:
				new_brick = BlueBrick(brick*BRICK_WIDTH,(row+1)*BRICK_HEIGHT)
			bricks.append(new_brick)

	update = True

	while update:
		update = update_game()
		game.update()

	if balls:
		#If the level is completed, hide the ball and paddle
		game.itemconfig(ball.id, state="hidden")
		game.itemconfig(paddle.id, state="hidden")
		game.update_idletasks()
		#If the level is completed, display appropriate message and option to go to next level
		finished_label = Label(game, text=f"Congratulations! \n You have completed Level 2", font=("Courier New", 60), bg="black")
		finished_label.pack()
		finished_label.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")
		level_three_button = Button(game, text="Next Level", command= lambda: level_three(finished_label, level_three_button), font=("Courier New", 60),background="grey")
		level_three_button.pack()
		level_three_button.place(x=WIDTH/2, y=HEIGHT/2 + 120, anchor="center")
	else:
		#If game is lost, display
		#  appropriate message and option to play again
		game_over_label = Label(game, text=f"GAME OVER...", font=("Courier New", 60), bg="black")
		game_over_label.pack()
		game_over_label.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")

		play_again_button = Button(game, text="Save & Play Again", command= lambda: play_again(game_over_label,play_again_button),font=("Courier New", 60),background="grey")
		play_again_button.pack()
		play_again_button.place(x=WIDTH/2, y=HEIGHT/2 + 120, anchor="center")
	pass

def level_three(finished_label=None, level_three_button=None):
	#Start level two
	global balls
	global ball
	global score
	global score_label
	global bricks
	global paddle
	global level
	global level_label
	global saved_score

	#Destory labels from the end of level one if they exist
	try:
		finished_label.destroy()
		level_three_button.destroy()
		game.delete(level_label)
		game.delete(score_label)
	except:
		pass

	#Update score label and save the score from the end of level one
	saved_score = score
	level = 3
	game.pack()
	ball.speed = 15

	#Recreate score and level label
	level_label = game.create_text(3, 3, text=f"Level {level}", font=("Courier New", 28), fill="white", anchor="nw")
	score_label = game.create_text(WIDTH/2, 3, text=f"Score: {score}", font=("Courier New", 28), fill="white", anchor="n")

	#Put the paddle and bal back to the begining
	game.coords(ball.id, int(WIDTH/2), int(HEIGHT-paddle.image.height()-5-(ball.image.width()/2)))
	game.itemconfig(ball.id, state="normal")

	game.coords(paddle.id, int(WIDTH/2),int(HEIGHT)-5)
	game.itemconfig(paddle.id, state="normal")

	bricks = []

	#Update the screen
	game.update_idletasks()

	#Set the ball's velocities back to 0 and allow it to be refired
	ball.x_velocity = 0
	ball.y_velocity = 0
	ball.fired = False

	unbreakable_positions = [[1,2,3],[5,6,7],[0,1,5,6],[3,4,8,9]]

	#Loop to place bricks
	for row in range(int(NUMBER_OF_ROWS)):
		for brick in range(BRICKS_PER_ROW):
			x = brick * BRICK_WIDTH
			y = (row + 1) * BRICK_HEIGHT
			if brick in unbreakable_positions[row]:  # Every third brick is UnbreakableBrick
				new_brick = UnbreakableBrick(x, y, "grey")
			else:
				new_brick = LightBlueBrick(brick*BRICK_WIDTH,(row+1)*BRICK_HEIGHT)
			bricks.append(new_brick)

	update = True

	while update:
		update = update_game()
		game.update()

	if balls:
		#If the level is completed, hide the ball and paddle
		game.itemconfig(ball.id, state="hidden")
		game.itemconfig(paddle.id, state="hidden")
		game.update_idletasks()
		#If the level is completed, display appropriate message and option to go to next level
		finished_label = Label(game, text=f"Congratulations! \n You have completed the game!", font=("Courier New", 60), bg="black")
		finished_label.pack()
		finished_label.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")
		#Save the players go to a text file
		with open('history.txt', 'a') as file:
			file.write(f'{name},{score},{level},C\n') #Writing C to indicate completed game
		#Add a completion screen
	else:
		#If game is lost, print appropriate message and option to play again
		game_over_label = Label(game, text=f"GAME OVER...", font=("Courier New", 60), bg="black")
		game_over_label.pack()
		game_over_label.place(x=WIDTH/2, y=HEIGHT/2, anchor="center")

		play_again_button = Button(game, text="Save & Play Again", command= lambda: play_again(game_over_label,play_again_button),font=("Courier New", 60),background="grey")
		play_again_button.pack()
		play_again_button.place(x=WIDTH/2, y=HEIGHT/2 + 120, anchor="center")
	pass

def play_again(game_over_label,play_again_button):

	global score
	#Save the players go to a text file
	with open('history.txt', 'a') as file:
		file.write(f'{name},{score},{level},C\n') #Writing C to indicate completed game


	#Set score back to 0
	score = 0
	#If the game is play_agained, we want to destory the labels we just created
	game_over_label.destroy()
	play_again_button.destroy()
	game.update_idletasks()
	level_one()

def create_pause_menu():
	#Place the buttons for the pause menu

	button_width = int(WIDTH/85)
	button_height = int(HEIGHT/720)		

	resume_button = Button(pause_menu, text="Resume", command=unpause, font=("Courier New", 60),background="grey", width=button_width, height=button_height)
	resume_button.place(x=WIDTH/2, y=HEIGHT/5, anchor="center")

	leaderboard_button = Button(pause_menu, text="Leaderboard", command=show_leaderboard, font=("Courier New", 60),background="grey", width=button_width, height=button_height)
	leaderboard_button.place(x=WIDTH/2, y=(2*HEIGHT)/5, anchor="center")

	settings_button = Button(pause_menu, text="Settings", command=settings, font=("Courier New", 60),background="grey", width=button_width, height=button_height)
	settings_button.place(x=WIDTH/2, y=(3*HEIGHT)/5, anchor="center")

	save_and_exit_button = Button(pause_menu, text="Save and Exit", command=save_and_exit, font=("Courier New", 60),background="grey", width=button_width, height=button_height)
	save_and_exit_button.place(x=WIDTH/2, y=(4*HEIGHT)/5, anchor="center")

def pause(event=None):
	#When called will remove the game from the window and show the pause menu
	global paused

	paused = True
	game.pack_forget()
	pause_menu.pack()
	window.unbind("<Escape>")
	window.bind("<Escape>", unpause)

def unpause(event="None"):
	#When called will remove the pause menu from the window and show the game
	global paused
	paused = False
	pause_menu.pack_forget()
	settings_menu.pack_forget()
	leaderboard.pack_forget()
	game.pack()
	window.unbind("<Escape>")
	window.bind("<Escape>", pause)
	pass

def show_leaderboard(event=None):
	window.bind("<Escape>", unpause)
	#When called will remove what is currently showing, and show the leaderboard
	#Read from history file
	pause_menu.pack_forget()
	with open("history.txt", 'r') as file:
		lines = file.readlines()

	#Turn data into a list of lists for each play through for easier access
	data = [line.strip().split(',') for line in lines]

	#Sort the items in the data with descending scores
	ordered_scores = sorted(data, key=lambda x: int(x[1]) if x[1].isdigit() else 0, reverse=True)

	#Create title text for the leaderboard
	leaderboard.create_text(WIDTH/2, HEIGHT/100, anchor="n", text="Leaderboard:", font=("Courier New", 60, "bold"))
	leaderboard.pack()

	#Create column text
	header_text = "{:<9} {:<10} {:<6}".format("RANK", "NAME", "SCORE")
	leaderboard.create_text(WIDTH/4, (0.9*HEIGHT)/8, anchor="n", text="RANK", font=("Courier New", 50, "bold"))
	leaderboard.create_text((2*WIDTH)/4, (0.9*HEIGHT)/8, anchor="n", text="NAME", font=("Courier New", 50, "bold"))
	leaderboard.create_text((3*WIDTH)/4, (0.9*HEIGHT)/8, anchor="n", text="SCORE", font=("Courier New", 50, "bold"))

	#Display the top ten leaderboard scores
	for i, (name, score, level, completed) in enumerate(ordered_scores[:10], 1):
		y_position = (1.2*HEIGHT)/8 + i * (HEIGHT/16)
		leaderboard.create_text(WIDTH/4, y_position, anchor="n", text=i, font=("Courier New", 40))
		leaderboard.create_text((2*WIDTH)/4, y_position, anchor="n", text=name, font=("Courier New", 40))
		leaderboard.create_text((3*WIDTH)/4, y_position, anchor="n", text=score, font=("Courier New", 40))

def create_settings(event=None):
	#Creates the text and buttons that sit on the settings canvas
	settings_text = settings_menu.create_text(WIDTH/2, HEIGHT/5, text="Settings", font=("Courier New", 60, "bold"), fill="white", anchor="center")
	left_text = settings_menu.create_text(WIDTH/3.5, (2*HEIGHT)/5, text="Move Left", font=("Courier New", 25), fill="white", anchor="w")
	right_text = settings_menu.create_text(WIDTH/3.5, (3*HEIGHT)/5, text="Move Right", font=("Courier New", 25), fill="white", anchor="w")
	fire_text = settings_menu.create_text(WIDTH/3.5, (4*HEIGHT)/5, text="Fire", font=("Courier New", 25), fill="white", anchor="w")
	
	button_width = int(WIDTH/85)
	button_height = int(HEIGHT/240)

	left_button = Button(settings_menu, text="Left Arrow", command=lambda: wait_for_key_press(event,left_button,"left"), font=("Courier New", 25),background="grey", width=button_width, height=button_height)
	left_button.place(x=WIDTH/2, y=(2*HEIGHT)/5, anchor="w")

	right_button = Button(settings_menu, text="Right Arrow", command=lambda: wait_for_key_press(event,right_button,"right"), font=("Courier New", 25),background="grey", width=button_width, height=button_height)
	right_button.place(x=WIDTH/2, y=(3*HEIGHT)/5, anchor="w")

	fire_button = Button(settings_menu, text="Left Click", command=lambda: wait_for_key_press(event,fire_button,"fire"), font=("Courier New", 25),background="grey", width=button_width, height=button_height)
	fire_button.place(x=WIDTH/2, y=(4*HEIGHT)/5, anchor="w")

def settings():
	#Will take user to settings page when called
	window.bind("<Escape>", unpause)

	pause_menu.pack_forget()
	settings_menu.pack()

def wait_for_key_press(event,button,action):
	#Function that waits for a key press to change settings
	button.config(text="Press a key...")

	#Temporarily bind the pressed key can call capture_key
	#Note has to manually bind some keys as they don't automatically generate <Key> events

	keys_to_handle = ["<Key>", "<Left>", "<Right>", "<Up>", "<Down>", "<BackSpace>", "<Delete>",
                      "<Return>", "<Shift_L>", "<Shift_R>", "<Control_L>", "<Control_R>",
                      "<Alt_L>", "<Alt_R>"]
	
	for key in keys_to_handle:
		window.bind(key, lambda event: capture_key(event, button, keys_to_handle, action))

def capture_key(event,button, keys_to_handle, action):
	#Captures the new key press and binds it to the setting
	#Unbinds the temporary keys

	pressed_key = event.keysym

	button.config(text=f"{pressed_key}")

	#Depending on the button, rebind the key to the selected one
	if action == "left":
		window.bind(pressed_key, lambda event: paddle.move_left(event))
	elif action == "right":
		window.bind(pressed_key, lambda event: paddle.move_right(event))
	elif action == "fire":
		window.bind(pressed_key, lambda event: ball.fire(event.x,event.y))

def save_and_exit():
	#Will save the name, score and level to a text file called history.txt

	# Open the file in append mode and write the data
	with open('history.txt', 'a') as file:
		file.write(f'{name},{saved_score},{level},S\n') #Writing S to indicate saved game
														#Writing saved score as loading an incomplete game will start from beginning of latest level

	#Close window
	window.destroy()

def start_game():
	window.bind("<Return>", lambda event: submit_name(event, name_entry.get()))
	enter_text = start.create_text(WIDTH/2, HEIGHT/4, text="Enter your name:", font=("Courier New", 50, "bold"), fill="white", anchor="center")
	# submit_text = start.create_text(WIDTH/2, (2*HEIGHT)/4, text="Press Enter to Submit...", font=("Courier New", 50), fill="white", anchor="center")

	widget_width = int(WIDTH/50)
	widget_height = int(HEIGHT/360)

	#Create an entry for a user to enter their name
	name_entry = Entry(start, font=("Courier New", 49), width=int(widget_width/2))
	name_entry.place(x = WIDTH/2.1,y = (1.5*HEIGHT)/4, anchor="e")

	# Create a button to submit the name
	new_game_button = Button(start, text="New Game", command = lambda: submit_name(None,name_entry.get()), font=("Courier New", 30), height=int(widget_height), width=int(widget_width/1.3))
	new_game_button.place(x = WIDTH/1.9,y = (1.5*HEIGHT)/4, anchor="w")

	or_text = start.create_text(WIDTH/2, (2.1*HEIGHT)/4, text="or", font=("Courier New", 50, "bold"), fill="white", anchor="center")

	#Create a button to load previous game
	load_game_button = Button(start, text="Load Previous Game", command = load_previous, font=("Courier New", 30), height=int(widget_height), width=int(widget_width))
	load_game_button.place(x = WIDTH/2,y = (2.5*HEIGHT)/4, anchor="n")

def submit_name(event,name_entered):
	global name
	name = name_entered

	#If they have entered a name...we start the game
	if name_entered:
		start.pack_forget()
		window.unbind("<Return>")
		window.bind("<Button-1>", lambda event: ball.fire(event.x,event.y))
		level_one()

def load_previous():
	global score
	global name

	#Read the data of previous goes
	with open("history.txt", 'r') as file:
		lines = file.readlines()
		#Take the most recent data item
		data = [line.strip().split(',') for line in lines][-1]

	if data[3] == "C":
		#If the previous game was completed, then it cannot be loaded
		no_data_text = start.create_text(WIDTH/2, (3.2*HEIGHT)/4, text="Uh Oh... There is no game to load!", font=("Courier New", 30, "bold"), fill="white", anchor="center")
	else:
		#Otherwise it can be loaded so we load it
		#Remove the last line, as we don't want duplicates in the leaderboard
		lines = lines[:-1]
		with open("history.txt", 'w') as file:
			file.writelines(lines)

		start.pack_forget()
		window.bind("<Button-1>", lambda event: ball.fire(event.x,event.y))

		#Assign the global variables from the data
		name = data[0]
		score = int(data[1])

		#Start at the correct level
		if data[2] == "1":
			level_one()
			level = 1
		elif data[2] == "2":
			ball.id, paddle.id, paddle.image, ball.image = create_elements()
			level_two()
			level = 2
		elif data[2] == "3":
			ball.id, paddle.id, paddle.image, ball.image = create_elements()
			level_three()
			level = 3
	
def create_elements():
	global ball
	global paddle
	#Load paddle image and resize using PIL
	#Usable under CC license
	paddle_image = Image.open("paddle.png")
	paddle_image = paddle_image.resize((154, 41))
	paddle_image = ImageTk.PhotoImage(paddle_image)
	paddle_id = game.create_image(int(WIDTH/2),int(HEIGHT)-5, anchor="s", image=paddle_image)
	paddle = Paddle(paddle_id,paddle_image)

	#Load ball image and resize using PIL
	#Usable under CC license
	ball_image = Image.open("ball.png")
	ball_image = ball_image.resize((int(73/1.5), int(72//1.5)))
	ball_image = ImageTk.PhotoImage(ball_image)
	ball_id = game.create_image(int(WIDTH/2),int(HEIGHT-paddle_image.height()-5-(ball_image.width()/2)), anchor="center", image=ball_image)
	
	ball = Ball(ball_id, ball_image)
	balls.append(ball)

	return ball_id, paddle_id, paddle_image, ball_image

def boss_button(event=None):
	#When the boss button is pressed we show the boss screen
	#We also activate the pause menu in the background
	if not paused:
		pause()
	#Stop displaying any other screens that may be present
	pause_menu.pack_forget()
	leaderboard.pack_forget()
	settings_menu.pack_forget()
	#Pack the boss screen
	boss_screen.pack()
	#Put image on the canvas
	teams_screenshot_id = boss_screen.create_image(0,0, anchor="nw", image = teams_screenshot)
	#We now bind the boss button to the function to end it
	window.bind("<Control-b>", end_boss_button)

def end_boss_button(event=None):
	#If the boss button is called again, we end it and take the user to the pause menu
	window.bind("<Control-b>", boss_button)
	boss_screen.pack_forget()
	pause_menu.pack()

def cheat_code_check(event):
	global cheat_sequence
    # Check if the pressed keys match the desired sequence
	if event.keysym == "1":  # state 0 means no modifiers (Shift, Ctrl, Alt)
		cheat_sequence.append("1")
	elif event.keysym == "2":
		cheat_sequence.append("2")
	elif event.keysym == "3":
		cheat_sequence.append("3")
	elif event.keysym == "4":
		cheat_sequence.append("4")
	else:
		cheat_sequence = []

    # Check if the current sequence matches the cheat sequence
	if "1234" in "".join(cheat_sequence):
		cheat()
		cheat_sequence = []

def cheat():
	global paddle
	# original_coords = paddle.get_coords()

	#Load paddle image and resize using PIL to larger than normal
	#Usable under CC license
	big_paddle_image = Image.open("paddle.png")
	big_paddle_image = big_paddle_image.resize((254, 41))
	big_paddle_image = ImageTk.PhotoImage(big_paddle_image)

	#Change the size of the paddle
	paddle.image = big_paddle_image
	game.itemconfig(paddle.id, image=big_paddle_image)


#Initialise window
window = Tk()

#Change desired width and height here
WIDTH = 1280
HEIGHT=720

window.geometry(f"{WIDTH}x{HEIGHT}")
window.title("Classic Brick Breaker")

#Create canvas for starting game on window
start = Canvas(window,bg="black",width=WIDTH,height=HEIGHT)
start.pack()

#Create game canvas on window
game = Canvas(window,bg="black",width=WIDTH,height=HEIGHT)
paused = False

#Create canvas for pause menu
pause_menu = Canvas(window, bg="black", width=WIDTH,height=HEIGHT)
create_pause_menu()

#Create canvas for settings_menu
settings_menu = Canvas(window, bg="black", width=WIDTH,height=HEIGHT)
create_settings(None)

#Create canvas for leaderboard
leaderboard = Canvas(window, bg="black", width=WIDTH,height=HEIGHT)

boss_screen = Canvas(window, bg="black", width=WIDTH,height=HEIGHT)

balls = []
cheat_sequence = []

BRICKS_PER_ROW = 10
BRICK_WIDTH = WIDTH // BRICKS_PER_ROW
BRICK_HEIGHT = int(BRICK_WIDTH * (57 / 170))

NUMBER_OF_ROWS = 4

score = 0
saved_score = 0

#Load and resize grey_brick_image
#Usable under CC license
grey_brick_image = Image.open("grey_brick.png")
grey_brick_image = grey_brick_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
grey_brick_image = ImageTk.PhotoImage(grey_brick_image)

#Load and resize grey_brick_cracked_image
#Usable under CC license
grey_brick_cracked_image = Image.open("grey_brick_cracked.png")
grey_brick_cracked_image = grey_brick_cracked_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
grey_brick_cracked_image = ImageTk.PhotoImage(grey_brick_cracked_image)

#Load and resize blue_brick_image
#Usable under CC license
blue_brick_image = Image.open("blue_brick.png")
blue_brick_image = blue_brick_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
blue_brick_image = ImageTk.PhotoImage(blue_brick_image)

#Load and resize blue_brick_cracked_image
#Usable under CC license
blue_brick_cracked_image = Image.open("blue_brick_cracked.png")
blue_brick_cracked_image = blue_brick_cracked_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
blue_brick_cracked_image = ImageTk.PhotoImage(blue_brick_cracked_image)

#Usable under CC license
#Load and resize light_blue_brick_image
light_blue_brick_image = Image.open("light_blue_brick.png")
light_blue_brick_image = light_blue_brick_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
light_blue_brick_image = ImageTk.PhotoImage(light_blue_brick_image)

#Load and resize light_blue_brick_cracked_image
#Usable under CC license
light_blue_brick_cracked_image = Image.open("light_blue_brick_cracked.png")
light_blue_brick_cracked_image = light_blue_brick_cracked_image.resize((BRICK_WIDTH, BRICK_HEIGHT))
light_blue_brick_cracked_image = ImageTk.PhotoImage(light_blue_brick_cracked_image)

#Load and resize teams_screenshot for the boss button
#Usable under CC license
teams_screenshot = Image.open("teams_screenshot.png")
teams_screenshot = teams_screenshot.resize((WIDTH, HEIGHT))
teams_screenshot = ImageTk.PhotoImage(teams_screenshot)

bricks = []
start_game()

#Bind left and right keys to move paddle
window.bind("<Left>", lambda event: paddle.move_left(event))
window.bind("<Right>", lambda event: paddle.move_right(event))

#Bind escape to the pause function
window.bind("<Escape>", pause)

#Bind Control + b to be the boss button
window.bind("<Control-b>", boss_button)

#Bind 1,2,3,4 to the function to test for the boss sequence
window.bind("1", cheat_code_check)
window.bind("2", cheat_code_check)
window.bind("3", cheat_code_check)
window.bind("4", cheat_code_check)


window.mainloop()
