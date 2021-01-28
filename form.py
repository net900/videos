import requests
import json
import random
from Crypto.Cipher import AES
import base64
import time
import os
from io import BytesIO
from Crypto.Util.Padding import pad
import urllib
import re
from datetime import datetime

user = ''#账号
upass = ''#密码
area = 'xx省/xx市/xx区'#xx省/xx市/xx区
address = '中国xx省xx市xx区xx路'#中国xx省xx市xx区xx路
lat = ''#纬度,必填，填写定位时需要
lon = ''#经度,必填，填写定位时需要
host = 'https://gpc.campusphere.net'
host2 = 'http://authserver.gpc.net.cn/authserver'
Cpextension = 'Y/DE+I/fjjCrIIPtu3Bcy4wBIP/NBSjQEIVKqHISHDF9SPgoSFP4M2eeTezmYmVrCisEW2nFPFstjjbXIYY0lvsutIV/zEj8eGBDZcBxzWcv+2EE5llmqCicLHqBlgnCWeodr2rdc/sxZMFaCTFW14OQsYLHrdJWsIOlDk6r9edYQD/yjVHp3Auz8PeTpJgL1uGoYcsDKnGWURaA7mCkUof5e1g1i/ZhyyNDhvu30KF414ZZRQChXxw0/v8Z0vGpHJIIXo0u6Xg='
#Cpextension只有问卷提交才会使用到，app每次更新都会换一次 Des加密 这里用的还是8.2.14的加密 暂未失效仍可使用
session = requests.Session()


def str_rand(length=64):
    num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
    return num_str


def encrypt(text, key):
    text = text.encode('utf-8')
    key = key.encode('utf-8')
    iv = str_rand(16).encode('utf-8')
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    pad_pkcs7 = pad(text, AES.block_size, style='pkcs7')
    ciphertext = cryptor.encrypt(pad_pkcs7)
    return base64.b64encode(ciphertext)


def get_curl(url, post='', cookies='', pass_cookie=False, header=''):
    if header == 1:
        header = {"Content-Type": "application/json; charset=utf-8"}
    if post:
        if pass_cookie:
            ret = session.post(url, data=post, headers=header)
            cookies = requests.utils.dict_from_cookiejar(session.cookies)
            session.cookies.update(cookies)
        else:
            ret = requests.post(url, data=post, headers=header, cookies=cookies)
    else:
        if pass_cookie:
            ret = session.get(url, headers=header)
            cookies = requests.utils.dict_from_cookiejar(session.cookies)
            session.cookies.update(cookies)
        else:
            ret = requests.get(url, headers=header, cookies=cookies)
    return ret


def ocr_captcha(url):
    filename = str(int(time.time())) + '.jpg'
    img = get_curl(url, 0, 0, 1).content
    f = BytesIO(img)
    with open(filename, 'wb') as f:
        f.write(img)
    f.close()
    ret = requests.post("http://tools.bugscaner.com/api/orc/", files={'file': open(filename, 'rb'), 'file_id': '0'})
    ret = json.loads(ret.text)["infos"]
    ret.replace(" ", "")
    os.unlink(filename)
    return ret


def login(username, password):
    url = '{host}/portal/login'.format(host=host)
    ret = get_curl(url, 0, 0, 1)
    login_url = ret.url
    ret = ret.text
    lt = re.findall('name="lt" value="(.*)"/>', ret)[0]
    execution = re.findall('name="execution" value="(.*)"/>', ret)[0]
    salt = re.findall('id="pwdDefaultEncryptSalt" value="(.*)"/>', ret)[0]
    epass = encrypt(str_rand(64) + password, salt)

    # check captcha
    iscaptcha = get_curl('{host}/needCaptcha.html?username={username}&pwdEncrypt2=pwdEncryptSalt&_={time}'.format(host=host2,username=username,time=int(time.time())))
    if iscaptcha.text == 'true':
        captcha = ocr_captcha('{host}/captcha.html?ts=112'.format(host=host2))
    else:
        captcha = ''
    body = {"username": username, "password": epass, "lt": lt, "captcha": captcha, "rememberMe": "true","dllt": "userNamePasswordLogin", "execution": execution, "_eventId": "submit", "rmShown": "1"}
    ret = get_curl(login_url, body, 0, 1)
    error = re.findall('style="top:-19px;">(.*)</span>', ret.text)
    if error != []:
        print(error[0])
        return False
    else:
        print('{user}登录成功！'.format(user=username))
        return True


