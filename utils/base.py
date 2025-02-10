"""
算法的核心。
"""

import time
import sys
import traceback
import os
import threading
import ctypes
import json
from threading import Thread
from typing import (List, Tuple, Optional, Union, Dict, Any, SupportsIndex, Generic,
                    Literal, final, overload, TypeVar, Callable, Iterable, Iterator,
                    Type)
from collections import OrderedDict
import datetime
import copy
import math
import pickle
import dill as pickle
import inspect
from queue import Queue
import platform
from typing_extensions import Iterable, Mapping
import inspect
from typing import Callable

try:
    from utils.system import system, SystemLogger
    from utils.high_precision_operation import HighPrecision
except ImportError:
    traceback.print_exc()
    from system import system, SystemLogger
    from high_precision_operation import HighPrecision

from types import TracebackType

from abc import ABC, abstractmethod
import random

def utc(prec: int = 3):
    "获取当前UTC时间"
    return int(time.time() * (10 ** prec))
if sys.stdout is None:
    if sys.__stdout__ is None:
        sys.stdout = open(os.getcwd() + "/log/log_{}_stdout.log".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "w", encoding="utf-8")
        sys.stderr = open(os.getcwd() + "/log/log_{}_stderr.log".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "w", encoding="utf-8")
        sys.__stdout__ = sys.stdout
        sys.__stderr__ = sys.stderr
    else:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def get_function_namespace(func) -> str:
    "获取函数的命名空间"
    module = inspect.getmodule(func)
    if not hasattr(func, "__module__"):
        try:
            return func.__qualname__
        except:
            try:
                return func.__name__
            except:
                if isinstance(func, property):
                    return str(func.fget.__qualname__)
                elif isinstance(func, classmethod):
                    return str(func.__func__.__qualname__)
                try:
                    return func.__class__.__qualname__
                except:
                    return func.__class__.__name__            
    if module is None:
        module_name = func.__self__.__module__ if hasattr(func, "__self__") else func.__module__
    else:
        module_name = module.__name__

    return f"{module_name}.{func.__qualname__}"

def format_exc_like_java(exc: Exception) -> List[str]:
    "不是我做这东西有啥用啊"
    result = [f"{get_function_namespace(exc.__class__)}: " + (str(exc) if str(exc).strip() else "no further information"), "Stacktrace:"]
    tb = exc.__traceback__
    while tb is not None:
        frame = tb.tb_frame
        filename = frame.f_code.co_filename
        filename_strip = os.path.basename(filename)
        lineno = tb.tb_lineno
        funcname = frame.f_code.co_name
        _locals = frame.f_locals.copy()
        instance = None
        method_obj = None
        for i in _locals.values():
            if isinstance(i, object) and hasattr(i, "__class__"):
                instance = i
                class_obj = instance.__class__
                method_obj = getattr(class_obj, funcname, None)
                if method_obj:
                    break
        if instance and method_obj:
            full_path = get_function_namespace(method_obj)
            result.append(f"  at {full_path}({filename_strip}:{lineno})")
        else:
            func_obj = frame.f_globals.get(funcname) or frame.f_locals.get(funcname)
            if func_obj:
                qualname = get_function_namespace(func_obj)
                result.append(f"  at {qualname}({filename_strip}:{lineno})")
        tb = tb.tb_next
    return result

from ctypes import c_int, c_int8, c_int16, c_int32, c_int64, c_uint, c_uint8, c_uint16, c_uint32, c_uint64

_cinttype = Union[int, c_int, c_uint, c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64]

def cinttype(dtype: _cinttype, name: Optional[str] = None):
    """搓了一个我自己的cint类型（bushi
    
    :param dtype: 要继承的数据类型
    :param name:  类名
    :return: 继承了cint类型的类

    byd越来越癫了
    """
    if name is None:
        name = dtype.__name__
    class _CIntType:
        "继承cint类型的类"
        
        def __init__(self, value: _cinttype):
            try:
                value = int(value)
            except:
                value = int(value.value)

            self._dtype: _cinttype = dtype
            self._data: _cinttype = self._dtype(value)
            self._tpname: str = name

        
        def __str__(self):
            return str(self._data.value)
        
        def __repr__(self):
            return f"{self._tpname}({repr(self._data.value)})"
        
        def __int__(self):
            return int(self._data.value)
        
        def __float__(self):
            return float(self._data.value)
        
        def __bool__(self):
            return bool(self._data.value)
        
        def __hash__(self):
            return hash(self._data.value)
        
        def __eq__(self, other):
            if other == inf:
                return False
            if other == -inf:
                return False
            if math.isnan(other):
                return False
            return self._data.value == int(other)
        
        def __ne__(self, other):
            if other == inf:
                return True
            if other == -inf:
                return True
            if math.isnan(other):
                return True
            return self._data.value != int(other)
        
        def __lt__(self, other):
            if other == inf:
                return True
            if other == -inf:
                return False
            if math.isnan(other):
                return False
            return self._data.value < int(other)
        
        def __le__(self, other):
            if other == inf:
                return True
            if other == -inf:
                return False
            if math.isnan(other):
                return False
            return self._data.value <= int(other)
        
        def __gt__(self, other):
            if other == inf:
                return False
            if other == -inf:
                return True
            if math.isnan(other):
                return False
            return self._data.value > int(other)
        
        def __ge__(self, other):
            if other == inf:
                return True
            if other == -inf:
                return True
            if math.isnan(other):
                return False
            return self._data.value >= int(other)
        
        def __abs__(self):
            return cinttype(self._dtype, self._tpname)(abs(self._data.value))
        
        def __neg__(self):
            return cinttype(self._dtype, self._tpname)(-self._data.value)
        
        def __pos__(self):
            return cinttype(self._dtype, self._tpname)(+self._data.value)
    
        def __round__(self, ndigits=None):
            return cinttype(self._dtype, self._tpname)(round(self._data.value, ndigits))
        
        def __add__(self, other: Any):
            return cinttype(self._dtype, self._tpname)(self._data.value + int(other))
        
        def __sub__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value - int(other))
        
        def __mul__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value * int(other))
        
        def __truediv__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value / int(other))
        
        def __floordiv__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value // int(other))
        
        def __mod__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value % int(other))
        
        def __pow__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value ** int(other))
        
        def __lshift__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value << int(other))
        
        def __rshift__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value >> int(other))
        
        def __and__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value & int(other))
        
        def __or__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value | int(other))
        
        def __xor__(self, other):
            return cinttype(self._dtype, self._tpname)(self._data.value ^ int(other))
        
        def __invert__(self):
            return cinttype(self._dtype, self._tpname)(~self._data.value)
        
        def __iadd__(self, other):
            self._data.value += int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __isub__(self, other):
            self._data.value -= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __imul__(self, other):
            self._data.value *= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __itruediv__(self, other):
            self._data.value /= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __ifloordiv__(self, other):
            self._data.value //= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __imod__(self, other):
            self._data.value %= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __ipow__(self, other):
            self._data.value **= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __ilshift__(self, other):
            self._data.value <<= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __irshift__(self, other):
            self._data.value >>= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __iand__(self, other):
            self._data.value &= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)

        def __ior__(self, other):
            self._data.value |= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)
        
        def __ixor__(self, other):
            self._data.value ^= int(other)
            return cinttype(self._dtype, self._tpname)(self._data.value)
        
        def __radd__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) + self._data.value)
        
        def __rsub__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) - self._data.value)

        def __rmul__(self, other):

            return cinttype(self._dtype, self._tpname)(int(other) * self._data.value)

        def __rtruediv__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) / self._data.value)

        def __rfloordiv__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) // self._data.value)

        def __rmod__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) % self._data.value)

        def __rpow__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) ** self._data.value)

        def __rlshift__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) << self._data.value)

        def __rrshift__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) >> self._data.value)

        def __rand__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) & self._data.value)

        def __rxor__(self, other):
            return cinttype(self._dtype, self._tpname)(int(other) ^ self._data.value)



            

    return _CIntType


int8   = byte             = cinttype(c_int8,   "byte")
int16  = short            = cinttype(c_int16,  "short")
int32  = integer          = cinttype(c_int32,  "integer")
int64  = qword            = cinttype(c_int64,  "qword")
uint8  = unsigned_byte    = cinttype(c_uint8,  "unsigned_byte")
uint16 = unsigned_short   = cinttype(c_uint16, "unsigned_short")
uint32 = unsigned_integer = cinttype(c_uint32, "unsigned_integer")
uint64 = unsigned_qword   = cinttype(c_uint64, "unsigned_qword")


    




def get_function_module(func: Union[object, Callable]) -> str:
    "获取函数的模块"
    module = inspect.getmodule(func)
    if module is None:
        module_name = func.__self__.__module__ if hasattr(func, "__self__") else func.__module__
    else:
        module_name = module.__name__
    return module_name

cwd = os.getcwd()
"当前工作目录"

bs = "\\"

debug = True
"是否为调试模式"

LOG_FILE_PATH = os.getcwd() + "/log/log_{}.log".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
LOG_FILE_PATH = LOG_FILE_PATH.replace("/" if platform.platform() == "Windows"  else "\\", "\\" if platform.platform() == "Windows" else "/")
"日志文件名"

function = type(lambda: None)
"函数类型"


SOUND_BRUH = os.getcwd() + "/res/sounds/bruh.mp3"
"bruh"

class NULLPTR:
    "虽然没用"
    def __eq__(self, value: object) -> bool:
        return isinstance(value, NULLPTR)
    
    def __ne__(self, value: object) -> bool:
        return not isinstance(value, NULLPTR)

    def __str__(self) -> str:
        return "nullptr"

    def __repr__(self) -> str:
        return "nullptr"
    
    def __hash__(self):
        return -1
    
    def __bool__(self):
        return False
    

null = NULLPTR()
"空指针"

if not os.path.isdir("log"):
    os.mkdir("log")

# 先把所有的输出流存起来作为备份
stdout_orig = sys.stdout
stderr_orig = sys.stderr


NoneType = type(None)

function = Callable



class Stack:
    "非常朴素的栈"

    def __init__(self):
        "初始化栈"
        self.items = []

    def is_empty(self):
        "判断栈是否为空"
        return self.items == []

    def push(self, item):
        "添加元素到栈顶"
        self.items.append(item)

    def pop(self):
        "移除栈顶元素并返回该元素"
        return self.items.pop()

    def peek(self):
        "返回栈顶元素"
        return self.items[len(self.items) - 1]

    def size(self):
        "返回栈的大小"
        return len(self.items)

    def clear(self):
        "清空栈"
        self.items = []


def steprange(start:Union[int, float], stop:Union[int, float], step:int) -> List[float]:
    """生成step步长的从start到stop的列表
    
    :param start: 起始值
    :param stop: 结束值
    :param step: 步长
    :return: 从start到stop的列表

    举个例子

    >>> steprange(0, 10, 5)
    [0, 2.5, 5.0, 7.5, 10]
    """
    if (stop - start) % step != 0:
        return [start + i * (int(stop - start) / step) for i in range(step)][:-1] + [stop]
    else:
        return [start + i * (int(stop - start) / (step - 1)) for i in range(step)]

class Thread(threading.Thread):
    "自己做的一个可以返回数据的Thread"

    def __init__(
            self,
            group: None = None,
            target: Optional[Callable] = None,
            name: Optional[str] = None,
            args: Iterable[Any] = None,
            kwargs: Optional[Mapping[str, Any]] = None,
            *,
            daemon: Optional[bool] = None) -> None:
        """初始化线程
        
        :param group: 线程组，默认为None
        :param target: 线程函数，默认为None
        :param name: 线程名称，默认为None
        :param args: 线程函数的参数，默认为空元组
        :param kwargs: 线程函数的关键字参数，默认为None
        """
        args = () if args is None else args
        kwargs = {} if kwargs is None else kwargs
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._return = None
        self._finished = False
        
    @property
    def return_value(self):
        "返回线程的返回值"
        if self._finished:
            return self._return
        else:
            raise RuntimeError("线程并未执行完成")
    

    def run(self):
        "运行线程"
        self.thread_id = ctypes.CFUNCTYPE(ctypes.c_long) (lambda: ctypes.pythonapi.PyThread_get_thread_ident()) ()
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
        self._finished = True
        

    def join(self, timeout:Optional[float]=None) -> Any:
        """"等待线程完成并返回结果
        
        :param timeout: 超时时间，默认为None，表示无限等待"""
        super().join(timeout=timeout)
        return self._return



