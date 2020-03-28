from __future__ import absolute_import
from distutils.core import setup

setup(
    name='Reversi',
    version='0.1dev',
    author='Jeff Bradberry',
    author_email='jeff.bradberry@gmail.com',
    packages=['reversi'],
    entry_points={
        'jrb_board.games': 'reversi = reversi.reversi:Board',
    },
    install_requires=['six'],
    license='LICENSE',
    description="An implementation of the board game Reversi.",
)
