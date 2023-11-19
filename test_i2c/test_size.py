from PyQt5.QtWidgets import QApplication

app = QApplication([])

# Get the primary screen
primary_screen = app.primaryScreen()

# Get the geometry of the primary screen
screen_geometry = primary_screen.geometry()

# Print the width and height of the screen
print(f"Screen Size: {screen_geometry.width()}x{screen_geometry.height()} pixels")

app.exec()
