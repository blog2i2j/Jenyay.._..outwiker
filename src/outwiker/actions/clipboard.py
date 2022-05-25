# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import (copyTitleToClipboard,
                                    copyLinkToClipboard,
                                    copyPathToClipboard,
                                    copyAttachPathToClipboard,
                                    showInfo)


class CopyPageTitleAction(BaseAction):
    """
    Копировать в буфер обмена заголовок текущей страницы
    """
    stringId = "CopyPageTitle"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Page Title")

    @property
    def description(self):
        return _("Copy current page title to clipboard")

    def run(self, page=None):
        if page is None:
            page = self._application.selectedPage

        if page is None:
            return

        if copyTitleToClipboard(page):
            title = _('Copied to clipboard')
            text = _('Page title has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)


class CopyPagePathAction(BaseAction):
    """
    Копировать в буфер обмена путь до текущей страницы
    """
    stringId = u"CopyPagePath"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Page Path")

    @property
    def description(self):
        return _("Copy path to current page to clipboard")

    def run(self, page=None):
        if page is None:
            page = self._application.selectedPage

        if page is None:
            return

        if copyPathToClipboard(page):
            title = _('Copied to clipboard')
            text = _('Path to the page has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)


class CopyAttachPathAction(BaseAction):
    """
    Копировать в буфер обмена путь до прикрепленных файлов
    """
    stringId = "CopyAttachPath"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Attachments Path")

    @property
    def description(self):
        return _("Copy path to attachments for current page to clipboard")

    def run(self, page=None):
        if page is None:
            page = self._application.selectedPage

        if page is None:
            return

        is_current_page = page is self._application.selectedPage

        if copyAttachPathToClipboard(page, is_current_page):
            title = _('Copied to clipboard')
            text = _('Path to the page attachments has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)


class CopyPageLinkAction(BaseAction):
    """
    Копировать в буфер обмена ссылку на текущую страницу
    """
    stringId = u"CopyPageLink"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Page Link")

    @property
    def description(self):
        return _("Copy link to current page to clipboard")

    def run(self, page=None):
        if page is None:
            page = self._application.selectedPage

        if page is None:
            return

        if copyLinkToClipboard(page):
            title = _('Copied to clipboard')
            text = _('Link to the page has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)
