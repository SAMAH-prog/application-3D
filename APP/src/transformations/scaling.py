"""
Scaling transformation for 3D modeling application.
"""
import numpy as np

def apply_scaling(obj, sx=1.0, sy=1.0, sz=1.0):
    """
    Apply a scaling transformation to a 3D object.
    
    Args:
        obj: The Object3D instance to transform
        sx (float): Scaling factor along X axis
        sy (float): Scaling factor along Y axis
        sz (float): Scaling factor along Z axis
    """
    # Update the object's scale
    obj.scale *= np.array([sx, sy, sz], dtype=np.float32)
    
    return obj
