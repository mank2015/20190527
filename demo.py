import datetime
import time
import urllib3
import ssl
import logging
import sys
from qcloud_cos import CosS3Client
from qcloud_cos import CosConfig
import numpy as np
import cv2
import base64
import json
from urllib import parse
# 人脸搜索的库
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20180301 import iai_client, models

COS_SECRETID = 'AKIDJSzMUObiI3kR1PsqDJUbbPyNZXLrD8uW'
COS_SECRETKEY = 'ue9Qzc1QOCm9JEzVfhXLyMVSItHRPCoC'
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = COS_SECRETID      # 替换为用户的 secretId
secret_key = COS_SECRETKEY      # 替换为用户的 secretKey
region = 'ap-chongqing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = ''            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id,
                   SecretKey=secret_key, Token=token)
# 2. 获取客户端对象

# 获取对象连接
client = CosS3Client(config)

# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py


cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象

flag = 1  # 设置一个标志，用来输出视频信息
num = 1  # 递增，用来保存文件名
while(cap.isOpened()):  # 循环读取每一帧
    # 返回两个参数，第一个是bool是否正常打开，第二个是照片数组，如果只设置一个则变成一个tumple包含bool和图片
    ret_flag, Vshow = cap.read()
    cv2.imshow("Capture_Test", Vshow)  # 窗口显示，显示名为 Capture_Test
    k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
    if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
        lujin = "D:/openvc/" + str(time.time()) + ".jpg"
        cv2.imwrite(lujin, Vshow)
        print(cap.get(3))  # 得到长宽
        print(cap.get(4))
        print("success to save"+lujin+".jpg")
        print("-------------------------")
        # 获取对象连接
        client = CosS3Client(config)
        # 上传cos
        response = client.put_object_from_local_file(
            Bucket='mank2019-1251356201',
            LocalFilePath=lujin,
            Key=lujin,
        )
        print(response)
        # 获取连接
        response_huoqu = client.get_auth(
            Method='GET',
            Bucket='mank2019-1251356201',
            Key=lujin
        )
        # 组装url
        urlA = 'https://mank2019-1251356201.cos.ap-chongqing.myqcloud.com/' + \
            parse.quote(lujin) + '?' + response_huoqu
        print(urlA)

        # 人脸搜索

        try:
            cred = credential.Credential(COS_SECRETID, COS_SECRETKEY)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iai.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = iai_client.IaiClient(cred, "ap-chongqing", clientProfile)

            req = models.SearchFacesRequest()
            params = {'GroupIds': ['1'], 'Url': urlA}
            params = json.dumps(params)
            req.from_json_string(params)

            resp = client.SearchFaces(req)
            return_face = resp.to_json_string()
            print(return_face)
            print(resp)
            facedata = json.loads(return_face)
            faceid = facedata["Results"][0]["Candidates"][0]["FaceId"]
            facesource = facedata["Results"][0]["Candidates"][0]["Score"]
            facePersonId = facedata["Results"][0]["Candidates"][0]["PersonId"]
            print(facePersonId)
            if facesource > 85:
                #人员库对比
                cred = credential.Credential(COS_SECRETID, COS_SECRETKEY)
                httpProfile = HttpProfile()
                httpProfile.endpoint = "iai.tencentcloudapi.com"
                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                client = iai_client.IaiClient(cred, "ap-chongqing", clientProfile)
                req = models.GetPersonBaseInfoRequest()
                params = {'PersonId': facePersonId }
                params = json.dumps(params)
                req.from_json_string(params)
                resp = client.GetPersonBaseInfo(req)
                print(resp)
                print(resp.to_json_string())
                PersonData = json.loads(resp.to_json_string())
                PersonName = PersonData["PersonName"]
                print("人脸识别成功，这是" + PersonName)
            else:
                print("该人员还没有入库")
                pass
        except TencentCloudSDKException as err: 
            print(err) 
    elif k == ord('q'):  # 若检测到按键 ‘q’，退出
        break
cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 删除建立的全部窗口


