 

module ProjectionCamera ( camera, rotate_by, rotate_to, translate_by_global, translate_by_local, translate_to, project ) where

import Numeric.LinearAlgebra

--					  rotation        position
data Camera = Camera (Matrix Double) (Matrix Double) deriving Show

-- camera
camera :: Camera
camera = Camera (ident 3) (col [0,0,0] )

-- camera matrix
camera_matrix :: (Camera) -> (Matrix Double)
camera_matrix (Camera rot pos) = rot ||| pos

-- Rotations
rotate_by :: Camera -> [Double] -> Camera
rotate_by (Camera cam_rot cam_pos ) rotations = Camera ( rot_mat rotations <> cam_rot ) cam_pos

rotate_to :: Camera -> [Double] -> Camera
rotate_to (Camera _ cam_pos ) rotations = Camera (rot_mat rotations) cam_pos

rot_mat :: [Double] -> (Matrix Double)
rot_mat [y,p,r] = ( rot_roll <> rot_pitch <> rot_yaw ) where
    rot_yaw   = matrix 3 [ 1, 0, 0, 0, cos(y), -sin(y), 0, sin(y), cos(y) ]
    rot_pitch = matrix 3 [ cos(p), 0, sin(p), 0, 1, 0, -sin(p), 0, cos(p) ]
    rot_roll  = matrix 3 [ cos(r), -sin(r), 0, sin(r), cos(r), 0, 0, 0, 1 ]

-- Translations
translate_by_global :: Camera -> [Double] -> Camera
translate_by_global (Camera cam_rot cam_pos ) = Camera cam_rot . (+cam_pos) . col

translate_to :: Camera -> [Double] -> Camera
translate_to (Camera cam_rot _ ) = Camera ( cam_rot ) . col

translate_by_local :: Camera -> [Double] -> Camera
translate_by_local (Camera cam_rot cam_pos ) = Camera cam_rot . (+cam_pos) . (cam_rot <>) . col

-- Projections
project :: Camera -> [Double] -> (Matrix Double)
project cam glob = (camera_matrix cam <>) . col $ glob ++ [1]

