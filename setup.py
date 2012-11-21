#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Lidio Ramalho
# lidios@gmail.com

# Issues Stats is free software: you can redistribute it and/or modify it under the terms MIT License

# Issues Stats is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the MIT Public License for more details.

from distutils.core import setup, Command
import textwrap
import sys
import glob

class test( Command ):
    user_options = []

    def initialize_options( self ):
        pass

    def finalize_options( self ):
        pass

    def run( self ):
        pass

setup(
    name = "issues_stats",
    version = "0.1",
    description = "Github Issues Statistics",
    author = "Lidio Ramalho",
    author_email = "lidios@gmail.com",
    url = "https://github.com/lidios/issues_stats",
    long_description = textwrap.dedent( """\
        Tutorial
        ========

        ...""" ),
    packages = [
        "stats",
    ],
    package_data = {
        "stats": [ "ReadMe.md", "LICENSE*", ]
    },
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: MIT ",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)