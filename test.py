import  json


def wirte_config(ip, port):
    file=open('config.ini','w')
    info_dict={}
    info_dict['Repchain']=ip
    info_dict['port'] = port
    print(info_dict)
    json.dump(info_dict,file)
    print(file)
    file.close()
ip='1.1.1.2'
port='8081'
wirte_config(ip,port)