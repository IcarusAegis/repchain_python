import  json

import bound as bound
import requests
from flask import jsonify
def wirte_config(ip, port):
    file=open('config.ini','w')
    info_dict={}
    info_dict['Repchain']=ip
    info_dict['port'] = port
    print(info_dict)
    json.dump(info_dict,file)
    print(file)
    file.close()


class MultipartFormData(object):
    """multipart/form-data格式转化"""

    @staticmethod
    def format(data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW", headers={}):
        """
        form data
        :param: data:  {"req":{"cno":"18990876","flag":"Y"},"ts":1,"sig":1,"v": 2.0}
        :param: boundary: "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        :param: headers: 包含boundary的头信息；如果boundary与headers同时存在以headers为准
        :return: str
        :rtype: str
        """
        # 从headers中提取boundary信息
        if "content-type" in headers:
            fd_val = str(headers["content-type"])
            if "boundary" in fd_val:
                fd_val = fd_val.split(";")[1].strip()
                boundary = fd_val.split("=")[1].strip()
            else:
                raise "multipart/form-data头信息错误，请检查content-type key是否包含boundary"
        # form-data格式定式
        jion_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'
        end_str = "--{}--".format(boundary)
        args_str = ""

        if not isinstance(data, dict):
            raise "multipart/form-data参数错误，data参数应为dict类型"
        for key, value in data.items():
            args_str = args_str + jion_str.format(boundary, key, value)

        args_str = args_str + end_str.format(boundary)
        args_str = args_str.replace("\'", "\"")
        return args_str
if __name__=="__main__":
#     url='http://chain.repchain.net.cn/uct/api/v1/gateway/login'
#     args={
#     "username": "533417627046",
#     "password": "jk1016",
#     "clientId": "ef96dfcf-0aa2-4c45-91d7-0f103ce794cf"
# }
#     res=requests.post(url=url,json=args)
#     print(res.json())
#     token=res.json()['datas']
#     print(token)
#
    url='http://chain.repchain.net.cn/uct/api/v1/data/jks_download'
    data={'token': 'c42b97873ff903972731e52e3b6aafe9', 'repcertid': '810000199906250113.testcert000',
     'username': '533417627046', 'passwd': 'jk1016'}

    m = MultipartFormData.format(data, boundary=bound)
    res=requests.post(url=url,data=data)
    print(res.json())