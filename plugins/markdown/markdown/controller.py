# -*- coding: utf-8 -*-

import os

from outwiker.api.core.events import pagetype
from outwiker.api.core.text import writeTextFile
from outwiker.api.core.pagestyle import getPageStyle
from outwiker.api.core.tree import addPageFactory, removePageFactory

from outwiker.gui.pagedialogpanels.appearancepanel import (
    AppearancePanel,
    AppearanceController,
)
from outwiker.pages.wiki.htmlcache import HtmlCache

from .colorizercontroller import ColorizerController
from .markdownhtmlgenerator import MarkdownHtmlGenerator
from .markdownpage import MarkdownPageFactory, MarkdownPage
from .i18n import get_


class Controller:
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        """ """
        self._plugin = plugin
        self._application = application

        self._appearancePanel = None
        self._appearanceController = None

        self._colorizerController = ColorizerController(
            self._application, MarkdownPage.getTypeString()
        )

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        addPageFactory(MarkdownPageFactory())
        self._application.onPageDialogPageFactoriesNeeded += (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageTypeChanged += (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded

    def clear(self):
        """
        Вызывается при отключении плагина
        """
        removePageFactory(MarkdownPageFactory().getTypeString())
        self._application.onPageDialogPageFactoriesNeeded -= (
            self.__onPageDialogPageFactoriesNeeded
        )
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageTypeChanged -= (
            self.__onPageDialogPageTypeChanged
        )
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(MarkdownPageFactory())

    @pagetype(MarkdownPage)
    def __onPageViewCreate(self, page):
        self._colorizerController.initialize(page)

    @pagetype(MarkdownPage)
    def __onPageViewDestroy(self, page):
        self._colorizerController.clear()

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == MarkdownPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController(self._appearanceController)
            params.dialog.removePanel(self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None

    def _addTab(self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel(dialog.getPanelsParent())
            dialog.addPanel(self._appearancePanel, _("Appearance"))

            self._appearanceController = AppearanceController(
                self._appearancePanel, self._application, dialog
            )

            dialog.addController(self._appearanceController)

    def __onPageDialogDestroy(self, page, params):
        self._appearancePanel = None
        self._appearanceController = None

    @pagetype(MarkdownPage)
    def __onPageUpdateNeeded(self, page, params):
        if page.readonly:
            return

        if not params.allowCache:
            HtmlCache(page, self._application).resetHash()
        self._updatePage(page)

    def _updatePage(self, page):
        path = page.getHtmlPath()
        cache = HtmlCache(page, self._application)

        # Проверим, можно ли прочитать уже готовый HTML
        if cache.canReadFromCache() and os.path.exists(path):
            return

        stylepath = getPageStyle(page)
        generator = MarkdownHtmlGenerator(page)

        html = generator.makeHtml(stylepath)
        writeTextFile(path, html)
        cache.saveHash()
