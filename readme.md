#基于的flask的Repchain后端
##目录结构:
```
│  main.py  #主运行文件
│  readme.md 
│  requirements.txt
│  
│              
├─certs
│      121000005l35120456.node1.jks #测试用jks文件
│      121000005l35120456.node1.pem
└─src
    │  back.py #与main.py功能相同 测试用
    │  chaininfo.py #封装的请求接口以及返回值数据的处理
    │  peer_pb.py
    │  peer_pb2.py
    │  postTranByString.py #处理交易相关的代码
```
 
##使用库：
```
cryptography==37.0.4
Flask==2.0.2
Flask_Cors==3.0.10
protobuf==3.18.1
pyjks==20.0.0
requests==2.28.1
gunicorn
gevent


```
##用法：
在ide中运行：
打开main.py，填写url、client_url。在app.run中指定后端运行ip和端口。不填写默认为127.0.0.1:5000。
稳定运行：
使用gunicorn和gevent，配置根目录下的gunicorn.conf.py文件。
使用gunicorn main:app -c ./gunicorn.conf.py 命令运行


##chaininfo

```
save_json(save_path, data):
```
保存接口返回的json文件，测试用函数

```
load_json(file_path)
```
加载接口返回的json文件，测试用函数
```
get_chain_info(url)
```
请求/chaininfo,获取区块链总体信息
```
get_block_info_by_height(url, blockheight)
```
请求/block/height,指定高度的块，返回详细的块信息。
```
block_info_process(block_info)
```
对返回的blockinfo进行处理。
把blockinfo返回的多层嵌套json处理为单层的dict。  
dict的key为参数名，value为参数值。


```
args_info_process(data)
```
处理前端传来的交易的参数信息
```
convert_jks2pem(jks_path,password)
```
读取前端传入的jks文件，处理为pem格式

##postTranByString
创建交易，提交交易
```
class Client:
    
    __init__(self, host,pem_path, password, credit_code, cert_name):
     

    # 指定唯一合约:名称+版本号
   __get_cid(self, chaincode_name, chaincode_ver):
  

    # 指定用于签名的证书:证书名+用户名
    __get_certid(self):
       

    # 从pem文件中得到私钥
    __get_pvkey(self):
 

    # 得到对交易的签名signature
    __get_sig(self, transaction):
       

    ##从文件路径得到内容
    __get_code(self, package_path):
       

    # 创建设置状态交易:交易标识string,合约名称string,合约版本int,更改状态bool
    create_trans_set_state(self, trans_id, chaincode_name, chaincode_ver, state):
 

    # 创建部署/升级合约交易:交易标识string,合约名称string,合约版本int,合约代码类型string,
    # 超时时间int,合约路径string,法律描述string
    create_trans_deploy(self, trans_id, chaincode_name, chaincode_ver, chaincode_type, \
                            timeout=1000, package_path=os.path.dirname(__file__) + '\\contracts\\ConEvidence.scala',
                            legalprose=""):


    # 创建调用合约交易:交易标识string,合约名称string,合约版本int,合约方法string,方法参数string
    create_trans_invoke(self, trans_id, chaincode_name, chaincode_ver, func, params):
        
    ## 进行http请求
    doPost(self, url, data):
        headers = {'Content-Type': 'application/json'}
        
    # 提交带签名的交易
    postTranByString(self, data):
       
    # 从交易id得到交易内容
    getTransById(self, tx_id):
        
```

##main
url=''#指定http请求的地址
Client_url=''指定区块链的ip
```
get_chain_info():

```
获取区块链的基础信息
```

get_height():
```
通过高度获取区块链的信息
```
get_block_info():
 
```
测试代码，通过高度获取区块链的信息
```


upload_jks():

        return "上传失败"

        return "上传成功"

#必须先执行upload_jks，才能执行submit_transinfo

```
接收前端上传的jks秘钥文件，并返回前端上传结果
```
submit_transinfo():
   
```

把jks文件转换为pem文件，使用前端参数创建交易，并提交交易。