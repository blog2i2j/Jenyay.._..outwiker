# -*- coding: utf-8 -*-

from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.api.core.text import readTextFile

from markdownparser.parser import Parser


class MarkdownHtmlGenerator:
    """
    Class to convert Markdown to HTML code.
    """

    def __init__(self, page):
        self.page = page

    def makeHtml(self, stylepath):
        parser = Parser()
        css = parser.getCSS()
        head = "<style>\n{}\n</style>".format(css)

        html = parser.convert(self.page.content)
        tpl = HtmlTemplate(readTextFile(stylepath))
        result = tpl.substitute(
            content=html, userhead=head, title=self.page.display_title
        )
        return result
