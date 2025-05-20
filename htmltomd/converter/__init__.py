"""
Módulo de conversão para Markdown

Este módulo é responsável por converter HTML parseado para Markdown.
"""

from .md_converter import convert_to_markdown, clean_markdown

__all__ = ['convert_to_markdown', 'clean_markdown']