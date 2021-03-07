from app import taskapp
from . import blueprintutil



@blueprintutil.taskgenerator.route('/task/<string:str1>',methods=['GET'])
def task_execute(str1):
   taskapp.task.edit_file(str1)
   taskapp.task.edit_file.schedule(args=(str1,),delay=1)
   return f"Enqueued job to write {str1}"

   