inf = float("inf")
"无穷大"

ninf = float("-inf")
"无穷小"

nan = float("nan")
"非数"




class ModifyingError(Exception):"修改出现错误。"



import colorama

colorama.init(autoreset=True)
class Color:
    """颜色类（给终端文字上色的）
    
    :example:
    
    >>> print(Color.RED + "Hello, " + Color.End + "World!")
    Hello, World!       (红色Hello，默认颜色的World)
    
    """
    RED     =   colorama.Fore.RED
    "红色"
    GREEN   =   colorama.Fore.GREEN
    "绿色"
    YELLOW  =   colorama.Fore.YELLOW
    "黄色"
    BLUE    =   colorama.Fore.BLUE
    "蓝色"
    MAGENTA =   colorama.Fore.MAGENTA
    "品红色"
    CYAN    =   colorama.Fore.CYAN
    "青色"
    WHITE   =   colorama.Fore.WHITE
    "白色"
    BLACK   =   colorama.Fore.BLACK
    "黑色"
    END     =   colorama.Fore.RESET
    "着色结束"
    BOLD    =   colorama.Style.BRIGHT
    "加粗"
    UNDERLINE = colorama.Style.DIM
    "下划线"
    NORMAL = colorama.Style.NORMAL
    "正常"
    
    @staticmethod
    @final
    def from_rgb(r:int, g:int, b:int) -> str:
        "从RGB数值中生成颜色"
        return f"\033[38;2;{r};{g};{b}m"

log_file = open(LOG_FILE_PATH, "a", buffering=1, encoding="utf-8")

class Mutex:
    "一个简单的互斥锁"
    def __init__(self):
        self.locked = False

    def lock(self):
        "锁定"
        if self.locked:
            raise RuntimeError("互斥锁已经被锁定")
        self.locked = True

    def unlock(self):
        "解锁"
        if not self.locked:
            raise RuntimeError("互斥锁没有被锁定")
        self.locked = False

    def __enter__(self):
        self.lock()
    
    def __exit__(self, exc_type: Type[BaseException], exc_val: Exception, exc_tb: TracebackType):
        if exc_type is not None:
            Base.log_exc("互斥锁异常退出", "Mutex.__exit__", exc=exc_val)
        self.unlock()





class FrameCounter:
    "帧计数器"
    def __init__(self, maxcount: Optional[int] = None, timeout: Optional[float] = None):
        "初始化帧计数器"
        self.maxcount = maxcount
        self.timeout = timeout
        self._c = 0
        self.running = False
        
    @property
    def _t(self):
        "获取当前时间戳"
        return time.time()
    
    @property
    def framerate(self):
        "获取帧率"
        if self._c == 0 or not self.running:
            return 0
        return self._c / self._t


    def start(self):
        "启动计数器"
        if self.running:
            raise RuntimeError("这个计数器已经启动过了！")
        self._c = 0
        self.running = True
        while (self.maxcount is None or self._c < self.maxcount) and (self.timeout is None or time.time() - self._t <= self.timeout) and self.running:
            self._c += 1

    def stop(self):
        "停止计数器"
        self.running = False


def gen_uuid(len: int = 32) -> str:
    return "".join([str(random.choice("0123456789abcdef")) for _ in range(len)])


def sep_uuid(uuid, sep: str = "/", length: int = 8) -> str:
    return sep.join([uuid[i:i+length] for i in range(0, len(uuid), length)])

class Object(object):
    "一个基础类"

    @property
    def uuid(self):
        "获取对象的UUID"
        if not hasattr(self, "_uuid"):
            self._uuid = gen_uuid()
        return self._uuid
    
    @uuid.setter
    def uuid(self, value):
        "设置对象的UUID"
        Base.log("I", f"设置对象{self!r}的UUID: {self.uuid} -> {value}", "Object.uuid.setter")
        self._uuid = value

    @uuid.deleter
    def uuid(self):
        "删除对象的UUID"
        raise AttributeError("不能删除对象的UUID")


    def copy(self):
        "给自己复制一次，两个对象不会互相影响"
        return copy.deepcopy(self)

    def __repr__(self):
        "返回这个对象的表达式"
        return f"{self.__class__.__name__}({', '.join([f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
        # 我个人认为不要把下划线开头的变量输出出来（不过只以一个下划线开头的还得考虑考虑）
    
def utc(precision:int=3):
    """返回当前时间戳

    :param precision: 精度，默认为3
    """
    return int(time.time() * pow(10, precision))

class Base(Object):
    "工具基层"
    log_file = log_file
    "日志文件"
    fast_log_file = open("log_buffered.txt", "a", buffering=1, encoding="utf-8")
    "临时日志文件（现在没用了）"
    stdout_orig = stdout_orig
    "标准输出"
    stderr_orig = stderr_orig
    "标准错误"
    stdout = SystemLogger(sys.stdout, logger_name="sys.stdout", level="I", function=lambda l, m, s: Base.log(l, m, s))
    "经过处理的输出"
    stderr = SystemLogger(sys.stderr, logger_name="sys.stderr", level="E", function=lambda l, m, s: Base.log(l, m, s))
    "经过处理的错误输出"
    window_log_queue = Queue()
    "主窗口显示日志的队列（每一个项目是一行的字符串）"
    console_log_queue = Queue()
    "控制台日志队列"
    logfile_log_queue = Queue()
    "日志文件日志队列"
    log_mutex = Mutex()
    "记录日志的互斥锁（现在没用了）"
    log_file_keepcount = 20
    "日志文件保留数量"
    _writing = False
    "没用的东西"
    thread_id = ctypes.CFUNCTYPE(ctypes.c_long) (lambda: ctypes.pythonapi.PyThread_get_thread_ident()) ()
    "当前进程的pid"
    thread_name = threading.current_thread().name
    "当前进程的名称"
    thread = threading.current_thread()
    "当前进程的线程对象"
    logger_running = True
    "日志记录器是否在运行（我自己都不知道有没有用，忘了）"
    log_level:Literal["I", "W", "E", "F", "D", "C"] = "D"
    "日志记录器等级"


    @staticmethod
    def utc(precision:int=3):
        """返回当前时间戳

        :param precision: 精度，默认为3
        """
        return int(time.time() * pow(10, precision))


    @staticmethod
    def gettime():
        "获得当前时间"
        lt = time.localtime()
        return F"{lt.tm_year}-{lt.tm_mon:02}-{lt.tm_mday:02} {lt.tm_hour:02}:{lt.tm_min:02}:{lt.tm_sec:02}.{int((time.time()%1)*1000):03}"

    @staticmethod
    def log(type:Literal["I", "W", "E", "F", "D", "C"], msg:str, source:str="MainThread"):
                """
                向控制台和日志输出信息

                :param type: 类型
                :param msg: 信息
                :param send: 发送者
                :return: None
                """
                # 如果日志等级太低就不记录
                if (type == "D" and Base.log_level not in ("D"))                \
                or (type == "I" and Base.log_level not in ("D", "I"))            \
                or (type == "W" and Base.log_level not in ("D", "I", "W"))        \
                or (type == "E" and Base.log_level not in ("D", "I", "W", "E"))    \
                or (type == "F" or type == "C" and Base.log_level not in ("D", "I", "W", "E", "F", "C")):
                    return

                if not isinstance(msg, str):
                    msg = msg.__repr__()
                for m in msg.splitlines():
                    if type == "I":
                        color = Color.GREEN
                    elif type == "W":
                        color = Color.YELLOW
                    elif type == "E":
                        color = Color.RED
                    elif type == "F" or type == "C":
                        color = Color.MAGENTA
                    elif type == "D":
                        color = Color.CYAN
                    else:
                        color = Color.WHITE
                    
                    if not m.strip():
                        continue
                    frame = inspect.currentframe()
                    lineno = frame.f_back.f_lineno
                    file = frame.f_back.f_code.co_filename.replace(cwd, "")
                    if file == "<string>":
                        lineno = 0
                    if file.startswith(("/", "\\")):
                        file = file[1:]
                    cm = f"{Color.BLUE}{Base.gettime()}{Color.END} {color}{type}{Color.END} {Color.from_rgb(50, 50, 50)}{source.ljust(35)}{color} {m}{Color.END}"
                    lm = f"{Base.gettime()} {type} {(source).ljust(35)} {m}" 
                    lfm = f"{Base.gettime()} {type} {(source + f' -> {file}:{lineno}').ljust(60)} {m}"
                    Base.window_log_queue.put(lm)
                    Base.console_log_queue.put(cm)
                    # Base.logfile_log_queue.put(lfm)
                    Base.log_file.write(lfm + "\n")
                    # print(lfm, file=Base.fast_log_file)
                    Base.log_file.flush()

    @staticmethod
    def log_thread_logfile():
        "把日志写进日志文件的线程的运行函数"
        while Base.logger_running:
            s = Base.logfile_log_queue.get()
            Base.log_file.write(s + "\n")
            Base.log_file.flush()


    @staticmethod
    def log_thread_console():
        "把日志写在终端的线程的运行函数"
        while Base.logger_running:
            s = Base.console_log_queue.get()
            Base.stdout_orig.write(s + "\n")
            Base.stdout_orig.flush()

    @staticmethod
    def stop_loggers():
        "停止所有日志记录器"
        Base.logger_running = False

    console_log_thread = Thread(target=lambda: Base.log_thread_console(), daemon=True, name="ConsoleLogger")
    "把日志写在终端的线程的线程对象"
    logfile_log_thread = Thread(target=lambda: Base.log_thread_logfile(), daemon=True, name="FileLogger")
    "把日志写进日志文件的线程的线程对象"

    from abc import abstractmethod
    abstract = abstractmethod
    "抽象方法"

    @staticmethod
    def clear_oldfile(keep_count:int=10):
        "清理日志文件"
        if not os.path.exists(LOG_FILE_PATH):
            return
        log_files = sorted([f for f in os.listdir(os.path.dirname(LOG_FILE_PATH)) if f.startswith("log_") and f.endswith(".log")], reverse=True)
        if len(log_files) > keep_count:
            for f in log_files[keep_count:]:
                os.remove(os.path.join(os.path.dirname(LOG_FILE_PATH), f))
    
    @staticmethod
    def read_ini(filepath:str="options.ini",encoding="utf-8",nospace:bool=True) -> Union[int,Dict[str,Union[bool,str]]]:
        """读取一个写满了<变量名>=<值>的文本文件然后返回一个字典
        
        :param filepath: 文件路径
        :param encoding: 编码
        :param nospace: 是否去除空格
        :return: 一个dict
        """
        reading_file = open(filepath,encoding=encoding,mode="r",errors="ignore")
        content = reading_file.readlines()
        reading_file.close()
        if len(content) == 0:
            return {}
        output = {}
        for i in range(len(content)):
            try:
                line_setting = str(content[i]).split("=",2)
                prop = str(line_setting[0])   
                value = line_setting[1].split("\n",1)[0]
                if nospace:value = value.replace(" ","")
                if value.upper() == "FALSE": value = False
                if value.upper() == "TRUE":  value = True
                output[prop]=value
            except:
                continue
        return output  

    @staticmethod
    def log_exc(info:str="未知错误：", 
                sender="MainThread -> Unknown", 
                level:Literal["I", "W", "E", "F", "D", "C"]="E", 
                exc:Exception=None):
        """向控制台和日志报错。
        
        :param info: 信息
        :param sender: 发送者
        :param level: 级别
        :param exc: 指定的Exception，可以不传（就默认是最近发生的一次）
        :return: None
        """
        if exc is None:
            exc = sys.exc_info()[1]
            if exc is None:
                return
        Base.log(level, info, sender)
        Base.log(level, ("").join(traceback.format_exception(exc.__class__, exc, exc.__traceback__)), sender)
        Base.log(level, "\n".join(format_exc_like_java(exc)), sender)

    @staticmethod
    def log_exc_short(info:str="未知错误：", 
                        sender="MainThread -> Unknown", 
                        level:Literal["I", "W", "E", "F", "D", "C"]="W", 
                        exc:Exception=None):
        if exc is None:
            exc = sys.exc_info()[1]
            if exc is None:
                return
        Base.log(level, f"{info} [{exc.__class__.__qualname__}] {exc}", sender)



