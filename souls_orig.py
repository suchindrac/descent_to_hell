import tkinter as tk
import random
import threading
import time

green = '#008000'
red = '#ff0000'
yellow = '#ffff00'

people = None
canvas = None

def down():
	global people
	global canvas
	
	#
	# Select the person
	#
	person = random.randint(0, len(people)-1)
	person = people[person]
	
	#
	# Find out which state he is in
	#
	if person.num_changes % 2 == 0:
		#
		# If he has to pay back karma
		#  after going to animal world simulation, then
		#  mark his color as current color + a tint towards red
		#
		person.color = get_color(person.color, person.free_will, -person.free_will, 0)
		#
		# Reduce his free will, frequency and energy
		#
		person.free_will -= 10
		person.frequency -= 10
		person.energy -= 10
		
		#
		# Find out which hell he goes to
		#  NOTE: This will be a real world hell simulation, 
		#         as this was the original design
		#
		x_chg = random.randint(0, 100)
		y_chg = random.randint(0, 100)
		new_x = person.location[0] + x_chg
		new_y = person.location[1] + y_chg
	else:
		#
		# If the person has paid his karma,
		#  then he is supposed to be marked as current color + a tint towards green,
		#  but because of the mercy of the universe, he is marked as green
		#
		# person.color = get_color(person.color, -person.free_will, person.free_will, 0)
		person.color = green
		#
		# His soul's free will, frequency and energy are increased
		#
		person.free_will += 10
		person.frequency += 10
		person.energy += 10

		#
		# In this case also, he goes to the real world itself,
		#  as this is the original simulation
		#
		x_chg = random.randint(0, 100)
		y_chg = random.randint(0, 100)
		new_x = person.location[0] - x_chg
		new_y = person.location[1] - y_chg

	#
	# Increase the number of lives the preson has gone through, by 1
	#
	person.num_changes += 1
	
	#
	# The person should be in the bounds of the multiverse!
	#
	if new_x >= 600:
		new_x = 600
	if new_y >= 400:
		new_y = 400

	#
	# If he has gone beyond animal world simulation boundary,
	#  then just put him at the boundary
	#
	if new_y > 210:
		new_y = 210

	#
	# Store the person's location
	#
	person.location = [new_x, new_y]

	#
	# Remove him from his original place, and put him
	#  in the new place
	# NOTE: Change the color accordingly
	#
	canvas.delete(person.box)
	person.box = canvas.create_oval(new_x, new_y, new_x+20, new_y+20, fill=person.color, outline=person.color)
	canvas.pack()

	#
	# Call the system of a down again!
	#
	canvas.after(10, down)

def force_range(x):
	if x < 0:
		x = 0
	if x > 255:
		x = 255
	return hex(x)[2:]

def get_color(cur, cr, cg, cb):
	cur = cur[1:]
	cur_r = int(cur[:2], 16)
	cur_g = int(cur[2:4], 16)
	cur_b = int(cur[4:], 16)

	cur_r += cr
	cur_g += cg
	cur_b += cb
	
	[cur_r, cur_g, cur_b] = map(force_range, [cur_r, cur_g, cur_b])

	return "#" + str(cur_r).zfill(2) + str(cur_g).zfill(2) + str(cur_b).zfill(2)

class Person:
	def __init__(self):
		self.canvas = None
		self.energy = 100
		self.frequency = 100
		self.free_will = 100
		self.box = None
		self.in_freedom_env = True
		self.color = green
		self.location = []
		self.num_changes = 0

class Universe:
	def __init__(self, *args, **kwargs):
		self.people = []

	def create_people(self):
		for p in range(100):
			person = Person()
			self.people.append(person)

	def populate(self, root):
		global people
		global canvas
		self.board = tk.Canvas(root, width=640, height=480)
		self.board.pack()
		for p in self.people:
			rx = random.randint(0, 600)
			#
			# 0 to 200 is real world simulation
			#  which has freedom
			# 200 to 400 is animal world simulation
			#  which does not have freedom
			#
			ry = random.randint(0, 200)
			p.box = self.board.create_oval(rx, ry, rx+20, ry+20, fill=p.color)
			p.location = [rx, ry]
		people = self.people
		canvas = self.board

if __name__ == "__main__":
	root = tk.Tk()
	root.geometry("640x480")
	
	u = Universe(root)
	u.create_people()
	u.populate(root)

	root.after(1, down)
	
	root.mainloop()
