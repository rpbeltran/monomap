

module SinglePoint where

import Numeric.LinearAlgebra
import Common



------------
-- Camera --
------------

--                    rotation        position       FOVX    Resolution
data Camera = Camera (Matrix Double) (Matrix Double) Double (Double, Double) deriving Show

camera :: Double -> (Double, Double) -> Camera
camera fov res = Camera (col [0,1,0]) (col [0,0,0]) fov res

default_camera :: Camera
default_camera = camera 2.094 (1920, 1080)

driven_camera :: Double -> Camera
driven_camera d = Camera (col [0,1,0]) (col [0,d,0]) 2.094 (1920, 1080)



-----------------------
-- 2 Point Technique --
-----------------------

-- Calculate Local:
-- Returns the 3D coordinates representing the position of a point realtive to the position of the robot
-- The output does not take into account the camera angle, but rather gives output in terms of +y being the inline with the direction the camera is facing

calculate_local :: Camera -> (Matrix Double) -> Camera -> (Matrix Double) -> (Matrix Double)
calculate_local (Camera rot p0 fovx (rx, ry) ) l0 (Camera _ p1 _ _ ) l1 = col [y*cos(axy), x, y*sin(axy) ] where

    -- Robot Motion
    dist = sqrt $ (\v -> dot v v) (p1 - p0) -- Distance travelled by robot

    -- Depth Components
    y = dist * ( (1.0/(tan a0)) - (1.0/(tan a1)) )
    x = y / (tan a1)

    -- Angles
    a0 = atan( (sqrt $ dot l0_norm l0_norm ) / f ) -- Alpha_0
    a1 = atan( (sqrt $ dot l1_norm l1_norm ) / f ) -- Alpha_1
    axy = (\p -> atan( p!!1!!0 / p!!0!!0 ) ) $ toLists p1 -- Alpha_xy
    
    -- Normalized positions
    l0_norm = l0 - half_res -- Point 0 with radix shifted to center of image
    l1_norm = l1 - half_res -- Point 1 with radix shifted to center of image

    -- camera properties
    half_res = col [rx/2, ry/2] -- Half resolution of camera (for normalizing l0 and l1)
    f = rx / tan( fovx / 2 ) / 2   -- Focal Length of Camera (in pixels)


calculate_global :: Camera -> (Matrix Double) -> Camera -> (Matrix Double) -> (Matrix Double)
calculate_global cam1@(Camera _ _ _ _ ) l0 cam2@(Camera rot1 p1 _ _ ) l1 = p1 + ( rotmat <> loc ) where
    
    -- Local position of point relative to camera 2
    loc = calculate_local cam1 l0 cam2 l1

    -- Rotation matrix for finding global position of point relative to camera 2
    rotmat = rotation_matrix rot1
    





------------------------------
-- N Point Sprint Technique --
------------------------------
-------------------------------------------
-- N Sprint Stitch Trilaterate Technique --
-------------------------------------------