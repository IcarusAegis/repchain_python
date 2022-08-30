import  json
import requests

def wirte_config(ip, port):
    file=open('config.ini','w')
    info_dict={}
    info_dict['Repchain']=ip
    info_dict['port'] = port
    print(info_dict)
    json.dump(info_dict,file)
    print(file)
    file.close()

if __name__=="__main__":
    url='http://chain.repchain.net.cn/uct/api/v1/gateway/login'
    args={
    "username": "533417627046",
    "password": "jk1016",
    "clientId": "ef96dfcf-0aa2-4c45-91d7-0f103ce794cf"
}
    res=requests.post(url=url,json=args)
    print(res.json())
    token=res.json()['datas']
    print(token)
    url='http://chain.repchain.net.cn/uct/api/v1/data/jks_download'
    data={
        'token':token,
        "repcertid": "810000199906250113.testcert000",
        "username": "533417627046",
        "password": "jk1016",

    }
    res=requests.post(url=url,json=data)
    print(res.json())