from utils.classdtypes import *
from concurrent.futures import ThreadPoolExecutor
import zipfile
import sqlite3
import shutil


# 数据加载器

class NullParam:

    def __hash__(self):
        return -1

BaseDataType = Union[int, float, bool, str]

_UT = TypeVar("_UT")

class UUIDKind(Generic[_UT], str):
    "uuid类型, UUIDKind[Student]代表这个uuid可以加载出一个学牲"
    def __init__(self, uuid: str):
        self.uuid = uuid
    def __hash__(self):
        return hash(self.uuid)
    def __eq__(self, other):
        return isinstance(other, UUIDKind) and self.uuid == other.uuid
    def __repr__(self):
        return f"UUIDKind({self.uuid})"
    def __str__(self):
        return self.uuid



_RT = TypeVar("_RT", *ClassDataType)
class DataKind(Generic[_UT], str):
    "数据类型, DataKind[Student]代表这个对象在被访问之后会变成一个对象"
    
    def __init__(self, instance: _RT, bound_chunk: "Chunk", 
                history_uuid: Union[UUIDKind[History], Literal["Current"]]) -> Union["DataKind[_RT]", _RT]:
        """
        根据数据类型生成一个未加载的数据类型。
        
        :param instance: 数据实例
        :param bound_chunk: 数据所在分块
        :return: 数据类型

        - 注意，``Union["DataKind[_RT]", _RT]``中的``_RT``只是用来给类成员提示的，实际上**并不会返回原来的数据类型！**
        """
        self.data_type: Type[ClassDataType] = instance.__class__
        self.instance = instance
        self.chunk = bound_chunk
        self.history_uuid = history_uuid

    def __getattr__(self, item: str) -> Any:
        value = getattr(self.instance, item)
        if isinstance(value, UUIDKind):
            try:
                return DataObject.loaded_object_list[self.history_uuid][self.data_type.chunk_type_name][value.uuid]
            except KeyError:
                # TODO: 给ClassDataType全部写上load_from_string方法
                obj = self.data_type.load_from_string(
                    self.chunk.get_object_rdata(self.history_uuid, value.uuid, self.data_type.chunk_type_name))
                DataObject.loaded_object_list[self.history_uuid][self.data_type.chunk_type_name][value.uuid] = obj
                setattr(self.instance, item, obj)
                return obj
        else:
            return value


_NT = TypeVar("_NT")
class StringObjectDataKind(Generic[_NT], str):
    "对象数据类型, ObjectDataKind[Student]代表这个字符串可以加载出一个学牲"

class UserDataBase(Object):
    "用户数据库"

    def __init__(self,
                user:                   Optional[str] = NullParam,
                save_time:              Optional[float] = NullParam,
                version:                Optional[str] = NullParam,
                version_code:           Optional[int] = NullParam,
                last_reset:             Optional[float] = NullParam,
                history_data:           Optional[Dict[float, History]] = NullParam,
                classes:                Optional[Dict[str, Class]] = NullParam,
                templates:              Optional[Dict[str, "ClassObj.ScoreModificationTemplate"]] = NullParam,
                achievements:           Optional[Dict[str, AchievementTemplate]] = NullParam,
                last_start_time:        Optional[float] = NullParam,
                weekday_record:         Optional[List[DayRecord]] = NullParam,
                current_day_attendance: Optional[AttendanceInfo] = NullParam):
        """构建一个数据库对象。
        :param user: 用户名
        :param save_time: 保存时间
        :param version: 算法核心版本
        :param version_code: 算法核心版本号
        :param last_reset: 上次重置时间戳
        :param history_data: 历史数据
        :param classes: 当前班级列表
        :param templates: 当前分数模板
        :param achievements: 当前成就模板
        :param last_start_time: 上次启动时间
        :param current_day_attendance: 今日出勤状况"""
        self.loaded = False
        self.set(user, save_time, version, version_code, last_reset, history_data,
                 classes, templates, achievements, last_start_time, weekday_record, current_day_attendance)
        
    def set(self,
            user:                   Optional[str] = NullParam,
            save_time:              Optional[float] = NullParam,
            version:                Optional[str] = NullParam,
            version_code:           Optional[int] = NullParam,
            last_reset:             Optional[float] = NullParam,
            history_data:           Optional[Dict[float, History]] = NullParam,
            classes:                Optional[Dict[str, Class]] = NullParam,
            templates:              Optional[Dict[str, "ClassObj.ScoreModificationTemplate"]] = NullParam,
            achievements:           Optional[Dict[str, AchievementTemplate]] = NullParam,
            last_start_time:        Optional[float] = NullParam,
            weekday_record:         Optional[List[DayRecord]] = NullParam,
            current_day_attendance: Optional[AttendanceInfo] = NullParam):
        """构建一个数据库对象。
        :param user: 用户名
        :param save_time: 保存时间
        :param version: 算法核心版本
        :param version_code: 算法核心版本号
        :param last_reset: 上次重置时间戳
        :param history_data: 历史数据
        :param class: 当前班级列表
        :param templates: 当前分数模板
        :param achievements: 当前成就模板
        :param last_start_time: 上次启动时间
        :param current_day_attendance: 今日出勤状况"""
        self.user = user
        self.save_time = save_time
        self.version = version
        self.version_code = version_code
        self.last_reset = last_reset
        self.history_data = history_data
        self.classes = classes
        self.templates = templates
        self.achievements = achievements
        self.last_start_time = last_start_time
        self.weekday_record = weekday_record
        self.current_day_attendance = current_day_attendance
        self.loaded = user is not NullParam # 任一参数非空即视为已加载





