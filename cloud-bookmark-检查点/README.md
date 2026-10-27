# 云书签检查点

**云书签（cloud-bookmark）**是贯穿本课程的项目：一个管理网址收藏的 Web 应用。第2章写出后端（路由、页面、表单、测试），之后各章依次加上前端、数据库、REST 接口、容器部署、微服务、安全与监控。

你自己的云书签在 `~/work/cloud-bookmark/`，每讲都在上面接着写、接着提交。**本目录只存参考快照**：课上跟丢了，或者自己的代码改坏了，从这里复制对应阶段的文件，接着往下做。不要在本目录里改文件。

## 各阶段

| 阶段 | 讲次 | 做到哪里 | 文件 |
|---|---|---|---|
| `S0-接口表` | 第3讲 | 项目的起点：写代码之前先定好对外接口，7 个操作各用什么方法、URL，成功和失败时返回什么 | `docs/接口表.md` |
| `S1a-最小应用` | 第4讲第一段 | 首页 `/` 返回「书签列表」 | `app.py` |
| `S1b-添加与编辑` | 第4讲第二段 | 加上 `/add`、`/edit/<int:bookmark_id>`，各分 GET、POST | `app.py` |
| `S1-路由骨架` | 第4讲结束 | 五条路由齐全，含 `/delete`、`/health`；留出「拓展写在这里」 | `app.py`、`requirements.txt`、`docs/接口表.md` |
| `S2a-数据进入页面` | 第5讲第二段 | 首页用模板渲染：预设三条书签交给 `index.html`，for 循环输出，`length` 显示条数 | `app.py`、`templates/`、`static/` |
| `S2b-模板继承` | 第5讲第三段 | 页头和导航移到 `base.html`，`index.html` 继承它 | `app.py`、`templates/`、`static/` |
| `S2-列表页` | 第5讲结束 | 模板里的链接和样式表地址全部改用 `url_for` | `app.py`、`templates/`、`static/`、`requirements.txt`、`docs/接口表.md` |
| `S3a-接收表单` | 第6讲第一段 | 添加表单提交后，视图函数按 name 取值、存进列表 | `app.py`、`templates/`、`static/` |
| `S3b-重定向与提示` | 第6讲第二段 | 添加成功后 flash 提示、重定向回首页，按 F5 不重复提交；`base.html` 加消息显示区 | `app.py`、`templates/`、`static/` |
| `S3-添加书签` | 第6讲结束 | `validators.py` 服务端验证，失败留在表单并回填 | `app.py`、`validators.py`、`templates/`、`static/`、`requirements.txt`、`docs/接口表.md` |

后面的阶段随课程进度逐讲加入。

## 怎样用

任选一种：

- **命令**：在终端执行（输入 `cl` 后按 Tab、输入 `S1b` 后按 Tab 可自动补全）：

  ```bash
  cp ~/cloud-app-dev-2026/cloud-bookmark-检查点/S1b-添加与编辑/app.py ~/work/cloud-bookmark/
  ```

- **VS Code**：在资源管理器里打开检查点的 `app.py`，全选、复制，粘贴替换自己 `app.py` 的全部内容，保存。

S0 是文档不是代码：自己的 `docs/接口表.md` 丢了或和参考方案出入较大时，复制过去覆盖即可（`cp …/S0-接口表/docs/接口表.md ~/work/cloud-bookmark/docs/`）。

开发服务器开着调试模式时，保存后会自动重载，刷新浏览器即可。复制后 `git status` 显示 `app.py` 被修改是正常的，跟完本段后照常提交。
