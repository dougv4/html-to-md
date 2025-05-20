#!/usr/bin/env python3
"""
Setup para o pacote htmltomd
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="htmltomd",
    version="0.1.0",
    description="Conversor de HTML para Markdown com interface web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="E-docente",
    author_email="contato@e-docente.com",
    url="https://github.com/e-docente/html-to-markdown",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.11.1",
        "html2text>=2020.1.16",
        "streamlit>=1.22.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "htmltomd=htmltomd.ui.app:main",
        ],
    },
)