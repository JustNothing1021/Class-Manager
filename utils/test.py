class HighPrecision:
    def __init__(self, basic_num):
        self.basic_num = basic_num

    def __and__(self, other_num: "HighPrecision"):
        if not isinstance(other_num, HighPrecision):
            other_num = HighPrecision(other_num)
        is_int = self.basic_num % 1 == 0 and other_num.basic_num % 1 == 0

        if is_int:
            bin_basic = bin(self.basic_num).split("b")[-1]
            bin_other = bin(other_num.basic_num).split("b")[-1]
            list_bin_basic = [char for char in bin_basic]
            list_bin_other = [ccc for ccc in bin_other]
            if len(list_bin_basic) > len(list_bin_other):
                times = int(len(list_bin_basic) - len(list_bin_other))
                for i in range(times):
                    list_bin_other.insert(0, str(0))
            elif len(list_bin_basic) < len(list_bin_other):
                times = int((HighPrecision(len(list_bin_other)) - HighPrecision(len(list_bin_basic))).__repr__())
                for i in range(times):
                    list_bin_basic.insert(0, str(0))
            list_result = []
            for u, j in zip(list_bin_basic, list_bin_other):
                if u == str(1) and j == str(1):
                    list_result.append(str(1))
                else:
                    list_result.append(str(0))
            bin_result = ""
            for k in list_result:
                bin_result = bin_result + k
            result = int(bin_result, 2)
            return HighPrecision(result)
        else:
            raise TypeError(f"无法对浮点数进行按位与操作（{self.basic_num}）")
    def __repr__(self):
        return F"{repr(self.basic_num)}"
        

a = HighPrecision(114) & HighPrecision(51)
print(a)