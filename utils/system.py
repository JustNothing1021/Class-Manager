import sys
import time
import subprocess
from io import TextIOWrapper
from typing_extensions import TextIO
from typing import Literal, Optional, Union, Any, Callable
from queue import Queue
from typing import NamedTuple
from threading import Thread

stdout_queue = Queue()
stderr_queue = Queue()
output_list = []


class SystemLogger(TextIOWrapper):    # 虽然对windows上的os.system没什么用
    """一个用来重定向标准输出的类"""

    def __init__(self, *args, 
                 logger_name:str = "sys.stdout", 
                 level:Literal["I", "W", "E"]="I", 
                 function: Callable[[str, str, str], Any]=None,
                   **kwargs):
        super().__init__(*args, **kwargs)
        self.logger_name = logger_name
        self.line = ""
        self.level = level
        self.function = function

    def write(self, s:str):
        "也不知道为什么会有IndexError，所以pass掉了"
        self.line += s
        if "\n" in self.line:
            try:
                log_content = self.line.rsplit("\n", 1)[0].strip()
                # 如果有function函数，则调用它记录日志，但不再将日志放入队列
                # 这样可以避免重复输出
                if self.function:
                    self.function(self.level, log_content, self.logger_name)
                # 如果没有function函数，则将日志放入队列
                else:
                    # 根据日志类型将日志放入对应队列
                    if self.logger_name == "sys.stdout":
                        stdout_queue.put(log_content)
                    elif self.logger_name == "sys.stderr":
                        stderr_queue.put(log_content)
                self.line = self.line.rsplit("\n", 1)[1]
            except IndexError:
                pass

        return len(s)
    
    def writelines(self, lines):
        try:
            self.line += "\n".join(lines)
            if "\n" in self.line:
                log_content = self.line.rsplit("\n", 1)[0].strip()
                # 如果有function函数，则调用它记录日志，但不再将日志放入队列
                # 这样可以避免重复输出
                if self.function:
                    self.function(self.level, log_content, self.logger_name)
                # 如果没有function函数，则将日志放入队列
                else:
                    # 根据日志类型将日志放入队列
                    if self.logger_name == "sys.stdout":
                        stdout_queue.put(log_content)
                        output_list.append(log_content)
                    elif self.logger_name == "sys.stderr":
                        stderr_queue.put(log_content)
                        output_list.append(log_content)
                self.line = self.line.rsplit("\n", 1)[1]
            return len(lines)
        except IndexError:
            pass
    
    def flush(self):
        super().flush()


class CommandOutput(NamedTuple):
    "系统命令输出"
    stdout:       str
    stderr:       str
    final_output: str
    returncode:   int
    pid:          int
    time_cost:    float
    orig_popen:   subprocess.Popen


