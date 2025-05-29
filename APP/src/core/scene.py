"""
Scene management module for 3D modeling application.
"""

class Scene:
    """
    Represents a 3D scene containing multiple objects.
    """
    
    def __init__(self, name="Untitled"):
        """
        Initialize a new scene.
        
        Args:
            name (str): The name of the scene
        """
        self.name = name
        self.objects = []  # List of Object3D instances
        self.selected_object = None
        self.modified = False
    
    def add_object(self, obj):
        """
        Add an object to the scene.
        
        Args:
            obj: The Object3D instance to add
        """
        self.objects.append(obj)
        self.modified = True
        return obj
    
    def remove_object(self, obj):
        """
        Remove an object from the scene.
        
        Args:
            obj: The Object3D instance to remove
        """
        if obj in self.objects:
            self.objects.remove(obj)
            if self.selected_object == obj:
                self.selected_object = None
            self.modified = True
            return True
        return False
    
    def select_object(self, obj):
        """
        Select an object in the scene.
        
        Args:
            obj: The Object3D instance to select
        """
        if obj in self.objects or obj is None:
            self.selected_object = obj
            return True
        return False
    
    def clear(self):
        """
        Remove all objects from the scene.
        """
        self.objects.clear()
        self.selected_object = None
        self.modified = True
    
    def __len__(self):
        """
        Get the number of objects in the scene.
        """
        return len(self.objects)
