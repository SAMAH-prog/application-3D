"""
OpenGL utilities for 3D modeling application.
"""
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

def setup_lighting():
    """
    Setup basic lighting for the 3D scene.
    """
    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Set light properties
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Set material properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)

def setup_viewport(width, height):
    """
    Setup the viewport and projection matrix.
    
    Args:
        width (int): Viewport width
        height (int): Viewport height
    """
    # Prevent division by zero
    if height == 0:
        height = 1
    
    # Set viewport to window dimensions
    glViewport(0, 0, width, height)
    
    # Set perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)
    
    # Switch back to modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_grid(size=10, step=1):
    """
    Draw a grid on the XZ plane.
    
    Args:
        size (int): Half-size of the grid
        step (int): Step size between grid lines
    """
    # Save current attributes
    glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT)
    
    # Disable lighting for the grid
    glDisable(GL_LIGHTING)
    
    # Set grid color
    glColor3f(0.5, 0.5, 0.5)
    
    # Enable line stipple for a dashed pattern
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0xAAAA)
    
    # Draw grid lines
    glBegin(GL_LINES)
    
    # X lines
    for i in range(-size, size + 1, step):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
    
    # Z lines
    for i in range(-size, size + 1, step):
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)
    
    glEnd()
    
    # Draw coordinate axes with solid lines
    glDisable(GL_LINE_STIPPLE)
    glLineWidth(2.0)
    
    # X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(size, 0, 0)
    glEnd()
    
    # Y axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(0, size, 0)
    glEnd()
    
    # Z axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, size)
    glEnd()
    
    # Restore attributes
    glPopAttrib()

def draw_object(obj):
    """
    Draw a 3D object.
    
    Args:
        obj: The Object3D instance to draw
    """
    if not obj.visible or len(obj.points) == 0:
        return
    
    # Save current matrix
    glPushMatrix()
    
    # Apply object's transformation matrix
    transform = obj.get_transformation_matrix()
    glMultMatrixf(transform.T)
    
    # Set rendering mode
    if obj.wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Draw each face
    for face in obj.faces:
        # Set face color if specified, otherwise use object color
        color = face.couleur if face.couleur else obj.color
        glColor3f(*color)
        
        # Calculate face normal for lighting
        normal = face.calculate_normal(obj.points)
        
        # Draw the face
        if face.nb_sommets == 3:  # Triangle
            glBegin(GL_TRIANGLES)
        elif face.nb_sommets == 4:  # Quad
            glBegin(GL_QUADS)
        else:  # Polygon
            glBegin(GL_POLYGON)
        
        # Set normal for the entire face
        glNormal3f(normal[0], normal[1], normal[2])
        
        # Add vertices
        for idx in face.indices:
            vertex = obj.points[idx]
            glVertex3f(vertex[0], vertex[1], vertex[2])
        
        glEnd()
    
    # Restore polygon mode
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Restore matrix
    glPopMatrix()
