#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

from gui.TextEditor import TextEditor
from gui.BaseTextPanel import BaseTextPanel

class TextPanel (BaseTextPanel):
	"""
	Класс для представления текстовых страниц
	"""

	def __init__ (self, page, parent, *args, **kwds):
		BaseTextPanel.__init__ (self, *args, **kwds)

		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, parent, *args, **kwds)

		self.__layout()

		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.page = page

	
	def onEditorConfigChange (self):
		self.textEditor.setDefaultSettings()
	

	def UpdateView (self, page):
		self.textEditor.textCtrl.SetText (self._currentpage.content)
		self.textEditor.textCtrl.EmptyUndoBuffer()
		self.textEditor.textCtrl.SetReadOnly (page.readonly)
	

	def __layout (self):
		self.textEditor = TextEditor(self, -1)

		mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
		mainSizer.Add(self.textEditor, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)


	def onAttachmentPaste (self, fnames):
		text = self._getAttachString (fnames)
		self.textEditor.textCtrl.AddText (text)
		self.textEditor.textCtrl.SetFocus()


	def onClose (self, event):
		BaseTextPanel.Close (self)
	

	def GetContentFromGui (self):
		return  self.textEditor.textCtrl.GetText()


	def GetSearchPanel (self):
		return self.textEditor.searchPanel
