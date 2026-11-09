# tests/test_bookmarks.py　第7讲第三段：给云书签写的两个测试
import app as bookmark_app


def test_add_bookmark():
    bookmark_app.bookmarks.clear()               # 从干净的状态开始：预设书签里就有「Flask」
    client = bookmark_app.app.test_client()      # 模拟浏览器，不用真的启动服务器
    resp = client.post('/add',
                       data={'title': 'Flask', 'url': 'https://flask.palletsprojects.com'},
                       follow_redirects=True)    # 跟着重定向走到首页
    assert resp.status_code == 200
    assert 'Flask' in resp.get_data(as_text=True)


def test_reject_bad_url():
    bookmark_app.bookmarks.clear()
    client = bookmark_app.app.test_client()
    client.post('/add', data={'title': 'Flask', 'url': 'flask.com'})
    assert len(bookmark_app.bookmarks) == 0      # 不合法的 URL 不应被保存
