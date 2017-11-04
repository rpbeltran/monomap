import math

class Camera:

	def __init__( self, fovx, res ):

		self.fov = fov
		self.res = res

		self.rot = [0,1,0]
		self.pos = [0,0,0]

		self.focal_length = res[0] / math.tan( self.fovx / 2) / 2

	def normalize_point( self, pos ):

		return (pos[0] - (res[0] / 2), pos[1] - (res[1] / 2) )

	def angle_to ( self, point ):

		p_norm = self.normalize_point( point )

		return math.atan( (p_norm[0] * p_norm[0] + p_norm[1] * p_norm[1]) / self.focal_length )



def calculate_local( cam_0, cam_1, p_0, p_1 ):

	a_0 = cam0.angle_to( p_0 )
	a_1 = cam1.angle_to( p_1 )
	a_xy = math.atan( p_1[1] / p_1[0] )

	dist = ((p_1[0]-p_0[0])**2+(p_1[1]-p_0[1])**2)**0.5

	y = dist * ( (1.0/math.tan(a_0)) - (1.0/math.tan(a_1)) )

	x = y / math.tan( a_1 )
