"""
Control panel for 3D modeling application.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QDoubleSpinBox, QGroupBox, QComboBox, QCheckBox,
    QFormLayout, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSlot

from ..transformations import apply_translation, apply_rotation, apply_scaling

class ControlPanel(QWidget):
    """
    Panel for controlling object transformations and properties.
    """
    
    def __init__(self, scene):
        """
        Initialize the control panel.
        
        Args:
            scene: The Scene instance to control
        """
        super().__init__()
        
        self.scene = scene
        self.transform_mode = "translate"  # Default mode
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create object list
        self.create_object_list(layout)
        
        # Create transformation controls
        self.create_transform_controls(layout)
        
        # Create object properties
        self.create_object_properties(layout)
        
        # Add stretch to push controls to the top
        layout.addStretch()
    
    def create_object_list(self, layout):
        """
        Create the object list widget.
        
        Args:
            layout: The layout to add the widget to
        """
        # Create group box
        group_box = QGroupBox("Objects")
        group_layout = QVBoxLayout()
        
        # Create list widget
        self.object_list = QListWidget()
        self.object_list.itemClicked.connect(self.on_object_selected)
        group_layout.addWidget(self.object_list)
        
        # Set group box layout
        group_box.setLayout(group_layout)
        
        # Add to main layout
        layout.addWidget(group_box)
    
    def create_transform_controls(self, layout):
        """
        Create the transformation controls.
        
        Args:
            layout: The layout to add the controls to
        """
        # Create group box
        group_box = QGroupBox("Transformations")
        group_layout = QVBoxLayout()
        
        # Create mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Translate", "Rotate", "Scale"])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        group_layout.addLayout(mode_layout)
        
        # Create transformation controls
        transform_layout = QFormLayout()
        
        # X control
        x_layout = QHBoxLayout()
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setRange(-100, 100)
        self.x_slider.setValue(0)
        self.x_slider.valueChanged.connect(self.on_x_changed)
        x_layout.addWidget(self.x_slider)
        
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-10.0, 10.0)
        self.x_spin.setSingleStep(0.1)
        self.x_spin.setValue(0.0)
        self.x_spin.valueChanged.connect(self.on_x_spin_changed)
        x_layout.addWidget(self.x_spin)
        
        transform_layout.addRow("X:", x_layout)
        
        # Y control
        y_layout = QHBoxLayout()
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setRange(-100, 100)
        self.y_slider.setValue(0)
        self.y_slider.valueChanged.connect(self.on_y_changed)
        y_layout.addWidget(self.y_slider)
        
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-10.0, 10.0)
        self.y_spin.setSingleStep(0.1)
        self.y_spin.setValue(0.0)
        self.y_spin.valueChanged.connect(self.on_y_spin_changed)
        y_layout.addWidget(self.y_spin)
        
        transform_layout.addRow("Y:", y_layout)
        
        # Z control
        z_layout = QHBoxLayout()
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setRange(-100, 100)
        self.z_slider.setValue(0)
        self.z_slider.valueChanged.connect(self.on_z_changed)
        z_layout.addWidget(self.z_slider)
        
        self.z_spin = QDoubleSpinBox()
        self.z_spin.setRange(-10.0, 10.0)
        self.z_spin.setSingleStep(0.1)
        self.z_spin.setValue(0.0)
        self.z_spin.valueChanged.connect(self.on_z_spin_changed)
        z_layout.addWidget(self.z_spin)
        
        transform_layout.addRow("Z:", z_layout)
        
        group_layout.addLayout(transform_layout)
        
        # Add apply button
        apply_button = QPushButton("Apply Transformation")
        apply_button.clicked.connect(self.apply_transformation)
        group_layout.addWidget(apply_button)
        
        # Set group box layout
        group_box.setLayout(group_layout)
        
        # Add to main layout
        layout.addWidget(group_box)
    
    def create_object_properties(self, layout):
        """
        Create the object properties controls.
        
        Args:
            layout: The layout to add the controls to
        """
        # Create group box
        group_box = QGroupBox("Object Properties")
        group_layout = QFormLayout()
        
        # Create name field
        self.name_edit = QComboBox()
        self.name_edit.setEditable(True)
        self.name_edit.currentTextChanged.connect(self.on_name_changed)
        group_layout.addRow("Name:", self.name_edit)
        
        # Create visibility checkbox
        self.visible_check = QCheckBox("Visible")
        self.visible_check.setChecked(True)
        self.visible_check.stateChanged.connect(self.on_visible_changed)
        group_layout.addRow("", self.visible_check)
        
        # Create wireframe checkbox
        self.wireframe_check = QCheckBox("Wireframe")
        self.wireframe_check.setChecked(False)
        self.wireframe_check.stateChanged.connect(self.on_wireframe_changed)
        group_layout.addRow("", self.wireframe_check)
        
        # Set group box layout
        group_box.setLayout(group_layout)
        
        # Add to main layout
        layout.addWidget(group_box)
    
    def update_controls(self):
        """
        Update the controls to reflect the current scene state.
        """
        # Update object list
        self.update_object_list()
        
        # Update transformation controls
        self.update_transform_controls()
        
        # Update object properties
        self.update_object_properties()
    
    def update_object_list(self):
        """
        Update the object list.
        """
        # Clear the list
        self.object_list.clear()
        
        # Add objects to the list
        for obj in self.scene.objects:
            item = QListWidgetItem(obj.name)
            item.setData(Qt.UserRole, obj.id)
            self.object_list.addItem(item)
            
            # Select the current object
            if self.scene.selected_object == obj:
                self.object_list.setCurrentItem(item)
    
    def update_transform_controls(self):
        """
        Update the transformation controls.
        """
        # Block signals to prevent feedback loops
        self.x_slider.blockSignals(True)
        self.y_slider.blockSignals(True)
        self.z_slider.blockSignals(True)
        self.x_spin.blockSignals(True)
        self.y_spin.blockSignals(True)
        self.z_spin.blockSignals(True)
        
        # Reset controls
        self.x_slider.setValue(0)
        self.y_slider.setValue(0)
        self.z_slider.setValue(0)
        self.x_spin.setValue(0.0)
        self.y_spin.setValue(0.0)
        self.z_spin.setValue(0.0)
        
        # Unblock signals
        self.x_slider.blockSignals(False)
        self.y_slider.blockSignals(False)
        self.z_slider.blockSignals(False)
        self.x_spin.blockSignals(False)
        self.y_spin.blockSignals(False)
        self.z_spin.blockSignals(False)
    
    def update_object_properties(self):
        """
        Update the object properties controls.
        """
        # Block signals to prevent feedback loops
        self.name_edit.blockSignals(True)
        self.visible_check.blockSignals(True)
        self.wireframe_check.blockSignals(True)
        
        # Get selected object
        obj = self.scene.selected_object
        
        if obj:
            # Update name
            self.name_edit.setCurrentText(obj.name)
            
            # Update visibility
            self.visible_check.setChecked(obj.visible)
            
            # Update wireframe
            self.wireframe_check.setChecked(obj.wireframe)
            
            # Enable controls
            self.name_edit.setEnabled(True)
            self.visible_check.setEnabled(True)
            self.wireframe_check.setEnabled(True)
        else:
            # Disable controls
            self.name_edit.setEnabled(False)
            self.visible_check.setEnabled(False)
            self.wireframe_check.setEnabled(False)
        
        # Unblock signals
        self.name_edit.blockSignals(False)
        self.visible_check.blockSignals(False)
        self.wireframe_check.blockSignals(False)
    
    def set_transform_mode(self, mode):
        """
        Set the current transformation mode.
        
        Args:
            mode (str): Transformation mode ("translate", "rotate", "scale")
        """
        self.transform_mode = mode
        
        # Update combo box
        if mode == "translate":
            self.mode_combo.setCurrentIndex(0)
        elif mode == "rotate":
            self.mode_combo.setCurrentIndex(1)
        elif mode == "scale":
            self.mode_combo.setCurrentIndex(2)
        
        # Update slider ranges and spin box settings
        if mode == "translate":
            self.x_slider.setRange(-100, 100)
            self.y_slider.setRange(-100, 100)
            self.z_slider.setRange(-100, 100)
            self.x_spin.setRange(-10.0, 10.0)
            self.y_spin.setRange(-10.0, 10.0)
            self.z_spin.setRange(-10.0, 10.0)
            self.x_spin.setSingleStep(0.1)
            self.y_spin.setSingleStep(0.1)
            self.z_spin.setSingleStep(0.1)
        elif mode == "rotate":
            self.x_slider.setRange(-180, 180)
            self.y_slider.setRange(-180, 180)
            self.z_slider.setRange(-180, 180)
            self.x_spin.setRange(-180.0, 180.0)
            self.y_spin.setRange(-180.0, 180.0)
            self.z_spin.setRange(-180.0, 180.0)
            self.x_spin.setSingleStep(1.0)
            self.y_spin.setSingleStep(1.0)
            self.z_spin.setSingleStep(1.0)
        elif mode == "scale":
            self.x_slider.setRange(-100, 100)
            self.y_slider.setRange(-100, 100)
            self.z_slider.setRange(-100, 100)
            self.x_spin.setRange(0.1, 10.0)
            self.y_spin.setRange(0.1, 10.0)
            self.z_spin.setRange(0.1, 10.0)
            self.x_spin.setSingleStep(0.1)
            self.y_spin.setSingleStep(0.1)
            self.z_spin.setSingleStep(0.1)
    
    @pyqtSlot(QListWidgetItem)
    def on_object_selected(self, item):
        """
        Handle object selection.
        
        Args:
            item (QListWidgetItem): Selected item
        """
        # Get object ID
        obj_id = item.data(Qt.UserRole)
        
        # Find object in scene
        for obj in self.scene.objects:
            if obj.id == obj_id:
                self.scene.select_object(obj)
                break
        
        # Update controls
        self.update_object_properties()
    
    @pyqtSlot(int)
    def on_mode_changed(self, index):
        """
        Handle mode selection.
        
        Args:
            index (int): Selected index
        """
        if index == 0:
            self.set_transform_mode("translate")
        elif index == 1:
            self.set_transform_mode("rotate")
        elif index == 2:
            self.set_transform_mode("scale")
    
    @pyqtSlot(int)
    def on_x_changed(self, value):
        """
        Handle X slider change.
        
        Args:
            value (int): Slider value
        """
        # Update spin box
        if self.transform_mode == "translate":
            self.x_spin.setValue(value / 10.0)
        elif self.transform_mode == "rotate":
            self.x_spin.setValue(float(value))
        elif self.transform_mode == "scale":
            self.x_spin.setValue(1.0 + value / 100.0)
    
    @pyqtSlot(int)
    def on_y_changed(self, value):
        """
        Handle Y slider change.
        
        Args:
            value (int): Slider value
        """
        # Update spin box
        if self.transform_mode == "translate":
            self.y_spin.setValue(value / 10.0)
        elif self.transform_mode == "rotate":
            self.y_spin.setValue(float(value))
        elif self.transform_mode == "scale":
            self.y_spin.setValue(1.0 + value / 100.0)
    
    @pyqtSlot(int)
    def on_z_changed(self, value):
        """
        Handle Z slider change.
        
        Args:
            value (int): Slider value
        """
        # Update spin box
        if self.transform_mode == "translate":
            self.z_spin.setValue(value / 10.0)
        elif self.transform_mode == "rotate":
            self.z_spin.setValue(float(value))
        elif self.transform_mode == "scale":
            self.z_spin.setValue(1.0 + value / 100.0)
    
    @pyqtSlot(float)
    def on_x_spin_changed(self, value):
        """
        Handle X spin box change.
        
        Args:
            value (float): Spin box value
        """
        # Update slider
        if self.transform_mode == "translate":
            self.x_slider.setValue(int(value * 10.0))
        elif self.transform_mode == "rotate":
            self.x_slider.setValue(int(value))
        elif self.transform_mode == "scale":
            self.x_slider.setValue(int((value - 1.0) * 100.0))
    
    @pyqtSlot(float)
    def on_y_spin_changed(self, value):
        """
        Handle Y spin box change.
        
        Args:
            value (float): Spin box value
        """
        # Update slider
        if self.transform_mode == "translate":
            self.y_slider.setValue(int(value * 10.0))
        elif self.transform_mode == "rotate":
            self.y_slider.setValue(int(value))
        elif self.transform_mode == "scale":
            self.y_slider.setValue(int((value - 1.0) * 100.0))
    
    @pyqtSlot(float)
    def on_z_spin_changed(self, value):
        """
        Handle Z spin box change.
        
        Args:
            value (float): Spin box value
        """
        # Update slider
        if self.transform_mode == "translate":
            self.z_slider.setValue(int(value * 10.0))
        elif self.transform_mode == "rotate":
            self.z_slider.setValue(int(value))
        elif self.transform_mode == "scale":
            self.z_slider.setValue(int((value - 1.0) * 100.0))
    
    @pyqtSlot()
    def apply_transformation(self):
        """
        Apply the current transformation.
        """
        # Get selected object
        obj = self.scene.selected_object
        
        if obj:
            # Get transformation values
            x = self.x_spin.value()
            y = self.y_spin.value()
            z = self.z_spin.value()
            
            # Apply transformation
            if self.transform_mode == "translate":
                apply_translation(obj, x, y, z)
            elif self.transform_mode == "rotate":
                apply_rotation(obj, x, y, z)
            elif self.transform_mode == "scale":
                # Scale values are relative to current scale
                apply_scaling(obj, x, y, z)
            
            # Reset controls
            self.update_transform_controls()
    
    @pyqtSlot(str)
    def on_name_changed(self, name):
        """
        Handle object name change.
        
        Args:
            name (str): New name
        """
        # Get selected object
        obj = self.scene.selected_object
        
        if obj:
            # Update object name
            obj.name = name
            
            # Update object list
            self.update_object_list()
    
    @pyqtSlot(int)
    def on_visible_changed(self, state):
        """
        Handle object visibility change.
        
        Args:
            state (int): Checkbox state
        """
        # Get selected object
        obj = self.scene.selected_object
        
        if obj:
            # Update object visibility
            obj.visible = (state == Qt.Checked)
    
    @pyqtSlot(int)
    def on_wireframe_changed(self, state):
        """
        Handle object wireframe mode change.
        
        Args:
            state (int): Checkbox state
        """
        # Get selected object
        obj = self.scene.selected_object
        
        if obj:
            # Update object wireframe mode
            obj.wireframe = (state == Qt.Checked)
