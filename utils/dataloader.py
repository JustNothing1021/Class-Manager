from utils.classdtypes import *
from concurrent.futures import ThreadPoolExecutor
import zipfile
import sqlite3
import shutil
import sys


# 数据加载器

class NullParam:

    def __hash__(self):
        return -1

BaseDataType = Union[int, float, bool, str]






_RT = TypeVar("_RT", Student, Class, Group, 
                      AttendanceInfo, 
                      ScoreModification, ScoreModificationTemplate,
                      Achievement, AchievementTemplate, 
                      DayRecord)


class DataKind(Generic[_RT], str):
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
                return DataObject.loaded_object_list[(self.history_uuid, self.data_type.chunk_type_name, value.uuid)]
            except KeyError:
                obj = self.data_type.from_string(
                    self.chunk.get_object_rdata(self.history_uuid, value.uuid, self.data_type.chunk_type_name))
                DataObject.loaded_object_list[(self.history_uuid, self.data_type.chunk_type_name, value.uuid)] = obj
                setattr(self.instance, item, obj)
                return obj
        else:
            return value



_RDT = TypeVar("_RDT", Student, Class, Group, 
                      AttendanceInfo, 
                      ScoreModification, ScoreModificationTemplate,
                      Achievement, AchievementTemplate, 
                      DayRecord)



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

    def __contains__(self, key):
        return key in self.__dict__ and self.__dict__[key] is not NullParam and self.__dict__[key] is not None





