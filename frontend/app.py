
def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    from frontend.views.MainWindow import MainWindow

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
