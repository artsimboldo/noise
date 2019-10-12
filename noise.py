import math
import time
import arcade

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128
SCREEN_TITLE = "noise"
NOISE_FREQ = 1/20

"""
Class Noise
https://mrl.nyu.edu/~perlin/noise/
http://zreference.com/canvas-perlin-noise/
"""
NOISE_PERMUTATION = [151,160,137,91,90,15,
	131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
	190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
	88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
	77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
	102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
	135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
	5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
	223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
	129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
	251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
	49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
	138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

class Noise():
	def __init__(self):
		self.p = [NOISE_PERMUTATION[i] for i in range(256)] * 2

	@staticmethod
	def fade(t):
		return t * t * t * (t * (t * 6 - 15) + 10)

	@staticmethod
	def lerp(t, a, b):
		return a + t * (b - a)
   
	@staticmethod
	def grad(hash, x, y, z):
		h = hash & 15
		u = x if h < 8 else y
		v = y if h < 4 else x if (h == 12 or h == 14) else z
		return (u if (h & 1) == 0 else -u + v if (h & 2) == 0 else -v)

	def __call__(self, x, y, z):
		X = math.floor(x) & 255
		Y = math.floor(y) & 255
		Z = math.floor(z) & 255
		x -= math.floor(x)
		y -= math.floor(y)
		z -= math.floor(z)
		u, v, w = Noise.fade(x), Noise.fade(y), Noise.fade(z)
		A  = self.p[X] + Y
		AA = self.p[A] + Z
		AB = self.p[A + 1] + Z
		B  = self.p[X + 1] + Y
		BA = self.p[B] + Z
		BB = self.p[B + 1] + Z
		return Noise.lerp(w, Noise.lerp(v, Noise.lerp(u, 
			Noise.grad(self.p[AA], x, y, z), 
			Noise.grad(self.p[BA], x - 1, y, z)),
			Noise.lerp(u, Noise.grad(self.p[AB], x, y - 1, z), 
			Noise.grad(self.p[BB], x - 1, y - 1, z))), 
			Noise.lerp(v, Noise.lerp(u, Noise.grad(self.p[AA + 1], x, y, z - 1), 
			Noise.grad(self.p[BA + 1], x - 1, y, z - 1)), 
			Noise.lerp(u, Noise.grad(self.p[AB + 1], x, y - 1, z - 1), 
			Noise.grad(self.p[BB + 1], x - 1, y - 1, z - 1))))

class Demo(arcade.Window):
	def __init__(self, width, height, title):
		super().__init__(width, height, title)
		self.width = width
		self.height = height

	def setup(self, freq):
		self.noise = Noise()
		self.z = 0
		point_list = []
		for y in range(self.height):
			for x in range(self.width):
				point_list.extend([(x,y),(x+1,y),(x+1,y+1),(x,y+1)])
		self.point_list = point_list
		self.coord_list = [(x*freq, y*freq) for y in range(self.height) for x in range(self.width)]

	def on_draw(self):
		arcade.start_render()
		arcade.create_rectangles_filled_with_colors(self.point_list, self.color_list).draw()

	def on_update(self, delta_time):
		self.z += 0.02
		color_list = []
		for (x,y) in self.coord_list:
			col = int(abs(self.noise(x, y, self.z)) * 400)
			color_list.extend((col,col,col) for _ in range(4))
		self.color_list = color_list

if __name__ == '__main__':
	game = Demo(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	game.setup(NOISE_FREQ)
	arcade.run()