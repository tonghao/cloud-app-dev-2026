"""
云书签 S10a：资源的 JSON 表述（第10讲　第一段的检查点）

做到这里：在 S9 上——
    Bookmark 加 to_dict()，把一个书签对象转成字典；
    app.json.ensure_ascii = False，JSON 里的中文不再转义；
    新增 GET /api/bookmarks：视图返回列表，Flask 自动转成 JSON。页面路由不动。
应看到：curl http://127.0.0.1:5000/api/bookmarks 输出三条书签的 JSON，中文正常；
    浏览器打开 / 与 /api/bookmarks，是同一组书签的两种表述（页面与 JSON）。
完成后提交「S10a: 书签列表的 JSON 接口」。
跟丢了：复制本目录的 app.py（会覆盖你的 app.py）。

与教材 5.1、4.2.3 的差别：不用 jsonify（视图返回字典、列表即自动转 JSON，二者等价）；URL 不加 /api/v1。
自检：tests/test_api.py、tests/test_routes.py（教师核对用）。
"""
import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from validators import validate_bookmark

app = Flask(__name__)
# flash 存在会话里，会话要用密钥签名；密钥从环境变量读，代码里只留开发用的默认值
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
# 数据库地址从环境变量读；没设时用 SQLite 文件（实际放在 instance/bookmarks.db）
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bookmarks.db')
db = SQLAlchemy(app)
# JSON 里的中文原样输出；不写这一行，中文会被转义成 \u4e66\u7b7e 一类的样子
app.json.ensure_ascii = False


class Bookmark(db.Model):
    """书签模型：类对应表，对象对应一行，属性对应一列"""
    __tablename__ = 'bookmarks'                          # 表名；不写时默认是类名小写 bookmark
    id = db.Column(db.Integer, primary_key=True)         # 主键，数据库自动编号，代替原来的 next_id
    title = db.Column(db.String(100), nullable=False)    # 长度与 validators.py 的上限一致
    url = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        """书签的 JSON 表述：对象先转成字典，视图返回字典或列表时 Flask 再转成 JSON"""
        return {'id': self.id, 'title': self.title, 'url': self.url}


PRESETS = [
    ('Flask 官方文档', 'https://flask.palletsprojects.com/'),
    ('Jinja2 模板文档', 'https://jinja.palletsprojects.com/'),
    ('阿里云开发者社区', 'https://developer.aliyun.com/'),
]

# 在请求之外操作数据库，要先进入应用上下文；视图函数里不用写
with app.app_context():
    db.create_all()                                      # 按模型建表；表已存在就跳过，不会改表
    if Bookmark.query.count() == 0:                      # 表为空（第一次运行）时插入预设三条
        db.session.add_all([Bookmark(title=t, url=u) for t, u in PRESETS])
        db.session.commit()


# 接口表「查看列表」：视图函数只准备数据，页面长什么样由模板决定
@app.route('/')
def index():
    bookmarks = Bookmark.query.all()                     # SELECT * FROM bookmarks
    return render_template('index.html', bookmarks=bookmarks)


# 接口表「打开添加表单」「提交新书签」：同一个地址，GET 显示，POST 处理
@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    if request.method == 'POST':
        # 按表单的 name 取值；.get 给默认值，字段缺失也不出错；strip 去掉首尾空格
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()

        errors = validate_bookmark(title, url)
        if errors:                                       # 失败：报错，留在表单上，回填已填内容
            for e in errors:
                flash(e, 'error')
            return render_template('add.html', title=title, url=url)

        db.session.add(Bookmark(title=title, url=url))   # 登记到会话
        db.session.commit()                              # 提交：生成 INSERT 写入数据库
        flash('书签添加成功！', 'success')
        return redirect(url_for('index'))   # PRG：浏览器接着 GET /，刷新只重发这个 GET
    return render_template('add.html')


def find_bookmark(bookmark_id):
    """按 id 找书签，找不到返回 None；编辑、删除都用它"""
    return db.session.get(Bookmark, bookmark_id)        # 按主键查询


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

        bookmark.title = title                         # 改对象的属性
        bookmark.url = url
        db.session.commit()                            # 提交：生成 UPDATE
        flash('书签更新成功！', 'success')
        return redirect(url_for('index'))
    # GET：表单先填好这条书签的当前值
    return render_template('edit.html', title=bookmark.title, url=bookmark.url)


# 接口表「删除」：只收 POST，按钮放在 index.html 的表单里
@app.route('/delete/<int:bookmark_id>', methods=['POST'])
def delete_bookmark(bookmark_id):
    bookmark = find_bookmark(bookmark_id)
    if bookmark is None:
        flash('书签不存在', 'error')
    else:
        db.session.delete(bookmark)                    # 登记删除
        db.session.commit()                            # 提交：生成 DELETE
        flash('书签已删除', 'success')
    return redirect(url_for('index'))


# 接口表「健康检查」：返回（字典, 200），字典自动转成 JSON，第二项是状态码
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200


# ===== JSON 接口（第10讲）：给程序用，与上面给人看的页面共用一个模型 =====

# JSON 接口「查看列表」：返回书签集合的 JSON 表述
@app.route('/api/bookmarks', methods=['GET'])
def api_list_bookmarks():
    bookmarks = Bookmark.query.all()
    return [bm.to_dict() for bm in bookmarks]            # 返回列表，Flask 自动转成 JSON


# ===== 拓展写在这里：不改上面五条路由，新路由都放在这一行和 if 之间 =====


if __name__ == '__main__':
    app.run(debug=True)
