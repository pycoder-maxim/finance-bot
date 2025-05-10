from setuptools import setup

setup(name='handlera',
      version='1.0',
      description='Пакет инструментов для обработки команд пользователя',
      author='YK',
      author_email='',
      packages=['.'],
      py_modules=["telebot", "database", "loader"]
      )