"""
云书签 S9a：在 Python 中执行 SQL（第9讲　第一段的检查点）

做到这里：app.py 不动，新建本文件，用 Python 自带的 sqlite3 操作一个独立的练习库 demo.db——
    建 bookmarks 表（主键自增；title、url 不能为空；url 不能重复），
    用占位符 ? 插入两条，commit 后才真正写进文件，
    查询打印；最后用两种写法按标题查找，比较拼接与占位符。
应看到：第一次运行打印两条书签；再运行一次，插入被 UNIQUE 约束拒绝（打印「已存在，跳过」），
    表里仍是第一次的两条——数据存在 demo.db 文件里，程序结束也不丢。
    拼接写法查出全部记录（SQL 注入），占位符写法查到 0 条。
完成后提交「S9a: 在 Python 中执行 SQL」。
跟丢了：复制本目录的 sql_demo.py 与 .gitignore（demo.db 不进仓库）。
"""
import sqlite3

conn = sqlite3.connect('demo.db')        # 连接数据库文件，不存在就新建
cur = conn.cursor()

# 建表：表已存在就跳过
cur.execute('''
    CREATE TABLE IF NOT EXISTS bookmarks (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        url   VARCHAR(500) NOT NULL UNIQUE
    )
''')

# 增：数据用占位符 ? 传入，不拼进 SQL 字符串
presets = [('Flask 官方文档', 'https://flask.palletsprojects.com/'),
           ('阿里云开发者社区', 'https://developer.aliyun.com/')]
for title, url in presets:
    try:
        cur.execute('INSERT INTO bookmarks (title, url) VALUES (?, ?)', (title, url))
    except sqlite3.IntegrityError as e:    # 违反约束：数据库拒绝写入
        print('已存在，跳过：', e)
conn.commit()                              # 写操作提交后才保存到文件

# 查：逐行取出查询结果，每行是一个元组
for row in cur.execute('SELECT id, title, url FROM bookmarks'):
    print(row)

# 对比：用户输入的「标题」里藏着一段 SQL
keyword = "' OR '1'='1"
spliced = cur.execute(f"SELECT title FROM bookmarks WHERE title = '{keyword}'").fetchall()
safe = cur.execute('SELECT title FROM bookmarks WHERE title = ?', (keyword,)).fetchall()
print('拼接：', spliced)                   # 输入改变了 SQL 的意思，查出全部
print('占位符：', safe)                    # 输入只当作数据，查不到

conn.close()
