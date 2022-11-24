# _*_coding:utf-8_*_
import json
import os
import time
from plistlib import load


# @PROJECT : plist_make_offset
# @Time : 2022/11/10 10:09
# @Author : Byseven
# @File : main.py
# @SoftWare:


# 读取本地json文件
def read_json(filename: str):
    with open(filename) as json_file:
        # 读取json文件数据，转成dict数据
        json_c = json.load(json_file)
    return json_c


# 解析一个plist 成 dict
def parse_plist(filename):
    plist_json_data = {}
    # 解析Plist文件
    with open(filename, "rb") as fp:
        data = load(fp)
        # print(pl)
        # print(type(pl))
        # 将dict数据转化成json数据
        # data = json.dumps(pl)
        frames = data['frames']
        for key in frames:
            frames_item = frames[key]
            frame = frames_item['frame'].replace('}', '').replace('{', '').split(',')
            offset = frames_item['offset'].replace('{', '').replace('}', '').split(',')
            rotated = frames_item['rotated']
            sourceColorRect = frames_item['sourceColorRect'].replace('{', '').replace('}', '').split(',')
            sourceSize = frames_item['sourceSize'].replace('{', '').replace('}', '').split(',')
            f = {
                'frame': list(map(float, frame)),
                'offset': list(map(str, offset)),
                'rotated': rotated,
                'sourceColorRect': list(map(float, sourceColorRect)),
                'sourceSize': list(map(float, sourceSize))
            }
            plist_json_data[key] = f
        # json_data = json.dumps(plist_json_data)
        dict_data = plist_json_data
        return dict_data


# '''输出plist文件'''
def write_plist(dict_data: dict, filename: str, sdata: dict):
    write_head(filename)
    write_body(dict_data, filename, **sdata)
    write_last(filename)


def mergers_plist(parse_pl):
    pass


# 必须确保write的filename参数一致
def write_head(new_file_name: str):
    # 写入头部数据
    with open(f'{new_file_name}.plist', 'w+', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">\n''')
        f.write('    <dict>\n')
        f.write('        <key>frames</key>\n')
        f.write('        <dict>\n')


def write_body(dict_data: dict, new_file_name: str, **kwargs) -> any:
    data = dict_data
    for key in data:
        # 写入中间关键数据
        with open(f'{new_file_name}.plist', 'a', encoding='utf-8') as f:
            ls_frame = data[key]["frame"]
            ls_sourceColorRect = data[key]['sourceColorRect']
            ls_sourceSize = data[key]['sourceSize']
            item_isRotated = data[key]['rotated']
            if kwargs == {}:
                # 原版验证逻辑
                ox = ls_sourceColorRect[0] - (ls_sourceSize[0] - ls_frame[2]) / 2
                oy = -(ls_sourceColorRect[1] - (ls_sourceSize[1] - ls_frame[3]) / 2)
                ls_offset = [ox, oy]
            else:
                # 源texturpackage输出文件的offset,xy
                _x = data[key]['offset'][0]
                _y = data[key]['offset'][1]
                # 匹配数据中的offset
                x = kwargs[key]['offset'][0]
                y = kwargs[key]['offset'][1]

                ox = float(_x) + float(x)
                oy = float(_y) + float(y)
                ls_offset = [ox, oy]
            f.write('            <key>' + key + '</key>\n')
            f.write('            <dict>\n')
            f.write('                <key>frame</key>\n')
            f.write('                <string>{{%d,%d},{%d,%d}}</string>\n' % (
                ls_frame[0], ls_frame[1], ls_frame[2], ls_frame[3]))
            f.write('                <key>offset</key>\n')
            f.write('                <string>{%d,%d}</string>\n' % (ls_offset[0], ls_offset[1]))
            f.write('                <key>rotated</key>\n')
            f.write('                <%s/>\n' % str(item_isRotated).lower())
            f.write('                <key>sourceColorRect</key>\n')
            f.write('                <string>{{%d,%d},{%d,%d}}</string>\n' % (
                0, 0, ls_sourceColorRect[2], ls_sourceColorRect[3]))
            f.write('                <key>sourceSize</key>\n')
            f.write('                <string>{%d,%d}</string>\n' % (ls_sourceSize[0], ls_sourceSize[1]))
            f.write('            </dict>\n')


def write_last(new_file_name):
    # 写入尾部
    with open(f'{new_file_name}.plist', 'a', encoding='utf-8') as f:
        f.write('        </dict>\n')
        f.write('        <key>metadata</key>\n')
        f.write('        <dict>\n')
        f.write('            <key>format</key>\n')
        f.write('            <integer>2</integer>\n')
        f.write('            <key>realTextureFileName</key>\n')
        f.write('            <string>%s</string>\n' % (new_file_name + '.png'))
        f.write('            <key>size</key>\n')
        f.write('            <string>{2048,2048}</string>\n')
        f.write('            <key>smartupdate</key>\n')
        str_time = time.asctime(time.localtime(time.time()))
        f.write('            <string>Author:%s$SmartUpdate:%s$</string>\n' % ("MadeByseven", str_time))
        f.write('            <key>textureFileName</key>\n')
        f.write('            <string>%s</string>\n' % (new_file_name + '.png'))
        f.write('        </dict>\n')
        f.write('    </dict>\n')
        f.write('</plist>')
    pass


# 遍历返回子文件
def get_filelist(path: str) -> list:
    file_list = []
    for home, dirs, files in os.walk(path):
        for filename in files:
            # 文件名列表，包含完整路径
            file_list.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            # Filelist.append( filename)
    return file_list


# 检索后缀为 hz 的文件
def get_hz_file(Element_path, hz):
    ls = get_filelist(Element_path)
    xml_ls = []
    for i in ls:
        last_name = i.split('.').pop()

        if last_name == hz:
            xml_ls.append(i)
    return xml_ls


# 得到手写off的原始字典数据
def get_yuans_data(path):
    file_ls = get_hz_file(path, 'plist')
    resault = {}
    for lis in file_ls:
        pl = parse_plist(lis)
        for i in pl:
            resault.update({i: {'offset': pl[i]['offset']}})
    return resault

    # srt = json.dumps(resault)
    # print(srt)


def tes(a, **kwargs):
    if kwargs == {}:
        return kwargs, a
    else:
        return a, kwargs


if __name__ == '__main__':
    # file_path = sys.argv[1]

    to_pl = parse_plist(r'D:\bak\new_pain\Pain.plist')  # 解析texturepackage处理过的plist
    sdata = get_yuans_data(r'D:\bak\pain\xxx\Element')  # 源数据off
    # 处理生成
    write_plist(to_pl, 'Pain', sdata)