def get_form_info(wid):
    url = '{host}/wec-counselor-collector-apps/stu/collector/detailCollector'.format(host=host)
    body = {"collectorWid": wid}
    ret = get_curl(url, json.dumps(body), 0, 1, 1)
    ret = json.loads(ret.text)
    return ret


def get_form_data(wid, fid, area):
    url = '{host}/wec-counselor-collector-apps/stu/collector/getFormFields'.format(host=host)
    body = {"collectorWid": wid, "formWid": fid}
    ret = get_curl(url, json.dumps(body), 0, 1, 1)
    ret = json.loads(ret.text)
    ret = ret['datas']['rows']
    temp = []
    for item in ret:
        for fielditems in item['fieldItems']:
            '''
            #根据上次记录填写(这里有时辅导员没有开启这个功能，所以直接手动最好)
            if fielditems['isSelected'] == 1:
                temp.append(fielditems)
            '''
            if fielditems['content'] == '健康，无异常' or fielditems['content'] == '36.1~37.2℃':
                fielditems['isSelected'] = 1
                item['fieldItems'] = [fielditems]
                temp.append(item)
            elif (item['colName'] == 'field003' or item['colName'] == 'field004' or item['colName'] == 'field005') and fielditems['content'] == '否':
                fielditems['isSelected'] = 1
                item['fieldItems'] = [fielditems]
                temp.append(item)
            elif item['colName'] == 'field008' and fielditems['content'] == '是':
                fielditems['isSelected'] = 1
                item['fieldItems'] = [fielditems]
                temp.append(item)
        if item['colName'] == 'field006':
            item['value'] = '无'
            temp.append(item)
        if item['colName'] == 'field007':
            item['value'] = area
            temp.append(item)
    return temp


def submitform(wid, fid, stwid, form, address, latitude, longitude):
    url = '{host}/wec-counselor-collector-apps/stu/collector/submitForm'.format(host=host)
    body = {
        'formWid': fid,
        'address': address,
        'collectWid': wid,
        'schoolTaskWid': stwid,
        'form': form,
        'latitude': latitude,
        'longitude': longitude,
        'uaIsCpadaily': True
    }
    header = {"Cpdaily-Extension": Cpextension, "Content-Type": "application/json; charset=utf-8"}
    ret = get_curl(url, json.dumps(body), 0, 1, header)
    ret = json.loads(ret.text)
    if ret['message'] == 'SUCCESS':
        return 'succ'
    else:
        return ret['message']


if login(user, upass):
    # 获取最新的问卷
    body = {
        "pageSize": 1,
        "pageNumber": 1
    }
    ret = get_curl('{host}/wec-counselor-collector-apps/stu/collector/queryCollectorProcessingList'.format(host=host),json.dumps(body), 0, 1, 1)
    ret = json.loads(ret.text)
    ret = ret["datas"]["rows"]
    if ret == []:
        print('暂无需要填写的问卷')
        exit(-1)
    else:
        sum = 0
        succ = 0
        for item in ret:
            if item['isHandled'] == 1:
                continue
            else:
                wid = item['wid']
                fid = item['formWid']
                stwid = get_form_info(wid)['datas']['collector']['schoolTaskWid']
                form = get_form_data(wid, fid, area)
                ret_1 = submitform(wid, fid, stwid, form, address, lat, lon)
                if ret_1 == 'succ':
                    succ = + 1
                    print('填表成功')
                else:
                    print(ret_1)
            sum = + 1
        print("共：{sum}个 成功：{succ}个".format(sum=sum, succ=succ))

else:
    print(user + '登录失败')
