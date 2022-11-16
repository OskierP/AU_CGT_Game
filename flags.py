class Flag:
    def __init__(self):
        self.flag = False

    def get_flag(self):
        print(self.flag)
        return self.flag

    def set_flag(self, new_flag):
        self.flag = new_flag


dog_dead_flag = Flag()
next_lvl_1 = Flag()
next_lvl_2 = Flag()

