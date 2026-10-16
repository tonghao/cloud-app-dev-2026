# 第4讲　拓展 E5　改正 AI 代码：下面是一段 AI 生成的代码，能运行，但有三处问题。
# 任务和验证方法见项目讲义「拓展」一节。
from flask import Flask

app = Flask(__name__)


@app.route('/bookmark/<id>')
def show(id):
    return f'第 {id} 号书签'


@app.route('/delete/<id>')
def delete(id):
    return f'书签 {id} 已删除'


app.run(debug=True, host='0.0.0.0')
