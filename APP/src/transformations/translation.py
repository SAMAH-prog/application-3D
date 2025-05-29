"""
Translation transformation for 3D modeling application.
"""
import numpy as np

def apply_translation(obj, dx=0.0, dy=0.0, dz=0.0):
    """
    Apply a translation transformation to a 3D object.
    
    Args:
        obj: The Object3D instance to transform
        dx (float): Translation along X axis
        dy (float): Translation along Y axis
        dz (float): Translation along Z axis
    """
    # Update the object's position
    obj.position += np.array([dx, dy, dz], dtype=np.float32)
    
    return obj
