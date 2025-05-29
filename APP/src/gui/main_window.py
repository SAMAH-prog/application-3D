"""
Main window for 3D modeling application.
"""
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QMenu, QToolBar, QDockWidget,
    QSplitter, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from .view_panel import ViewPanel
from .control_panel import ControlPanel
from ..core.scene import Scene
from ..utils.file_io import save_scene, save_obj, load_obj

class MainWindow(QMainWindow):
    """
    Main application window.
    """
    
    def __init__(self):
        """
        Initialize the main window.
        """
        super().__init__()
        
        # Initialize scene
        self.scene = Scene()
        
        # Setup UI
        self.setWindowTitle("3D Modeling Application")
        self.setMinimumSize(1024, 768)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget
        self.create_central_widget()
        
        # Create dock widgets
        self.create_dock_widgets()
        
        # Show the window
        self.show()
    
    def create_menu_bar(self):
        """
        Create the application menu bar.
        """
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_scene)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Quit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = self.menuBar().addMenu("&Edit")
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)
        
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)
        
        delete_action = QAction("&Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_selected)
        edit_menu.addAction(delete_action)
        
        # Primitives menu
        primitives_menu = self.menuBar().addMenu("&Primitives")
        
        cube_action = QAction("&Cube", self)
        cube_action.triggered.connect(lambda: self.add_primitive("cube"))
        primitives_menu.addAction(cube_action)
        
        sphere_action = QAction("&Sphere", self)
        sphere_action.triggered.connect(lambda: self.add_primitive("sphere"))
        primitives_menu.addAction(sphere_action)
        
        cylinder_action = QAction("C&ylinder", self)
        cylinder_action.triggered.connect(lambda: self.add_primitive("cylinder"))
        primitives_menu.addAction(cylinder_action)
        
        cone_action = QAction("Co&ne", self)
        cone_action.triggered.connect(lambda: self.add_primitive("cone"))
        primitives_menu.addAction(cone_action)
        
        torus_action = QAction("&Torus", self)
        torus_action.triggered.connect(lambda: self.add_primitive("torus"))
        primitives_menu.addAction(torus_action)
        
        # View menu
        view_menu = self.menuBar().addMenu("&View")
        
        wireframe_action = QAction("&Wireframe", self)
        wireframe_action.setCheckable(True)
        wireframe_action.triggered.connect(self.toggle_wireframe)
        view_menu.addAction(wireframe_action)
    
    def create_toolbar(self):
        """
        Create the application toolbar.
        """
        # Main toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        
        # Add primitive actions
        cube_action = QAction("Cube", self)
        cube_action.triggered.connect(lambda: self.add_primitive("cube"))
        toolbar.addAction(cube_action)
        
        sphere_action = QAction("Sphere", self)
        sphere_action.triggered.connect(lambda: self.add_primitive("sphere"))
        toolbar.addAction(sphere_action)
        
        cylinder_action = QAction("Cylinder", self)
        cylinder_action.triggered.connect(lambda: self.add_primitive("cylinder"))
        toolbar.addAction(cylinder_action)
        
        cone_action = QAction("Cone", self)
        cone_action.triggered.connect(lambda: self.add_primitive("cone"))
        toolbar.addAction(cone_action)
        
        torus_action = QAction("Torus", self)
        torus_action.triggered.connect(lambda: self.add_primitive("torus"))
        toolbar.addAction(torus_action)
        
        toolbar.addSeparator()
        
        # Add transformation actions
        translate_action = QAction("Translate", self)
        translate_action.triggered.connect(lambda: self.set_transform_mode("translate"))
        toolbar.addAction(translate_action)
        
        rotate_action = QAction("Rotate", self)
        rotate_action.triggered.connect(lambda: self.set_transform_mode("rotate"))
        toolbar.addAction(rotate_action)
        
        scale_action = QAction("Scale", self)
        scale_action.triggered.connect(lambda: self.set_transform_mode("scale"))
        toolbar.addAction(scale_action)
    
    def create_central_widget(self):
        """
        Create the central widget with view panels.
        """
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Create view panel
        self.view_panel = ViewPanel(self.scene)
        main_splitter.addWidget(self.view_panel)
        
        # Set as central widget
        self.setCentralWidget(main_splitter)
    
    def create_dock_widgets(self):
        """
        Create dock widgets for controls.
        """
        # Create control panel dock widget
        control_dock = QDockWidget("Controls", self)
        control_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.control_panel = ControlPanel(self.scene)
        control_dock.setWidget(self.control_panel)
        
        self.addDockWidget(Qt.RightDockWidgetArea, control_dock)
    
    def new_scene(self):
        """
        Create a new scene.
        """
        if self.scene.modified:
            reply = QMessageBox.question(
                self, "New Scene",
                "Do you want to save the current scene before creating a new one?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return
        
        self.scene.clear()
        self.view_panel.update_view()
        self.control_panel.update_controls()
    
    def open_file(self):
        """
        Open a file.
        """
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "OBJ Files (*.obj);;All Files (*)"
        )
        
        if filename:
            try:
                obj = load_obj(filename)
                self.scene.add_object(obj)
                self.view_panel.update_view()
                self.control_panel.update_controls()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
    
    def save_file(self):
        """
        Save the current scene or selected object.
        """
        if self.scene.selected_object:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Object", "", "OBJ Files (*.obj);;All Files (*)"
            )
            
            if filename:
                try:
                    save_obj(filename, self.scene.selected_object)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
        else:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Scene", "", "Scene Files (*.scene);;All Files (*)"
            )
            
            if filename:
                try:
                    save_scene(filename, self.scene)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    
    def delete_selected(self):
        """
        Delete the selected object.
        """
        if self.scene.selected_object:
            self.scene.remove_object(self.scene.selected_object)
            self.view_panel.update_view()
            self.control_panel.update_controls()
    
    def add_primitive(self, primitive_type):
        """
        Add a primitive to the scene.
        
        Args:
            primitive_type (str): Type of primitive to add
        """
        from ..primitives import (
            create_cube, create_sphere, create_cylinder,
            create_cone, create_torus
        )
        
        obj = None
        
        if primitive_type == "cube":
            obj = create_cube()
        elif primitive_type == "sphere":
            obj = create_sphere()
        elif primitive_type == "cylinder":
            obj = create_cylinder()
        elif primitive_type == "cone":
            obj = create_cone()
        elif primitive_type == "torus":
            obj = create_torus()
        
        if obj:
            self.scene.add_object(obj)
            self.scene.select_object(obj)
            self.view_panel.update_view()
            self.control_panel.update_controls()
    
    def toggle_wireframe(self, checked):
        """
        Toggle wireframe mode for the selected object or all objects.
        
        Args:
            checked (bool): Whether wireframe mode is enabled
        """
        if self.scene.selected_object:
            self.scene.selected_object.wireframe = checked
        else:
            for obj in self.scene.objects:
                obj.wireframe = checked
        
        self.view_panel.update_view()
    
    def set_transform_mode(self, mode):
        """
        Set the current transformation mode.
        
        Args:
            mode (str): Transformation mode ("translate", "rotate", "scale")
        """
        self.control_panel.set_transform_mode(mode)