Base.console_log_thread.start()
Base.logfile_log_thread.start()

class SupportsKeyOrdering(ABC):
    # 注：Supports是支持的意思（
    # 还有，其实把鼠标悬浮在"SupportsKeyOrdering"上就可以看到这个注释了，经过美化了的
    """支持key排序的抽象类。
    
        意思就是说这个类有一个``key``属性，这个属性是``str``类型

        这个``SupportsKeyOrdering``是为了方便使用而设计的，因为很多类都需要一个``key``属性

        （比如``ScoreModifactionTemplate``的``key``就表示模板本身的标识符）

        只要这个类实现了``key``属性，那么就可以使用``OrderedKeyList``（后面有讲）来存储这个类

        （比如``OrderedKeyList[ScoreModificationTemplate]``）

        还有，只要继承这个类，然后自己写一下key的实现，就可以直接使用``OrderedKeyList``来存储这个类了

        就像这样：
        >>> class SomeClassThatSupportsKeyOrdering(SupportsKeyOrdering):
        ...     def __init__(self, key: str):
        ...         self.key = key      # 在一个OrderedKeyList里面每一个元素都有自己的key
        ...                             # 至于这个key表示的是什么就由你来决定了
        >>>                             # 但是但是，这个key只能是str，因为int拿来做索引值了，float和tuple元组)之类的懒得写


        以前以来我们都用``collections.OrderedDict``来寻找模板，比如这样

        >>> DEFAULT_SCORE_TEMPLATES: OrderedDict[str, ScoreModificationTemplate] = OrderedDict([
        ...   "go_to_school_early": ScoreModificationTemplate(
        ...         "go_to_school_early", 1.0,  "7:20前到校", "早起的鸟儿有虫吃"),
        ...   "go_to_school_late": ScoreModificationTemplate(
        ...         "go_to_school_late", -1.0, "7:25后到校", "早起的虫儿被鸟吃"),
        ... ])
        >>> DEFAULT_SCORE_TEMPLATES["go_to_school_early"]
        ScoreModificationTemplate("go_to_school_early", 1.0,  "7:20前到校", "早起的鸟儿有虫吃")

        这样做的好处是我们可以直接通过key来获取模板，也可以通过模板反向找到它的key值
        
        但是缺点是如果``OrderedDict``中的key和``ScoreModification``中的key不一致就会出错
        
        现在我们可以用``OrderedKeyList``来存储模板这类"SupportsKeyOrdering"的对象，就不用写dict的key

        这样就不用担心dict中的key和模板中的不一样了

        >>> DEFAULT_SCORE_TEMPLATES = OrderedKeyList([
        ...   ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃"),
        ...   ScoreModificationTemplate("go_to_school_late", -1.0, "7:25后到校", "早起的虫儿被鸟吃"),
        ... ])   # 这就不需要写Key了，而且这个东西支持所有list的方法和部分dict的方法
        >>>      #（比如append，keys和items之类）
        >>> DEFAULT_SCORE_TEMPLATES[0]
        ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃")
        >>> DEFAULT_SCORE_TEMPLATES["go_to_school_early"]
        ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃")

        你学废了吗？
        """



_Template = TypeVar("_Template", bound=SupportsKeyOrdering)
"""这东西不用管，写类型注释用的，方便理解

（可以理解为写在类型注释里的一个变量，绑定``SupportsKeyOrdering``的类，传进去什么类型就传出来什么类型）

如果你给一个``OrderedKeyList``初始值是``ScoreModificationTemplate``的列表，他就会自动识别为``OrderedKeyList[ScoreModificationTemplate]``

那么这个``OrderedKeyList``迭代或者取值的时候VSCode就会知道取出来的东西ScoreModificationTemplate，就方便查看它的属性和方法，肥肠方便

（但是对于写类型注释的人并不方便）
"""


class OrderedKeyList(list, Iterable[_Template]):
    """有序的key列表，可以用方括号来根据SupportsKeyOrdering对象的key，索引值或者对象本身来获取对象

    举个例子

    建立一个新的OrderedKeyList
    >>> template = ScoreModificationTemplate("go_to_school_late_more", -2.0, "7:30后到校", "哥们为什么不睡死在家里？")
    >>> # 这里有一个存在变量里面的模板，我们叫它template
    >>> DEFAULT_SCORE_TEMPLATES = OrderedKeyList([
    ...   ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃"),
    ...   ScoreModificationTemplate("go_to_school_late", -1.0, "7:25后到校", "早起的虫儿被鸟吃"),
    ...   template
    ... ])

    获取里面的元素
    >>> DEFAULT_SCORE_TEMPLATES[0]
    ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃")
    >>> DEFAULT_SCORE_TEMPLATES["go_to_school_early"]
    ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃")
    >>> DEFAULT_SCORE_TEMPLATES[template]
    ScoreModificationTemplate("go_to_school_late_more", -2.0, "7:30后到校", "哥们为什么不睡死在家里？")
    >>> DEFAULT_SCORE_TEMPLATES.keys()
    ["go_to_school_early", "go_to_school_late", "go_to_school_late"]
    >>> len(DEFAULT_SCORE_TEMPLATES)
    3

    添加元素
    >>> DEFAULT_SCORE_TEMPLATES.append(ScoreModificationTemplate("Chinese_class_good", 2.0,"语文课堂表扬","王の表扬"))
    >>> DEFAULT_SCORE_TEMPLATES.append(template) # 这里如果设置了不允许重复的话还往里面放同一个模板就会报错
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
        DEFAULT_SCORE_TEMPLATES.append(template)
      File "<stdin>", line 166, in append
        raise ValueError(F"模板的key（{getattr(v, self.keyattr)!r}）重复")
    ValueError: 模板的key（'go_to_school_late_more'）重复


    交换里面的元素顺序
    >>> DEFAULT_SCORE_TEMPLATES.swaps(0, 1)     # 交换索引0和1的元素，当然也可以填模板的key
    OrderedKeyList([
        ScoreModificationTemplate("go_to_school_late", -1.0, "7:25后到校", "早起的虫儿被鸟吃"),
        ScoreModificationTemplate("go_to_school_early", 1.0, "7:20前到校", "早起的鸟儿有虫吃"),
        ScoreModificationTemplate("go_to_school_late_more", -2.0, "7:30后到校", "哥们为什么不睡死在家里？")
    ])

    删掉/修改里面的元素
    >>> del DEFAULT_SCORE_TEMPLATES["go_to_school_early"]    # 删除key为"go_to_school_early"的元素
    >>> DEFAULT_SCORE_TEMPLATES.pop(0)                       # 删除索引为0的元素
    >>> len(DEFAULT_SCORE_TEMPLATES)                         # 查看长度（现在只剩一个7:30以后到校的了）
    1

    """

    allow_dumplicate = False
    "是否允许key重复"

    dumplicate_suffix = "_copy"
    "key重复时自动添加的后缀（如果允许放行重复的key进到列表里）"

    keyattr = "key"
    'SupportsKeyOrdering的这个"Key"的属性名'


    def __init__(self, objects: Union[Iterable[_Template], 
                                        Dict[str, _Template], 
                                        "OrderedDict[str, _Template]", 
                                        "OrderedKeyList[_Template]"]):
        """初始化OrderedKeyList
        
        :param templates: 模板列表
        """

        super().__init__()
        if isinstance(objects, (dict, OrderedDict)):
            for k, v in objects.items():
                if getattr(v, self.keyattr) != k:
                    Base.log("W", F"模板在dict中的key（{k!r}）与模板本身的（{getattr(v, self.keyattr)!r}）不一致，"
                                    "已自动修正为dict中的key", "OrderedTemplateGroup.__init__")
                    setattr(v, self.keyattr, k)
                self.append(v)
        elif isinstance(objects, OrderedKeyList):
            self.extend([t for t in objects])
        else:
            keys = []
            for v in objects:
                if getattr(v, self.keyattr) in keys:
                    if not self.allow_dumplicate:
                        raise ValueError(F"模板的key（{getattr(v, self.keyattr)!r}）重复")
                    Base.log("W", F"模板的key（{getattr(v, self.keyattr)!r}）重复，补充为{getattr(v, self.keyattr)!r}{self.dumplicate_suffix}", "OrderedTemplateGroup.__init__")
                    setattr(v, self.keyattr, getattr(v, self.keyattr) + self.dumplicate_suffix)
                keys.append(getattr(v, self.keyattr))
                self.append(v)

    def __getitem__(self, key: Union[int, str, _Template]) -> _Template:
        "返回指定索引或key的模板"
        if isinstance(key, int):
            return super().__getitem__(key)
        else:
            for obj in self:
                if getattr(obj, self.keyattr) == key:
                    return obj
            for obj in self:
                if obj is key:
                    return obj
            raise KeyError(F"列表中不存在key为{key!r}的模板")

    def __setitem__(self, key: Union[int, str, _Template], value: _Template):
        "设置指定索引或key的模板"
        if isinstance(key, int):
            super().__setitem__(key, value)
        else:
            for i, obj in enumerate(self):
                if getattr(obj, self.keyattr) == key:
                    super().__setitem__(i, value)
                    return
                elif obj is key:
                    super().__setitem__(i, value)
            if getattr(value, self.keyattr) == key and isinstance(value, SupportsKeyOrdering) and isinstance(key, str):
                self.append(value)  # 如果key是字符串，并且value是模板，则直接添加到列表中
            else:
                raise KeyError(F"列表中不存在key为{key!r}的模板")
        
    
    def __delitem__(self, key: Union[int, str]):
        "删除指定索引或key的模板"
        if isinstance(key, int):
            super().__delitem__(key)
        else:
            for i, obj in enumerate(self):
                if getattr(obj, self.keyattr) == key:
                    super().__delitem__(i)
                    return
            raise KeyError(F"列表中不存在key为{key!r}的模板")

    def __len__(self) -> int:
        "返回列表中模板的数量"
        return super().__len__()


    def __reversed__(self) -> Iterator[_Template]:
        "返回列表的反向迭代器"
        return super().__reversed__()

    def __contains__(self, item: _Template) -> bool:
        "判断列表中是否包含指定模板"
        return super().__contains__(item) or [getattr(obj, self.keyattr) for obj in self].count(item) > 0

    def swaps(self, lh: Union[int, str], rh: Union[int, str]):
        "交换指定索引或key的模板"
        if  isinstance(lh, str):
            for i, obj in enumerate(self):
                if getattr(obj, self.keyattr) == lh:
                    lh = i
                    break
            else:
                raise KeyError(F"列表中不存在key为{lh!r}的模板")
        if isinstance(rh, str):
            for i, obj in enumerate(self):
                if getattr(obj, self.keyattr) == rh:
                    lh = i
                    break
            else:
                raise KeyError(F"列表中不存在key为{rh!r}的模板")
        self[lh], self[rh] = self[rh], self[lh]
        return self
    
    def __iter__(self) -> Iterator[_Template]:
        "返回列表的迭代器"
        return super().__iter__()

    def append(self, obj: _Template):
        "添加到列表"
        if getattr(obj, self.keyattr) in self.keys():
            if not self.allow_dumplicate:  # 如果不允许重复直接抛出异常
                raise ValueError(F"模板的key（{getattr(obj, self.keyattr)!r}）重复")
            Base.log("W", F"模板的key（{getattr(obj, self.keyattr)!r}）重复，补充为{getattr(obj, self.keyattr)!r}{self.dumplicate_suffix}", "OrderedTemplateGroup.append")
            setattr(obj, self.keyattr, getattr(obj, self.keyattr) + self.dumplicate_suffix)
        super().append(obj)
        return self

    def extend(self, templates: Iterable[_Template]):
        "扩展列表"
        for template in templates:
            self.append(template)
        return self
    
    def keys(self) -> List[str]:
        "返回列表中所有元素的key"
        return [getattr(obj, self.keyattr) for obj in self]
    
    def values(self) -> List[_Template]:
        "返回列表中所有模板"
        return [obj for obj in self]

    def items(self) -> List[Tuple[str, _Template]]:
        "返回列表中所有模板的key和模板"
        return [(getattr(obj, self.keyattr), obj) for obj in self]
    

    def __copy__(self) -> "OrderedKeyList[_Template]":
        "返回列表的浅拷贝"
        return OrderedKeyList(self)
    
    def __deepcopy__(self, memo: dict) -> "OrderedKeyList[_Template]":
        "返回列表的深拷贝"
        return OrderedKeyList([copy.deepcopy(obj, memo) for obj in self])
    
    def copy(self) -> "OrderedKeyList[_Template]":
        "返回列表的拷贝"
        return self.__copy__()
    
    def to_dict(self) -> Dict[str, _Template]:
        "返回列表的字典表示"
        return dict(self.items())

    def __repr__(self) -> str:
        "返回列表的表达式"
        return F"OrderedTemplateGroup({super().__repr__()})"
    



