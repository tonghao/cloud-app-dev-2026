"""
云书签 S1：路由骨架（第4讲　跟敲第三段的同步点，也是本讲主线的终点）

跟敲到这里：按第3讲的接口表（docs/接口表.md），7 个操作对应的 5 条路由全部建好。
视图函数暂时只返回占位文字，后面几讲逐步填上：
    第5讲　index 换成模板页面
    第6讲　add_bookmark、edit_bookmark 实现验证、保存、回填
    第7讲　delete_bookmark 真正删除
应看到：curl -i http://127.0.0.1:5000/delete/1 得到 405，响应头有 Allow: POST, OPTIONS；
       curl -i http://127.0.0.1:5000/health 得到 200，Content-Type 为 application/json。
跟丢了：把本文件复制成 ~/work/cloud-bookmark/app.py，再做本讲的拓展。

视图函数名与教材配套代码 v2 一致，第5讲的 url_for、第7讲的测试都按这些名字引用。
"""
from flask import Flask, request

app = Flask(__name__)


# 接口表「查看列表」
@app.route('/')
def index():
    return '书签列表'


# 接口表「打开添加表单」「提交新书签」：同一个地址，GET 显示，POST 处理
@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    if request.method == 'POST':
        return '收到新书签'
    return '添加书签的表单'


# 接口表「打开编辑表单」「提交修改」：<int:...> 不是整数就 404
@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
def edit_bookmark(bookmark_id):
    if request.method == 'POST':
        return f'收到对书签 {bookmark_id} 的修改'
    return f'编辑书签 {bookmark_id} 的表单'


# 接口表「删除」：只收 POST，地址栏、爬虫、误点发出的 GET 都删不了数据（得到 405）
@app.route('/delete/<int:bookmark_id>', methods=['POST'])
def delete_bookmark(bookmark_id):
    return f'删除书签 {bookmark_id}'


# 接口表「健康检查」：返回（字典, 200），字典自动转成 JSON，第二项是状态码
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200


# ===== 拓展写在这里：不改上面五条路由，新路由都放在这一行和 if 之间 =====


if __name__ == '__main__':
    app.run(debug=True)
