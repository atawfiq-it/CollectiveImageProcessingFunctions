from app import ImageProcessingWindow
import sys
from PyQt5.QtWidgets import QApplication

#The main function that runs the whole app
def main():
    app = QApplication(sys.argv)
    ip_windows = ImageProcessingWindow()
    ip_windows.showMaximized()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()