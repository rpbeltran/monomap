
import numpy
from scipy.optimize import minimize

# Readings
# [ ( (x, y), distance ) ]

def trilaterate ( readings ):

	def squared_error ( p ):

		error_accumulator = 0.0
		for read in readings:
			calc_dist = ( ( p[0] - read[0][0] ) ** 2.0  +  ( p[1] - read[0][1] ) ** 2.0 ) ** 0.5
			error_accumulator += ( calc_dist - read[1] ) ** 2.0

		return error_accumulator

	nearest_reading = min( readings, key = lambda r : r[1] )

	mined = minimize(
		squared_error,        # The error function
		nearest_reading[0],   # The initial guess
		method  = 'L-BFGS-B', # The optimisation algorithm
		options = {
			'ftol':1e-5,      # Tolerance
			'maxiter': 1e+6   # Maximum iterations
		}
	)

	return mined.x


# Depth Maps
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

def stitch ( depth_maps ):

	master_ledger = {}

	for dmap in depth_maps:
		for pid in dmap.keys():
			if master_ledger.has_key( pid ):
				master_ledger[pid].append( ( point, dmap[pid] ) )
			else:
				master_ledger[pid] = [(point,dmap[pid])]

	stitched_map = {}
	for pid in master_ledger.keys():
		stitched_map[pid] = trilaterate( master_ledger[pid] )

	return stitched_map


