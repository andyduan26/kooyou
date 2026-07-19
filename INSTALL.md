# 本地搭建

## 1. 安装并锁定 Python

```bash
brew install pyenv
pyenv install 3.12.4
cd /Users/andyduan26/Documents/优酷2.0
pyenv local 3.12.4
python --version
```

项目已通过 `.python-version` 锁定 `3.12.4`。Django 使用当前 LTS 线 `5.2.x`。

## 2. 创建独立虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

依赖清单包含：

- Django
- djangorestframework
- django-simpleui
- django-cors-headers
- gunicorn
- python-multipart
- Pillow
- django-filter
- dj-database-url
- psycopg

## 4. 一键项目初始化命令

本仓库已创建 Django 主项目 `kooyou_backend` 与业务 APP `video`。从零复现的等价命令如下：

```bash
django-admin startproject kooyou_backend .
python manage.py startapp video
```

## 5. 数据库迁移与管理员

```bash
python manage.py migrate
python scripts/create_superuser.py
```

## 6. 本地启动

```bash
python manage.py runserver
```

API 根路径：`http://127.0.0.1:8000/api/`

后台路径：`http://127.0.0.1:8000/admin/`

## 7. 验证

```bash
python manage.py check
python manage.py test
```
