import json
import pathlib

import requests
from flask import Flask, render_template, request, jsonify
from src import chaininfo
from src import peer_pb2
from flask_cors import CORS, cross_origin
from src import postTranByString as trans

app = Flask(__name__)  # 在当前文件下创建应用

cors = CORS(app)
def load_config():
    f=open('config.ini','r')
    content=f.read()
    info=json.loads(content)
    ip=info['Repchain']
    port=info['port']
    url='http://'+ip+':'+port
    Client_url =ip+':'+port
    return url,Client_url

def wirte_config(ip, port):
    file=open('config.ini','w')
    info_dict={}
    info_dict['Repchain']=ip
    info_dict['port'] = port
    print(info_dict)
    json.dump(info_dict,file)
    print(file)
    file.close()


# url='http://192.168.100.132:8081'
# Client_url='192.168.100.132:8081'
# 192.168.100.133:8081
# flag=True
# while flag:
#     url=input('输入Repchain地址：')
#     Client_url=url
#     url_http='http://'+url
#     print(url)
#     if url==None:
#         flag=True
#     else:
#         flag=False




jks_file_path=[]
@app.route('/')
def test():
    url,Client_url=load_config()
    return url
@app.route("/setting")
def get_setting_info():
    url,Client_url=load_config()
    return url

@app.route("/setting_submit",methods=['POST'])
def setiing_submit():
    data=request.get_json()
    print(data)
    wirte_config(data['ip'],data['port'])
    return 'success'

@app.route("/chain_info",methods=["GET"])  # 装饰器，url，路由
def get_chain_info():
    url, Client_url = load_config()
    info=chaininfo.get_chain_info(url)
    return jsonify(eval(info.content))
@app.route('/height',methods=["GET","POST"])
def get_height():
    url, Client_url = load_config()
    data=request.get_json()
    # print(data)
    info = chaininfo.get_block_info_by_height(url, data['height'])
    res = chaininfo.block_info_process(info)
    return jsonify(res)

@app.route('/blockinfo',methods=["GET"])
def get_block_info():
    url, Client_url = load_config()
    info=chaininfo.get_block_info_by_height(url,2)
    res=chaininfo.block_info_process(info)
    # print(info)
    return jsonify(res)

@app.route('/upload_jks',methods=["POST"])
def upload_jks():
    url, Client_url = load_config()
    data=request.files['file']#接受传来的jks文件
    if data is None:
        return "上传失败"
    else:
        name=data.filename
        print(data)
        # global jks_file_path
        jks_file_path.append(str('./certs/'+name))
        print('jks_file_path',jks_file_path)
        data.save(r'./certs/'+name)
        return "上传成功"

#必须先执行upload_jks，才能执行submit_transinfo
@app.route('/submit_transinfo',methods=["POST"])
def submit_transinfo():
    url, Client_url = load_config()
    # global jks_file_path
    data=request.get_json()#接收表单的信息
    # print(data)
    args=chaininfo.args_info_process(data)#获取交易参数
    # print(args)
    # print(data['password'])
    print('jks_file_path', jks_file_path[0])
    pem_path=chaininfo.convert_jks2pem(jks_file_path[0],data['password'])#转换jks文件到pem文件
    # print('pem_path',pem_path)

    #加一个jks文件中不存在credit_code,credit_name的情况，判断传来的里面是否有这个，没有的话再根据文件名获取。




    credit_code,credit_name=pathlib.Path(pem_path).stem.split('.')#从pem文件名中提取信息

    client=trans.Client(host=Client_url,pem_path=pem_path,credit_code=credit_code,cert_name=credit_name,password=None)#选择证书地址等 问题 密码加密
    tran_info=client.create_trans_invoke(data['trans_id'],data['chaincode_name'],data['chaincode_ver'],data['func_name'],json.dumps(args))#创建交易信息
    # print(tran_info)
    res=client.postTranByString(tran_info)
    # print(res.json().keys())
    if 'err' in dict(res.json()).keys():
        print('err',res.json()['err'])
        return res.json()['err']
    #写错误返回值的提醒
    if (args=='error'):
        flag='error'
        return flag
    else:
        return 'success'
    jks_file_path.pop(0)
    print('jks_file_path', jks_file_path)
#jks转换pem没问题了
#8.11做jks页面上的上传和密码填写
@app.route('/submit_api_login',methods=["POST"])
def submit_api_login():
    data=request.get_json()
    print(data)
    url='http://chain.repchain.net.cn/uct/api/v1/gateway/login'
    res=requests.post(url=url,json=data)
    print(res.json())
    return res.json()

@app.route('/submit_api_register',methods=["POST"])
def submit_api_register():
    data=request.get_json()
    print(data)
    url='http://chain.repchain.net.cn/uct/api/v1/data/api_register'
    res=requests.post(url=url,json=data)
    # print(res.json())
    return res.json()

@app.route('/submit_jks_download',methods=["POST"])
def submit_jks_download():
    data=request.get_json()
    print(data)
    url='http://chain.repchain.net.cn/uct/api/v1/data/jks_download'
    res=requests.post(url=url,json=data)
    print(res.json())
    return res.json()

if __name__ == "__main__":
    app.run(debug=True)  # 运行app

