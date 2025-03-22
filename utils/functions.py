import cv2
import pygame
import sys
import time
import functools
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QMessageBox
from typing import Callable, Literal
from threading import Thread
from utils.basetypes import Base
def addrof(obj) -> str:
    "获取对象的内存地址"
    return "0x" + hex(id(obj))[2:].zfill(16).upper()

def mat_to_pixmap(mat: cv2.Mat) -> QPixmap:
    """把一个cv2.Mat对象转换为一个QPixmap对象"""
    height, width, channels = mat.shape
    bytes_per_line = channels * width
    qimage = QImage(mat.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap




def repeat(count):
    """装饰器，用于重复执行函数

    :param func: 要装饰的函数
    :param count: 重复执行的次数
    :return: 装饰后的函数
    
    实例
    >>> @repeat(3)
    ... def func():
    ...     print("wdnmd")
    >>> # 这样的话func这个函数每次被调用之后就会被重复执行3次
    >>> func()
    wdnmd
    wdnmd
    wdnmd
    """
    def executor(func):
        def wrapper(*args, **kwargs):
            for _ in range(count):
                func(*args, **kwargs)
        return wrapper
    return executor


nl = "\n"
"换行符（在3.8.10的f-string里面有奇效）"




pygame.mixer.init()
# 初始化pygame的混音器

def play_sound(filename, volume=1):
    "播放声音"
    Thread(target=_play_sound, args=(filename, volume), daemon=True, name="SoundPlayerThread").start()

def _play_sound(filename, volume=1, loop:int=0, fade_ms:int=0):
    "播放声音"
    try:
        sound = pygame.mixer.Sound(filename)
        sound.set_volume(volume)
        sound.play(loops=loop, fade_ms=fade_ms)
    except:
        Base.log_exc("播放声音失败")


def play_music(filename:str, volume:float=0.5, loop:int=0, fade_ms:int=0):
    "播放音乐"
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=loop, fade_ms=fade_ms)
    except:
        Base.log_exc("播放音乐失败")

def stop_music():
    "停止音乐"
    pygame.mixer.music.stop()


def canbe(value, _class:type):
        "检查一个数据是否能作为另一个类型，比如can_be(\"11.4514\",float) == True"
        try:
            _class(value)
            return True
        except:
            return False



def pass_exceptions(func):
    """装饰器，用于捕获函数执行过程中抛出的异常
    
    :param func: 要装饰的函数
    :return: 装饰后的函数
    
    举个栗子
    >>> @pass_exceptions
    ... def func():
    ...     raise Exception("wdnmd")

    >>> func()  # 在运行func这个函数捕获到错误之后程序不会崩溃
    ---------------------------ExceptionCaught-----------------------------
    执行函数'func'时捕获到异常
    -----------------------------------------------------------------------
    Traceback (most recent call last):
     File "C:\\Users\\ljy09\\Desktop\\project_3\\main_pyside6.py", line 101, in wrapper
       return func(*args, **kwargs)
     File "C:\\Users\\ljy09\\Desktop\\project_3\\main_pyside6.py", line 109, in func
       raise Exception("wdnmd")
    Exception: wdnmd
    -----------------------------------------------------------------------
    builtins.Exception: wdnmd
    Stacktrace:
     at __main__.pass_exceptions.<locals>.wrapper(main_pyside6.py:109)
    -----------------------------------------------------------------------


    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            Base.log_exc(f"执行函数{repr(func.__name__)}时捕获到异常", f"pass_exceptions -> {func.__name__}")

    return wrapper

def exc_info_short(desc:str="出现了错误：", level:Literal["I", "W", "E"]="E"):
    "简单报一句错"
    Base.log(level, f"{desc}  [{sys.exc_info()[1].__class__.__name__}] {sys.exc_info()[1].args[0] if sys.exc_info()[1].args else ''}")

