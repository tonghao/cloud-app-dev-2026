# HTML 速查卡（二）　表单

> 课程：云应用开发　|　第6讲用。三条规则、页面骨架见第5讲的「HTML 速查卡（一）页面」。

表单在第3章系统学习（教材 3.1.4）。本卡只列云书签、拓展和留言板用到的写法。表单怎样变成请求，见 PPT 第 5 页。

---

## 表单与控件

| 写法 | 作用 | 云书签里 | 教材 |
|---|---|---|---|
| `<form action="地址" method="post">…</form>` | 表单。`action` 是提交到哪个地址；`method` 是方法，不写时为 `get` | 起始代码 `add.html` 第 5 行 | 2.6.1 |
| `<input type="text" name="title">` | 单行输入框。`name` 是这个字段在请求里的名字，视图函数按它取值 | `add.html` 第 6 行 | 2.6.1 |
| `<input type="url" …>` | 网址输入框，浏览器提交前查格式。同类的还有 `email`、`number`、`date` | `add.html` 第 7 行 | 3.1.4 |
| `<button type="submit">添加</button>` | 提交按钮。表单里的 `<button>` 不写 `type` 时也是提交 | `add.html` 第 8 行；`index.html` 的删除按钮 | 2.6.1 |
| `<textarea name="content">…</textarea>` | 多行输入框，适合留言、反馈这类长文字 | 云书签未用 | — |
| `<label for="nick">昵称</label>` 配 `<input id="nick" …>` | 输入框前的文字。`for` 与 `id` 相同时，点文字就能选中输入框 | 云书签未用 | 2.6.1 |

---

## 输入框的属性

| 属性 | 作用 | 教材 |
|---|---|---|
| `name="title"` | 字段名。**没有 `name` 的输入框不会被提交** | 2.6.1 |
| `value="…"` | 输入框里的初始内容。回填时写 `value="{{ title }}"`（第6讲第三段） | 2.6.3 |
| `required` | 必填，空着提交时浏览器先拦下 | 2.6.3 |
| `maxlength="100"`、`minlength="3"` | 最多、最少几个字 | 2.6.3 |
| `placeholder="https://"` | 输入框为空时显示的灰色提示，不会被提交 | 3.1.4 |

`required`、`maxlength`、`type="url"` 都只在浏览器里检查，用 curl 就能绕过。服务器上一定要再验证（PPT 第 14 页）。

---

## 两处容易写错

- **`<textarea>` 回填不用 `value`**：已填的文字写在两个标签之间，例如 `<textarea name="content">{{ content }}</textarea>`。
- **GET 表单的数据在地址里**：`method="get"` 的表单提交后，字段出现在地址 `?` 后面，例如 `/search?q=flask`。视图函数用 `request.args.get` 取，不用 `request.form`（PPT 第 6、7 页）。

---

## 一个完整的例子

报名表：两个输入框、一个多行输入框。`action` 用 `url_for` 生成（第5讲）。

```html
<form action="{{ url_for('signup') }}" method="post">
    <p><label for="nick">昵称：</label><input id="nick" type="text" name="nick" required maxlength="20"></p>
    <p><label for="mail">邮箱：</label><input id="mail" type="email" name="mail" required></p>
    <p><label for="note">备注：</label></p>
    <p><textarea id="note" name="note" rows="4" cols="40" maxlength="200"></textarea></p>
    <p><button type="submit">报名</button></p>
</form>
```

提交后，请求体是 `nick=…&mail=…&note=…`，视图函数用 `request.form.get('nick', '')` 等取值。

写好后，在浏览器右键「查看网页源代码」，确认 `action` 的地址对、每个输入框都有 `name`。
