from typing import Literal


app_style: Literal['windowsvista', 'Windows', 'Fusion', 'windows11'] = 'windows11'
"软件的样式"


app_stylesheet: str = """
QMainWindow { color: black; }
QWidget {color: black; }
"""
"软件的样式表"

nl = "\n"
"换行符，3.8.10中的f-string有奇效"