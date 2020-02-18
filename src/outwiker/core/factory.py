# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import os.path
from typing import List, Callable

from .exceptions import ReadonlyException
from .tree_commands import getAlternativeTitle
from .tree import RootWikiPage, WikiPage


# Functions to calculate new page order

def orderCalculatorTop(_parent: RootWikiPage,
                       _alias: str,
                       _tags: List[str]) -> int:
    '''
    Add a page to top of the siblings
    '''
    return 0


def orderCalculatorBottom(parent: RootWikiPage,
                          _alias: str,
                          _tags: List[str]) -> int:
    '''
    Add a page to bottom of the siblings
    '''
    return len(parent.children)


def orderCalculatorAlphabetically(parent: RootWikiPage,
                                  alias: str,
                                  _tags: List[str]) -> int:
    '''
    Sort a page alias alphabetically
    '''
    order = len(parent.children)
    alias_lower = alias.lower()
    for n, page in enumerate(parent.children):
        if alias_lower < page.display_title.lower():
            order = n
            break

    return order


class PageFactory(metaclass=ABCMeta):
    """
    Класс для создания страниц
    """

    def create(self,
               parent: RootWikiPage,
               alias: str,
               tags: List[str],
               order_calculator: Callable[[RootWikiPage, str, List[str]], int] = orderCalculatorBottom
               ) -> WikiPage:
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        if parent.readonly:
            raise ReadonlyException

        siblings = [child_page.title for child_page in parent.children]
        title = getAlternativeTitle(alias, siblings)
        path = os.path.join(parent.path, title)

        pageType = self.getPageType()
        page = pageType(path, title, parent)
        order = order_calculator(parent, alias, tags)
        parent.addToChildren(page, order)

        try:
            page.initAfterCreating(tags)
        except Exception:
            parent.removeFromChildren(page)
            raise

        if title != alias:
            page.alias = alias

        return page

    @abstractmethod
    def getPageType(self):
        """
        Метод возвращает тип создаваемой страницы (не экземпляр страницы)
        """

    @abstractproperty
    def title(self):
        """
        Название страницы, показываемое пользователю
        """

    @abstractmethod
    def getPageView(self, parent, application):
        """
        Метод возвращает контрол,
        который будет отображать и редактировать страницу
        """

    def getTypeString(self):
        return self.getPageType().getTypeString()
