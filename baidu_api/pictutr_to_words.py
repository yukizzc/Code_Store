from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '11286919'
API_KEY = 'WySjxnDaEW5pNYeG1skW85ej'
SECRET_KEY = 'gmGbipv6Paga8MUpVHVN52jFNHwWeFia '

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(r'C:\Users\zzc\Desktop\绿色版\mm.png')

""" 调用通用文字识别（高精度版） """
client.basicAccurate(image);

""" 如果有可选参数 """
options = {}
options["detect_direction"] = "true"
options["probability"] = "false"

""" 带参数调用通用文字识别（高精度版） """
out = client.basicAccurate(image, options)
data = out['words_result']
string = ''
for i in data:
    string+=i['words']
print(string)
