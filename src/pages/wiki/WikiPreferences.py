#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed Nov 24 21:52:16 2010

import wx

from gui.preferences.ConfigElements import BooleanElement, IntegerElement
from core.application import Application
from wikiconfig import WikiConfig
import wikipage

# begin wxGlade: extracode
# end wxGlade



class WikiPrefGeneralPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: WikiPrefGeneralPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.htmlCodeCheckbox = wx.CheckBox(self, -1, _("Show HTML Code Tab"))
		self.showAttachInsteadBlank = wx.CheckBox(self, -1, _("Show Attachments Instead Blank page"))
		self.thumbSizeLabel = wx.StaticText(self, -1, _("Thumbnail Size"))
		self.thumbSize = wx.SpinCtrl(self, -1, "250", min=1, max=10000)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		self.config = WikiConfig (Application.config)


	def __set_properties(self):
		# begin wxGlade: WikiPrefGeneralPanel.__set_properties
		self.showAttachInsteadBlank.SetValue(1)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: WikiPrefGeneralPanel.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		grid_sizer_1 = wx.FlexGridSizer(1, 2, 0, 0)
		mainSizer.Add(self.htmlCodeCheckbox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		mainSizer.Add(self.showAttachInsteadBlank, 0, wx.ALL, 2)
		grid_sizer_1.Add(self.thumbSizeLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_1.Add(self.thumbSize, 0, wx.ALL|wx.EXPAND, 2)
		grid_sizer_1.AddGrowableRow(0)
		grid_sizer_1.AddGrowableCol(0)
		grid_sizer_1.AddGrowableCol(1)
		grid_sizer_1.AddGrowableCol(2)
		mainSizer.Add(grid_sizer_1, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableCol(0)
		# end wxGlade
	

	def LoadState(self):
		# Показывать ли вкладку с кодом HTML?
		self.showHtmlCodeOption = BooleanElement (self.config.showHtmlCodeOptions, self.htmlCodeCheckbox)

		# Размер превьюшек по умолчанию
		self.thumbSizeOption = IntegerElement (self.config.thumbSizeOptions, self.thumbSize, 1, 10000)

		self.showAttachInsteadBlankOption = BooleanElement (self.config.showAttachInsteadBlankOptions, 
				self.showAttachInsteadBlank)


	def Save (self):
		changed = self.showHtmlCodeOption.isValueChanged() or \
			self.thumbSizeOption.isValueChanged() or \
			self.showAttachInsteadBlankOption.isValueChanged()

		self.showHtmlCodeOption.save()
		self.thumbSizeOption.save()
		self.showAttachInsteadBlankOption.save()

		if changed:
			currpage = Application.wikiroot.selectedPage
			Application.wikiroot.selectedPage = None
			Application.wikiroot.selectedPage = currpage

# end of class WikiPrefGeneralPanel


