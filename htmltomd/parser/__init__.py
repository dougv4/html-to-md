"""
Módulo de parsing HTML

Este módulo é responsável por analisar o HTML e aplicar transformações iniciais.
"""

from .html_parser import parse_html, mark_page_breaks, remove_media, process_links

__all__ = ['parse_html', 'mark_page_breaks', 'remove_media', 'process_links']