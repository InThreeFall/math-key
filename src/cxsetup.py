#coding=utf-8
#cxsetup.py代码
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    'include_files':['../static','../config'],
}

setup(
    name="math-key",
    version="0.0.1",
    description="测试版本",
    options = {"build_exe": build_exe_options},
    author="yysq",
    executables=[Executable("main.py", base=base, icon="../static/icon.ico")]
)
