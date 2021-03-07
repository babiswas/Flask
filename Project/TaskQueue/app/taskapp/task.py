from . import config

huey=config.huey

@huey.task()
def edit_file(str1):
   with open("test600.txt",'w') as file:
       file.write(str1)
   return True