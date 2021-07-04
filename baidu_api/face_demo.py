from aip import AipFace
""" 你的 APPID AK SK """
APP_ID = '10777848'
API_KEY = 'ifcHAWfOSsOQQTuhI1wbinyP'
SECRET_KEY = 'OCoPqGVZOMeVPlrEAkC15AdIZqXOsuYh'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(r'C:\Users\yukizzc\Pictures\小妹.JPG')

""" 调用人脸检测 """
client.detect(image);

""" 如果有可选参数 """
options = {}
options["max_face_num"] = 2
options["face_fields"] = "age,beauty"

""" 带参数调用人脸检测 """
out = client.detect(image, options)
print(out['result'][0]['beauty'])