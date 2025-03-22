from utils.basetypes import * # 导入所有基础类型(lazy)
import base64

def get_random_template(templates: "OrderedKeyList[ClassObj.ScoreModificationTemplate]"):

    # tip:IDE可以查看上方定义的注释说明
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


class ClassObj(Base):     
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
            self.belongs_to:str = "CLASS_TEST"
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


# Tip:如果需要在类型标注中使用尚未定义的类，可以用引号括起来
    class Student(Object, SupportsKeyOrdering):
            "一个学牲"

            chunk_type_name: Literal["Student"] = "Student"

            score_dtype = HighPrecision
            "记录分数的数据类型（还没做完别乱改）"

            def __init__(self, 
                        name:                     str, 
                        num:                      int, 
                        score:                    float, 
                        belongs_to:               str, 
                        history:                  Dict[Any, "ClassObj.ScoreModification"] = None, 
                        last_reset:               Optional[float]                = None,
                        highest_score:            float                          = 0.0, 
                        lowest_score:             float                          = 0.0,
                        achievements:             Dict[int, "ClassObj.Achievement"]       = None, 
                        total_score:              float                          = None,
                        highest_score_cause_time: float                          = 0.0, 
                        lowest_score_cause_time:  float                          = 0.0,
                        belongs_to_group:         Optional[str]                  = None,
                        last_reset_info:          Optional["ClassObj.Student"]            = None):
                
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
                # 带下划线的属性为内部存储用，实际访问应使用property
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
                self.history:      Dict[int, "ClassObj.ScoreModification"] = history if history is not None else {}
                "历史记录， key为时间戳（utc*1000）"
                self.achievements: Dict[int, "ClassObj.Achievement"] = achievements if achievements is not None else {}
                "所获得的所有成就， key为时间戳（utc*1000）"
                self.belongs_to_group = belongs_to_group
                "所属小组"
                self.last_reset_info = ClassObj.DummyStudent() if last_reset_info is None else last_reset_info
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
                    raise ClassObj.OpreationError(f"请求更改的名字\"{val}\"过长")
                self._name = val
                Base.log("I","更改完成！","Student.name.setter")

            @name.deleter
            def name(self):
                Base.log("E","错误：用户尝试删除学生名","Student.num.deleter")
                raise ClassObj.OpreationError("不允许删除学生的名字")
            

            @property
            def num(self):
                "学生的学号。"
                return self._num

            @num.setter
            def num(self, val:int):
                Base.log("W",f"正在尝试更改学号为{self._name}的学生的学号：由{self._num}更改为{val}","Student.num.setter")
                if val >= 100:
                    Base.log("E","更改学号失败：学号过大了，不太合理","Student.name.setter")
                    raise ClassObj.OpreationError(f"请求更改的学号{val}过大了, 无法设置")
                self._num = val
                Base.log("I","更改完成！","Student.name.setter")

            @num.deleter
            def num(self):
                Base.log("E","错误：用户尝试删除学号（？？？？）","Student.name.deleter")
                raise ClassObj.OpreationError("不允许删除学生的学号")
            
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
                raise ClassObj.OpreationError("不允许直接删除学生的分数")
            
            @property
            def belongs_to(self):
                "学生归属班级。"
                return self._belongs_to

            @belongs_to.setter
            def belongs_to(self,_):
                Base.log("E","错误：用户尝试修改班级","Student.belongs_to.setter")
                raise ClassObj.OpreationError("不允许直接修改学生的班级")

            @belongs_to.deleter
            def belongs_to(self):
                Base.log("E","错误：用户尝试删除班级（？？？？？？？）","Student.belongs_to.deleter")
                raise ClassObj.OpreationError("不允许直接删除学生的班级")


            @property
            def total_score(self):
                return round(self._total_score, 1) if isinstance(self._total_score, float) else round(float(self._total_score), 1)
            
            @total_score.setter
            def total_score(self, value):
                self._total_score = self.score_dtype(value)


            def reset_score(self) -> Tuple[float, float, float, Dict[int, "ClassObj.ScoreModification"]]:
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
                self.history:Dict[int, ClassObj.ScoreModification] = dict()
                self.achievements = dict()
                return returnval
            

            def reset_achievements(self) -> Dict[int, "ClassObj.Achievement"]:
                """重置学生成就。
                
                :return: Dict[成就达成时间utc*1000, 成就]"""
                Base.log("W", f"  -> 重置{self.name} ({self.num})的成就")
                returnval = dict(self.achievements)
                self.achievements = dict()
                return returnval

            def reset(self, reset_achievments:bool=True) -> Tuple[float, float, float, 
                                                    Dict[int, "ClassObj.ScoreModification"], Optional[Dict[int, "ClassObj.Achievement"]]]:
                """重置学生分数和成就。
                    这个操作会更新学生的last_reset_info属性，以记录重置前的分数和成就。
                
                :param reset_achievments: 是否重置成就
                :return: Tuple[当前分数, 历史最高分, 历史最低分, Dict[分数变动时间utc*1000, 分数变动记录], Dict[成就达成时间utc*1000, 成就]"""
                self.last_reset_info = copy.deepcopy(self)
                score, highest, lowest, history = self.reset_score()
                achievements = None
                if reset_achievments:
                    achievements = self.reset_achievements()
                self.refresh_uuid()
                return (score, highest, lowest, history, achievements)

            def get_group(self, class_obs:"ClassStatusObserver") -> "ClassObj.Group":
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
                    ranking_data:List[Tuple[int, "ClassObj.Student"]] = class_obs.rank_non_dumplicate
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
                    ranking_data:List[Tuple[int, "ClassObj.Student"]] = class_obs.rank_non_dumplicate
                    for index, student in ranking_data:
                        if student.num == self.num:
                            return index
                raise ValueError("但是你确定这个学生在这个班？")
                        
            def __add__(self, value: Union["ClassObj.Student", float]) -> "ClassObj.Student":
                "这种东西做出来是致敬班级小管家的（bushi"
                if isinstance(value, ClassObj.Student):
                    history = self.history.copy()
                    history.update(value.history)
                    achievements = self.achievements.copy()
                    achievements.update(value.achievements)
                    Base.log("W", f"  -> 合并学生：({self.name}, {value.name})", "Student.__add__")
                    Base.log("W", "孩子，这不好笑", "Student.__add__")
                    return ClassObj.Student(f"合并学生：({self.name.replace('合并学生：(', '').replace(')', '')}, {value.name.replace('合并学生：(', '').replace(')', '')})",
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
                
            def __iadd__(self, value: Union["ClassObj.Student", float]) -> "ClassObj.Student":
                if isinstance(value, ClassObj.Student):
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
                    "type":                     self.chunk_type_name,
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
            def __init__(self, stu: "ClassObj.Student"):...

            @overload
            def __init__(self, name:str, num:int, score:float, belongs_to:str, history:dict):...
            
            def __init__(self, stu_or_name, num=None, score=None, belongs_to=None, history=None, **kwargs):
                if isinstance(stu_or_name, ClassObj.Student):
                    super().__init__(stu_or_name._name, stu_or_name._num, stu_or_name._score, stu_or_name._belongs_to, {}, **(kwargs))
                else:
                    super().__init__(stu_or_name, num, score, belongs_to, {})
                del self.history            # 单独处理历史记录(防炸)

    class Group(Object):
        "一个小组"
        chunk_type_name: Literal["Group"] = "Group"

        def __init__(self, 
                    key:          str, 
                    name:         str, 
                    leader:       "ClassObj.Student", 
                    members:      List["ClassObj.Student"], 
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
            return (round((sum([s.score for s in self.members]) - min(*[s.score for s in self.members])) / (len(self.members) - 1), 2)) if len(self.members) > 1 else 0.0 # 如果只有一人则返回0


        def has_member(self, student: "ClassObj.Student"):
            "查看一个学生是否在这个小组。"
            return any([s.num == student.num for s in self.members])
        
        def to_string(self):
            "将小组对象转化为字符串。"
            return json.dumps(
                {
                    "type": self.chunk_type_name,
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
            chunk_type_name: Literal["ScoreModificationTemplate"] = "ScoreModificationTemplate"
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
                        "type": self.chunk_type_name,
                        "key": self.key,
                        "mod": self.mod,
                        "title": self.title,
                        "description": self.desc,
                        "cant_replace": self.cant_replace,
                        "is_visible": self.is_visible
                    }
                )




    class ScoreModification(Object):
            chunk_type_name: Literal["ScoreModification"] = "ScoreModification"
            def __init__(self,  template:     "ClassObj.ScoreModificationTemplate",
                                target:       "ClassObj.Student",
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
                            # 重新计算最高分和最低分
                            for i in self.target.history:
                                tmp: ClassObj.ScoreModification = self.target.history[i]

                                if tmp.execute_time_key != self.execute_time_key and tmp.executed: # 排除自身
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
                                tmp: ClassObj.ScoreModification = self.target.history[i]
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
                        "type":              self.chunk_type_name,
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
        chunk_type_name: Literal["HomeworkRule"] = "HomeworkRule"
        def __init__(self, 
                    key:           str, 
                    subject_name:  str, 
                    ruler:         str, 
                    rule_mapping:  Dict[str, "ClassObj.ScoreModificationTemplate"]):
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
                    "type":             self.chunk_type_name,
                    "key":              self.key,
                    "subject_name":     self.subject_name,
                    "ruler":            self.ruler,
                    "rule_mapping":     dict([(n, t.uuid) for n, t in self.rule_mapping.items()]),
                }
            )




    class Class(Object, SupportsKeyOrdering):
            "一个班级"
            chunk_type_name: Literal["Class"] = "Class"
            def __init__(self, 
                        name:            str, 
                        owner:           str, 
                        students:        Union[Dict[int, "ClassObj.Student"], OrderedKeyList["ClassObj.Student"]], 
                        key:             str,  
                        groups:          Union[Dict[int, "ClassObj.Group"], OrderedKeyList["ClassObj.Group"]],
                        cleaing_mapping: Optional[Dict[int, Dict[Literal["member", "leader"], List["ClassObj.Student"]]]] = None,
                        # 某种历史遗留:cleaning拼写错误,但是改不了了
                        homework_rules:  Optional[Union[Dict[str, "ClassObj.HomeworkRule"], OrderedKeyList["ClassObj.HomeworkRule"]]] = None):
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
                return self.student_total_score / max(self.student_count, 1) # Tip:避免除以零错误

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
                stu_list2:List[Tuple[int, "ClassObj.Student"]] = [] 
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
                stu_list2:List[Tuple[int, "ClassObj.Student"]] = [] 
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


            def reset(self) -> "ClassObj.Class":
                "重置班级"
                class_orig = copy.deepcopy(self)
                Base.log("W", f" -> 重置班级：{self.name} ({self.key})")
                for s in self.students.values():
                    s.reset()
                self.refresh_uuid()
                return class_orig


            def to_string(self) -> str:
                return json.dumps(
                    {
                        "type":      self.chunk_type_name,
                        "key":       self.key,
                        "name":      self.name,
                        "onwer":       self.owner,
                        "students":  [s.uuid for s in self.students.values()],
                        "groups":    [g.uuid for g in self.groups.values()],
                        "cleaing_mapping": [(k, [(t, [_s.uuid for _s in s]) for t, s in v.items()]) for k, v in self.cleaing_mapping.items()],
                        "homework_rules": {n: t.uuid for n, t in self.homework_rules.items()}
                    }
                )



    class ClassData(Object):
        "班级数据，用于判断成就"
        def __init__(self, 
                    student:         "ClassObj.Student",
                    classes:          Dict[str, "ClassObj.Class"]   = None, 
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
            chunk_type_name: Literal["AchievementTemplate"] = "AchievementTemplate"
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
                        others:Optional[Union[Callable[["ClassObj.ClassData"],  bool], Iterable[Callable[["ClassObj.ClassData"], bool]]]]=None,                                # 其他条件
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

            def achieved(self, student: "ClassObj.Student", class_obs:"ClassStatusObserver"):
                """
                判断一个成就是否达成
                :param student: 学生
                :param class_obs: 班级状态侦测器
                :raise ObserverError: lambda或者function爆炸了
                :return: 是否达成"""
                # 非常规写法(抽象)
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
                        if hasattr(self, "other") and not all([func(ClassObj.ClassData(student=student, 
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
                            raise ClassObj.ObserverError(F"位于成就{self.name}({self.key})的lambda函数出错")
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
                    obj = {"type": self.chunk_type_name}
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
                        obj["other"] = str(base64.b64encode(pickle.dumps(self.other)))

                    return json.dumps(obj)



    class Achievement(Object):
        "一个真实被达成的成就"
        chunk_type_name: Literal["Achievement"] = "Achievement"
        def __init__(self, 
                     template:      "ClassObj.AchievementTemplate", 
                     target:        "ClassObj.Student", 
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
                    "type": self.chunk_type_name,
                    "time": self.time,
                    "time_key": self.time_key,
                    "template": self.temp.uuid,
                    "target": self.target.uuid,
                    "sound": self.sound
                }
            )

    class AttendanceInfo(Object):
        "考勤信息"
        chunk_type_name: Literal["AttendanceInfo"] = "AttendanceInfo"
        def __init__(self, 
                    target_class:    str                   = "CLASS_TEST",
                    is_early:        List["ClassObj.Student"] = None, 
                    is_late:         List["ClassObj.Student"] = None, 
                    is_late_more:    List["ClassObj.Student"] = None,
                    is_absent:       List["ClassObj.Student"] = None, 
                    is_leave:        List["ClassObj.Student"] = None, 
                    is_leave_early:  List["ClassObj.Student"] = None, 
                    is_leave_late:   List["ClassObj.Student"] = None):
            
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
                "type":           self.chunk_type_name,
                "target_class":   self.target_class,
                "is_early":       [s.uuid for s in self.is_early],
                "is_late":        [s.uuid for s in self.is_late],
                "is_late_more":   [s.uuid for s in self.is_late_more],
                "is_absent":      [s.uuid for s in self.is_absent],
                "is_leave":       [s.uuid for s in self.is_leave],
                "is_leave_early": [s.uuid for s in self.is_leave_early],
                "is_leave_late":  [s.uuid for s in self.is_leave_late]
            })


        def is_normal(self, target_class: "ClassObj.Class") -> List["ClassObj.Student"]:
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
        chunk_type_name: Literal["DayRecord"] = "DayRecord"
        def __init__(self, 
                     target_class:   "ClassObj.Class",
                     weekday:         int, 
                     utc:             float, 
                     attendance_info: "ClassObj.AttendanceInfo"):
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

        def to_string(self):
            return json.dumps(
                {
                    "type":             self.chunk_type_name,
                    "target_class":     self.target_class.uuid,
                    "weekday":          self.weekday,
                    "utc":              self.utc,
                    "attendance_info":  self.attendance_info.uuid
                }
            )


    class History(Object):
        "每次重置保留的历史记录"
        chunk_type_name: Literal["History"] = "History"
        def __init__(self, 
                    classes:Dict[str, "ClassObj.Class"], 
                    weekdays:Union[List["ClassObj.DayRecord"], Dict[float, "ClassObj.DayRecord"]],
                    save_time: Optional[float] = None):
            self.classes = dict(classes)
            self.time = save_time or time.time()
            self.weekdays: Dict[float, DayRecord] = {d.utc: d for d in weekdays} \
                if isinstance(weekdays, list) else weekdays

        def __repr__(self):
            return  f"<History object at time {self.time:.3f}>"
        
        def to_string(self):

            if isinstance(self.weekdays, list):
                self.weekdays = {d.utc: d for d in self.weekdays}

            return json.dumps(
                {
                    "classes":  {k: v.uuid for k, v in self.classes.items()},
                    "time":     self.time,
                    "weekdays": {k: v.uuid for k, v in self.weekdays.items()}
                }
            )
        



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
    classes:                   Dict[str, ClassObj.Class]
    "所有班级，是一个字典（ID, 班级对象）"
    target_class:              ClassObj.Class
    "目标班级"
    templates:                 Dict[str, ClassObj.ScoreModificationTemplate]
    "所有模板"
    opreation_record:          Stack
    "操作记录"
    groups:                    Dict[str, ClassObj.Group]
    "所有小组"
    base:                     "ClassObj"
    "后面用到的ClassObjects，算法基层"
    last_update:               float
    "上次更新时间"
    tps:                       int
    "最大每秒更新次数"
    rank_non_dumplicate:       List[Tuple[int, ClassObj.Student]]  
    "去重排名"              
    rank_dumplicate:           List[Tuple[int, ClassObj.Student]]
    "不去重排名"



class AchievementStatusObserver(Object):
    on_active:                  bool
    "是否激活"
    class_id:                   str
    "班级ID"
    classes:                    Dict[str, ClassObj.Class]
    "所有班级"
    achievement_templates:      Dict[str, ClassObj.AchievementTemplate]
    "所有成就模板"
    class_obs:                  ClassStatusObserver
    "班级状态侦测器"
    display_achievement_queue:  Queue
    "成就显示队列"
    achievement_displayer:      Callable[[str, ClassObj.Student], Any]
    "成就显示函数"
    last_update:                float
    "上次更新时间"
    base:                       "ClassObj.ClassObjects"
    "算法基层"
    tps:                        int
    "最大每秒更新次数"

# 标准输出重定向（停用）
# stdout = sys.stdout
# stderr = sys.stderr
# Base.clear_oldfile(Base.log_file_keepcount)

Student = ClassObj.Student
DummyStudent = ClassObj.DummyStudent
StrippedStudent = ClassObj.SimpleStudent

Class = ClassObj.Class
Group = ClassObj.Group

AttendanceInfo = ClassObj.AttendanceInfo

ScoreModification = ClassObj.ScoreModification
ScoreModificationTemplate = ClassObj.ScoreModificationTemplate

Achievement = ClassObj.Achievement
AchievementTemplate = ClassObj.AchievementTemplate

HomeworkRule = ClassObj.HomeworkRule
DayRecord = ClassObj.DayRecord
Day = ClassObj.DayRecord


ClassData = ClassObj.ClassData
History = ClassObj.History

ClassDataType = Union[Student, Class, Group, 
                      AttendanceInfo, 
                      ScoreModification, ScoreModificationTemplate,
                      Achievement, AchievementTemplate, 
                      DayRecord]

default_score_template = ScoreModificationTemplate("如果你看到了这行信息，多半是加载存档出问题了", 0, "默认模板", "这个模板没用，只是占位用的")
default_student = Student("如果你看到了这行信息，多半是加载存档出问题了", 114514, 1919810, "CLASS_1145")
default_achievement_template = AchievementTemplate("如果你看到了这行信息，多半是加载存档出问题了", 
                                                   "一个不可能达成的成就", 
                                                   "这个成就正如字面意思，是不可能达成的", 
                                                   condition_info="别看了，不可能达成就是不可能达成", 
                                                   further_info="我触发条件都写的lambda: 0.1 + 0.2 == 0.3，怎么可能达成", 
                                                   others=lambda: 0.1 + 0.2 == 0.3) # 浮点数精度测试，disable-python:S1244