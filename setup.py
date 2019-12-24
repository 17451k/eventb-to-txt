# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import setuptools

setuptools.setup(
    name='eventb-to-txt',
    version='1.2',
    author='Ilya Shchepetkov',
    author_email='ilya.shchepetkov@yandex.ru',
    license='LICENSE.txt',
    description="Event-B to txt converter",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    url="https://github.com/17451k/eventb-to-txt",
    packages=['eventb_to_txt'],
    entry_points={
        'console_scripts': [
            'eventb-to-txt=eventb_to_txt.__main__:main',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X"
    )
)
