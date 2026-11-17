"""
云书签 S4：编辑、删除、测试与配置（第7讲　第三段的检查点）——第2章完成版

做到这里：在 S4a 上收尾——
    tests/test_bookmarks.py 两个测试：每个先清空列表（预设书签会让坏代码也通过），再用 test_client 发请求、assert 写期望；
    pytest.ini 让 pytest 找得到 app 模块，python -m pytest -v 一次跑完；
    secret_key 改从环境变量 SECRET_KEY 读取，没设时用开发默认值（配置外部化）。
/health 自第4讲就有，供云平台判断应用是否存活。
应看到：python -m pytest -v 两个测试通过；删掉 validators.py 的网址前缀检查再跑，恰好 test_reject_bad_url 失败。
完成后提交「S4: 编辑、删除、测试与配置」，课后打 tag ch2。
跟丢了：复制本目录的 app.py、tests/、pytest.ini、requirements.txt。

与教材配套代码 v2 的差别：预设三条书签；编辑失败回填用户刚填的内容；删除用 remove；没有查重（拓展 E2）。
离上云还差的：数据在进程内存里（第4章换数据库，只改 Model），配置与健康检查到第6章、第8章落地。
自检：tests/test_routes.py（教师核对用）。
"""
import os

from flask import Flask, render_template, request, redirect, url_for, flash
from validators import validate_bookmark

app = Flask(__name__)
# flash 存在会话里，会话要用密钥签名；密钥从环境变量读，代码里只留开发用的默认值
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

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


def find_bookmark(bookmark_id):
    """按 id 找书签，找不到返回 None；编辑、删除都用它"""
    for bm in bookmarks:
        if bm['id'] == bookmark_id:
            return bm
    return None


# 接口表「打开编辑表单」「提交修改」：先找到书签，其余与添加相同
@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
def edit_bookmark(bookmark_id):
    bookmark = find_bookmark(bookmark_id)
    if bookmark is None:                               # 找不到：提示后回首页
        flash('书签不存在', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()

        errors = validate_bookmark(title, url)
        if errors:                                     # 失败：回填用户刚填的，不是原来的
            for e in errors:
                flash(e, 'error')
            return render_template('edit.html', title=title, url=url)

        bookmark['title'] = title                      # 成功：改字段，不追加
        bookmark['url'] = url
        flash('书签更新成功！', 'success')
        return redirect(url_for('index'))
    # GET：表单先填好这条书签的当前值
    return render_template('edit.html', title=bookmark['title'], url=bookmark['url'])


# 接口表「删除」：只收 POST，按钮放在 index.html 的表单里
@app.route('/delete/<int:bookmark_id>', methods=['POST'])
def delete_bookmark(bookmark_id):
    bookmark = find_bookmark(bookmark_id)
    if bookmark is None:
        flash('书签不存在', 'error')
    else:
        bookmarks.remove(bookmark)                     # 删掉找到的那个字典
        flash('书签已删除', 'success')
    return redirect(url_for('index'))


# 接口表「健康检查」：返回（字典, 200），字典自动转成 JSON，第二项是状态码
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200


# ===== 拓展写在这里：不改上面五条路由，新路由都放在这一行和 if 之间 =====


if __name__ == '__main__':
    app.run(debug=True)