def system(args:            Union[str, list],
           show_output:     bool              = True,
           stdin:           Optional[TextIO]  = None,
           stdout:          Optional[TextIO]  = None,
           stderr:          Optional[TextIO]  = None,
           encoding:        str               = "gbk",
           cwd:             Optional[str]     = None,
           sync_update_bit: int               = 1
        ) -> CommandOutput:
    """执行命令，采用了世界上最脑溢血的写法
    
    :param args: 命令
    :param show_output: 是否显示输出，默认为True
    :param stdin: 标准输入，默认为None
    :param stdout: 标准输出，默认为None
    :param stderr: 标准错误，默认为None
    :param encoding: 编码，默认为gbk
    :param cwd: 工作目录，默认为None
    :param sync_update_bit: 同步更新位数，默认为1（每次从输出里面读取的字节数）
    """
    st = time.time()
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr

    _popen = subprocess.Popen(args,
                            stdin = sys.stdin,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            cwd = cwd,
                            encoding = encoding,
                            bufsize = sync_update_bit,
                            shell = True,
                            errors = "replace")
    _stdout_sb = ""
    _stderr_sb = ""
    _outprt_pointer = 0
    _errprt_pointer = 0
    _final_output = ""
    def _write():
        nonlocal _stderr_sb, _stdout_sb
        nonlocal _outprt_pointer, _errprt_pointer
        while not(len(_stdout_sb)<=_outprt_pointer and
                 len(_stderr_sb)<=_errprt_pointer) or _popen.poll() == None:
                if len(_stdout_sb)>_outprt_pointer:
                    _written = len(_stdout_sb)
                    if show_output:
                        stdout.write(_stdout_sb[_outprt_pointer:_written])
                    _outprt_pointer = _written
                if len(_stderr_sb)>_errprt_pointer:
                    _written = len(_stderr_sb)
                    if show_output:
                        stderr.write(_stderr_sb[_errprt_pointer:_written])
                    _errprt_pointer = _written
    t = Thread(target=_write)
    t.start()
    def _read_stdout():
        nonlocal _stdout_sb, _popen, _final_output
        while True:
            try:
                c = _popen.stdout.read(sync_update_bit)
            except:
                c = "?"
            if c == "" and _popen.poll() is not None:
                return
            _stdout_sb += c
            _final_output += c
            
    def _read_stderr():
        nonlocal _stderr_sb, _popen, _final_output
        while True:
            try:
                c = _popen.stderr.read(sync_update_bit)
            except:
                c = "?"
            if c == "" and _popen.poll() is not None:
                return
            _stderr_sb += c
            _final_output += c
    out_reader = Thread(target=_read_stdout)
    err_reader = Thread(target=_read_stderr)
    out_reader.start()
    err_reader.start()
    while (_popen.poll() == None) or (out_reader.is_alive() and err_reader.is_alive()):
        "就这等着吧"
    pid = _popen.pid
    returncode = _popen.returncode
    sys.stdout.flush()
    sys.stderr.flush()
    while t.is_alive(): "等待直到输出线程结束"
    return CommandOutput(_stdout_sb, _stderr_sb, _final_output, returncode, pid, time.time() - st, _popen)

def system_lined(args:            Union[str, list],
                show_output:     bool              = True,
                stdin:           Optional[TextIO]  = None,
                stdout:          Optional[TextIO]  = None,
                stderr:          Optional[TextIO]  = None,
                encoding:        str               = "gbk",
                cwd:             Optional[str]     = None,
                ) -> CommandOutput:
    """执行命令，但是输出按行
    
    :param args: 命令
    :param show_output: 是否显示输出，默认为True
    :param stdin: 标准输入，默认为None
    :param stdout: 标准输出，默认为None
    :param stderr: 标准错误，默认为None
    :param encoding: 编码，默认为gbk
    :param cwd: 工作目录，默认为None
    :param sync_update_bit: 同步更新位数，默认为1（每次从输出里面读取的字节数）
    """
    st = time.time()
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr

    _popen = subprocess.Popen(args,
                            stdin = sys.stdin,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            cwd = cwd,
                            encoding = encoding,
                            bufsize = 1,
                            shell = True,
                            errors = "replace")
    _stdout_sb = ""
    _stderr_sb = ""
    _final_output = ""

    def _read_stdout():
        nonlocal _stdout_sb, _popen, _final_output
        while True:
            c = _popen.stdout.readline()
            if c == "" and _popen.poll() is not None:
                return
            if show_output:
                sys.stdout.write(c)
            _stdout_sb += c
            _final_output += c
            
    def _read_stderr():
        nonlocal _stderr_sb, _popen, _final_output
        while True:
            c = _popen.stderr.readline()
            if c == "" and _popen.poll() is not None:
                return
            if show_output:
                sys.stderr.write(c)
            _stderr_sb += c
            _final_output += c
    out_reader = Thread(target=_read_stdout)
    err_reader = Thread(target=_read_stderr)
    out_reader.start()
    err_reader.start()
    while (_popen.poll() == None) or (out_reader.is_alive() and err_reader.is_alive()):
        "就这等着吧"
    pid = _popen.pid
    returncode = _popen.returncode
    sys.stdout.flush()
    sys.stderr.flush()
    return CommandOutput(_stdout_sb, _stderr_sb, _final_output, returncode, pid, time.time() - st, _popen)

if __name__ == "__main__":
    print(system_lined("ping baidu.com"))