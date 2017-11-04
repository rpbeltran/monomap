
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def render_map( stitched_map ):
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ps = stitched_map.values()
	xs = [ p[0] for p in ps ]
	ys = [ p[1] for p in ps ]

	ax.scatter( xs, ys )

	plt.show()

def render_list( stitched_list, maximum = 10000 ):
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	l = len(stitched_list)
	ps = stitched_list[::l]
	xs = [ p[0] for p in ps ]
	ys = [ p[1] for p in ps ]
	zs = [ p[2] for p in ps ]

	ax.scatter( xs, ys, zs )

	plt.show()


#render_list( [ [0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1] ] )