class DataObject:
    "数据对象"

    loaded_objects = 0
    "加载了的对象数量"

    saved_objects = 0
    "保存了的对象数量"

    conn_list: Dict[str, Dict[str, sqlite3.Connection]] = {}
    "连接列表，conn_list[数据类型名称][uuid前两位]=连接对象"

    loaded_object_list: Dict[Tuple[UUIDKind[History], str, UUIDKind[ClassDataType]], ClassDataType] = {}
    "加载目标列表"

    load_tasks: List[Tuple[UUIDKind[History], str, UUIDKind[ClassDataType]]] = []
    "加载任务列表"

    def clear_tasks(self):
        "清空加载任务列表"
        self.load_tasks.clear()

    def clear_loaded_objects(self):
        "清空加载对象列表"
        self.loaded_object_list.clear()

    def relase_connections(self):
        "释放所有连接"
        for conn in self.conn_list.values():
            for c in conn.values():
                try:
                    c.close()
                except:
                    pass
        self.conn_list.clear()



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
                        raise ValueError(f"对于{uuid!r}的对象，数据库中已经存在一个不同类型的对象！"
                                        f"（当前为{type_name!r}，数据库中为{existing_class[0]!r}）\n"
                                        "如果你看见了这个错误，你可能碰见了1/340282366920938463463374607431768211456的概率"
                                        "（不知道该恭喜你还是感到遗憾）")
                else:
                    cursor.execute("""
                        INSERT INTO datas (uuid, class, data)
                        VALUES (?, ?, ?)
                    """, (uuid, type_name, string))
                    conn.commit()

                DataObject.saved_objects += 1
                return

            except Exception as e:

                Base.log_exc(f"处理数据时出现错误，对象：{self.object!r}，0.1秒后重试", "DataObject.save", "W", exc=e)
                conn.rollback()
                time.sleep(0.1)
                continue

        Base.log_exc(f"处理数据时出现错误，对象：{self.object!r}，重试3次后仍然失败", "DataObject.save", "E")


    
    def load_stage1(self, data: str) -> ClassDataType:
        "从某个文件加载这个对象，阶段1 - 只加载基本数据"

        data: Dict[str, Any] = json.loads(data)

        try:
            data_type = data.pop("type")        # 移除类型信息避免参数错误
        except KeyError as e:
            raise KeyError("对象没有具体的数据类型！") from e
        
        uuid = data.pop("uuid")
        archive_uuid = data.pop("archive_uuid")

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
            self.object = ScoreModificationTemplate(**data)
            self.object_load_state = "normal" # 默认加载状态，无需手动连接

        elif data_type == ScoreModification.chunk_type_name:
            self.modify_temp: UUIDKind[ScoreModificationTemplate] = data.pop("template")
            self.modify_target: UUIDKind[Student] = data.pop("target")
            self.modify_execute_time_key: int = data.pop("execute_time_key")
            data["template"] = default_score_template
            data["target"] = default_student
            self.object = ScoreModification(**data)
            self.object.execute_time_key = self.modify_execute_time_key
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

        self.object.uuid = uuid
        self.archive_uuid = archive_uuid
        return self


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

    database_connections: Dict[Tuple[Union[UUIDKind[History], Literal["Current"]], str, str], sqlite3.Connection] = {}
    "数据库连接池，database_connection[(历史记录uuid,数据类型名,对象组uuid第一位)] = sqlite3.Connection"


    def __init__(self, path: str, bound_database: Optional[UserDataBase] = None):
        self.path = path
        self.bound_db = bound_database or UserDataBase(path)
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
            conn = self.database_connections[(history_uuid, data_type, uuid[:1])]
        except KeyError:
            conn = sqlite3.connect(os.path.join(self.path, data_type, f"spilt_{uuid[:1]}.db"), check_same_thread=False)
            self.database_connections[(history_uuid, data_type, uuid[:1])] = conn
        result = conn.execute("SELECT data FROM datas WHERE uuid = ?", (uuid,)).fetchone()
        if result is None:
            raise ValueError("数据不存在")
        return result[0]


    def load_history(self, history_uuid: Union[UUIDKind[History], Literal["Current"]] = "Current") -> History:
        """加载历史记录。

        :param history_uuid: 历史记录uuid
        :return: 历史记录
        :raise ValueError: 历史记录不存在
        """
        failures = []
        def _load_object(uuid: UUIDKind[_DT], data_type: ClassDataType, history_uuid: UUIDKind[History] = history_uuid) -> _DT:
            _id = (history_uuid, data_type.chunk_type_name, uuid)

            DataObject.load_tasks.append(_id)
            try:
                # 尝试直接从缓存中获取
                obj = DataObject.loaded_object_list[_id]
                DataObject.load_tasks.remove(_id)
                return obj

            except KeyError:
                # 如果不存在的话就从数据库读取
                try:
                    # 从连接池获取连接
                    conn = self.database_connections[(history_uuid, data_type.chunk_type_name, uuid[:1])]
                except KeyError:    
                    # 如果没连接就直接开一个新的连接放连接池，不用反复开开关关的节约性能（加载完记得relase_connections，清理内存）
                    conn = sqlite3.connect(
                        os.path.join(path, data_type.chunk_type_name, f"spilt_{uuid[:1]}.db"), 
                        check_same_thread=False)

                    self.database_connections[(history_uuid, data_type.chunk_type_name, uuid[:1])] = conn


                result = conn.execute("SELECT data FROM datas WHERE uuid = ?", (uuid,)).fetchone()
                if result is None:
                    Base.log("W", f"数据不存在，将会返回默认\n数据：{data_type.__qualname__}({uuid})", "Chunk.load_history")
                    DataObject.load_tasks.remove(_id)
                    failures.append(_id)
                    return data_type.new_dummy()
                DataObject.loaded_object_list

                obj_shallow_loaded = data_type.new_dummy()
                # 先浅层加载一下，防止触发无限递归
                DataObject.loaded_object_list[_id] = obj_shallow_loaded
                # 再深层处理，这样就不用担心了
                DataObject.loaded_object_list[_id].inst_from_string(result[0])
                obj = DataObject.loaded_object_list[_id]
                DataObject.load_tasks.remove(_id)
                return obj
        ClassObj.LoadUUID = _load_object
        if history_uuid == "Current":
            path = os.path.join(self.path, "Current")
        else:
            path = os.path.join(self.path, "Histories", history_uuid[:2], history_uuid[2:])
        if not os.path.isdir(path):
            raise ValueError("历史记录不存在")
        class_uuids = json.load(open(os.path.join(path, "classes.json"), "r", encoding="utf-8"))
        weekday_uuids = json.load(open(os.path.join(path, "weekdays.json"), "r", encoding="utf-8"))
        classes = {}
        for key, class_uuid in class_uuids:
            _class: Class = ClassObj.LoadUUID(class_uuid, Class)
            classes[_class.key] = _class

        for key, weekday_uuid in weekday_uuids:
            weekday: DayRecord = ClassObj.LoadUUID(weekday_uuid, DayRecord)
            self.bound_db.weekday_record[weekday.utc] = weekday

        history = History(classes, self.bound_db.weekday_record, 
                        json.load(open(os.path.join(path, "info.json"), "r", encoding="utf-8"))["save_time"])
        
        return history
    

    def load_data(self, load_all: bool = False) -> UserDataBase:
        """加载数据。

        :return: 对象数据
        :param load_all: 是否加载所有数据
        """
        current_record = self.load_history("Current")
        histories = {}

        templates = []
        achievements = []
        current_day_attendance = AttendanceInfo()

        # 有个细节，这里的LoadUUID是纲刚刚加载完这周的，所以不用填默认参数
        template_uuids = json.load(open(os.path.join(self.path, "Current", "templates.json"), "r", encoding="utf-8"))
        for key, template_uuid in template_uuids:
            templates.append(ClassObj.LoadUUID(template_uuid, ScoreModificationTemplate))

        achievement_uuids = json.load(open(os.path.join(self.path, "Current", "achievements.json"), "r", encoding="utf-8"))
        for key, achievement_uuid in achievement_uuids:
            achievements.append(ClassObj.LoadUUID(achievement_uuid, AchievementTemplate))

        info = json.load(open(os.path.join(self.path, "info.json"), "r", encoding="utf-8"))
        self.bound_db.uuid = info["uuid"]
        self.bound_db.save_time = info["save_time"]
        self.bound_db.version = info["version"]
        self.bound_db.version_code = info["version_code"]
        self.bound_db.last_reset = info["last_reset"]
        self.bound_db.last_start_time = info["last_start_time"]
        if load_all:
            for uuid in info["histories"]:
                h = self.load_history(uuid)
                histories[h.time] = h
        return UserDataBase(
            info["user"],
            info["save_time"],
            info["version"],
            info["version_code"],
            info["last_reset"],
            histories,
            current_record.classes,
            templates,
            achievements,
            info["last_start_time"],
            current_record.weekdays,
            current_day_attendance,
        )


    def relase_connections(self) -> None:
        """释放所有连接"""
        for v in self.database_connections.values():
            v.close()
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
        history = History(self.bound_db.classes, self.bound_db.weekday_record)
        save_tasks: List[Tuple[str, History, bool]] = [("Current", history, clear_current)]
        if save_history:
            for k, v in self.bound_db.history_data.items():
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
                path = os.path.join(self.path, "Current")
            if clear:
                shutil.rmtree(path, ignore_errors=True)
            os.makedirs(path, exist_ok=True)
            total_objects = 0
            t = time.time()
            modify_templates: List[ScoreModificationTemplate] = list(self.bound_db.templates.values())
            achivement_templates: List[AchievementTemplate] = list(self.bound_db.achievements.values())
            day_records: List[DayRecord] = list(self.bound_db.weekday_record)
            day_records.append(self.bound_db.current_day_attendance)
            students: List[Student] = []
            modifies: List[ScoreModification] = []
            achievements: List[Achievement] = []
            groups: List[Group] = []
            classes: List[Class] = []
            for _class in current_history.classes.values():
                classes.append(_class)
                for student in _class.students.values():
                    students.append(student)
                    modifies.extend(student.history.values())
                    achievements.extend(student.achievements.values())
                    i = 0
                    while student.last_reset_info:
                        students.append(student.last_reset_info)
                        modifies.extend(student.last_reset_info.history.values())
                        achievements.extend(student.last_reset_info.achievements.values())
                        i += 1
                        student.last_reset_info = None
                        if i > Student.last_reset_info_keep_times:
                            break

                groups.extend(_class.groups.values())
            Base.log("D", F"历史记录中的{uuid}的数据汇总完成，耗时{time.time() - t}秒", "Chunk.save")
            t = time.time()
            c = 0
            for _class in classes:
                DataObject(_class, self).save(path)
                c += 1
                total_objects += 1
            c = max(1, c)
            Base.log("D", F"历史记录中的{uuid}的班级保存完成，耗时{time.time() - t}秒，共{c}个，速率{c / (time.time() - t if (time.time() - t) > 0 else 1): .3f}个/秒", "Chunk.save")
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
            Base.log("D", F"历史记录中的{uuid}的当前出勤保存完成，时间耗时{time.time() - t}秒", "Chunk.save")

            DataObject.relase_connections()
            DataObject.conn_list = {}
            Base.log("D", "当前数据库连接已关闭", "Chunk.save")
            Base.log("D", "保存基本信息", "Chunk.save")
            json.dump(
                {
                    "uuid": uuid if uuid != "Current" else None,
                    "save_time": self.bound_db.save_time,
                    "version": self.bound_db.version,
                    "version_code": self.bound_db.version_code,
                    "last_start_time": self.bound_db.last_start_time,
                    "last_reset": self.bound_db.last_reset,
                    "user": self.bound_db.user,
                    "total_objects": total_objects          # 这个可以在后面用来做加载进度条
                },                                          # 防止进度条因为分配不合理看起来像卡死了
                open(os.path.join(path, "info.json"), "w", encoding="utf-8"),
                indent=4
            )
            json.dump([(c.key, c.uuid) for c in current_history.classes.values()], 
                    open(os.path.join(path, "classes.json"), "w", encoding="utf-8"), indent=4)
            json.dump([(d.utc, d.uuid) for d in current_history.weekdays.values()],
                    open(os.path.join(path, "weekdays.json"), "w", encoding="utf-8"), indent=4)
            json.dump([(t.key, t.uuid) for t in self.bound_db.templates.values()],
                    open(os.path.join(path, "templates.json"), "w", encoding="utf-8"), indent=4)
            json.dump([(a.key, a.uuid) for a in self.bound_db.achievements.values()],
                    open(os.path.join(path, "achievements.json"), "w", encoding="utf-8"), indent=4)


            Base.log("I", f"{uuid}的存档信息保存完成({index}/{total})", "Chunk.save")
        i = 1
        for uuid, current_history, clear in save_tasks:
            save_part(uuid, current_history, clear, i)
            i += 1

        
        Base.log("D", "所有数据保存完成", "Chunk.save")

        # # 保存整个存档数据用的，没必要存json了（多几个文件也让存档文件看起来充实点?）
        json.dump(
            {
                "uuid": uuid if uuid != "Current" else None,
                "user": self.bound_db.user,
                "save_time": self.bound_db.save_time,
                "version": self.bound_db.version,
                "version_code": self.bound_db.version_code,
                "last_start_time": self.bound_db.last_start_time,
                "last_reset": self.bound_db.last_reset,
                "histories": [c.uuid for c in self.bound_db.history_data.values()]

            },
            open(os.path.join(self.path, "info.json"), "w", encoding="utf-8"),
        )












