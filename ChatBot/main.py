from DataBase import DataSource
import numpy

ds = DataSource.data()

# ds.insert_request("test", "testing")
# ds.insert_response("test", "OK")

print(ds.get_answers_by_tag("test"))

