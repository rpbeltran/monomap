
from monomap import Tracking, Depth_Map, Rendering
import cv2

tracker = Tracking.Tracker()

for i in range( 15 ):
	
	tracker.capture( (0,i) )

	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

tracker.stop()

tracker.calculate_points()

points = tracker.usable_points()

print "Succesfully Calculated: %s meaningful tracking points in frames" % len( points )
print "\nMoving on to Depth Mapping"

dmapper = Depth_Map.Depth_Mapper( points )

dmapper.calculate_depth_maps()

print "Sucessfully Calculated %s global points from depth maps" % len( dmapper.global_points )
print "\nMoving onto rendering"

Rendering.render_list( dmapper.global_points, maximum = 1000 )






