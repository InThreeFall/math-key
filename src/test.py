import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 400, 50)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)
        
        self.mainLayout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()

        # 设置布局的间距为0
        self.mainLayout.setSpacing(0)
        self.button_layout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.button_list = []
        self.tipLabel_list = []
        for i in range(5):
            label = QLabel(str(i), self)
            label.setFixedSize(8, 50)  # 减少标签大小以适应窗口
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont('Arial', 10))  # 减小字体大小
            self.tipLabel_list.append(label)
            self.button_layout.addWidget(label)
            
            btn = QPushButton("", self)
            btn.setFixedSize(74, 50)  # 固定按钮大小为74x50
            btn.setFont(QFont('Arial', 10))  # 减小字体大小
            btn.setStyleSheet('background-color: white; color: blue; padding: 0px; margin: 0px;')
            self.button_list.append(btn)
            self.button_layout.addWidget(btn)
        
        self.mainLayout.addLayout(self.button_layout)
        self.setLayout(self.mainLayout)
       
        self.setStyleSheet("background-color: rgba(255,255,255, 80%);")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__updateState)
        self.timer.start(100)

    def __updateState(self):
        # 这里应包含更新状态的逻辑
        pass

# 应用程序主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())