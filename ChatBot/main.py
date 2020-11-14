from DataBase import DB
import numpy

ds = DB.MyData()

# ds.insert_request("test", "testing")
# ds.insert_response("test", "OK")

print(ds.get_answers_by_tag("test"))

