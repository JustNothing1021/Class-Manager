import os

def install_packages():
    package = ["dill", "pyqtgraph", "PySide6", "psutil", "typing_extensions", "pyaudio", "colorama", "opencv-python"]
    for i in package:
        os.system(f"pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple {i}")

if __name__ == "__main__":
    install_packages()