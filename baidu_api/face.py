import sys
import ssl
from urllib import request, parse


# client_id 为官网获取的AK， client_secret 为官网获取的SK
# 获取token
def get_token():
    client_id = 'ifcHAWfOSsOQQTuhI1wbinyP'
    client_secret = 'OCoPqGVZOMeVPlrEAkC15AdIZqXOsuYh'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
    client_id, client_secret)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(req)
    # 获得请求结果
    content = response.read()
    # 结果转化为字符
    content = bytes.decode(content)
    # 转化为字典
    content = eval(content[:-1])
    #print(content['access_token'])
    return content['access_token']



# 转换图片
# 读取文件内容，转换为base64编码
# 二进制方式打开图文件
def imgdata(file1path, file2path):
    import base64
    f = open(r'%s' % file1path, 'rb')
    pic1 = base64.b64encode(f.read())
    f.close()
    f = open(r'%s' % file2path, 'rb')
    pic2 = base64.b64encode(f.read())
    f.close()
    # 将图片信息格式化为可提交信息，这里需要注意str参数设置
    params = {"images": str(pic1, 'utf-8') + ',' + str(pic2, 'utf-8')}
    return params


# 提交进行对比获得结果
def img(file1path, file2path):
    token = get_token()
    # 人脸识别API
    # url = 'https://aip.baidubce.com/rest/2.0/face/v2/detect?access_token='+token
    # 人脸对比API
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/match?access_token=' + token
    params = imgdata(file1path, file2path)
    # urlencode处理需提交的数据
    data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url, data=data)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = request.urlopen(req)
    content = response.read()
    content = bytes.decode(content)
    content = eval(content)
    # 获得分数
    score = content['result'][0]['score']
    #print(content)
    if score > 80:
        return '照片相似度：' + str(score) + ',同一个人'
    else:
        return '照片相似度：' + str(score) + ',不是同一个人'



if __name__ == '__main__':
    file1path = r'C:\Users\zzc\Desktop\laopo\1.jpg'
    file2path = r'C:\Users\zzc\Desktop\laopo\11.png'
    #get_token()
    # 单个图片识别
    def one():
        res = img(file1path, file2path)
        print(res)
    # 批量图片识别
    def multi():
        for i in range(2, 12):
            file2path = r'C:\Users\zzc\Desktop\laopo\%s.jpg' % i
            res = img(file1path, file2path)
            print('第%s图片' % i, res)

    one()