def get_random_template(templates: "OrderedKeyList[ClassDataObj.ScoreModificationTemplate]"):
    
    # 把鼠标移到上面这个黄色的东西看注释吧
    """
    关于某些抽象的类型注释，比如``OrderedKeyList[ScoreModificationTemplate]``

    就比如你在给一个函数写类型注释的时候，你可能会这样写：

    ```python
    def get_random_template(templates: OrderedKeyList[ScoreModificationTemplate]):
        return random.choice(templates)

    ```

    **  如果没看懂的话解释一下，因为``OrderedKeyList``继承了``typing``的``Iterable``，

        ``Iterable``的定义就是一个可以迭代（"for i in 某种东西" 这种就是迭代）的对象

        ``Iterable[某种类型]`` 表示的是这个可迭代对象里面包含的全部都是某种类型，for循环出来的``i``自然也就是这种类型了

        所以``OrderedKeyList``的类型标注和Iterable是一个道理，

        ``OrderedKeyList[ScoreModificationTemplate]``的意思就是这个``OrderedKeyList``里面包含的全部都是``ScoreModificationTemplate``

        迭代出来的自然也就全都是``ScoreModificationTemplate``了

        还有，直接用python自带的类型（比如``list[ScoreModificationTemplate]``这种）去写方括号的类型标注是不行的，会报错

        但是可以``from typing import List``，然后写``List[ScoreModificationTemplate]``，这样就可以表示一个``ScoreModififaction``的列表了



    然后你把鼠标放到这个东西上面去的时候

    ```python
    template = get_random_template(DEFAULT_SCORE_TEMPLATES)
    ```

    你就会惊喜（也许只有我我会惊喜吧？）的发现VSCode识别出来了template是一个``ScoreModificationTemplate``类型的对象

    然后只要系统知道了template是``ScoreModificationTemplate``类型的对象，那么VSCode就可以把这玩意的所有method都显示出来，方便写代码


    """
    return random.choice(templates)


class ClassDataObj(Base):     
    "班级数据对象"

    _class_obs_update_count = 0
    _achievement_obs_update_count = 0

    class_observer_update_rate = 0
    "班级状态侦测器更新频率（单位：次/秒）"
    
    achievement_observer_update_rate = 0
    "成就状态侦测器更新频率（单位：次/秒）"

    class OpreationError(Exception):"修改出现错误。"

    class DummyStudent(Object, SupportsKeyOrdering):
        "一个工具人"
        def __init__(self):
                
            self.name = "我是工具人"
            self.num = 0
            self.score = 0.0
            self.belongs_to:str = "CLASS_2216"
            self.highest_score:float = 0.0
            self.lowest_score:float = 0.0
            self.total_score = 0.0
            self.last_reset = 0.0
            "分数上次重置的时间"
            self.highest_score_cause_time = 0.0
            self.lowest_score_cause_time = 0.0
            self.achievements = {}
            "所获得的所有成就"
            self.belongs_to_group = "group_0"
            "所属小组"
            self.last_reset_info = None
            "上次重置的信息"
            self.history = {}
            "历史分数记录"


