from app import ImageProcessingWindow
import sys

from PyQt5.QtWidgets import QApplication

def main():
    
    app = QApplication(sys.argv)
    ip_windows = ImageProcessingWindow()
    ip_windows.show()
    sys.exit(app.exec_()) 



if __name__ == '__main__':
    main()