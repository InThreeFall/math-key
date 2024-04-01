import sys
from PyQt5.QtCore import Qt, QPoint, QEvent, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout

# 桌面底部的状态提示窗口
class StatusBarWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        print('StatusBarWin')

    def initUI(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        # 宽度可以根据需要设置，这里举例使用100px的宽度
        status_width = 100
        # 高度可以根据需要设置，这里举例使用30px的高度
        status_height = 30
        
        # 靠右对齐，离底部一定高度(例如离底部10px)
        self.setGeometry(screen_geometry.width() - status_width - 10, screen_geometry.height() - status_height - 10, status_width, status_height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")

        # 添加一些内容到窗体
        text_label = QLabel('状态提示', self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("QLabel { color : white; }")  # 根据背景颜色调整字体颜色

        self.show()

# 跟随鼠标移动的输入法窗口
class InputWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口的大小
        self.setFixedSize(200, 50)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)

        # 添加一些内容到窗体
        text_label = QLabel('输入法窗口', self)

        text_label.setAlignment(Qt.AlignCenter)


    def followMouse(self, pos):
        # 移动窗口到鼠标位置
        self.move(pos.x(), pos.y() + 20)  # 位置稍微往下偏移，避免阻碍视线
        self.show()


# 运行程序
def main():
    app = QApplication(sys.argv)
    status_bar = StatusBarWin()
    input_win = InputWin()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()