from utils.classdtypes import *
from concurrent.futures import ThreadPoolExecutor
import zipfile
import sqlite3

# 这次没用AI，我全都手打的

class NullParam:

    def __hash__(self):
        return -1

BaseDataType = Union[int, float, bool, str]

_UT = TypeVar("_UT")

class UUIDKind(Generic[_UT], str):
    "uuid类型, UUIDKind[Student]代表这个uuid可以加载出一个学牲"


_NT = TypeVar("_NT")
class ObjectDataKind(Generic[_NT], str):
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
        self.loaded = user is not NullParam # 只要有一个不是空的就当作已经加载了





class DataObject:
    "数据对象"

    loaded_objects = 0
    "加载了的对象数量"

    saved_objects = 0
    "保存了的对象数量"

    conn_list: Dict[str, Dict[str, sqlite3.Connection]] = {}
    "连接列表，conn_list[数据类型名称][uuid前两位]=连接对象"
    def __init__(self, data: ClassDataType, chunk: "Chunk", state: Literal["none", "detached", "normal"] = "normal"):
        self.object = data
        self.chunk = chunk
        self.object_load_state: Literal["none", "detached", "normal"] = state


    def save(self):
        "在数据分组中保存这个对象。"
        uuid = self.object.uuid
        string = self.object.to_string()
        type_name = self.object.chunk_type_name
        if type_name not in self.conn_list:
            os.makedirs(os.path.join(self.chunk.path, type_name), exist_ok=True)
            dictionary: Dict[str, sqlite3.Connection] = {}
            for i in range(256):
                prefix = f"{i:02x}"
                conn = sqlite3.connect(os.path.join(self.chunk.path, type_name, f"{prefix}.db"), check_same_thread=False)
                dictionary[prefix] = conn
                cur = conn.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS datas (
                                            uuid   text       primary key,    -- 数据UUID
                                            class  text,                      -- 数据类型
                                            data   text                       -- 数据
                                    )""")
                # conn.commit()
            self.conn_list[type_name] = dictionary

        conn = self.conn_list[type_name][uuid[:2]]
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
        
        data.pop("type")        # 防止一会传参TypeError

        if data_type == Student.chunk_type_name:
            self.student_history: list[UUIDKind[ScoreModification]] = data.pop("history")
            self.student_achievements: list[UUIDKind[Achievement]] = data.pop("achievements")
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
            self.object_load_state = "normal" # 因为本来就不需要手动连接

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
            # 长  难  句
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

    min_task_per_thread = 200
    max_task_per_thread = 500

    use_threadpool = True

    def __init__(self, path: str, bound_database: UserDataBase):
        self.path = path
        self.bound_data = bound_database
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
        
    def get_object_rdata(self, uuid: UUIDKind[_DT], data_type: str) -> ObjectDataKind[_DT]:
        conn = sqlite3.connect(os.path.join(self.path, data_type, f"{uuid[:2]}.db"), check_same_thread=False)
        result = conn.execute("SELECT data FROM datas WHERE uuid = ?", (uuid,)).fetchone()
        if result is None:
            raise ValueError("数据不存在")
        return result[0]

    def save(self, max_workers: int = 256):
        """保存这个数据分组。
        
        :param max_workers: 最大线程数
        """
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ChunkSave") as executor:

            
            
            tasks = spilt_list(self.bound_data.templates.values(), max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
            running_task = 0
            index = 0
            # total_task = 0
            finished_task = 0
            max_index = tasks.__len__()
            for task_list in tasks:
                def _save_template_list(task_list: List[ScoreModificationTemplate] = task_list):
                    nonlocal running_task
                    for template in task_list:
                        DataObject(template, self).save()
                    running_task -= 1
                    nonlocal finished_task
                    finished_task += 1
                if self.use_threadpool:
                    executor.submit(_save_template_list)
                else:
                    _save_template_list()


                index += 1
                running_task += 1
                # total_task += 1
                Base.log("D", f"分数模板列表保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")


            tasks = spilt_list(self.bound_data.achievements.values(), max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
            index = 0
            max_index = tasks.__len__()
            for task_list in tasks:
                def _save_achievement_template_list(task_list: List[AchievementTemplate] = task_list):
                    nonlocal running_task
                    for achievement in task_list:
                        DataObject(achievement, self).save()
                    running_task -= 1
                    nonlocal finished_task
                    finished_task += 1
                index += 1
                running_task += 1

                if self.use_threadpool:
                    executor.submit(_save_achievement_template_list)
                else:
                    _save_achievement_template_list()
                Base.log("D", f"成就模板列表保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")


            tasks = spilt_list(self.bound_data.history_data.values(), max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
            index = 0
            max_index = tasks.__len__()
            for task_list in tasks:
                def _save_history_list(task_list: List[History] = task_list):
                    nonlocal running_task
                    for history in task_list:
                        DataObject(history, self).save()
                    running_task -= 1
                    nonlocal finished_task
                    finished_task += 1
                index += 1
                running_task += 1
                # total_task += 1
                # executor.submit(_save_history_list)
                if self.use_threadpool:
                    executor.submit(_save_history_list)
                else:
                    _save_history_list()
                Base.log("D", f"历史记录列表保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")



            class_list: List[Class] = list(self.bound_data.classes.values())
            day_record_list: List[DayRecord] = self.bound_data.weekday_record.copy()

            for history in self.bound_data.history_data.values():
                class_list.extend(history.classes.values())
                day_record_list.extend(history.weekdays.values())


            tasks = spilt_list(class_list, max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
            index = 0
            max_index = tasks.__len__()
            for task_list in tasks:
                index = 0
                def _save_class_list(task_list: List[Class] = task_list):
                    nonlocal running_task
                    for _class in task_list:
                        DataObject(_class, self).save()
                        running_task -= 1
                    nonlocal finished_task
                    finished_task += 1
                index += 1
                running_task += 1
                # total_task += 1
                # executor.submit(_save_class_list)
                if self.use_threadpool:
                    executor.submit(_save_class_list)
                else:
                    _save_class_list()
                Base.log("D", f"班级列表保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")
                for _class in task_list:
                    stu_list = _class.students.values()
                    tasks = spilt_list(stu_list, max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
                    index = 0
                    max_index = tasks.__len__()
                    for task_list in tasks:
                        def _save_student_list(stu_list: List[Student] = task_list):
                            nonlocal running_task
                            for student in stu_list:
                                DataObject(student, self).save()
                            running_task -= 1
                            nonlocal finished_task
                            finished_task += 1
                        index += 1
                        running_task += 1
                        # total_task += 1
                        # executor.submit(_save_student_list)
                        if self.use_threadpool:
                            executor.submit(_save_student_list)
                        else:
                            _save_student_list()
                        Base.log("D", f"学生列表保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")

                    for student in _class.students.values():
                        stu_history_list = student.history.values()
                        tasks = spilt_list(stu_history_list, max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
                        index = 0
                        max_index = tasks.__len__()
                        for task_list in tasks:
                            def _save_history_list(history_list: List[History] = task_list):
                                nonlocal running_task
                                for history in history_list:
                                    DataObject(history, self).save()
                                running_task -= 1
                                nonlocal finished_task
                                finished_task += 1
                            index += 1
                            running_task += 1
                            # total_task += 1
                            # executor.submit(_save_history_list)
                            if self.use_threadpool:
                                executor.submit(_save_history_list)
                            else:
                                _save_history_list()

                            Base.log("D", f"历史记录保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")

                        stu_achievement_list = student.achievements.values()
                        tasks = spilt_list(stu_achievement_list, max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
                        index = 0
                        max_index = tasks.__len__()

                        for task_list in tasks:
                            def _save_achievement_list(achievement_list: List[Achievement] = task_list):
                                nonlocal running_task
                                for achievement in achievement_list:
                                    DataObject(achievement, self).save()
                                    nonlocal finished_task
                                    finished_task += 1
                                running_task -= 1
                            index += 1
                            running_task += 1
                            # total_task += 1
                            # executor.submit(_save_achievement_list)
                            if self.use_threadpool:
                                executor.submit(_save_achievement_list)
                            else:
                                _save_achievement_list()
                            Base.log("D", f"成就记录保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")


            tasks = spilt_list(day_record_list, max_workers, Chunk.max_task_per_thread, Chunk.min_task_per_thread)
            index = 0
            max_index = tasks.__len__()
            for task_list in tasks:
                def _save_day_record_list(task_list: List[DayRecord] = task_list):
                    for day_record in task_list:
                        DataObject(day_record, self).save()
                # total_task += 1
                # executor.submit(_save_day_record_list) 
                if self.use_threadpool:
                    executor.submit(_save_day_record_list)
                else:
                    _save_day_record_list()
                Base.log("D", f"每日记录保存任务部署，任务数量: {len(task_list)} ({index}/{max_index})", "Chunk.save")
            



            DataObject(self.bound_data.current_day_attendance, self).save()

        for conns in DataObject.conn_list.values():
            for conn in conns.values():
                conn.commit()
                conn.close()

        DataObject.conn_list = {}

        Base.log("D", "所有数据库连接已关闭", "Chunk.save")



        # 存储卫生人员列表
        if hasattr(self.bound_data, 'cleaning_staff') and self.bound_data.cleaning_staff:
            try:
                cleaning_staff_path = os.path.join(self.path, "cleaning_staff")
                with open(cleaning_staff_path, "w+", encoding="utf-8") as f:
                    json.dump(self.bound_data.cleaning_staff, f, ensure_ascii=False, indent=2)
                Base.log("D", f"卫生人员列表已保存到 {cleaning_staff_path}", "Chunk.save")
            except Exception as e:
                Base.log("E", f"保存卫生人员列表失败: {str(e)}", "Chunk.save")

        # 保存其他基
            








