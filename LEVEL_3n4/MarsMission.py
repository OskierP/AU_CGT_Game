# import flags as flags
# from LEVEL_3n4.levels import level4_1, level4_2
# import LEVEL_3n4.Restart_page as Restart_page
#
# run1 = True
# run2 = True
# run3 = True
#
# while not flags.next_lvl_1.get_flag():
#     if not level4_1.run_level(run1):
#         if flags.dog_dead_flag.get_flag():
#             Restart_page.restart()
#             run1 = True
#             flags.dog_dead_flag.set_flag(False)
#
# while not flags.next_lvl_2.get_flag():
#     if not level4_2.run_level(run2):
#         if flags.dog_dead_flag.get_flag():
#             Restart_page.restart()
#             run2 = True
#             flags.dog_dead_flag.set_flag(False)
#
# while not flags.next_lvl_3.get_flag():
#     print('lvl3')
#
#
