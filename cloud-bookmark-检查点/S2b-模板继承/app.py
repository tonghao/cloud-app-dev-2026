"""
云书签 S2b：模板继承（第5讲　跟敲第二段的同步点）

跟敲到这里：app.py 与 S2a 相同；模板拆成两个——
    templates/base.html 放各页面共用的页头、导航，挖出 title、content 两个块；
    templates/index.html 第一行 extends base.html，只填这两个块。编辑、删除的地址仍是写死的。
应看到：页面和 S2a 一样；查看网页源代码，<title> 是「书签列表」。
跟丢了：把本目录的 templates/ 复制到 ~/work/cloud-bookmark/（覆盖 index.html，新增 base.html），接着跟第三段。
"""
from flask import Flask, render_template, request

app = Flask(__name__)

# 预设三条书签：本讲只负责「显示」，添加功能第6讲再做；第4章改存数据库
bookmarks = [
    {'id': 1, 'title': 'Flask 官方文档', 'url': 'https://flask.palletsprojects.com/'},
    {'id': 2, 'title': 'Jinja2 模板文档', 'url': 'https://jinja.palletsprojects.com/'},
    {'id': 3, 'title': '阿里云开发者社区', 'url': 'https://developer.aliyun.com/'},
]


# 接口表「查看列表」：视图函数只准备数据，页面长什么样由模板决定
@app.route('/')
def index():
    return render_template('index.html', bookmarks=bookmarks)


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
