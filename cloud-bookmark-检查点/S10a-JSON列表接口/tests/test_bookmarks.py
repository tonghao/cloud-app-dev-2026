# tests/test_bookmarks.py　第7讲第三段写的两个测试，第9讲第二段改为连数据库
import app as bookmark_app


def reset_db():
    """删表再建表：每个测试从空表开始（代替第7讲的 bookmarks.clear()）"""
    with bookmark_app.app.app_context():
        bookmark_app.db.drop_all()
        bookmark_app.db.create_all()


def test_add_bookmark():
    reset_db()                                   # 从干净的状态开始：预设书签里就有「Flask」
    client = bookmark_app.app.test_client()      # 模拟浏览器，不用真的启动服务器
    resp = client.post('/add',
                       data={'title': 'Flask', 'url': 'https://flask.palletsprojects.com'},
                       follow_redirects=True)    # 跟着重定向走到首页
    assert resp.status_code == 200
    assert 'Flask' in resp.get_data(as_text=True)


def test_reject_bad_url():
    reset_db()
    client = bookmark_app.app.test_client()
    client.post('/add', data={'title': 'Flask', 'url': 'flask.com'})
    with bookmark_app.app.app_context():         # 在请求之外查数据库，要进入应用上下文
        assert bookmark_app.Bookmark.query.count() == 0   # 不合法的 URL 不应被保存
