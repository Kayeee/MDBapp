courseObject.students.add(studentObj)
studentObj.course_set

rabbitmq:
user:Kevin
pass:ASUi3dea
env:pi_env
run command: rabbitmq-server

CELERY:
Run from ~/Documents/MDB/MyDigitalBackpack2
celery worker -A MDB.tasks -l info


Running on Windows
start env: navigate to teema folder. run: "env/Scripts/activate"
