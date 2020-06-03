# -*- coding: utf-8 -*-


'''

# 将字典转换为字符串
astring = json.dumps(adict)
# 将字符串转换为字典
adict = json.loads(astring)

'''


def dict_to_file(mydict, file):
    import json
    with open(file, 'w') as fp:
        # 将字典转换为字符串
        strings = json.dumps(mydict)
        # 将字符串写入文件
        fp.write(strings)


def file_to_dict(file):
    import json
    with open(file, 'r') as fp:
        # 读取文件，读取后为结果为一个字符串
        strings = fp.read()
        # 将字符串转换为字典
        mydict = json.loads(strings)

    print(mydict)


def main():
    adict = {'monitor-adapter': {

        'project': 'whale',
        'yamlfile': '/home/cld/conf/custom-metrics-apiserver-deployment.yaml',
        'jsonfile': '',
        'start_method': 'deployment',
    },

        'nks-validating-webhook': {

            'project': 'scheduler',
            'yamlfile': '',
            'jsonfile': '/home/cld/conf/luna_nks-validating-webhook.json',
            'start_method': 'deployment',
        }

    }
    alist = [1, 2, 3, 4]
    dict_to_file(adict, 'atestfile.txt')
    file_to_dict('atestfile.txt')

    dict_to_file(alist, 'btestfile.txt')
    file_to_dict('btestfile.txt')


if __name__ == '__main__':
    main()
