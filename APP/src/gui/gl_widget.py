"""
OpenGL widget for 3D modeling application.
"""
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent

from OpenGL.GL import *
from OpenGL.GLU import *

from ..utils.gl_utils import setup_lighting, setup_viewport, draw_grid, draw_object

class GLWidget(QOpenGLWidget):
    """
    OpenGL widget for rendering 3D scenes.
    """
    
    def __init__(self, scene, view_type="perspective"):
        """
        Initialize the OpenGL widget.
        
        Args:
            scene: The Scene instance to render
            view_type (str): Type of view ("perspective", "top", "front", "side")
        """
        super().__init__()
        
        self.scene = scene
        self.view_type = view_type
        
        # Camera parameters
        self.camera_distance = 5.0
        self.camera_rotation_x = 30.0
        self.camera_rotation_y = 45.0
        self.camera_target = np.array([0.0, 0.0, 0.0])
        
        # Mouse tracking
        self.last_pos = QPoint()
        self.setMouseTracking(True)
        
        # Set focus policy to accept keyboard input
        self.setFocusPolicy(Qt.StrongFocus)
    
    def initializeGL(self):
        """
        Initialize OpenGL settings.
        """
        # Set clear color (background)
        glClearColor(0.2, 0.2, 0.2, 1.0)
        
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        # Enable backface culling
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        
        # Enable smooth shading
        glShadeModel(GL_SMOOTH)
        
        # Setup lighting
        setup_lighting()
    
    def resizeGL(self, width, height):
        """
        Handle widget resize events.
        
        Args:
            width (int): New width
            height (int): New height
        """
        setup_viewport(width, height)
    
    def paintGL(self):
        """
        Render the scene.
        """
        # Clear the buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Set up camera based on view type
        if self.view_type == "perspective":
            # Position camera
            eye_x = self.camera_distance * np.sin(np.radians(self.camera_rotation_y)) * np.cos(np.radians(self.camera_rotation_x))
            eye_y = self.camera_distance * np.sin(np.radians(self.camera_rotation_x))
            eye_z = self.camera_distance * np.cos(np.radians(self.camera_rotation_y)) * np.cos(np.radians(self.camera_rotation_x))
            
            gluLookAt(
                eye_x, eye_y, eye_z,  # Eye position
                self.camera_target[0], self.camera_target[1], self.camera_target[2],  # Target
                0.0, 1.0, 0.0  # Up vector
            )
        elif self.view_type == "top":
            # Top view (looking down Y axis)
            gluLookAt(
                0.0, 10.0, 0.0,  # Eye position
                0.0, 0.0, 0.0,   # Target
                0.0, 0.0, 1.0    # Up vector
            )
        elif self.view_type == "front":
            # Front view (looking along Z axis)
            gluLookAt(
                0.0, 0.0, 10.0,  # Eye position
                0.0, 0.0, 0.0,   # Target
                0.0, 1.0, 0.0    # Up vector
            )
        elif self.view_type == "side":
            # Side view (looking along X axis)
            gluLookAt(
                10.0, 0.0, 0.0,  # Eye position
                0.0, 0.0, 0.0,   # Target
                0.0, 1.0, 0.0    # Up vector
            )
        
        # Draw grid
        draw_grid()
        
        # Draw objects
        for obj in self.scene.objects:
            draw_object(obj)
        
        # Draw selection highlight
        if self.scene.selected_object:
            # Save attributes
            glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LINE_BIT)
            
            # Disable lighting for the highlight
            glDisable(GL_LIGHTING)
            
            # Set highlight color and line width
            glColor3f(1.0, 1.0, 0.0)  # Yellow
            glLineWidth(2.0)
            
            # Enable stipple for dashed lines
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, 0xF0F0)
            
            # Draw wireframe
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            draw_object(self.scene.selected_object)
            
            # Restore attributes
            glPopAttrib()
    
    def mousePressEvent(self, event):
        """
        Handle mouse press events.
        
        Args:
            event (QMouseEvent): Mouse event
        """
        self.last_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        """
        Handle mouse move events.
        
        Args:
            event (QMouseEvent): Mouse event
        """
        if event.buttons() & Qt.LeftButton and self.view_type == "perspective":
            # Rotate camera
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()
            
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x += dy * 0.5
            
            # Limit vertical rotation
            self.camera_rotation_x = max(-89.0, min(89.0, self.camera_rotation_x))
            
            self.update()
        elif event.buttons() & Qt.MiddleButton and self.view_type == "perspective":
            # Pan camera
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()
            
            # Calculate pan direction based on camera orientation
            right_x = np.sin(np.radians(self.camera_rotation_y + 90))
            right_z = np.cos(np.radians(self.camera_rotation_y + 90))
            
            # Pan horizontally
            self.camera_target[0] -= right_x * dx * 0.01
            self.camera_target[2] -= right_z * dx * 0.01
            
            # Pan vertically
            self.camera_target[1] += dy * 0.01
            
            self.update()
        
        self.last_pos = event.pos()
    
    def wheelEvent(self, event):
        """
        Handle mouse wheel events.
        
        Args:
            event (QWheelEvent): Wheel event
        """
        if self.view_type == "perspective":
            # Zoom camera
            delta = event.angleDelta().y()
            self.camera_distance -= delta * 0.01
            
            # Limit zoom
            self.camera_distance = max(0.1, min(20.0, self.camera_distance))
            
            self.update()
