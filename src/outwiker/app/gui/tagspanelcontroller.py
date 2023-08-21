# -*- coding: utf-8 -*-

import wx
from functools import cmp_to_key

from outwiker.app.services.messages import showError

from outwiker.core.tagslist import TagsList
from outwiker.core.tagscommands import removeTag, appendTag
from outwiker.core.sortfunctions import sortAlphabeticalFunction

from outwiker.gui.controls.pagelist import EVT_PAGE_CLICK
# from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.controls.taglabel2 import EVT_TAG_LEFT_CLICK, EVT_TAG_ADD, EVT_TAG_REMOVE, TagAddEvent, TagLeftClickEvent


class TagsPanelController:
    def __init__(self, tagsPanel, application):
        self.__tagsPanel = tagsPanel
        self.__application = application
        self.__currentTags = None

        self.__bindAppEvents()

        self.__application.onStartTreeUpdate += self.__onStartUpdate
        self.__application.onEndTreeUpdate += self.__onEndUpdate
        self.__application.onPageSelect += self.__onPageSelect

        self.__tagsPanel.Bind(EVT_PAGE_CLICK, handler=self.__onPageClick)
        self.__tagsPanel.Bind(EVT_TAG_LEFT_CLICK, handler=self.__onTagLeftClick)
        self.__tagsPanel.Bind(EVT_TAG_ADD, handler=self.__onTagAdd)
        self.__tagsPanel.Bind(EVT_TAG_REMOVE, handler=self.__onTagRemove)
        self.__tagsPanel.Bind(wx.EVT_CLOSE, handler=self.__onClose)

        self.updateTags()

    def __onClose(self, event):
        self.__tagsPanel.Unbind(EVT_PAGE_CLICK, handler=self.__onPageClick)
        self.__tagsPanel.Unbind(EVT_TAG_LEFT_CLICK, handler=self.__onTagLeftClick)
        self.__tagsPanel.Unbind(EVT_TAG_ADD, handler=self.__onTagAdd)
        self.__tagsPanel.Unbind(EVT_TAG_REMOVE, handler=self.__onTagRemove)
        self.__tagsPanel.Unbind(wx.EVT_CLOSE, handler=self.__onClose)

        self.__application.onStartTreeUpdate -= self.__onStartUpdate
        self.__application.onEndTreeUpdate -= self.__onEndUpdate
        self.__application.onPageSelect -= self.__onPageSelect

        self.__unbindAppEvents()

        self.__tagsPanel.clearTags()
        self.__tagsPanel.Destroy()

    def __onStartUpdate(self, page):
        self.__unbindAppEvents()

    def __onEndUpdate(self, page):
        self.__bindAppEvents()
        self.updateTags()

    # def __runAction(self, action, tagname):
    #     if action == TagsConfig.ACTION_MARK_TOGGLE:
    #         self.__toggleMarkTag(tagname)
    #     else:
    #         self.__showPopup(tagname)

    def __showPopup(self, tagname):
        pages = self.__currentTags[tagname][:]
        pages.sort(key=cmp_to_key(sortAlphabeticalFunction))

        self.__tagsPanel.showPopup(pages)

    # def __toggleMarkTag(self, tagname):
    #     selectedPage = self.__application.selectedPage
    #     if selectedPage is None:
    #         return

    #     if selectedPage.readonly:
    #         showError(self.__application.mainWindow,
    #                   _('Page is opened as read-only'))
    #         return

    #     if tagname in selectedPage.tags:
    #         removeTag(selectedPage, tagname)
    #     else:
    #         appendTag(selectedPage, tagname)

    def __onTagLeftClick(self, event: TagLeftClickEvent):
        """
        Клик левой кнопкой мыши по тегу
        """
        assert self.__currentTags is not None
        self.__showPopup(event.text)

    def __onTagAdd(self, event: TagAddEvent):
        selectedPage = self.__application.selectedPage
        if selectedPage is None:
            return

        if selectedPage.readonly:
            showError(self.__application.mainWindow,
                      _('Page is opened as read-only'))
            return

        appendTag(selectedPage, event.text)

    def __onTagRemove(self, event):
        selectedPage = self.__application.selectedPage
        if selectedPage is None:
            return

        if selectedPage.readonly:
            showError(self.__application.mainWindow,
                      _('Page is opened as read-only'))
            return

        removeTag(selectedPage, event.text)

    def __onPageClick(self, event):
        assert event.page is not None
        self.__application.selectedPage = event.page

    def __bindAppEvents(self):
        self.__application.onPageUpdate += self.__onUpdate
        self.__application.onPageRemove += self.__onUpdate
        self.__application.onPageCreate += self.__onUpdate
        self.__application.onTreeUpdate += self.__onUpdate
        self.__application.onWikiOpen += self.__onUpdate
        self.__application.onPreferencesDialogClose += self.__onPreferencesDialogClose

    def __unbindAppEvents(self):
        self.__application.onPageUpdate -= self.__onUpdate
        self.__application.onPageRemove -= self.__onUpdate
        self.__application.onPageCreate -= self.__onUpdate
        self.__application.onTreeUpdate -= self.__onUpdate
        self.__application.onWikiOpen -= self.__onUpdate
        self.__application.onPreferencesDialogClose -= self.__onPreferencesDialogClose

    def __onPreferencesDialogClose(self, dialog):
        self.updateTags()

    def __onPageSelect(self, page):
        self.__markTags()

    def __onUpdate(self, sender, **kwargs):
        self.updateTags()

    def __isEqual(self, taglist1, taglist2):
        """
        Возвращает True, если списки тегов одинаковые,
        и False в противном случае
        """
        if taglist1 is None or taglist2 is None:
            return False

        keys1 = taglist1.tags
        keys2 = taglist2.tags

        if keys1 != keys2:
            return False

        for key in keys1:
            if len(taglist2[key]) != len(taglist1[key]):
                return False

        return True

    def updateTags(self):
        if self.__application.wikiroot is None:
            self.__tagsPanel.clearMarks()
            self.__tagsPanel.clearTags()
            self.__currentTags = None
            return

        tags = TagsList(self.__application.wikiroot)

        if not self.__isEqual(tags, self.__currentTags):
            self.__tagsPanel.setTags(tags)
            self.__currentTags = tags
            self.__markTags()
        else:
            self.__tagsPanel.updateTagLabels()

    def __markTags(self):
        self.__tagsPanel.clearMarks()

        if self.__application.selectedPage is not None:
            for tag in self.__application.selectedPage.tags:
                self.__tagsPanel.mark(tag)
