from myutil import mysqlutil
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import hashlib
# from myutil import res_path
class SignInWidget(QWidget):
    is_admin_signal = pyqtSignal()
    is_student_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """窗口大小，标题和图标"""
        self.resize(900,600)
        self.setWindowTitle('欢迎使用资产管理系统')


        """实例化布局组件"""
        self.Vlayout = QVBoxLayout(self)
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.formlayout = QFormLayout()

        """文本占位符"""
        self.label1 = QLabel("账号: ")
        self.username = ""
        """设置字体方案"""
        labelFont = QFont()
        labelFont.setPixelSize(18)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        """为标签设置字体"""
        self.label1.setFont(labelFont)
        """单行文本框"""
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setFixedHeight(32)
        self.lineEdit1.setFixedWidth(180)
        self.lineEdit1.setFont(lineEditFont)
        self.lineEdit1.setMaxLength(10)

        """表单布局组件"""
        self.formlayout.addRow(self.label1, self.lineEdit1)
        """密码的文本框和输入框"""
        self.label2 = QLabel("密码: ")
        self.label2.setFont(labelFont)
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedHeight(32)
        self.lineEdit2.setFixedWidth(180)
        self.lineEdit2.setMaxLength(16)

        """密码的字体"""
        passwordFont = QFont()
        passwordFont.setPixelSize(10)
        self.lineEdit2.setFont(passwordFont)
        """设置密码方式输入"""
        self.lineEdit2.setEchoMode(QLineEdit.Password)
        """密码表单布局"""
        self.formlayout.addRow(self.label2, self.lineEdit2)
        """登陆按钮"""
        self.signIn = QPushButton("登 录")
        self.signIn.setFixedWidth(80)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)
        """表单布局"""
        self.formlayout.addRow("", self.signIn)
        """欢迎标示"""
        self.label = QLabel("飞行器智能监控系统")
        fontlabel = QFont()
        fontlabel.setPixelSize(30)
        self.label.setFixedWidth(310)
        # self.label.setFixedHeight(80)
        self.label.setFont(fontlabel)
        """标识语布局"""
        self.Hlayout1.addWidget(self.label, Qt.AlignCenter)
        self.widget1 = QWidget()
        self.widget1.setLayout(self.Hlayout1)
        """表单放进组件里"""
        self.widget2 = QWidget()
        self.widget2.setFixedWidth(300)
        self.widget2.setFixedHeight(150)
        self.widget2.setLayout(self.formlayout)
        self.Hlayout2.addWidget(self.widget2, Qt.AlignCenter)
        """完成布局"""
        self.widget = QWidget()
        self.widget.setLayout(self.Hlayout2)
        self.Vlayout.addWidget(self.widget1)
        self.Vlayout.addWidget(self.widget, Qt.AlignTop)

        """点击事件"""
        self.signIn.clicked.connect(self.signInCheck)
        self.lineEdit2.returnPressed.connect(self.signInCheck)
        self.lineEdit1.returnPressed.connect(self.signInCheck)

    def signInCheck(self):
        studentName = self.lineEdit1.text()
        password = self.lineEdit2.text()
        if (studentName == "" or password == ""):
            print(QMessageBox.warning(self, "警告", "账号和密码不可为空!", QMessageBox.Yes, QMessageBox.Yes))
            return
        sql = "select * FROM t_user WHERE username='%s'" % (studentName)
        data = mysqlutil.select_db(sql)
        print(data)
        if (data==()):
            print(QMessageBox.information(self, "提示", "该账号不存在!", QMessageBox.Yes, QMessageBox.Yes))
        else:
            if (studentName == data[0]['username'] and password == data[0]['password']):
                self.username = data[0]['username']
                self.is_admin_signal.emit()
            else:
                print(QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    S = SignInWidget()
    S.show()
    sys.exit(app.exec_())



