#!/usr/bin/env python
"""
Main entry point for 3D modeling application.
"""
import sys
from PyQt5.QtWidgets import QApplication

from src.gui import MainWindow

def main():
    """
    Main function to start the application.
    """
    # Create application
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    
    # Show window
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
