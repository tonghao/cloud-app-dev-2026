# CSS 速查卡

> 课程：云应用开发　|　第3章 前端开发基础　|　第8讲
> 按本讲四块排列。标 ★ 的本讲课上用过；其余是写作业、读云书签样式时可能用到的。原理见教材 3.2。

## 一　CSS基础与选择器

一条规则：

```css
选择器 {
    属性: 值;
    属性: 值;
}
```

引入外部样式表（写在 `<head>` 里）：

```html
<link rel="stylesheet" href="style.css">
```

| 选择器 | 写法 | 选中谁 |
|---|---|---|
| ★ 元素 | `p` | 所有 `p` |
| ★ 类 | `.card` | `class` 里有 `card` 的元素（一个元素可写几个 class，空格隔开） |
| ★ id | `#media` | `id="media"` 的那一个元素 |
| ★ 分组 | `h1, h2` | `h1` 和 `h2` 都选 |
| ★ 后代 | `header h1` | `header` 里面（任意深处）的 `h1` |
| 子元素 | `.actions > button` | `.actions` 的**直接**子元素 `button` |
| 相邻兄弟 | `h2 + p` | 紧跟在 `h2` 后面的那个 `p` |
| 通配符 | `*` | 所有元素 |
| ★ 伪类：悬停 | `a:hover` | 鼠标停在上面时 |
| 伪类：聚焦 | `input:focus` | 光标在输入框里时 |
| 伪类：位置 | `li:first-child`、`li:last-child` | 第一个、最后一个 `li` |
| 链接四态 | `a:link`、`a:visited`、`a:hover`、`a:active` | 未访问、访问过、悬停、按下的那一刻 |

注释写成 `/* … */`。

## 二　文字与颜色

| 属性 | 例子 | 说明 |
|---|---|---|
| ★ `font-family` | `"Microsoft YaHei", Arial, sans-serif` | 前面的字体没有，就用后面的 |
| ★ `font-size` | `40px` | 字号 |
| ★ `font-weight` | `bold` | 粗细 |
| `font-style` | `italic` | 斜体 |
| ★ `line-height` | `1.7` | 行高：字号的 1.7 倍 |
| ★ `text-align` | `center` | 对齐：`left`、`center`、`right` |
| ★ `text-decoration` | `none` | 下划线：`none` 去掉，`underline` 加上 |
| `letter-spacing` | `2px` | 字间距 |
| `text-transform` | `uppercase` | 英文转大写 |
| ★ `color` | `#3e2723` | 字的颜色 |
| ★ `background-color` | `#f3ede4` | 底色 |
| `background-image` | `url("media/bg.jpg")` | 背景图；常配 `background-size: cover` |

颜色写法：`white`、`#fff`（`#ffffff` 的简写）、`rgb(255, 255, 255)`；常用色用颜色名（输入 `color: ` 后从 VS Code 弹出的列表里选），要精确的颜色用十六进制；半透明用 `rgba(0, 0, 0, 0.5)`。

长度单位：`px` 像素；`em` 相对父元素的字号；`rem` 相对根元素（`html`）的字号；`%` 相对父元素。

冲突与继承（PPT 第 9 页）：两条规则同改一个属性，更具体的赢，一样具体后写的赢；颜色、字体、行高会传给里面的元素，链接例外。

## 三　盒模型

| 属性 | 例子 | 说明 |
|---|---|---|
| ★ `padding` | `10px 30px 20px` | 内边距（写法见下） |
| ★ `margin` | `0`、`20px` | 外边距；`margin-left: auto; margin-right: auto` 左右居中 |
| ★ `border` | `1px solid #d7ccc8` | 边框：粗细、样式、颜色；样式还有 `dashed`、`dotted` |
| ★ `border-left` | `6px solid #8d6e63` | 只画一边：`border-top`、`border-right`、`border-bottom` |
| ★ `border-radius` | `8px` | 圆角 |
| `width`、`height` | `300px`、`100%` | 宽、高 |
| ★ `max-width` | `900px` | 最大宽度 |
| ★ `box-sizing` | `border-box` | 宽度算到边框为止；写在 `* { }` 里，放样式表开头 |
| `overflow` | `hidden`、`auto` | 内容超出盒子时：剪掉、出滚动条 |

几个值的写法（`padding`、`margin` 相同）：

| 写法 | 意思 |
|---|---|
| `20px` | 四边都是 20 |
| `10px 30px` | 上下 10，左右 30 |
| `10px 30px 20px` | 上 10，左右 30，下 20 |
| `10px 20px 30px 40px` | 上、右、下、左（顺时针） |

## 四　Flexbox布局

| 属性 | 例子 | 说明 |
|---|---|---|
| ★ `display` | `block`、`inline`、`none`、`flex` | 块级、内联、不显示、弹性容器 |
| `list-style` | `none` | 去掉列表前的圆点、编号 |
| `cursor` | `pointer` | 鼠标移上去变成手形 |

写在**容器**上（只管直接子元素）：

| 属性 | 例子 | 说明 |
|---|---|---|
| ★ `display` | `flex` | 子元素沿主轴排成一行 |
| ★ `gap` | `20px` | 子元素之间的间隔 |
| ★ `justify-content` | `flex-start`、`center`、`space-between` | 沿主轴（左右）怎么放 |
| ★ `align-items` | `stretch`（默认）、`flex-start`、`center` | 交叉轴（上下）怎么对齐；默认拉伸 |
| `flex-direction` | `column` | 主轴改成竖向 |
| `flex-wrap` | `wrap` | 放不下时换行（默认不换行，挤压） |

写在**子元素**上：

| 属性 | 例子 | 说明 |
|---|---|---|
| ★ `flex` | `1`、`2` | 按比例分剩下的空间：两个都写 `1` 平分，`2` 和 `1` 按 2:1 分 |

两栏的常见写法：

```css
main { display: flex; gap: 20px; }
.list { flex: 2; }
.form { flex: 1; }
```

## 本讲不讲的

| 内容 | 什么时候用到 |
|---|---|
| `transition`（过渡）：`transition: background-color 0.3s;` 让属性变化慢慢发生 | 本讲拓展 E2 |
| 媒体查询：`@media (max-width: 600px) { main { flex-direction: column; } }` 窄屏时改样式 | 本讲拓展 E3（选做） |
| `position`、`z-index`（定位）、`float`（浮动）、Grid（网格布局） | 教材 3.2 之外，需要时查 MDN |
