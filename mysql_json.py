import MySQLdb, json
from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


db=MySQLdb.connect(host="elvis.rowan.edu",port=3306,user="",passwd="",db="adventureworks")
temp = db.cursor(MySQLdb.cursors.DictCursor)
temp.execute("SET session group_concat_max_len=15000")
db.commit()
cursor = db.cursor(MySQLdb.cursors.DictCursor)


with open('sql.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
    cursor.execute(data)
res = cursor.fetchall()
with open('out.txt', 'w') as myfile:
    #myfile.write(json.dumps(res,default=json_serial))
    myfile.write("[")
    outFile = ""
    for row in res:
        out = json.dumps(row,default=json_serial)
        out = out.replace("\\","").replace('}"',"}").replace('"{',"{").replace(']"',"]").replace('"[',"[")        
        print(out) #[1:-1]
        outFile = outFile + out + ",\n"
    myfile.writelines(outFile[:-1])
    myfile.write("]")

#print(json.dumps(res,default=json_serial))