class DataObject:
    "数据对象"

    loaded_objects = 0
    "加载了的对象数量"

    saved_objects = 0
    "保存了的对象数量"

    conn_list: Dict[str, Dict[str, sqlite3.Connection]] = {}
    "连接列表，conn_list[数据类型名称][uuid前两位]=连接对象"

    loaded_object_list: Dict[UUIDKind[History], Dict[str, Dict[UUIDKind[ClassDataType], ClassDataType]]] = {}
    "加载目标列表"



    def __init__(self, data: ClassDataType, chunk: "Chunk", state: Literal["none", "detached", "normal"] = "normal"):
        self.object = data
        self.chunk = chunk
        self.object_load_state: Literal["none", "detached", "normal"] = state


    def save(self, path: Optional[str] = None):
        "在数据分组中保存这个对象。"
        uuid = self.object.uuid
        string = self.object.to_string()
        type_name = self.object.chunk_type_name
        path = path or self.chunk.path
        if type_name not in self.conn_list:
            os.makedirs(os.path.join(path, type_name), exist_ok=True)
            dictionary: Dict[str, sqlite3.Connection] = {}
            for i in range(16):
                prefix = f"{i:01x}"
                conn = sqlite3.connect(os.path.join(path, type_name, f"spilt_{prefix}.db"), check_same_thread=False)
                dictionary[prefix] = conn
                cur = conn.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS datas (
                                            uuid   text       primary key,    -- 数据UUID
                                            class  text,                      -- 数据类型
                                            data   text                       -- 数据
                                    )""")
                # conn.commit() - 数据库提交操作（还未使用）
            self.conn_list[type_name] = dictionary

        conn = self.conn_list[type_name][uuid[:1]]
        for i in range(3):
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT class FROM datas WHERE uuid = ?", (uuid,))
                existing_class = cursor.fetchone()
                
                if existing_class:
                    if existing_class[0] == type_name:
                        cursor.execute("""
                            UPDATE datas
                            SET class = ?, data = ?
                            WHERE uuid = ?
                        """, (type_name, string, uuid ))
                    else:
                        raise ValueError(f"对于{uuid!r}的对象，数据库中已经存在一个不同类型的对象！（当前为{type_name!r}，数据库中为{existing_class[0]!r}）\n"
                                        "如果你看见了这个错误，你可能碰见了1/340282366920938463463374607431768211456的概率（不知道该恭喜你还是感到遗憾）")
                else:
                    cursor.execute("""
                        INSERT INTO datas (uuid, class, data)
                        VALUES (?, ?, ?)
                    """, (uuid, type_name, string))
                DataObject.saved_objects += 1
                return

            except Exception as e:

                Base.log_exc(f"处理数据时出现错误，对象：{self.object!r}，0.1秒后重试", "DataObject.save", "W", exc=e)
                conn.rollback()
                time.sleep(0.1)
                continue

        Base.log_exc(f"处理数据时出现错误，对象：{self.object!r}，重试3次后仍然失败", "DataObject.save", "E")


    
    def load_stage1(self, path: str) -> List[Exception]:
        "从某个文件加载这个对象，阶段1 - 只加载基本数据"
        with open(path, "rb") as file:
            string = base64.b64decode(file.read())
        data: Dict[str, BaseDataType] = json.loads(string.decode())
        try:
            data_type = data["type"]
        except KeyError as e:
            raise KeyError(F"来自{path!r}的对象没有具体的数据类型！") from e
        
        data.pop("type")        # 移除类型信息避免参数错误

        if data_type == Student.chunk_type_name:
            self.student_history: List[UUIDKind[ScoreModification]] = data.pop("history")
            self.student_achievements: List[UUIDKind[Achievement]] = data.pop("achievements")
            data["history"] = {}
            data["achievements"] = {}
            data["score"] = Student.score_dtype(data["score"])
            self.object = Student(**data)
            self.object_load_state = "detached"
        
        elif data_type == Group.chunk_type_name:
            self.group_leader: UUIDKind[Student] = data.pop("leader")
            self.group_members: List[UUIDKind[Student]] = data.pop("members")
            data["leader"] = default_student
            data["members"] = []
            self.object = Group(**data)
            self.object_load_state = "detached"

        elif data_type == ScoreModificationTemplate.chunk_type_name:
            self.object = Group(**data)
            self.object_load_state = "normal" # 默认加载状态，无需手动连接

        elif data_type == ScoreModification.chunk_type_name:
            self.modify_temp: UUIDKind[ScoreModificationTemplate] = data.pop("template")
            self.modify_target: UUIDKind[Student] = data.pop("target")
            data["template"] = default_score_template
            data["target"] = default_student
            self.object = ScoreModification(**data)
            self.object_load_state = "detached"

        elif data_type == HomeworkRule.chunk_type_name:
            self.homeworkrule_rule_mapping: Dict[str, UUIDKind[ScoreModificationTemplate]] = data.pop("rule_mapping")
            data["rule_mapping"] = {}
            self.object = HomeworkRule(**data)
            self.object_load_state = "detached"

        elif data_type == Class.chunk_type_name:
            self.class_students: List[UUIDKind[Student]] = data.pop("students")
            self.class_groups: List[UUIDKind[Group]] = data.pop("groups")
            self.class_cleaning_mapping: List[Tuple[int, List[Tuple[Literal["member", "leader"], List[UUIDKind[Student]]]]]] = data.pop("cleaning_mapping")
            # 复杂数据处理逻辑
            # 其实我的意思是这个类型注释过于幽默了
            self.class_homework_rules: Dict[str, UUIDKind[HomeworkRule]] = data.pop("homework_rules")
            data["students"] = {}
            data["groups"] = {}
            data["cleaning_mapping"] = {}
            data["homework_rules"] = {}
            self.object = Class(**data)
            self.object_load_state = "detached"

        elif data_type == AchievementTemplate.chunk_type_name:
            if "other" in data:
                data["other"] = pickle.loads(data[["other"]])
            self.object = AchievementTemplate(**data)
            self.object_load_state = "normal"

        elif data_type == Achievement.chunk_type_name:
            self.achievement_template: UUIDKind[AchievementTemplate] = data.pop("template")
            self.achievement_target: UUIDKind[Student] = data.pop("target")
            data["template"] = default_achievement_template
            data["target"] = default_student
            self.object = Achievement(**data)
            self.object_load_state = "detached"
        
        elif data_type == AttendanceInfo.chunk_type_name:
            self.atdinfo_is_early: List[UUIDKind[Student]] = data.pop("is_early")
            self.atdinfo_is_late: List[UUIDKind[Student]] = data.pop("is_late")
            self.atdinfo_is_late_more: List[UUIDKind[Student]] = data.pop("is_late_more")
            self.atdinfo_is_absent: List[UUIDKind[Student]] = data.pop("is_absent")
            self.atdinfo_is_leave: List[UUIDKind[Student]] = data.pop("is_leave")
            self.atdinfo_is_leave_early: List[UUIDKind[Student]] = data.pop("is_leave_early")
            self.atdinfo_is_leave_late: List[UUIDKind[Student]] = data.pop("is_leave_late")
            data["is_early"] = []
            data["is_late"] = []
            data["is_late_more"] = []
            data["is_absent"] = []
            data["is_leave"] = []
            data["is_leave_early"] = []
            data["is_leave_late"] = []
            self.object = AttendanceInfo(**data)

        elif data_type == DayRecord.chunk_type_name:
            self.dayrecord_target_class: UUIDKind[Class] = data.pop("target_class")
            self.dayrecord_attendance_info: UUIDKind[AttendanceInfo] = data.pop("attendance_info")
            data["target_class"] = None
            data["attendance_info"] = None
            self.object = DayRecord(**data)
            self.object_load_state = "detached"

        elif data_type == History.chunk_type_name:
            self.history_classes: Dict[str, UUIDKind[Class]] = data.pop("classes")
            self.history_weekdays: Dict[int, UUIDKind[DayRecord]] = data.pop("weekdays")
            data["classes"] = {}
            data["weekdays"] = {}
            self.object = History(**data)
            self.object_load_state = "detached"


_LT = TypeVar("_LT")
def spilt_list(lst: Iterable[_LT], slices: int, max_size: Optional[int] = None, min_size: Optional[int] = None) -> List[List[_LT]]:
    size = math.ceil(lst.__len__() / slices)
    if max_size is not None:
        size = min(size, max_size)
    if min_size is not None:
        size = max(size, min_size)
    result = []
    lst = list(lst)
    while lst.__len__() > 0:
        result.append(lst[:size])
        lst = lst[size:]
    return result


_DT = TypeVar("_DT")

class Chunk:
    "数据分组"

    database_connections: Dict[Union[UUIDKind[History], Literal["Current"]], Dict[str, Dict[str, sqlite3.Connection]]] = {}
    "数据库连接池，database_connection[历史记录uuid][数据类型名][分片名, 对象组uuid第一位] = sqlite3.Connection"


    def __init__(self, path: str, bound_database: UserDataBase):
        self.path = path
        self.bound_data = bound_database
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
        
    def get_object_rdata(self, history_uuid:Union[UUIDKind[History], Literal["Current"]], 
                                uuid: UUIDKind[_DT], data_type: str) -> StringObjectDataKind[_DT]:
        """获取对象数据。
        
        :param history_uuid: 历史记录uuid，Current为此周（还未重置的存档
        :param uuid: 对象uuid
        :param data_type: 数据类型名
        :return: 对象数据
        :raise ValueError: 数据不存在
        """
        try:
            conn = self.database_connections[history_uuid][data_type][uuid[:1]]
        except KeyError:
            conn = sqlite3.connect(os.path.join(self.path, data_type, f"spilt_{uuid[:1]}.db"), check_same_thread=False)
            self.database_connections[history_uuid][data_type][uuid[:1]] = conn
        result = conn.execute("SELECT data FROM datas WHERE uuid = ?", (uuid,)).fetchone()
        if result is None:
            raise ValueError("数据不存在")
        return result[0]

    def relase_connections(self) -> None:
        """释放所有连接"""
        for v in self.database_connections.values():
            for vv in v.values():
                for vvv in vv.values():
                    vvv.close()
        self.database_connections.clear()

    def save(self, 
            save_history: bool = True, 
            save_only_if_not_exist: bool = True,
            clear_current: bool = False,
            clear_histories: bool = False) -> None:
        """
        保存数据。

        :param save_history: 是否保存历史记录
        :param save_only_if_not_exist: 是否只保存不存在的数据
        :param clear_current: 是否清理当前数据
        :param clear_histories: 是否清理历史数据
        """
        Base.log("I", "开始保存数据", "Chunk.save")
        if clear_histories:
            shutil.rmtree(self.path, ignore_errors=True)
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(os.path.join(self.path, "Histories"), exist_ok=True)
        history = History(self.bound_data.classes, self.bound_data.weekday_record)
        save_tasks: List[Tuple[str, History, bool]] = [("Current", history, clear_current)]
        if save_history:
            for k, v in self.bound_data.history_data.items():
                if save_only_if_not_exist:
                    if not os.path.isfile(os.path.join(self.path, "Histories", v.uuid[:2], v.uuid[2:], "info.json")):
                        os.makedirs(os.path.join(self.path, "Histories", v.uuid[:2], v.uuid[2:]), exist_ok=True)
                        save_tasks.append((v.uuid, v, clear_histories))
                else:
                    os.makedirs(os.path.join(self.path, "Histories", v.uuid[:2], v.uuid[2:]), exist_ok=True)
                    save_tasks.append((v.uuid, v, clear_histories))
        i = 0
        total = save_tasks.__len__()
        def save_part(uuid: str, current_history: History, clear: bool, index: int) -> None:
            if uuid != "Current":
                path = os.path.join(self.path, "Histories", uuid[:2], uuid[2:])
            else:
                path = os.path.join(self.path, "Histories", "Current")
            if clear:
                shutil.rmtree(path, ignore_errors=True)
            os.makedirs(path, exist_ok=True)
            total_objects = 0
            t = time.time()
            modify_templates: List[ScoreModificationTemplate] = list(self.bound_data.templates.values())
            achivement_templates: List[AchievementTemplate] = list(self.bound_data.achievements.values())
            day_records: List[DayRecord] = list(self.bound_data.weekday_record)
            current_attendance = self.bound_data.current_day_attendance
            students: List[Student] = []
            modifies: List[ScoreModification] = []
            achievements: List[Achievement] = []
            groups: List[Group] = []
            for _class in current_history.classes.values():
                for student in _class.students.values():
                    students.append(student)
                    modifies.extend(student.history.values())
                    achievements.extend(student.achievements.values())
                groups.extend(_class.groups.values())
            Base.log("D", F"历史记录中的{uuid}的数据汇总完成，耗时{time.time() - t}秒", "Chunk.save")
            t = time.time()
            c = 0
            for student in students:
                DataObject(student, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的学生保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            c = 0
            for group in groups:
                DataObject(group, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的小组保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            c = 0
            for modify in modifies:
                DataObject(modify, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的分数修改记录保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            c = 0
            for achievement in achievements:
                DataObject(achievement, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的成就记录保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            c = 0
            for template in modify_templates:
                DataObject(template, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的分数修改模板保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            c = 0
            for template in achivement_templates:
                DataObject(template, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的成就模板保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            c = 0
            for record in day_records:
                DataObject(record, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的每日记录保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
            t = time.time()
            DataObject(current_attendance, self).save(path)
            Base.log("D", F"历史记录中的{uuid}的当前出勤保存完成，时间耗时{time.time() - t}秒", "Chunk.save")

            for dict in DataObject.conn_list.values():
                for conn in dict.values():
                    conn.commit()
                    conn.close()
            DataObject.conn_list = {}
            Base.log("D", "当前数据库连接已关闭", "Chunk.save")
            Base.log("D", "保存基本信息", "Chunk.save")
            json.dump(
                {
                    "uuid": uuid if uuid != "Current" else None,
                    "save_time": self.bound_data.save_time,
                    "version": self.bound_data.version,
                    "version_code": self.bound_data.version_code,
                    "last_start_time": self.bound_data.last_start_time,
                    "last_reset": self.bound_data.last_reset,
                    "user": self.bound_data.user,
                    "total_objects": total_objects          # 这个可以在后面用来做加载进度条
                },                                          # 防止进度条因为分配不合理看起来像卡死了
                open(os.path.join(path, "info.json"), "w", encoding="utf-8"),
                indent=4
            )
            Base.log("I", f"{uuid}的存档信息保存完成({index}/{total})", "Chunk.save")
        i = 1
        for uuid, current_history, clear in save_tasks:
            save_part(uuid, current_history, clear, i)
            i += 1

        
        Base.log("D", "所有数据保存完成", "Chunk.save")

        # 保存整个存档数据用的，没必要存json了（多几个文件也让存档文件看起来充实点?）
        json.dump(self.bound_data.user, open(os.path.join(self.path, "user"), "w+"))
        json.dump(self.bound_data.last_reset, open(os.path.join(self.path, "last_reset"), "w+"))
        json.dump(self.bound_data.save_time, open(os.path.join(self.path, "save_time"), "w+"))
        json.dump(self.bound_data.version, open(os.path.join(self.path, "version"), "w+"))
        json.dump(self.bound_data.version_code, open(os.path.join(self.path, "version_code"), "w+"))
        json.dump(self.bound_data.last_start_time, open(os.path.join(self.path, "last_start_time"), "w+"))





        # 有点小问题，因为其他Object为基类的对象都需要存uuid，因为没有具体的对象连接
        # 所以目前只能先给他uuid存进去，后面再用property（？）获取到具体的对象
        # 懒得写了，先把别的优化好再来写这个吧

        # 保存其他基础数据







