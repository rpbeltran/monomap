
import math
import numpy as np

class Camera:

	def __init__ ( self ):

		self.fov = 2.7925
		self.resolution = (1920.0,1080.0)
		self.p_to_v_mult = self.fov / ( self.resolution[0]*self.resolution[0] + self.resolution[1]*self.resolution[1] )**0.5

	def x_to_theta( self, x ):
		
		return x * self.fov / self.resolution[0]

	def y_to_theta( self, y ):

		return y * self.fov / self.resolution[0]

	def xy_to_theta( self, x, y ):

		return self.p_to_v_mult * ((x*x+y*y)**0.5)



class Depth_Mapper:

	
	def __init__( self, points, camera = None ):

		if( camera == None ):
			camera = Camera()

		self.camera = camera

		# points
		# [
		#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ],
		#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ],
		#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ]
		# ]

		self.points = points


	def calculate_depth_maps( self ):

		self.depth_maps = []# Depth Maps
							# [ 
							#	[
							#	point,
							#	{ 
							#		id1 : depth,
							#		id2 : depth,
							#		id3 : depth 
							#	},
							#	{ 
							#		id1 : depth,
							#		id2 : depth,
							#		id3 : depth 
							#	},
							#	{ 
							#		id1 : depth,
							#		id2 : depth,
							#		id3 : depth 
							#	}
							# 	] 
							# ]

		self.direction_maps = []

		self.global_points = []

		for point in self.points:

			Xr, Yr = point[0], point[1]

			# Memoiziation
			ys      =  [None]
			xs      =  [None]
			ds      =  [None]
			vdts    =  [None]
			pls     =  [None] # [ Np.array, Np.array ]
			pgs     =  [    ] # 
			boguses =  [True] 
			thetas  =  [    ]

			thetas.append(self.camera.xy_to_theta(point[0][2],point[0][3]))

			for i in range( 1,len(point) ):

				bogus = False 

				# Calculate Vdt
				dxr = point[i][0] - point[i-1][0]
				dxy = point[i][1] - point[i-1][1]
				vdts.append(( dxr*dxr + dxy*dxy )**0.5)

				# Calculate Thetas
				thetas.append(self.camera.xy_to_theta(point[i][2],point[i][3]))

				# Calculate Depth
				try:
					ys.append(vdts[i] * ( (1.0/math.tan(thetas[i-1])) - (1.0/math.tan(thetas[i])) ) )
				except:
					ys.append(-1)
					bogus = True

				try:
					xs.append(ys[i]/math.tan(thetas[i]))
				except:
					xs.append(-1)
					bogus = True

				ds.append( (ys[i]*ys[i] + xs[i]*xs[i] ) ** 0.5)

				# Calculate Local Coordinates
				pls.append( np.matrix( [ [ys[i]*math.cos(thetas[i])], [xs[i]], [ys[i]*math.sin(thetas[i])] ]) )

				if not bogus:
					pli = pls[i].tolist()
					pgs.append( [ pli[0][0] + point[i][0], pli[1][0] + point[i][1], pli[2][0] ] )

				boguses.append( bogus )

			if len(pgs) < 3:
				continue

			gx = sum( map( lambda x:x[0], pgs) ) / len(pgs)
			gy = sum( map( lambda x:x[1], pgs) ) / len(pgs)
			gz = sum( map( lambda x:x[2], pgs) ) / len(pgs)

			self.global_points.append( (gx,gy,gz) )
