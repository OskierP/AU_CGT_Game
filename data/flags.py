class Flag:
    def __init__(self):
        self.flag = False

    def get_flag(self):
        print(self.flag)
        return self.flag

    def set_flag(self, new_flag):
        self.flag = new_flag


menu_flag = Flag()
#### FLAGS LEVEL 1 ####
next_lvl_1 = Flag()
#### FLAGS LEVEL 2 ####
next_lvl_2 = Flag()

#### FLAGS LEVEL 3&4 ####
lvl3_dog_dead_flag = Flag()
next_lvl_3_1 = Flag()
next_lvl_3_2 = Flag()
next_lvl_4 = Flag()

#### FLAGS LEVEL 5 ####
next_lvl_5 = Flag()
#### FLAGS LEVEL 6 ####

#### FLAGS LEVEL BONUS ####

### others ####
lvl2_complete = Flag()
lvl3_1_complete = Flag()
lvl3_2_complete = Flag()
lvl4_complete = Flag()
lvl5_complete = Flag()