# 小寄巧：如果一个类在需要在类型标注里面用到但还没定义可以用引号括起来
    class Student(Object, SupportsKeyOrdering):
            "一个学牲"

            score_dtype = HighPrecision
            "记录分数的数据类型（还没做完别乱改）"

            def __init__(self, 
                        name:                     str, 
                        num:                      int, 
                        score:                    float, 
                        belongs_to:               str, 
                        history:                  Dict[Any, "ClassDataObj.ScoreModification"] = None, 
                        last_reset:               Optional[float]                = None,
                        highest_score:            float                          = 0.0, 
                        lowest_score:             float                          = 0.0,
                        achievements:             Dict[int, "ClassDataObj.Achievement"]       = None, 
                        total_score:              float                          = None,
                        highest_score_cause_time: float                          = 0.0, 
                        lowest_score_cause_time:  float                          = 0.0,
                        belongs_to_group:         Optional[str]                  = None,
                        last_reset_info:          Optional["ClassDataObj.Student"]            = None):
                
                """一个学生。

                :param name: 姓名
                :param num: 学号
                :param score: 当前分数
                :param belongs_to: 所属班级
                :param history: 历史记录
                :param last_reset: 上次重置时间
                :param highest_score: 最高分
                :param lowest_score: 最低分
                :param achievements: 成就
                :param total_score: 总分
                :param highest_score_cause_time: 最高分产生时间
                :param lowest_score_cause_time: 最低分产生时间
                :param belongs_to_group: 所属小组对应key
                :param last_reset_info: 上次重置的信息
                """
                super().__init__()
                self._name = name
                # 这些带下划线的都是内部用来存储的，实际访问的是property
                self._num = num
                self._score = score
                self._belongs_to:str = belongs_to
                self._highest_score:float = highest_score
                self._lowest_score:float = lowest_score
                self._total_score:float = total_score if total_score is not None else score
                self.last_reset = last_reset
                "分数上次重置的时间"
                self._highest_score_cause_time = highest_score_cause_time
                self._lowest_score_cause_time = lowest_score_cause_time
                self.history:      Dict[int, "ClassDataObj.ScoreModification"] = history if history is not None else {}
                "历史记录， key为时间戳（utc*1000）"
                self.achievements: Dict[int, "ClassDataObj.Achievement"] = achievements if achievements is not None else {}
                "所获得的所有成就， key为时间戳（utc*1000）"
                self.belongs_to_group = belongs_to_group
                "所属小组"
                self.last_reset_info = ClassDataObj.DummyStudent() if last_reset_info is None else last_reset_info
                "上次重置的信息"

            @property
            def highest_score(self):
                "最高分"
                return float(self._highest_score)
            
            @highest_score.setter
            def highest_score(self, value):
                Base.log("I", f"{self.name} 更改最高分：{self._highest_score} -> {value}")
                self._highest_score = self.score_dtype(value)
            
            @property
            def lowest_score(self):
                "最低分"
                return float(self._lowest_score)
            
            @lowest_score.setter
            def lowest_score(self, value):
                Base.log("I", f"{self.name} 更改最低分：{self._lowest_score} -> {value}")
                self._lowest_score = self.score_dtype(value)
            

            @property
            def highest_score_cause_time(self):
                "最高分对应时间"
                return self._highest_score_cause_time
            
            @highest_score_cause_time.setter
            def highest_score_cause_time(self, value):
                Base.log("I", f"{self.name} 更改最高分对应时间：{self._highest_score_cause_time} -> {value}")
                self._highest_score_cause_time = value

            @property
            def lowest_score_cause_time(self):
                "最低分对应时间"
                return self._lowest_score_cause_time
            
            @lowest_score_cause_time.setter
            def lowest_score_cause_time(self, value):
                Base.log("I", f"{self.name} 更改最低分对应时间：{self._lowest_score_cause_time} -> {value}")
                self._lowest_score_cause_time = value


            
            def __repr__(self):
                return (
        F"Student(name={self._name.__repr__()}, " +
        F"num={self._num.__repr__()}, score={self._score.__repr__()}, " +
        F"belongs_to={self._belongs_to.__repr__()}, " +
        ("history={...}, " if hasattr(self, "history") else "") +
        F"last_reset={repr(self.last_reset)}, " +
        F"highest_score={repr(self.highest_score)}, " +
        F"lowest_score={repr(self.highest_score)}, " +
        F"total_score={repr(self.highest_score)}, " +
        ("achievements={...}, " if hasattr(self, "achievements") else "") +
        F"highest_score_cause_time = {repr(self.highest_score_cause_time)}, " +
        f"lowest_score_cause_time = {repr(self.lowest_score_cause_time)}, " +
        f"belongs_to_group={repr(self.belongs_to_group)})")


            @property
            def name(self):
                "学生的名字。"
                return self._name
            
            @name.setter
            def name(self, val):
                Base.log("W", f"正在尝试更改学号为{self._num}的学生的姓名：由\"{self._name}\"更改为\"{val}\"", "Student.name.setter")
                if len(val) >= 50:
                    Base.log("E", f"更改名字失败：不是谁名字有{len(val)}个字啊？？？？", "Student.name.setter")
                    raise ClassDataObj.OpreationError(f"请求更改的名字\"{val}\"过长")
                self._name = val
                Base.log("I","更改完成！","Student.name.setter")

            @name.deleter
            def name(self):
                Base.log("E","错误：用户尝试删除学生名","Student.num.deleter")
                raise ClassDataObj.OpreationError("不允许删除学生的名字")
            

            @property
            def num(self):
                "学生的学号。"
                return self._num

            @num.setter
            def num(self, val:int):
                Base.log("W",f"正在尝试更改学号为{self._name}的学生的学号：由{self._num}更改为{val}","Student.num.setter")
                if val >= 100:
                    Base.log("E","更改学号失败：学号过大了，不太合理","Student.name.setter")
                    raise ClassDataObj.OpreationError(f"请求更改的学号{val}过大了, 无法设置")
                self._num = val
                Base.log("I","更改完成！","Student.name.setter")

            @num.deleter
            def num(self):
                Base.log("E","错误：用户尝试删除学号（？？？？）","Student.name.deleter")
                raise ClassDataObj.OpreationError("不允许删除学生的学号")
            
            @property
            def score(self):
                "学生的分数，操作时仅保留1位小数。"
                return float(self._score)

            @score.setter
            def score(self, val:float):
                logstr = f"""正在尝试更改学号为{self.name}的学生的分数：由{self.score}更改为{val}（{f"上升{val-self.score:.1f}分" if val >= self.score else f"下降{(val-self.score)*-1:.1f}分"}）"""
                self.total_score += val - self.score
                if abs(val-self.score) >= 1145:
                    logstr += "; 涉及到大分数操作，请注意此处"
                self._score = self.score_dtype(round(val, 1))
                if self.score > self.highest_score:
                    self.highest_score = self.score
                    logstr += "; 刷新新高分！"
                if self.score < self.lowest_score:
                    self.lowest_score = self.score
                    logstr += "; 刷新新低分！（不应该是件好事？）"
                Base.log("D", logstr, "Student.score.setter")

            @score.deleter
            def score(self):
                Base.log("E","错误：用户尝试删除分数（？？？？）","Student.score.deleter")
                raise ClassDataObj.OpreationError("不允许直接删除学生的分数")
            
            @property
            def belongs_to(self):
                "学生归属班级。"
                return self._belongs_to

            @belongs_to.setter
            def belongs_to(self,_):
                Base.log("E","错误：用户尝试修改班级","Student.belongs_to.setter")
                raise ClassDataObj.OpreationError("不允许直接修改学生的班级")

            @belongs_to.deleter
            def belongs_to(self):
                Base.log("E","错误：用户尝试删除班级（？？？？？？？）","Student.belongs_to.deleter")
                raise ClassDataObj.OpreationError("不允许直接删除学生的班级")


            @property
            def total_score(self):
                return round(self._total_score, 1) if isinstance (self._total_score, float) else self._total_score
            
            @total_score.setter
            def total_score(self, value):
                self._total_score = self.score_dtype(value)


            def reset_score(self) -> Tuple[float, float, float, Dict[int, "ClassDataObj.ScoreModification"]]:
                """重置学生分数。
                
                :return: Tuple[当前分数, 历史最高分, 历史最低分, Dict[分数变动时间utc*1000, 分数变动记录], Dict[成就达成时间utc*1000, 成就]"""
                Base.log("W", f"  -> 重置{self.name} ({self.num})的分数")

                returnval = (float(self.score), float(self.highest_score),
                            float(self.lowest_score), dict(self.history))
                self.score = 0.0
                self.highest_score = 0.0
                self.lowest_score = 0.0 
                self.highest_score_cause_time = 0.0 
                self.lowest_score_cause_time = 0.0 
                self.last_reset = time.time()
                self.history:Dict[int, ClassDataObj.ScoreModification] = dict()
                self.achievements = dict()
                return returnval
            

            def reset_achievements(self) -> Dict[int, "ClassDataObj.Achievement"]:
                """重置学生成就。
                
                :return: Dict[成就达成时间utc*1000, 成就]"""
                Base.log("W", f"  -> 重置{self.name} ({self.num})的成就")
                returnval = dict(self.achievements)
                self.achievements = dict()
                return returnval

            def reset(self, reset_achievments:bool=True) -> Tuple[float, float, float, 
                                                    Dict[int, "ClassDataObj.ScoreModification"], Optional[Dict[int, "ClassDataObj.Achievement"]]]:
                """重置学生分数和成就。
                    这个操作会更新学生的last_reset_info属性，以记录重置前的分数和成就。
                
                :param reset_achievments: 是否重置成就
                :return: Tuple[当前分数, 历史最高分, 历史最低分, Dict[分数变动时间utc*1000, 分数变动记录], Dict[成就达成时间utc*1000, 成就]"""
                self.last_reset_info = copy.deepcopy(self)
                score, highest, lowest, history = self.reset_score()
                achievements = None
                if reset_achievments:
                    achievements = self.reset_achievements()
                return (score, highest, lowest, history, achievements)

            def get_group(self, class_obs:"ClassStatusObserver") -> "ClassDataObj.Group":
                """获取学生所在小组。
                
                :param class_obs: 班级侦测器
                :return: Group对象"""
                return class_obs.classes[self._belongs_to].groups[self.belongs_to_group]
            
            def get_dumplicated_ranking(self, class_obs: "ClassStatusObserver") -> int:
                """获取学生在班级中计算重复名次的排名。

                :param class_obs: 班级侦测器
                :return: 排名"""
                if self._belongs_to != class_obs.class_id:
                    raise ValueError(f"但是从理论层面来讲你不应该把{repr(class_obs.class_id)}的侦测器给一个{repr(self._belongs_to)}的学生")
                
                else:
                    ranking_data:List[Tuple[int, "ClassDataObj.Student"]] = class_obs.rank_non_dumplicate
                    for index, student in ranking_data:
                        if student.num == self.num:
                            return index
                raise ValueError("但是你确定这个学生在这个班？")
            
            def get_non_dumplicated_ranking(self, class_obs: "ClassStatusObserver") -> int:
                """获取学生在班级中计算非重复名次的排名。

                :param class_obs: 班级侦测器
                :return: 排名"""
                if self._belongs_to != class_obs.class_id:
                    raise ValueError(f"但是从理论层面来讲你不应该把{repr(class_obs.class_id)}的侦测器给一个{repr(self._belongs_to)}的学生")

                else:
                    ranking_data:List[Tuple[int, "ClassDataObj.Student"]] = class_obs.rank_non_dumplicate
                    for index, student in ranking_data:
                        if student.num == self.num:
                            return index
                raise ValueError("但是你确定这个学生在这个班？")
                        
            def __add__(self, value: Union["ClassDataObj.Student", float]) -> "ClassDataObj.Student":
                "这种东西做出来是致敬班级小管家的（bushi"
                if isinstance(value, ClassDataObj.Student):
                    history = self.history.copy()
                    history.update(value.history)
                    achievements = self.achievements.copy()
                    achievements.update(value.achievements)
                    Base.log("W", f"  -> 合并学生：({self.name}, {value.name})", "Student.__add__")
                    Base.log("W", "孩子，这不好笑", "Student.__add__")
                    return ClassDataObj.Student(f"合并学生：({self.name.replace('合并学生：(', '').replace(')', '')}, {value.name.replace('合并学生：(', '').replace(')', '')})",
                                num=self.num + value.num,
                                score=self.score + value.score,
                                belongs_to=self.belongs_to,
                                history=history,
                                last_reset=self.last_reset,
                                achievements=achievements,
                                highest_score=self.highest_score + value.highest_score,
                                lowest_score=self.lowest_score + value.lowest_score,
                                highest_score_cause_time=self.highest_score_cause_time + value.highest_score_cause_time,
                                lowest_score_cause_time=self.lowest_score_cause_time,
                                belongs_to_group=self.belongs_to_group,
                                total_score=self.total_score + value.total_score
                                ).copy()
            
                else:
                    self.score += value
                    return self
                
            def __iadd__(self, value: Union["ClassDataObj.Student", float]) -> "ClassDataObj.Student":
                if isinstance(value, ClassDataObj.Student):
                    self.achievements.update(value.achievements)
                    self.history.update(value.history)
                    self.score += value
                    self.total_score += value
                    return self
                else:
                    self.score += value
                    self.total_score += value
                    return self
                
            
            def to_string(self) -> str:
                "将学生对象转换为JSON格式"
                return json.dumps({
                    "type":                     "Student",
                    "name":                     self.name,
                    "num":                      self.num,
                    "score":                    float(self.score),
                    "belongs_to":               self.belongs_to,
                    "history":                  [h.uuid for h in self.history.values()],
                    "last_reset":               self.last_reset,
                    "achievements":             [a.uuid for a in self.achievements.values()],
                    "highest_score":            self.highest_score,
                    "lowest_score":             self.lowest_score,
                    "highest_score_cause_time": self.highest_score_cause_time,
                    "lowest_score_cause_time":  self.lowest_score_cause_time,
                    "belongs_to_group":         self.belongs_to_group,
                    "total_score":              self.total_score
                })
            

            
            
            


    class SimpleStudent(Student):
            @overload
            def __init__(self, stu: "ClassDataObj.Student"):...

            @overload
            def __init__(self, name:str, num:int, score:float, belongs_to:str, history:dict):...
            
            def __init__(self, stu_or_name, num=None, score=None, belongs_to=None, history=None, **kwargs):
                if isinstance(stu_or_name, ClassDataObj.Student):
                    super().__init__(stu_or_name._name, stu_or_name._num, stu_or_name._score, stu_or_name._belongs_to, {}, **(kwargs))
                else:
                    super().__init__(stu_or_name, num, score, belongs_to, {})
                del self.history            # ...为什么不直接写在@overload下面
                                            # 因为写了会爆

    class Group(Object):
        "一个小组"

        def __init__(self, 
                    key:          str, 
                    name:         str, 
                    leader:       "ClassDataObj.Student", 
                    members:      List["ClassDataObj.Student"], 
                    belongs_to:   str,
                    further_desc: str            = "这个小组的组长还没有为这个小组提供详细描述") -> None:
            """小组的构造函数。
            
            :param key: 在dict中对应的key
            :param name: 名称
            :param leader: 组长
            :param members: 组员（包括组长）
            :param belongs_to: 所属班级
            :param further_desc: 详细描述"""
            self.key = key
            "在dict中对应的key"
            self.name = name
            "名称"
            self.leader = leader
            "组长"
            self.members = members
            "所有成员"
            self.further_desc = further_desc
            "详细描述"
            self.belongs_to = belongs_to
            "所属班级"
        
        @property
        def total_score(self):
            "查看小组的总分。"
            return round(sum([s.score for s in self.members]), 1)
        
        @property
        def average_score(self):
            "查看小组的平均分。"
            return round(sum([s.score for s in self.members]) / len(self.members), 2)
        
        @property
        def average_score_without_lowest(self):
            "查看小组去掉最低分后的平均分。"
            return (round((sum([s.score for s in self.members]) - min(*[s.score for s in self.members])) / (len(self.members) - 1), 2)) if len(self.members) > 1 else 0.0 # 如果只有一个人的话去掉最低分就没有人了。。


        def has_member(self, student: "ClassDataObj.Student"):
            "查看一个学生是否在这个小组。"
            return any([s.num == student.num for s in self.members])
        
        def to_string(self):
            "将小组对象转化为字符串。"
            return json.dumps(
                {
                    "type": "Group",
                    "key": self.key,
                    "name": self.name,
                    "leader": self.leader.uuid,
                    "members": [s.uuid for s in self.members],
                    "belongs_to": self.belongs_to,
                    "further_desc": self.further_desc

                }
            )
        
        def __repr__(self):
            return f"Group(key={repr(self.key)}, name={repr(self.name)}, leader={repr(self.leader)}, members={repr(self.members)}, belongs_to={repr(self.belongs_to)}, further_desc={repr(self.further_desc)}"
        



    class ScoreModificationTemplate(Object, SupportsKeyOrdering):
            "分数加减操作的模板。"
            def __init__(self, 
                        key:             str, 
                        modification:    float, 
                        title:           str, 
                        description:     str      = "该加减分模板没有详细信息。", 
                        cant_replace:    bool     = False, 
                        is_visible:      bool     = True):
                """
                分数操作模板的构造函数。

                :param key: 模板标识符
                :param modification: 模板修改分数
                :param title: 模板标题
                :param description: 模板描述
                :param cant_replace: 是否禁止替换
                :param is_visible: 是否可见
                """
                self.key = key
                self.mod = modification
                self.title = title
                self.desc = description
                self.cant_replace = cant_replace
                self.is_visible = is_visible

            def __repr__(self):
                return (f"ScoreModificationTemplate("
                    f"key={self.key.__repr__()}, "
                    f"modification={self.mod.__repr__()}, "
                    f"title={self.title.__repr__()}, "
                    f"description={self.desc.__repr__()}, "
                    f"cant_replace={self.cant_replace.__repr__()}, "
                    f"is_visible={self.is_visible.__repr__()})")
            
            def to_string(self):
                return json.dumps(
                    {
                        "type": "ScoreModificationTemplate",
                        "key": self.key,
                        "mod": self.mod,
                        "title": self.title,
                        "description": self.desc,
                        "cant_replace": self.cant_replace,
                        "is_visible": self.is_visible
                    }
                )




    class ScoreModification(Object):
            def __init__(self,  template:     "ClassDataObj.ScoreModificationTemplate",
                                target:       "ClassDataObj.Student",
                                title:        Optional[str]                = None,
                                desc:         Optional[str]                = None,
                                mod:          Optional[float]              = None,
                                execute_time: Optional[str]                = None,
                                create_time:  Optional[str]                = None,
                                executed:     bool                         = False):
                """
                分数加减操作的构造函数。

                :param template: 模板
                :param target: 目标学生
                :param title: 标题
                :param desc: 描述
                :param mod: 修改分数
                :param execute_time: 执行时间
                :param create_time: 创建时间
                :param executed: 是否已执行
                """
                if create_time is None:
                    create_time = Base.gettime()
                logstr = "新的待执行的加减分对象创建, "
                self.temp = template

                logstr += "模板信息："+("").join(str(self.temp.__str__()).splitlines(True)).strip().replace("\n",", ") + "; "

                if title == self.temp.title or title is None:
                    self.title = self.temp.title
                else:
                    logstr += "该加减分对象的原因有额外修改：" + title + "; "
                    self.title = title

                if desc == self.temp.desc or desc is None:
                    self.desc = self.temp.desc
                else:
                    logstr += "该加减分对象的详情有额外修改：" + desc + "; "
                    self.desc = desc

                if mod == self.temp.mod or mod is None:
                    self.mod = self.temp.mod
                else:
                    logstr += "该加减分对象的分数变化有额外修改：" + str(mod) + "; "
                    self.mod = mod

                
                self.target = target
                logstr += f"针对的学生：{target._name}({target._num}号，目前{target._score}分)"
                self.execute_time = execute_time
                self.create_time = create_time
                self.executed = executed
                Base.log("I",logstr + ", 模板创建成功！","ScoreModification.__init__")
            

            def __repr__(self):
                return f"ScoreModification(template={self.temp.__repr__()}, target={self.target.__repr__()}, title={self.title.__repr__()}, desc={self.desc.__repr__()}, mod={self.mod.__repr__()}, execute_time={self.execute_time.__repr__()}, create_time={self.create_time.__repr__()}, executed={self.executed.__repr__()})"


            def execute(self) -> bool:
                "执行当前的操作"
                if self.executed:
                    Base.log("W", "执行已经完成，无需再次执行，如需重新执行请创建新的ScoreModification对象", "ScoreModification.execute")
                    return False
                logstr = ""
                logstr += "开始执行当前加减分, "
                logstr += "信息：" + "".join(str(self).splitlines(True)).strip().replace("\n", ",") + ";"
                Base.log("I", logstr, "ScoreModification.execute")
                try:
                    self.execute_time = Base.gettime()    
                    "执行时间的字符串"
                    self.execute_time_key = int(time.time() * 1000)
                    "执行时间utc*1000"
                    if self.target.highest_score < self.target.score + self.mod:
                        Base.log("I",f"预计刷新最高分：{self.target.highest_score} -> {self.target.score + self.mod}","ScoreModification.execute")
                        self.target.highest_score = self.target.score + self.mod
                        self.target.highest_score_cause_time = self.execute_time_key
                        Base.log("I",f"修改完成，execute_time_key={self.execute_time_key}","ScoreModification.execute")

                    if self.target.lowest_score > self.target.score + self.mod:
                        Base.log("I",f"预计刷新最低分：{self.target.highest_score} -> {self.target.score + self.mod}","ScoreModification.execute")
                        self.target.lowest_score = self.target.score + self.mod
                        self.target.lowest_score_cause_time = self.execute_time_key 
                        Base.log("I",f"修改完成，execute_time_key={self.execute_time_key}","ScoreModification.execute")

                    self.target.score += self.mod
                    Base.log("I",f"执行完成，分数变化：{self.target._score - self.mod} -> {self.target._score}","ScoreModification.execute")
                    self.executed = True                
                    self.target.history[self.execute_time_key] = self
                    return True

                except:
                    if debug:
                        raise
                    Base.log("E","执行时出现错误：\n\t\t"+("\t"*2).join(str(traceback.format_exc()).splitlines(True)).strip(),"ScoreModification.execute")
                    return False

            def retract(self) -> Tuple[bool, str]:
                """撤销执行的操作
                
                :return: 是否执行成功（bool: 结果, str: 成功/失败原因）
                """
                if self not in self.target.history.values():
                    Base.log("W","当前操作未执行，无法撤回","ScoreModification.retract")
                    return False, "并不在本周历史中"
                if self.executed:
                    Base.log("I","尝试撤回上次操作...","ScoreModification.execute")
                    try:
                        if self.mod < 0:
                            findscore = 0.0
                            lowestscore = 0.0
                            lowesttimekey = 0
                            # 这一段就是重新算最高分和最低分
                            for i in self.target.history:
                                tmp: ClassDataObj.ScoreModification = self.target.history[i]

                                if tmp.execute_time_key != self.execute_time_key and tmp.executed: # 自己不参与
                                    findscore += tmp.mod

                                if lowestscore > findscore and tmp.execute_time_key != self.execute_time_key: 
                                    lowesttimekey = tmp.execute_time_key
                                    lowestscore = findscore

                            if self.execute_time_key == lowesttimekey:
                                lowestscore = 0

                            if self.target.lowest_score_cause_time != lowesttimekey:
                                Base.log("I",f"更新lowest_score_cause_time：{self.target.lowest_score_cause_time} -> {lowesttimekey}","ScoreModification.execute")
                                self.target.lowest_score_cause_time = lowesttimekey

                            if self.target.lowest_score != lowestscore:
                                Base.log("I",f"更新lowest_score：{self.target.lowest_score} -> "
                                        f"{lowestscore}","ScoreModification.execute")
                                self.target.lowest_score = lowestscore
                            
                            
                        else:
                            findscore = 0.0
                            highestscore = 0.0
                            highesttimekey = 0
                            for i in self.target.history:
                                tmp: ClassDataObj.ScoreModification = self.target.history[i]
                                if tmp.execute_time_key != self.execute_time_key and tmp.executed:
                                    findscore += tmp.mod

                                if highestscore < findscore and tmp.execute_time_key != self.execute_time_key:
                                    highesttimekey = tmp.execute_time_key
                                    highestscore = findscore
                            if self.execute_time_key == highesttimekey:
                                highestscore = 0
                            if self.target.highest_score_cause_time != highesttimekey:
                                Base.log("I", f"更新highest_score_cause_time："
                                            f"{self.target.highest_score_cause_time} -> {highesttimekey}", 
                                            "ScoreModification.execute")
                                self.target.highest_score_cause_time = highesttimekey 

                            if self.target.highest_score != highestscore:
                                Base.log("I",f"更新highest_score：{self.target.highest_score} -> "
                                        f"{highestscore}","ScoreModification.execute")
                                self.target.highest_score = highestscore


                        score_orig = self.target.score
                        self.target.score -= self.mod
                        Base.log("I",f"撤销完成，分数变化：{score_orig} -> {self.target._score}",
                                "ScoreModification.retract")
                        self.executed = False
                        self.execute_time = None
                        del self
                        return True, "操作成功完成"
                    except:
                        if debug:raise
                        Base.log("E","执行时出现错误：\n\t\t"+("\t"*2).join(str(traceback.format_exc()).splitlines(True)).strip(),"ScoreModification.retract")
                        return False, "执行时出现不可预测的错误"
                else:
                    Base.log("W","操作并未执行，无需撤回","ScoreModification.retract")
                    return False, "操作并未执行, 无需撤回"
                
            

            def to_string(self):
                return json.dumps(
                    {
                        "type":             "ScoreModification",
                        "template":          self.temp.uuid,
                        "target":            self.target.uuid,
                        "title":             self.title,
                        "mod":               self.mod,
                        "desc":              self.desc,
                        "executed":          self.executed,
                        "create_time":       self.create_time,
                        "execute_time":      self.execute_time,
                        "execute_time_key":  self.execute_time_key,
                    }
                )



    class HomeworkRule(Object, SupportsKeyOrdering):
        "作业规则"
        def __init__(self, 
                    key:           str, 
                    subject_name:  str, 
                    ruler:         str, 
                    rule_mapping:  Dict[str, "ClassDataObj.ScoreModificationTemplate"]):
            """
            作业规则构造函数。

            :param key: 在homework_rules中对应的key
            :param subject_name: 科目名称
            :param ruler: 规则制定者
            :param rule_mapping: 规则映射
            """
            self.key = key
            self.subject_name = subject_name
            self.ruler = ruler
            self.rule_mapping = rule_mapping


        def to_string(self):
            return json.dumps(
                {
                    "type":             "HomeworkRule",
                    "subject_name":     self.subject_name,
                    "ruler":            self.ruler,
                    "rule_mapping":     dict([(n, t.uuid) for n, t in self.rule_mapping.items()]),
                }
            )




    class Class(Object, SupportsKeyOrdering):
            "一个班级"
            def __init__(self, 
                        name:            str, 
                        owner:           str, 
                        students:        Union[Dict[int, "ClassDataObj.Student"], OrderedKeyList["ClassDataObj.Student"]], 
                        key:             str,  
                        groups:          Union[Dict[int, "ClassDataObj.Group"], OrderedKeyList["ClassDataObj.Group"]],
                        cleaing_mapping: Optional[Dict[int, Dict[Literal["member", "leader"], List["ClassDataObj.Student"]]]] = None,
                        # 我知道cleaning拼错了，但是改不了了。。。。
                        homework_rules:  Optional[Union[Dict[str, "ClassDataObj.HomeworkRule"], OrderedKeyList["ClassDataObj.HomeworkRule"]]] = None):
                """
                班级构造函数。

                :param name: 班级名称
                :param owner: 班主任
                :param students: 学生列表
                :param key: 在self.classes中对应的key
                :param cleaing_mapping: 打扫卫生人员的映射
                :param homework_rules: 作业规则
                """
                self.name     = name
                self.owner    = owner
                self.groups   = groups
                self.students = students
                self.key      = key
                self.cleaing_mapping = cleaing_mapping if cleaing_mapping is not None else {}
                self.homework_rules = OrderedKeyList(homework_rules) if homework_rules is not None else OrderedKeyList([])

            def __repr__(self):
                return f"Class(name={self.name.__repr__()}, owner={self.owner.__repr__()}, students={self.students.__repr__()}, key={self.key.__repr__()}, cleaing_mapping={self.cleaing_mapping.__repr__()})"


            @property 
            def total_score(self):
                "班级总分"
                return sum([s.score for s in self.students.values()])
            
            @property
            def student_count(self):
                "班级人数"
                return len(self.students)
            
            @property
            def student_total_score(self):
                "学生总分（好像写过了）"
                return sum([s.score for s in self.students.values()])
            
            @property
            def student_avg_score(self):
                "学生平均分"
                return self.student_total_score / max(self.student_count, 1) # 这边要注意小心不要除以0

            @property
            def stu_score_ord(self):
                "学生分数排序，这个不常用"
                return dict(enumerate(
                    sorted(list(self.students.values()), key=lambda a:a.score), start=1))

            @property
            def rank_non_dumplicate(self):
                """学生分数排序，去重
                
                至于去重是个什么概念，举个例子
                >>> target_class.rank_non_dumplicate
                [
                    (1, Student(name="某个学生", score=114, ...)),
                    (2, Student(name="某个学生", score=51,  ...)),
                    (2, Student(name="某个学生", score=51,  ...)),
                    (4, Student(name="某个学生", score=41,  ...)),
                    (5, Student(name="某个学生", score=9,   ...)),
                    (5, Student(name="某个学生", score=9,   ...)),
                    (7, Student(name="某个学生", score=1,   ...))
                ]"""
                stu_list = self.students.values()
                stu_list = sorted(stu_list, key=lambda s:s.score, reverse=True)
                stu_list2:List[Tuple[int, "ClassDataObj.Student"]] = [] 
                last = inf
                last_ord = 0
                cur_ord = 0
                for stu in stu_list:
                    cur_ord += 1
                    if stu.score == last:
                        _ord = last_ord
                    else:
                        _ord = cur_ord
                        last_ord = cur_ord
                    stu_list2.append((_ord, stu))
                    last = stu.score
                return stu_list2


            @property
            def rank_dumplicate(self):
                """学生分数排序，不去重
                
                也举个例子
                >>> target_class.rank_non_dumplicate
                [
                    (1, Student(name="某个学生", score=114, ...)),
                    (2, Student(name="某个学生", score=51,  ...)),
                    (3, Student(name="某个学生", score=51,  ...)),
                    (4, Student(name="某个学生", score=41,  ...)),
                    (5, Student(name="某个学生", score=9,   ...)),
                    (6, Student(name="某个学生", score=9,   ...)),
                    (7, Student(name="某个学生", score=1,   ...))
                ]"""
                stu_list = self.students.values()
                stu_list = sorted(stu_list, key=lambda s:s.score, reverse=True)
                stu_list2:List[Tuple[int, "ClassDataObj.Student"]] = [] 
                last = inf
                last_ord = 0
                cur_ord = 0
                for stu in stu_list:
                    if stu.score == last:
                        _ord = last_ord
                        cur_ord += 1

                    else:
                        cur_ord += 1
                        _ord = cur_ord
                        last_ord = cur_ord
                    stu_list2.append((_ord, stu))
                    last = stu.score               
                return stu_list2


            def reset(self) -> "ClassDataObj.Class":
                "重置班级"
                class_orig = copy.deepcopy(self)
                Base.log("W", f" -> 重置班级：{self.name} ({self.key})")
                for s in self.students.values():
                    s.reset()
                return class_orig


            def to_string(self) -> str:
                return json.dumps(
                    {
                        "type":      "Class",
                        "key":       self.key,
                        "name":      self.name,
                        "onwer":       self.owner,
                        "students":  [s.uuid for s in self.students.values()],
                        "groups":    [g.uuid for g in self.groups.values()],
                        "cleaing_mapping": {{k: {t: [_s.uuid for _s in s] for t, s in v.items()}} for k, v in self.cleaing_mapping.items()},
                        "homework_rules": {n: t.uuid for n, t in self.homework_rules.items()}
                    }
                )



    class ClassData(Object):
        "班级数据，用于判断成就"
        def __init__(self, 
                    student:         "ClassDataObj.Student",
                    classes:          Dict[str, "ClassDataObj.Class"]   = None, 
                    class_obs:       "ClassStatusObserver"       = None, 
                    achievement_obs: "AchievementStatusObserver" = None):
            """班级数据构造函数。

            :param student: 学生
            :param classes: 班级字典
            :param class_obs: 班级侦测器
            :param achievement_obs: 成就侦测器
            """
            self.classes = classes
            "班级的dict"
            self.class_obs = class_obs
            "班级侦测器"
            self.achievement_obs = achievement_obs
            "成就侦测器"
            self.student = student
            "学生"
            self.student_class = self.classes[self.student.belongs_to]
            "学生所在的班级"
            self.student_group = self.student_class.groups[self.student.belongs_to_group]
            "学生所在的组"
            self.groups = self.student_class.groups
            "班级中的所有组"
        





    class ObserverError(Exception):"侦测器出错"

    class AchievementTemplate(Object, SupportsKeyOrdering):
            def __init__(self,     
                        key:str,
                        name:str,
                        desc:str,                           
                        # 满足以下所有条件才会给成就
                        when_triggered:Union[Literal["any", "on_reset"], 
                                            Iterable[Literal["any", "on_reset"]]]="any", # 触发时机
                        name_equals:Optional[Union[str, Iterable[str]]]=None,   # 名称等于/在列表中
                        num_equals:Optional[Union[int, Iterable[int]]]=None,    # 学号等于/在列表中
                        name_not_equals:Optional[Union[str, Iterable[str]]]=None,  # 名称不等于/在列表中
                        num_not_equals:Optional[Union[int, Iterable[int]]]=None,# 学号不等于/在列表中
                        score_range:Optional[Union[Tuple[float, float], List[Tuple[float, float]]]]=None,         # 分数范围
                        score_rank_range:Optional[Tuple[int, int]]=None,       # 名次范围（不计算并列的，名词按1-2-2-3-3之类计算）
                        highest_score_range:Optional[Tuple[float, float]]=None, # 最高分数范围
                        lowest_score_range:Optional[Tuple[float, float]]=None,  # 最低分数范围
                        highest_score_cause_range:Optional[Tuple[int, int]]=None, # 最高分产生时间的范围（utc，*1000）
                        lowest_score_cause_range:Optional[Tuple[int, int]]=None,  # 最低分产生时间的范围
                        modify_key_range:Optional[Union[Tuple[str, int, int], Iterable[Tuple[str, int, int]]]]=None,          # 指定点评次数的范围（必须全部符合）
                        others:Optional[Union[Callable[["ClassDataObj.ClassData"],  bool], Iterable[Callable[["ClassDataObj.ClassData"], bool]]]]=None,                                # 其他条件
                        sound:Optional[str]=None,
                        icon:Optional[str]=None,
                        condition_info:str="具体就是这样，我也不清楚，没写",
                        further_info:str="貌似是那几个开发者懒得进行文学创作了，所以没有进一步描述"):
                
                """
                
                成就模板构造函数。

                :param key: 成就key
                :param name: 成就名称
                :param desc: 成就描述
                :param when_triggered: 触发时机
                :param name_equals: 名称等于/在列表中
                :param num_equals: 学号等于/在列表中
                :param score_range: 分数范围
                :param score_rank_range: 名次范围（不计算并列的，名词按1-2-2-3-3之类计算）
                :param highest_score_range: 最高分数范围
                :param lowest_score_range: 最低分数范围
                :param highest_score_cause_range: 最高分产生时间的范围（utc，*1000）
                :param lowest_score_cause_range: 最低分产生时间的范围
                :param modify_key_range: 指定点评次数的范围（必须全部符合）
                :param others: 一个或者一个list的lambda或者function，传进来一个Student
                :param sound: 成就达成时的音效
                :param icon: 成就图标（在提示中的）
                """

                self.key = key
                self.name = name
                self.desc = desc

                if name_equals is not None:
                    self.name_eq = name_equals if isinstance(name_equals, list) else [name_equals]

                if name_not_equals is not None:
                    self.name_ne = name_not_equals if isinstance(name_not_equals, list) else [name_not_equals]

                if num_equals is not None:
                    self.num_eq = num_equals if isinstance(num_equals, list) else [num_equals] 

                if num_not_equals is not None:
                    self.num_ne = num_not_equals if isinstance(num_not_equals, list) else [num_not_equals]

                

                if score_range is not None:
                    if not isinstance(score_range, list):
                        score_range = [score_range]
                    self.score_range = score_range

                if score_rank_range is not None:
                    self.score_rank_down_limit = score_rank_range[0]
                    self.score_rank_up_limit = score_rank_range[1]

                if highest_score_range is not None:
                    self.highest_score_down_limit = highest_score_range[0]
                    self.highest_score_up_limit =   highest_score_range[1]

                if lowest_score_range is not None:
                    self.lowest_score_down_limit = lowest_score_range[0]
                    self.lowest_score_up_limit =   lowest_score_range[1]

                if  highest_score_cause_range is not None:
                    self.highest_score_cause_range_down_limit = highest_score_cause_range[0]
                    self.highest_score_cause_range_up_limit =   highest_score_cause_range[1]
                
                if  lowest_score_cause_range is not None:
                    self.lowest_score_cause_range_down_limit = lowest_score_cause_range[0]
                    self.lowest_score_cause_range_up_limit =   lowest_score_cause_range[1]

                if modify_key_range is not None:
                    self.modify_ranges_orig = modify_key_range if isinstance(modify_key_range, list) else [modify_key_range]
                    self.modify_ranges = [{"key":item[0], "lowest":item[1], "highest":item[2]} for item in self.modify_ranges_orig]

                if others is not None:
                    if not isinstance(others, list):
                        self.other = [others]
                    else:
                        self.other = others


                self.when_triggered = when_triggered if isinstance(when_triggered, list) else [when_triggered]
                self.sound = sound
                self.icon = icon
                self.further_info = further_info
                self.condition_info = condition_info

            def achieved(self, student: "ClassDataObj.Student", class_obs:"ClassStatusObserver"):
                """
                判断一个成就是否达成
                :param student: 学生
                :param class_obs: 班级状态侦测器
                :raise ObserverError: lambda或者function爆炸了
                :return: 是否达成"""
                # 反人类写法又出现了
                if ("on_reset" in self.when_triggered and "any" not in self.when_triggered
                    ) and  (
                    not (student.highest_score == student.lowest_score == student.score == 0)):
                    return False
                
                if hasattr(self, "name_ne") and student.name in self.name_ne:
                    return False
                
                if hasattr(self, "num_ne") and student.num in self.num_ne:
                    return False


                if hasattr(self, "name_eq") and student.name not in self.name_eq:
                    return False
                
                if hasattr(self, "num_eq") and student.num not in self.num_eq:
                    return False
                
                if hasattr(self, "score_range") and not any([i[0] <= student.score <= i[1] for i in self.score_range]):
                    return False
                try:
                    if hasattr(self,"score_rank_down_limit"):
                        lowest_rank = max(*([i[0] for i in class_obs.rank_dumplicate]))
                        l = lowest_rank + self.score_rank_down_limit + 1 if self.score_rank_down_limit < 0 else self.score_rank_down_limit
                        r = lowest_rank + self.score_rank_up_limit + 1 if self.score_rank_up_limit < 0 else self.score_rank_up_limit
                        if not (l <= [i[0] for i in class_obs.rank_dumplicate if i[1].num == student.num][0] <= r):
                            return False
                except:
                    return False
                if hasattr(self, "highest_score_down_limit") and not self.highest_score_down_limit <= student.highest_score <= self.highest_score_up_limit:return False
                if hasattr(self, "highest_score_cause_range_down_limit") and not self.highest_score_cause_range_down_limit <= student.highest_score_cause_time <= self.highest_score_cause_range_up_limit:return False
                if hasattr(self, "lowest_score_down_limit") and not self.lowest_score_down_limit <= student.lowest_score <= self.lowest_score_up_limit:return False
                if hasattr(self, "lowest_score_cause_range_down_limit") and not self.lowest_score_cause_range_down_limit <= student.lowest_score_cause_time <= self.lowest_score_cause_range_up_limit:return False
                try:
                    if hasattr(self, "modify_ranges") and not all([item["lowest"] <= [history.temp.key for history in student.history.values() if history.executed].count(item["key"]) <= item["highest"] for item in self.modify_ranges]):return False
                except:
                    return False
                
    
                if hasattr(self, "other"):
                    try:
                        if hasattr(self, "other") and not all([func(ClassDataObj.ClassData(student=student, 
                                                                            classes=class_obs.classes,
                                                                            class_obs=class_obs,
                                                                            achievement_obs=class_obs.base.achievement_obs
                                                                            )) for func in self.other]):
                            return False
                    except:
                        Base.log_exc(f"位于成就{self.name}({self.key})的lambda函数出错：", "AchievementTemplate.achieved")
                        if self.key in class_obs.base.DEFAULT_ACHIEVEMENTS:
                            self.other = class_obs.base.DEFAULT_ACHIEVEMENTS[self.key].other
                            Base.log("I", "已经重置为默认值", "AchievementTemplate.achieved")
                        else:
                            raise ClassDataObj.ObserverError(F"位于成就{self.name}({self.key})的lambda函数出错")
                        return False


                return True
            
            def condition_desc(self, class_obs:"ClassStatusObserver"):
                """
                条件描述。
                
                :param class_obs: 班级状态侦测器

                :return: 一个字符串"""
                return_str = ""
                if hasattr(self, "name_eq"):
                    return_str += "仅适用于" + "，".join(self.name_eq) + "\n"

                if hasattr(self, "num_eq"):
                    return_str += "仅适用于学号为" + "，".join([str(n) for n in self.num_eq]) + "的学生\n"

                if hasattr(self, "name_ne"):
                    return_str += "不适用于" + "，".join(self.name_eq) + "\n"

                if hasattr(self, "num_ne"):
                    return_str += "不适用于学号为" + "，".join([str(n) for n in self.num_eq]) + "的学生\n"

                if hasattr(self, "score_range"):
                    first = True
                    for item in self.score_range:
                        if not first:
                            return_str += "或者"
                        first = False
                        down = item[0]
                        up = item[1]
                        if -2 ** 63 < down < up < 2 ** 63:
                            return_str += f"达成时分数介于{down:.1f}和{up:.1f}之间\n"
                        elif up == down:
                            return_str += f"达成时分数为{down:.1f}\n"
                        elif up > 2 ** 63:
                            return_str += f"达成时分数高于{down:.1f}\n"
                        elif down < -2 ** 63:
                            return_str += f"达成时分数低于{up:.1f}\n"
                        
                        else:
                            return_str += "分数为0\n"
                    
                if hasattr(self, "score_rank_down_limit"):
                    if self.score_rank_down_limit == self.score_rank_up_limit:
                        return_str += F"位于班上{('倒数' if self.score_rank_down_limit < 0 else '') + str(abs(self.score_rank_down_limit))}名\n"
                    else:
                        return_str += f"排名介于{('倒数' if self.score_rank_down_limit < 0 else '') + str(abs(self.score_rank_down_limit))}和{('倒数' if self.score_rank_up_limit < 0 else '') + str(abs(self.score_rank_up_limit))}之间\n"
                    
                if hasattr(self, "highest_score_down_limit"):
                    down = self.highest_score_down_limit
                    up = self.highest_score_up_limit
                    if -2 ** 63 < down < up < 2 ** 63:
                        return_str += f"历史最高分数介于{down:.1f}和{up:.1f}之间\n"
                    elif up == down:
                        return_str += f"历史最高分数为{down:.1f}\n"
                    elif up > 2 ** 63:
                        return_str += f"历史最高分数高于{down:.1f}\n"
                    elif down < -2 ** 63:
                        return_str += f"历史最高分数低于{up:.1f}\n"
                    else:
                        return_str += "没看懂，反正对历史最高分有要求（写的抽象了没法判断）\n"

                if hasattr(self, "lowest_score_down_limit"):
                    down = self.lowest_score_down_limit
                    up = self.lowest_score_up_limit
                    if -2 ** 63 < down < up < 2 ** 63:
                        return_str += f"历史最低分数介于{down:.1f}和{up:.1f}之间\n"
                    elif up == down:
                        return_str += f"历史最低分数为{down:.1f}\n"
                    elif up > 2 ** 63:
                        return_str += f"历史最低分数高于{down:.1f}\n"
                    elif down < -2 ** 63:
                        return_str += f"历史最低分数低于{up:.1f}\n"
                    else:
                        return_str += "没看懂，反正对历史最低分有要求（写的抽象了没法判断）\n"

                if hasattr(self, "modify_ranges"):
                    for item in self.modify_ranges:
                        return_str += (f"达成{item['lowest']}到{item['highest']}次\"{class_obs.templates[item['key']].title}\"\n" if item["lowest"] != item["highest"] != inf else 
                            f"达成{item['lowest']}次\"{class_obs.templates[item['key']].title}\"\n" if item["lowest"] == item["highest"] != inf else (
                            f"达成大于等于{item['lowest']}次\"{class_obs.templates[item['key']].title}\"\n" if item["highest"] == inf else (
                                "这写的什么抽象表达式，我看不懂\n"
                            )
                        ))
                        
                if hasattr(self, "other"):
                    return_str += "有一些其他条件，如果没写就自己摸索吧\n"

                if return_str == "":
                    return_str = "(无条件)"
                return_str += "\n" * 2  + self.condition_info
                return return_str
            

            def to_string(self):
                    obj = {"type": "AchievementTemplate"}
                    for attr in (
                    "name",
                    "desc",
                    "condition_info",
                    "further_info",
                    "sound",
                    "icon",
                    "when_triggered",
                    "name_eq",
                    "name_ne",
                    "num_eq",
                    "num_ne",
                    "score_range",
                    "score_rank_down_limit",
                    "score_rank_up_limit",
                    "modify_ranges",
                    "highest_score_up_limit",
                    "highest_score_down_limit",
                    "lowest_score_up_limit",
                    "lowest_score_down_limit",
                    "highest_score_cause_range_up_limit",
                    "highest_score_cause_range_down_limit",
                    "lowest_score_cause_range_up_limit",
                    "lowest_score_cause_range_down_limit"):
                        if hasattr(self, attr):
                            obj[attr] = getattr(self, attr)
                    
                    if hasattr(self, "other"):
                        obj["other"] = [pickle.dumps(c) for c in self.other]

                    return json.dumps(obj)



    class Achievement(Object):
        "一个真实被达成的成就"

        def __init__(self, 
                     template:      "ClassDataObj.AchievementTemplate", 
                     target:        "ClassDataObj.Student", 
                     reach_time:     str=None,
                     reach_time_key: int=None):
                """一个成就的实例。

                :param template: 成就模板
                :param target: 成就的获得者
                :param reach_time: 达成时间
                :param reach_time_key: 达成时间键值
                """
                if reach_time is None:
                    reach_time = Base.gettime()
                if reach_time_key is None:
                    reach_time_key = utc()
                Base.log("D", f"新成就模板创建：target={repr(target)}, time={repr(reach_time)}, key={reach_time_key}")
                self.time = reach_time
                self.time_key = reach_time_key
                self.temp = template
                self.target = target
                self.sound = self.temp.sound

        def give(self):
                "发放成就"
                Base.log("I", f"发放成就：target={repr(self.target)}, time={repr(self.time)}, key={self.time_key}")
                self.target.achievements[self.time_key] = self

        def delete(self):
                "删除成就"
                Base.log("I", f"删除成就：target={repr(self.target)}, time={repr(self.time)}, key={self.time_key}")
                del self

        def to_string(self):
            return json.dumps(
                {
                    "type": "Achievement",
                    "time": self.time,
                    "time_key": self.time_key,
                    "template": self.temp.uuid,
                    "target": self.target.uuid,
                    "sound": self.sound
                }
            )

    class AttendanceInfo(Object):
        "考勤信息"

        def __init__(self, 
                    target_class:    str                   = "CLASS_2216",
                    is_early:        List["ClassDataObj.Student"] = None, 
                    is_late:         List["ClassDataObj.Student"] = None, 
                    is_late_more:    List["ClassDataObj.Student"] = None,
                    is_absent:       List["ClassDataObj.Student"] = None, 
                    is_leave:        List["ClassDataObj.Student"] = None, 
                    is_leave_early:  List["ClassDataObj.Student"] = None, 
                    is_leave_late:   List["ClassDataObj.Student"] = None):
            
            """考勤信息

            :param target_class: 目标班级
            :param is_early: 早到的学生
            :param is_late: 晚到的学生
            :param is_late_more: 晚到得相当抽象的学生
            :param is_absent: 缺勤的学生
            :param is_leave: 临时请假的学生
            :param is_leave_early: 早退的学生
            :param is_leave_late: 晚退的学生，特指某些"热爱学校"的人（直接点我名算了）"""

            if is_early is None:
                is_early = []
            if is_late is None:
                is_late = []
            if is_late_more is None:
                is_late_more = []
            if is_absent is None:
                is_absent = []
            if is_leave is None:
                is_leave = []
            if is_leave_early is None:
                is_leave_early = []
            if is_leave_late is None:
                is_leave_late = []

            self.target_class = target_class
            "目标班级"
            self.is_early = is_early
            "早到的学生"
            self.is_late = is_late
            "晚到（7:25-7:30）的学生"
            self.is_late_more = is_late_more
            "7:30以后到的"
            self.is_absent = is_absent
            "缺勤的学生"
            self.is_leave = is_leave
            "请假的学生"
            self.is_leave_early = is_leave_early
            "早退的学生"
            self.is_leave_late = is_leave_late
            "晚退的学生"

        def to_string(self) -> str:
            return json.dumps({
                "target_class":   self.target_class,
                "is_early":       [s.uuid for s in self.is_early],
                "is_late":        [s.uuid for s in self.is_late],
                "is_late_more":   [s.uuid for s in self.is_late_more],
                "is_absent":      [s.uuid for s in self.is_absent],
                "is_leave":       [s.uuid for s in self.is_leave],
                "is_leave_early": [s.uuid for s in self.is_leave_early],
                "is_leave_late":  [s.uuid for s in self.is_leave_late]
            })


        def is_normal(self, target_class: "ClassDataObj.Class") -> List["ClassDataObj.Student"]:
            "正常出勤的学生，没有缺席"
            return [ s
                    for s in target_class.students.values()
                        if s.num not in [
                            abnormal_s.num for abnormal_s in (
                                self.is_absent
                            )
                        ]
                ]

        @property
        def all_attended(self) -> bool:
            "今天咱班全部都出勤了（不过基本不可能）"
            return len(self.is_absent) == 0
        

    class DayRecord(Object):
        "一天的记录"

        def __init__(self, 
                     target_class:   "ClassDataObj.Class",
                     weekday:         int, 
                     utc:             float, 
                    attendance_info: "ClassDataObj.AttendanceInfo"):
            """构造函数。

            :param target_class: 目标班级
            :param weekday: 星期几（1-7）
            :param utc: 时间戳
            :param attendance_info: 考勤信息
            """
            self.weekday = weekday
            self.utc = utc
            self.attendance_info = attendance_info
            self.target_class = target_class




    class History(Object):
        "每次重置保留的历史记录"
        
        def __init__(self, 
                    classes:Dict[str, "ClassDataObj.Class"], 
                    weekdays:Dict[int, "ClassDataObj.DayRecord"]):
            self.classes = dict(classes)
            self.time = time.time()
            self.weekdays = weekdays

        def __repr__(self):
            return  f"<History object at time {self.time:.3f}>"
        



