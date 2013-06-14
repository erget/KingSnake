#!/usr/bin/env python

from distutils.core import setup

setup(name='KingSnake',
      version='0.1.0',
      description='A Python chess game for two human players',
      author='Daniel Lee',
      author_email='Lee.Daniel.1986@gmail.com',
      url='https://github.com/erget/KingSnake',
      packages=['king_snake', 'king_snake.figures'],
      license="LICENSE",
      long_description=open("README").read(),
      scripts=["bin/KingSnake"]
     )
