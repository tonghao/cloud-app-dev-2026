# Flask-SQLAlchemy 速查卡

适用于云书签项目（单个 `app.py`，Flask-SQLAlchemy 3.1）。「讲次」一栏标出该写法首次出现的讲次；标「演示」的由教师演示，了解即可。「生成的 SQL」是简化写法：`SELECT *` 代替逐个列出的字段，`?` 是占位符。想看实际的 SQL，可在配置里加 `app.config['SQLALCHEMY_ECHO'] = True`，终端会打印每一条。

## 一、配置、模型与建表（第9讲）

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bookmarks.db')
db = SQLAlchemy(app)

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'                        # 表名
    id = db.Column(db.Integer, primary_key=True)       # 主键，自动编号
    title = db.Column(db.String(100), nullable=False)  # 非空
    url = db.Column(db.String(500), nullable=False)

with app.app_context():                                # 视图函数之外操作数据库须先进入应用上下文
    db.create_all()                                    # 表不存在时建表；已有的表不会改
```

## 二、增、删、改：先登记到会话，`commit` 后才写入（第9讲）

| 操作 | 写法 | 生成的 SQL |
|---|---|---|
| 增 | `db.session.add(Bookmark(title=t, url=u))` | `INSERT INTO bookmarks (title, url) VALUES (?, ?)` |
| 批量增 | `db.session.add_all([bm1, bm2])` | 多条 `INSERT` |
| 改 | `bm.title = '新标题'` | `UPDATE bookmarks SET title=? WHERE id = ?` |
| 删 | `db.session.delete(bm)` | `DELETE FROM bookmarks WHERE id = ?` |
| 提交 | `db.session.commit()` | 以上改动此时才写入数据库 |
| 撤销 | `db.session.rollback()` | 出错后放弃未提交的改动（第11讲） |

## 三、查询

| 目的 | 写法 | 生成的 SQL | 讲次 |
|---|---|---|---|
| 全部 | `Bookmark.query.all()` | `SELECT * FROM bookmarks` | 9 |
| 按主键取一条 | `db.session.get(Bookmark, 1)` | `… WHERE id = ?`，找不到返回 `None` | 9 |
| 计数 | `Bookmark.query.count()` | `SELECT count(*) …` | 9 |
| 等值条件 | `Bookmark.query.filter_by(url=u).first()` | `… WHERE url = ? LIMIT 1` | 9 |
| 模糊查询 | `.filter(Bookmark.title.like(f'%{q}%'))` | `… WHERE title LIKE ?` | 10 |
| 或条件 | `.filter(db.or_(Bookmark.title.like(k), Bookmark.url.like(k)))` | `… WHERE title LIKE ? OR url LIKE ?` | 10 |
| 排序 | `.order_by(Bookmark.id.desc())` | `… ORDER BY id DESC` | 9（拓展） |
| 取前几条、跳过几条 | `.limit(10).offset(20)` | `… LIMIT 10 OFFSET 20` | 10（拓展） |

查询可以逐步拼接，最后用 `.all()`、`.first()` 或 `.count()` 取结果：

```python
query = Bookmark.query
if q:
    query = query.filter(Bookmark.title.like(f'%{q}%'))   # filter 返回新查询，须赋值回 query
bookmarks = query.order_by(Bookmark.id.desc()).all()
```

## 四、一对多与关联查询（第11讲）

```python
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)      # 只存哈希，不存明文
    bookmarks = db.relationship('Bookmark', backref='user')        # 一个用户的全部书签

class Bookmark(db.Model):
    ...
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))     # 外键加在「多」的一方
```

| 目的 | 写法 | 讲次 |
|---|---|---|
| 由书签找用户 | `bm.user.username` | 11 |
| 由用户找书签 | `user.bookmarks` | 11 |
| 只查某个用户的书签 | `Bookmark.query.filter_by(user_id=uid).all()` | 11 |
| 连接查询 | `db.session.query(Bookmark.title, User.username).join(User).all()` | 11 演示 |
| 每个用户的书签数 | `db.session.query(User.username, db.func.count(Bookmark.id)).join(Bookmark).group_by(User.id).all()` | 11 演示 |

关系导航每访问一次就发一条查询。在循环里逐条访问 `bm.user` 最多产生 1 + N 条查询（N 为不同用户数，即 N+1 问题），数据多时改用连接查询。

## 五、常见错误

| 现象 | 原因 |
|---|---|
| 重启后新加的数据没有了 | 漏了 `db.session.commit()` |
| `no such column` | 给模型加了字段，表是旧的；`create_all` 不改已有的表，删库重建 |
| `Working outside of application context` | 在视图函数之外操作数据库，没有写 `with app.app_context():` |
| 加了条件，结果没变 | `query.filter(...)` 没有赋值回 `query` |
| `LegacyAPIWarning` | 用了 `Bookmark.query.get(1)`，改用 `db.session.get(Bookmark, 1)` |
