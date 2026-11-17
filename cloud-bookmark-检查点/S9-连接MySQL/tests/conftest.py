# tests/conftest.py　第9讲第二段：pytest 在所有测试之前先执行本文件
import os

# 测试连内存库（sqlite:// 后面不写文件名），不碰开发用的 SQLite 文件和 MySQL；
# 必须在导入 app 之前设好，app 导入时就按它连接数据库
os.environ['DATABASE_URL'] = 'sqlite://'
