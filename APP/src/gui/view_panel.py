"""
View panel for 3D modeling application.
"""
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent

from .gl_widget import GLWidget

class ViewPanel(QWidget):
    """
    Panel containing 3D and orthographic views.
    """
    
    def __init__(self, scene):
        """
        Initialize the view panel.
        
        Args:
            scene: The Scene instance to display
        """
        super().__init__()
        
        self.scene = scene
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create view splitter
        splitter = QSplitter(Qt.Vertical)
        
        # Create top splitter (main view)
        top_splitter = QSplitter(Qt.Horizontal)
        
        # Create main 3D view
        self.main_view = GLWidget(self.scene, "perspective")
        top_splitter.addWidget(self.main_view)
        
        # Add top splitter to main splitter
        splitter.addWidget(top_splitter)
        
        # Create bottom splitter (orthographic views)
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        # Create orthographic views
        self.top_view = GLWidget(self.scene, "top")
        self.front_view = GLWidget(self.scene, "front")
        self.side_view = GLWidget(self.scene, "side")
        
        bottom_splitter.addWidget(self.top_view)
        bottom_splitter.addWidget(self.front_view)
        bottom_splitter.addWidget(self.side_view)
        
        # Add bottom splitter to main splitter
        splitter.addWidget(bottom_splitter)
        
        # Set splitter sizes
        splitter.setSizes([int(self.height() * 0.7), int(self.height() * 0.3)])
        
        # Add splitter to layout
        layout.addWidget(splitter)
        
        # Set up update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_view)
        self.update_timer.start(16)  # ~60 FPS
    
    def update_view(self):
        """
        Update all views.
        """
        self.main_view.update()
        self.top_view.update()
        self.front_view.update()
        self.side_view.update()
