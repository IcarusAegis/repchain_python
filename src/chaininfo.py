
import requests
import json
import sys, base64, textwrap
import jks
import os
from pathlib import Path
def save_json(save_path, data):
    assert save_path.split('.')[-1] == 'json'
    with open(save_path, 'w') as file:
        json.dump(data, file)


def load_json(file_path):
    assert file_path.split('.')[-1] == 'json'
    with open(file_path, 'r') as file:
        data = json.load(file)


def get_chain_info(url):
    info = requests.get(url + '/chaininfo')
    return info


def get_block_info_by_height(url, blockheight):
    block_info = requests.get(url + '/block/' + str(blockheight))
    return block_info


def block_info_process(block_info):
    data = eval(block_info.content)
    res = []
    # print(data['result']['transactions'])
    for k, v in enumerate(data['result']['transactions']):
        temp = {}
        # print(k,v)
        temp.update({'no': k})
        if ('ipt' in v.keys()):
            temp.update({'ipt-function': v['ipt']['function']})
            if (v['ipt']['args'] != None):
                temp.update({'args': v['ipt']['args']})
            else:
                temp.update({'args': None})
        if ('spec' in v.keys()):
            temp.update({'spec-timeout': v['spec']['timeout']})
            temp.update({'spec-codePackage': v['spec']['codePackage']})
            temp.update({'spec-ctype': v['spec']['ctype']})

        temp.update(
            {
                'id': v['id'],
                'type': v['type'],
                'cid-chaincodeName': v['cid']['chaincodeName'],
                'cid-version': v['cid']['version'],
                'signature-certId-creditCode': v['signature']['certId']['creditCode'],
                'signature-certId-certName': v['signature']['certId']['certName'],
                'signature-tmLocal': v['signature']['tmLocal'],
                'signature-hash': v['signature']['signature'],
            })
        res.append(temp)
    # print(res)
    res.append({'height': data['result']['height'], 'version': data['result']['version']})
    print(res)
    return res


def args_info_process(data):
    temp = {}
    try:
        for i in data['args']:
            str1 = i['value']
            k, v = str1.split(":")
            # print(k, v)
            temp[k]=v
        # print(temp)
        return temp
    except ValueError as e:
        # print(e)
        print(type(e))
        return 'error'

def convert_jks2pem(jks_path,password):
    file_path=str(r'../certs/'+Path(jks_path).stem+".pem")
    f = open(file_path, 'a', encoding="utf-8")
    f.seek(0)
    f.truncate()
    def print_pem(der_bytes, type):
        # print("-----BEGIN %s-----" % type)
        # print("\r\n".join(textwrap.wrap(base64.b64encode(der_bytes).decode('ascii'), 64)))
        # print("-----END %s-----" % type)
        f.write("-----BEGIN %s-----" % type)
        f.write("\n")
        f.write("\n".join(textwrap.wrap(base64.b64encode(der_bytes).decode('ascii'), 64)))
        f.write("\n")
        f.write("-----END %s-----" % type)
        f.write("\n")

    ks = jks.KeyStore.load(jks_path, password)
    # if any of the keys in the store use a password that is not the same as the store password:
    # ks.entries["key1"].decrypt("key_password")

    for alias, pk in ks.private_keys.items():
        # print("Private key: %s" % pk.alias)
        if pk.algorithm_oid == jks.util.RSA_ENCRYPTION_OID:
            print_pem(pk.pkey, "RSA PRIVATE KEY")
        else:
            print_pem(pk.pkey_pkcs8, "PRIVATE KEY")

        for c in pk.cert_chain:
            print_pem(c[1], "CERTIFICATE")
        # print()

    for alias, c in ks.certs.items():
        # print("Certificate: %s" % c.alias)
        print_pem(c.cert, "CERTIFICATE")
        # print()

    for alias, sk in ks.secret_keys.items():
        pass
        # print("Secret key: %s" % sk.alias)
        # print("  Algorithm: %s" % sk.algorithm)
        # print("  Key size: %d bits" % sk.key_size)
        # print("  Key: %s" % "".join("{:02x}".format(b) for b in bytearray(sk.key)))
        # print()
    f.close()
    return file_path
if __name__ == "__main__":
    # pass
    info=requests.get('http://192.168.100.129:8081/chaininfo')
    # block=requests.get('http://192.168.100.129:8081/block/2')
    print(info.json())

    # data=res['result']
    # key_list=data.keys()
    # print(list(key_list))
    # for i in key_list:
    #     print(data[i])
    # url = 'http://192.168.100.129:8081'
    # info = get_block_info_by_height(url, 2)
    # res = info.json()
    # save_json('./1.json',res)
    # res=block_info_process(info)
    # print(info.content)
    # print(res)
    # res=eval(info.content)
    # # print(res)
    # data=res['result']['transactions'][0]['ipt']['args']
    # print(data)
    # var = {'domains': [{'value': '11231231'}, {'value': '1312312312', 'key': 1660028650766},
    #                    {'value': '13123123', 'key': 1660028651651}, {'value': '123', 'key': 1660028652055}],
    #        'name': '13131313'}
    # var2 = {
    #     'args': [{'value': '阿萨德:123'}, {'value': 'ad:123', 'key': 1660028951832}, {'value': '1额:!', 'key': 1660028952557},
    #              {'value': 'aDQ:!', 'key': 1660028953220}], 'name': 'sad'}
    # # print(var2['args'])
    # # try:
    # #     for i in var2['args']:
    # #         str1=i['value']
    # #         k,v=str1.split(":")
    # #         print(k,v)
    # # except ValueError as e:
    # #     print(e)
    #
    # res = args_info_process(var2)
    # print(res)
    # info={'txid': 'fd31e772-a46b-454b-9f9e-6b3dcff5dae2', 'err': 'test 已存在，当前值为 1'}
    # if 'err' in info.keys():
    #     print(info['err'])
    # path=r'C:\Users\13004\OneDrive\实习\中科院\RCPython\certs\121000005l35120456.node1.jks'
    # # file_name=Path(path).stem
    # # file_path=Path(path).parent
    # # print(file_path,file_name)
    # convert_jks2pem(path,'123')