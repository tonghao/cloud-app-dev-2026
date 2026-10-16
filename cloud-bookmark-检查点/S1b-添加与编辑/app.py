"""
云书签 S1b：添加与编辑的路由（第4讲　跟敲第二段的同步点）

跟敲到这里：在 S1a 上加 /add、/edit/<int:bookmark_id> 两条路由，
各自用 methods 声明 GET、POST，再用 request.method 分出两条分支。
应看到：curl -i http://127.0.0.1:5000/edit/abc 得到 404；
       curl -i -X POST http://127.0.0.1:5000/add 得到「收到新书签」。
跟丢了：把本文件复制成 ~/work/cloud-bookmark/app.py，接着跟第三段。
"""
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return '书签列表'


# 打开表单与提交表单是同一个地址的两次请求：GET 显示，POST 处理
@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    if request.method == 'POST':
        return '收到新书签'
    return '添加书签的表单'


# <int:...> 既取值又检查：不是整数就 404，函数不会被调用
@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
def edit_bookmark(bookmark_id):
    if request.method == 'POST':
        return f'收到对书签 {bookmark_id} 的修改'
    return f'编辑书签 {bookmark_id} 的表单'


# 新路由一律写在这一行上面：app.run() 启动后不返回，写在下面的路由登记不上
if __name__ == '__main__':
    app.run(debug=True)
