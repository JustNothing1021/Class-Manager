from typing import Literal, Any
import pickle
import os
import dill as pickle
from types import MethodType, FunctionType
from utils.basetypes import Base
from utils.update_check import CLIENT_VERSION, CLIENT_VERSION_CODE

class SettingsInfo:
        """设置信息"""

        current: "SettingsInfo"
        
        def __init__(self, **kwargs):
            """设置参数"""
            self.reset()
            for k, v in kwargs.items():
                setattr(self, k, v)

        def reset(self) -> "SettingsInfo":
            "重置设置"

            if not hasattr(self, "client_version"):
                self.client_version = CLIENT_VERSION
                self.client_version_code = CLIENT_VERSION_CODE
                
            self.opacity = 0.82
            self.score_up_color_mixin_begin = (0xca, 0xff, 0xca) 
            self.score_up_color_mixin_end = (0x33, 0xcf, 0x6c)
            self.score_up_color_mixin_step = 15
            self.score_up_color_mixin_start = 2
            self.score_up_flash_framelength_base = 300
            self.score_up_flash_framelength_step = 100
            self.score_up_flash_framelength_max = 2000

            self.score_down_color_mixin_begin = (0xfc, 0xb5, 0xb5)
            self.score_down_color_mixin_end = (0xa9, 0x00, 0x00)
            self.score_down_color_mixin_step = 15
            self.score_down_color_mixin_start = 2
            self.score_down_flash_framelength_base = 300
            self.score_down_flash_framelength_step = 100
            self.score_down_flash_framelength_max = 2000

            self.log_file_path = 'class_manager.log'
            self.log_format = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {module}:{function}:{line} - {message}'
            self.log_keep_linecount = 100
            self.log_update_interval = 0.1

            self.auto_save_enabled = True
            self.auto_save_interval = 300
            self.auto_save_path:Literal["folder", "user"] = "folder"
            self.auto_backup_scheme:Literal["none", "only_data", "all"] = "none"

            self.animation_speed = 1.0
            self.subwindow_x_offset = 0
            self.subwindow_y_offset = 0
            self.use_animate_background = False
            self.max_framerate = 60
            return self

        def save_to(self, file_path:str) -> "SettingsInfo":
            "保存设置"
            Base.log("I", f"保存设置到{file_path}", "SettingsInfo.save_to")
            if not os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
            os.remove(file_path) if os.path.exists(file_path) else None
            try:
                pickle.dump(self, open(file_path, "wb"))
            except Exception as e:
                Base.log_exc("保存设置失败", "SettingsInfo.save_to", exc=e)
            return self

        def load_from(self, file_path:str) -> "SettingsInfo":
            "加载设置"
            try:
                obj: "SettingsInfo" = pickle.load(open(file_path, "rb"))
                self.__dict__.update(obj.get_dict())
            except Exception as e:
                Base.log_exc("加载设置失败，将会返回默认", "SettingsInfo.load_from", exc=e)
                self.reset()
                self.save_to(file_path)
            return self

        def set(self, **kwargs) -> "SettingsInfo":
            "设置设置"
            Base.log("I", "设置设置", "SettingsInfo.set")
            for k, v in kwargs.items():
                setattr(self, k, v)
            return self
        
        def get(self, key:str) -> Any:
            "获取设置"
            return getattr(self, key)

        def get_dict(self):
            "返回设置字典"
            return dict((k, v) for k, v in self.__dict__.items() 
                        if (not k.startswith('__')) and 
                        (not isinstance(k, (FunctionType, MethodType))))
        
        def __repr__(self):
            "返回设置信息"
            return f"SettingsInfo({dict((k, v) for k, v in self.__dict__.items() if not k.startswith('__')) !r})"
        

SettingsInfo.current = SettingsInfo()