class ClassObj: ...

class ClassStatusObserver(Object):
    "班级状态侦测器"
    on_active:                 bool
    "是否激活"
    student_count:             int
    "学生人数"
    student_total_score:       float
    "学生总分"
    class_id:                  str
    "班级ID"
    stu_score_ord:             dict
    "学生分数排序"
    classes:                   Dict[str, ClassDataObj.Class]
    "所有班级，是一个字典（ID, 班级对象）"
    target_class:              ClassDataObj.Class
    "目标班级"
    templates:                 Dict[str, ClassDataObj.ScoreModificationTemplate]
    "所有模板"
    opreation_record:          Stack
    "操作记录"
    groups:                    Dict[str, ClassDataObj.Group]
    "所有小组"
    base:                     "ClassObj"
    "后面用到的ClassObjects，算法基层"
    last_update:               float
    "上次更新时间"
    tps:                       int
    "最大每秒更新次数"
    rank_non_dumplicate:       List[Tuple[int, ClassDataObj.Student]]  
    "去重排名"              
    rank_dumplicate:           List[Tuple[int, ClassDataObj.Student]]
    "不去重排名"



class AchievementStatusObserver(Object):
    on_active:                  bool
    "是否激活"
    class_id:                   str
    "班级ID"
    classes:                    Dict[str, ClassDataObj.Class]
    "所有班级"
    achievement_templates:      Dict[str, ClassDataObj.AchievementTemplate]
    "所有成就模板"
    class_obs:                  ClassStatusObserver
    "班级状态侦测器"
    display_achievement_queue:  Queue
    "成就显示队列"
    achievement_displayer:      Callable[[str, ClassDataObj.Student], Any]
    "成就显示函数"
    last_update:                float
    "上次更新时间"
    base:                       "ClassDataObj.ClassObjects"
    "算法基层"
    tps:                        int
    "最大每秒更新次数"

stdout = sys.stdout
stderr = sys.stderr
Base.clear_oldfile(Base.log_file_keepcount)

Student = ClassDataObj.Student
DummyStudent = ClassDataObj.DummyStudent
StrippedStudent = ClassDataObj.SimpleStudent

Class = ClassDataObj.Class
Group = ClassDataObj.Group

AttendanceInfo = ClassDataObj.AttendanceInfo

ScoreModification = ClassDataObj.ScoreModification
ScoreModificationTemplate = ClassDataObj.ScoreModificationTemplate

Achievement = ClassDataObj.Achievement
AchievementTemplate = ClassDataObj.AchievementTemplate

HomeworkRule = ClassDataObj.HomeworkRule
DayRecord = ClassDataObj.DayRecord
Day = ClassDataObj.DayRecord


ClassData = ClassDataObj.ClassData
History = ClassDataObj.History



