# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 定义目录路径和文件路径
directory_paths = {
    'directory1': '/root',
    'directory2': '/root/gx',
    'directory3': '/',
    'directory4': '/root/mysqlbf/hdgf',
    'directory5': '/data',
    'directory6': '/data/ftp',
    'directory7': '/data/ftp/template',
    'directory8': '/data/ftp/update',
    'directory9': '/data/ftp/phone',
    'directory10': '/root/mysqlbf',
}

txt_file_path = "/root/list.txt"  # 替换为您的 txt 文件路径

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

@app.route('/')
def index():
    # 获取目录1、目录2和脚本选项
    directory1_options = []
    directory2_options = []

    for path in directory_paths.values():  # 遍历目录路径的值
        directory1_options.extend(os.listdir(path))
        directory2_options.extend(os.listdir(path))

    script_options = read_txt_file(txt_file_path)

    return render_template('hpp.html', directory1_options=directory1_options,
                           directory2_options=directory2_options, script_options=script_options)

@app.route('/get_data', methods=['POST'])
def get_data():
    action = request.form.get('action')

    if action in directory_paths:
        # 根据传入的操作名称获取相应的路径
        path = directory_paths[action]

        # 获取指定目录的文件列表
        try:
            file_list = os.listdir(path)
            return jsonify(result='success', options=file_list)
        except OSError as e:
           return jsonify(result='error', message=str(e))

@app.route('/execute_script', methods=['POST'])
def execute_script():
    command = request.form.get('command')
    print(command)
    try:
        result = os.popen(command).read()
    except Exception as e:
        result = str(e)
    print(result)
    return jsonify(result=result)
    return render_template('hpp.html', execution_result=result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

