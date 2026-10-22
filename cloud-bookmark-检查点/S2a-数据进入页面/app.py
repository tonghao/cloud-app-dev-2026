"""
云书签 S2a：数据进入页面（第5讲　跟敲第一段的同步点）

跟敲到这里：在 S1 上把首页换成模板——
    app.py 导入 render_template，加一份预设书签数据，index 把数据交给 templates/index.html；
    index.html 用 for-else 输出书签、用 length 过滤器显示条数；编辑、删除的地址暂时写死。
应看到：浏览器打开 http://127.0.0.1:5000 显示三条书签和「共 3 条书签」。
跟丢了：把本目录的 templates/、static/ 复制到 ~/work/cloud-bookmark/，接着跟第二段。
       app.py 只差上面三处时照着改；要整个复制 app.py，先把自己「拓展写在这里」下面的代码剪出来，复制后再贴回去。
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
