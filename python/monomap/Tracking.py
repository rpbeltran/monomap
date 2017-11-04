
import math
import numpy as np
import cv2
import time

class Tracker:

	def __init__( self ):

		self.cap = cv2.VideoCapture(0)
		self.ret, initial_frame = self.cap.read()
		self.prev_frame = cv2.cvtColor(initial_frame,cv2.COLOR_BGR2GRAY)
		self.hsv = np.zeros_like(initial_frame)
		self.hsv[...,1] = 255

		self.pos_stack = [] 

		self.mag_stack = [] # [
							#	[[mag,mag,mag],[mag,mag,mag],[mag,mag,mag]], 
							# 	[[mag,mag,mag],[mag,mag,mag],[mag,mag,mag]], 
							#   [[mag,mag,mag],[mag,mag,mag],[mag,mag,mag]]
							# ]

		self.dir_stack = [] # [
							# 	[[dir,dir,dir],[dir,dir,dir],[dir,dir,dir]],
							# 	[[dir,dir,dir],[dir,dir,dir],[dir,dir,dir]],
							# 	[[dir,dir,dir],[dir,dir,dir],[dir,dir,dir]] 
							# ]

	# Description: Take an image, calculate shifts, push them into mag and dir stacks

	def capture( self, pos=(0,0), display = False ):

		self.ret, self.frame2 = self.cap.read()
		self.next = cv2.cvtColor(self.frame2,cv2.COLOR_BGR2GRAY)

		self.flow = cv2.calcOpticalFlowFarneback(self.prev_frame, self.next, 0.5, 3, 15, 3, 5, 1.2, 0 )

		self.mag, self.ang = cv2.cartToPolar(self.flow[...,0], self.flow[...,1])
		self.hsv[...,0] = self.ang*180/np.pi/2
		self.hsv[...,2] = cv2.normalize(self.mag,None,0,255,cv2.NORM_MINMAX)
		self.bgr = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)

		if display:
			cv2.imshow('frame2',self.bgr)

		self.prev_frame = self.next

		self.pos_stack.append(    pos   )
		self.mag_stack.append( self.mag )
		#print self.mag_stack

		self.dir_stack.append( self.ang )


	# Description: Releases Cameras

	def stop( self ):

		self.cap.release()
		cv2.destroyAllWindows()


	# Description: Calculate correlated points
	def calculate_points( self ):

		assert np.shape( self.mag_stack ) == np.shape( self.dir_stack )

		shift_comps = lambda m, d : ( m * math.sin(d), m * math.cos(d) ) # Confirm radians 

		shape = np.shape( self.mag_stack )

		self.correlated_points = [] # [
									#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ],
									#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ],
									#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ]
									# ]

		for layer in range(len(self.mag_stack))[::-1]:
			for y in range(shape[0]):
				for x in range(shape[1]):
					
					point_correlations = [  ]
					
					li, xi, yi = layer, x, y
					
					while ( self.mag_stack[li][yi][xi] != None ):

						point_correlations.append( ( self.pos_stack[li][0] - 960, self.pos_stack[li][1] - 540, xi, yi ) )

						(dx, dy) = shift_comps( self.mag_stack[li][yi][xi], self.dir_stack[li][yi][xi] )

						if( not li ):
							break

						li -= 1
						xi  = int( xi - round(dx) )
						xy  = int( yi - round(dy) )

					self.correlated_points.append( point_correlations )

	# Usable Points
	# [ 
	#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ],
	#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ],
	#	[ (Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp),(Xr,Yr,Xp,Yp) ]
	# ]
	def usable_points( self, min_pop = 10, min_diff = 8 ):

		keep = []

		for point in self.correlated_points:

			if( len(point) >= min_pop ):
				if( sum( map ( lambda p : sum(p) != sum(point[0]), point ) ) >= min_diff ):
					keep.append( point )

		return keep




