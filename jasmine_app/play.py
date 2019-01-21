import inspect
from werkzeug.utils import import_string

result = inspect.getmembers('jasmine_app')
for each in result:
    print(each)

res = import_string('jasmine_app')
print(res)
