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
	person = random.randint(0, len(people)-1)
	person = people[person]
	#
	# If the person commits crime in the real world simulation,
	#  then, he pays back his karma in a real world hell first, till
	#  he falls to animal world hell simulation, from where he goes on a
	#  complete downward journey till rasatala
	#
	if person.in_freedom_env:
		if person.num_changes % 2 == 0:
			#
			# Tint him towards red
			#
			person.color = get_color(person.color, person.free_will, -person.free_will, 0)

			#
			# Reduce his free will, frequency and energy
			#
			person.free_will -= 10
			person.frequency -= 10
			person.energy -= 10

			#
			# Place him in the real world, as he has committed the crime in the
			#  real world
			#
			x_chg = random.randint(0, 100)
			y_chg = random.randint(0, 100)
			new_x = person.location[0] + x_chg
			new_y = person.location[1] + y_chg
		else:
			#
			# Ideally, tint him towards green,
			#  but because of mercy of the universe, he is marked green
			#
			# person.color = get_color(person.color, -person.free_will, person.free_will, 0)
			person.color = green

			#
			# He has paid back in hell, so his free will, frequency and
			#  energy increase
			#
			person.free_will += 10
			person.frequency += 10
			person.energy += 10
			
			#
			# Place him in a real world hell
			#
			x_chg = random.randint(0, 100)
			y_chg = random.randint(0, 100)
			new_x = person.location[0] - x_chg
			new_y = person.location[1] - y_chg

		#
		# If he stumbles towards the animal world simulation, then place him in one
		#  of the simulations
		#
		if new_y > 200:
			new_y = 220
			person.in_freedom_env = False

		#
		# Make him be within the bounds
		#
		if new_x >= 600:
			new_x = 600
		if new_y >= 400:
			new_y = 400
	else:
		#
		# If he is in the animal world simulation already,
		#  then keep reducing his free will, frequency and energy
		#
		person.color = get_color(person.color, person.free_will, -person.free_will, 0)
		person.free_will -= 10
		person.frequency -= 10
		person.energy -= 10

		#
		# Take him to different hells in animal world simulation
		#
		x_chg = random.randint(0, 100)
		y_chg = random.randint(0, 100)
		new_x = person.location[0] + x_chg
		new_y = person.location[1] + y_chg
		if new_y > 200:
			#
			# There is no correction in range here, when he goes below
			#  the real world to animal world simulation boundary, 
			#  because the person is on a free fall
			#
			person.in_freedom_env = False
			person.free_will -= 10
			person.frequency -= 10
			person.energy -= 10

		#
		# Check for the boundaries in the multiverse though
		#
		if new_x >= 600:
			new_x = 600

		#
		# When the person has gone towards atala, vitala, talatala, patala, rasatala,
		#  and there is no more tala to go to, then push him to the real world
		#  hell
		#
		if new_y >= 400:
			new_x = random.randint(0, 150)
			new_y = random.randint(0, 150)
			person.in_freedom_env = True

	#
	# Increase the number of lives by 1
	#
	person.num_changes += 1
	
	#
	# Put him in the new location
	#
	person.location = [new_x, new_y]
	canvas.delete(person.box)
	person.box = canvas.create_oval(new_x, new_y, new_x+20, new_y+20, fill=person.color, outline=person.color)
	canvas.pack()
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
