"""
云书签 S1a：最小应用（第4讲　跟敲第一段的同步点）

跟敲到这里：一个应用实例、一条路由、一个视图函数、开发服务器。
应看到：浏览器打开 http://127.0.0.1:5000 显示「书签列表」，
       终端多出一行 "GET / HTTP/1.1" 200。
跟丢了：把本文件复制成 ~/work/cloud-bookmark/app.py，接着跟第二段。
"""
from flask import Flask

app = Flask(__name__)                  # ① 应用实例


@app.route('/')                        # ② 路由：把 / 登记给下面的函数
def index():                           # ③ 视图函数：返回值就是响应内容
    return '书签列表'


if __name__ == '__main__':             # ④ 直接运行本文件时才启动开发服务器
    app.run(debug=True)
