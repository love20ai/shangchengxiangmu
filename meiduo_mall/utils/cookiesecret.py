# !/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import pickle
import base64


class CookieSecret(object):
    # 加密
    @classmethod
    def dumps(cls, data):
        # 1. 将 data数据转换成bytes
        data_bytes = pickle.dumps(data)

        #2. 将bytes使用base64序列化加密
        base64_bytes = base64.b64encode(data_bytes)

        # 3. 将加密完毕的bytes以字符串类型输出
        base64_str = base64_bytes.decode()

        return base64_str

    # 解密
    @classmethod
    def loads(cls, data):
        # 1. 将数据解密转成bytes
        base64_bytes = base64.b64decode(data)
        # 2. 将bytes转回原来的数据类型
        pickle_data = pickle.loads(base64_bytes)
        return pickle_data


# json 作用 : pythondict list --json_str互转
# data_dict = {
#     1:{
#         "count":2,
#         "selected":True
#     }
# }
# # dict-- json_str互转
# json_str = json.dumps(data_dict)

# # json_str --- dict
# json_dict = json.loads(json_str)


# pickle 作用: 将python对象--->bytes--->还是原始数据类型
# pickle_bytes = pickle.dumps(data_dict)

# pickle_dict = pickle.loads(pickle_bytes)

# base64 编码解码
# base64_encode = base64.b64encode(pickle_bytes)

# base64_decode = base64.b64decode(base64_encode)

# print(base64_decode)
# print(pickle.loads(base64_decode))
