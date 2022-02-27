import sys
from PyQt5.QtWidgets import *
import qdarkstyle
from login.SignIn import SignInWidget
from login.SignUp import SignUpWidget
import sip
from MyClass import MyClass


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.widget = SignInWidget()
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用飞行器智能监控系统")
        self.setCentralWidget(self.widget)
        bar = self.menuBar()
        self.Menu = bar.addMenu("菜单栏")
        self.signUpAction = QAction("注册", self)
        self.signInAction = QAction("登录", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.quitAction = QAction("退出", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)
        self.signUpAction.setEnabled(True)

        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)
        self.widget.is_admin_signal.connect(self.adminSignIn)
        # self.widget.is_student_signal[str].connect(self.studentSignIn)
        self.Menu.triggered[QAction].connect(self.menuTriggered)
    # 删除登录界面，进入主界面
    def adminSignIn(self):
        username = self.widget.username
        print(username)
        sip.delete(self.widget)
        sip.delete(self.Menu)
        self.widget = MyClass(username)
        self.resize(1500, 900)
        self.setCentralWidget(self.widget)

    # 删除注册界面，进入登录界面
    def adminSignup(self):
        sip.delete(self.widget)
        sip.delete(self.Menu)
        self.layout = QHBoxLayout()
        self.widget = SignInWidget()
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用飞行器智能监控系统")
        self.setCentralWidget(self.widget)
        bar = self.menuBar()
        self.Menu = bar.addMenu("菜单栏")
        self.signUpAction = QAction("注册", self)
        self.signInAction = QAction("登录", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.quitAction = QAction("退出", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)
        self.signUpAction.setEnabled(True)

        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)
        self.widget.is_admin_signal.connect(self.adminSignIn)
        # self.widget.is_student_signal[str].connect(self.studentSignIn)
        self.Menu.triggered[QAction].connect(self.menuTriggered)


    def menuTriggered(self, q):
        if (q.text() == "注册"):
            sip.delete(self.widget)
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            # self.widget.student_signup_signal[str].connect(self.studentSignIn)
            self.widget.student_signup_signal[str].connect(self.adminSignup)

            self.signUpAction.setEnabled(False)

            self.signInAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            # self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)

            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            # self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)

            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出"):
            qApp = QApplication.instance()
            qApp.quit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())
