"""
云书签 S3：添加书签（第6讲　第三段的检查点，也是本讲主线的终点）

做到这里：在 S3b 上加验证——
    validators.py 的 validate_bookmark 逐条检查，返回错误列表；
    验证失败：逐条 flash 错误，重新渲染添加表单，并把已填的标题、网址传回去回填（不重定向，重定向就丢了）；
    验证通过：保存、flash、重定向（第二段已写好）。
浏览器里的 required、type="url" 只是提示，用 curl 能绕过；服务端验证才是最后一道防线。
编辑、删除仍是占位文字，第7讲实现；secret_key 暂时写死，第7讲改为从环境变量读取。
应看到：标题填三个空格、网址填 ftp://x，提交后留在添加页，两条红色错误，网址框里还是 ftp://x。
跟丢了：复制本目录的 templates/ 和 validators.py，app.py 照项目讲义第一至三段手改。

视图函数名、字段 id、title、url 与教材配套代码 v2 一致。
自检：tests/test_routes.py，python -m pytest -q（教师核对用，学生第7讲才学 pytest）。
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from validators import validate_bookmark

app = Flask(__name__)
app.secret_key = 'dev-secret-key'   # flash 存在会话里，会话要用密钥签名；第7讲改为从环境变量读取

# 预设三条书签：第4章改存数据库
bookmarks = [
    {'id': 1, 'title': 'Flask 官方文档', 'url': 'https://flask.palletsprojects.com/'},
    {'id': 2, 'title': 'Jinja2 模板文档', 'url': 'https://jinja.palletsprojects.com/'},
    {'id': 3, 'title': '阿里云开发者社区', 'url': 'https://developer.aliyun.com/'},
]
next_id = 4   # 新书签的编号接着预设的三条往下排


# 接口表「查看列表」：视图函数只准备数据，页面长什么样由模板决定
@app.route('/')
def index():
    return render_template('index.html', bookmarks=bookmarks)


# 接口表「打开添加表单」「提交新书签」：同一个地址，GET 显示，POST 处理
@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    global next_id                     # 要改的是函数外面的 next_id
    if request.method == 'POST':
        # 按表单的 name 取值；.get 给默认值，字段缺失也不出错；strip 去掉首尾空格
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()

        errors = validate_bookmark(title, url)
        if errors:                                       # 失败：报错，留在表单上，回填已填内容
            for e in errors:
                flash(e, 'error')
            return render_template('add.html', title=title, url=url)

        bookmarks.append({'id': next_id, 'title': title, 'url': url})
        next_id += 1
        flash('书签添加成功！', 'success')
        return redirect(url_for('index'))   # PRG：浏览器接着 GET /，刷新只重发这个 GET
    return render_template('add.html')


# 接口表「打开编辑表单」「提交修改」：<int:...> 不是整数就 404；第7讲实现
@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
def edit_bookmark(bookmark_id):
    if request.method == 'POST':
        return f'收到对书签 {bookmark_id} 的修改'
    return f'编辑书签 {bookmark_id} 的表单'


# 接口表「删除」：只收 POST，地址栏、爬虫、误点发出的 GET 都删不了数据（得到 405）；第7讲实现
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
