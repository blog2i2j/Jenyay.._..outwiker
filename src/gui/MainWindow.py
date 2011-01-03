# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Mar 23 21:59:58 2010

import os.path
import sys

import wx
import wx.aui

from core.controller import Controller
from core.tree import WikiDocument, RootWikiPage
from WikiTree import WikiTree
from gui.CurrentPagePanel import CurrentPagePanel
import core.commands
from core.recent import RecentWiki
import pages.search.searchpage
import core.system
from gui.preferences.PrefDialog import PrefDialog
from gui.about import AboutDialog
from core.application import Application
from gui.trayicon import OutwikerTrayIcon
from gui.AttachPanel import AttachPanel
import core.config

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade


class MainWindow(wx.Frame):
	def makeId (self):
		self.ID_NEW = wx.NewId()
		self.ID_OPEN = wx.NewId()
		self.ID_OPEN_READONLY = wx.NewId()
		self.ID_SAVE = wx.NewId()
		self.ID_SAVEAS = wx.NewId()
		self.ID_RELOAD = wx.NewId()
		self.ID_ADDPAGE = wx.NewId()
		self.ID_ADDCHILD = wx.NewId()
		self.ID_ATTACH = wx.NewId()
		self.ID_ABOUT = wx.NewId()
		self.ID_EXIT = wx.NewId()
		self.ID_COPYPATH = wx.NewId()
		self.ID_COPY_ATTACH_PATH = wx.NewId()
		self.ID_COPY_LINK = wx.NewId()
		self.ID_COPY_TITLE = wx.NewId()
		self.ID_BOOKMARKS = wx.NewId()
		self.ID_ADDBOOKMARK = wx.NewId()
		self.ID_EDIT = wx.NewId()
		self.ID_REMOVE_PAGE = wx.NewId()
		self.ID_GLOBAL_SEARCH = wx.NewId()
		self.ID_RENAME = wx.NewId()
		self.ID_HELP = wx.NewId()
		self.ID_PREFERENCES = wx.NewId()
		self.ID_RESTORE = wx.NewId()


	def __init__(self, *args, **kwds):
		self.makeId()

		self.disabledTools = [self.ID_SAVE, self.ID_SAVEAS, self.ID_RELOAD, 
				self.ID_ADDPAGE, self.ID_ADDCHILD, self.ID_ATTACH, 
				self.ID_COPYPATH, self.ID_COPY_ATTACH_PATH, self.ID_COPY_LINK,
				self.ID_COPY_TITLE, self.ID_BOOKMARKS, self.ID_ADDBOOKMARK,
				self.ID_EDIT, self.ID_REMOVE_PAGE, self.ID_GLOBAL_SEARCH,
				wx.ID_UNDO, wx.ID_REDO, wx.ID_CUT, wx.ID_COPY, wx.ID_PASTE]

		# Флаг, обозначающий, что в цикле обработки стандартных сообщений 
		# вроде копирования в буфер обмена сообщение вернулось обратно
		self.stdEventLoop = False

		# Идентификаторы для пунктов меню последних открытых вики
		# Ключ - id, значение - путь до вики
		self._recentId = {}

		# Идентификаторы для пунктов меню для открытия закладок
		# Ключ - id, значение - путь до страницы вики
		self._bookmarksId = {}

		# Флаг, который отмечает, что пришло первое событие onIdle.
		# Используется для определения момента, когда окно только загрузилось
		self.firstEvent = True

		# Ширина дерева по умолчанию
		self.defaultSash = 200

		Controller.instance().onTreeUpdate += self.onTreeUpdate
		Controller.instance().onPageSelect += self.onPageSelect
		Controller.instance().onBookmarksChanged += self.onBookmarksChanged
		Controller.instance().onMainWindowConfigChange += self.onMainWindowConfigChange
		
		# Путь к директории с программой/скриптом
		self.imagesDir = core.system.getImagesDir()

		# begin wxGlade: MainWindow.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		
		# Menu Bar
		self.mainMenu = wx.MenuBar()
		self.fileMenu = wx.Menu()
		self.fileMenu.Append(self.ID_NEW, _("&New\tCtrl+N"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN, _(u"&Open…\tCtrl+O"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN_READONLY, _("Open &Read-only...\tCtrl+Shift+O"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_SAVE, _("&Save\tCtrl+S"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_EXIT, _(u"&Exit…\tAlt+F4"), "", wx.ITEM_NORMAL)
		self.fileMenu.AppendSeparator()
		self.mainMenu.Append(self.fileMenu, _("&File"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_UNDO, _("&Undo\tCtrl+Z"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_REDO, _("&Redo\tCtrl+Y"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(wx.ID_CUT, _("Cu&t\tCtrl+X"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_COPY, _("&Copy\tCtrl+C"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_PASTE, _("&Paste\tCtrl+V"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_PREFERENCES, _("Pr&eferences...\tCtrl+F8"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, _("&Edit"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_ADDPAGE, _(u"Add &Sibling Page…\tCtrl+T"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ADDCHILD, _(u"Add &Child Page…\tCtrl+Shift+T"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_RENAME, _("Re&name Page\tF2"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_REMOVE_PAGE, _(u"Rem&ove Page…\tCtrl+Shift+Del"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_EDIT, _(u"&Edit Page Properties…\tCtrl+E"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, _("&Tree"))
		self.toolsMenu = wx.Menu()
		self.toolsMenu.Append(self.ID_GLOBAL_SEARCH, _(u"&Global Search…\tCtrl+Shift+F"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_ATTACH, _(u"&Attach Files…\tCtrl+Alt+A"), "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_COPY_TITLE, _("Copy Page &Title to Clipboard\tCtrl+Shift+D"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPYPATH, _("Copy &Page Path to Clipboard\tCtrl+Shift+P"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_ATTACH_PATH, _("Copy Atta&ches Path to Clipboard\tCtrl+Shift+A"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_LINK, _("Copy Page &Link to Clipboard\tCtrl+Shift+L"), "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_RELOAD, _("&Reload Wiki...\tCtrl+R"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(self.toolsMenu, _("T&ools"))
		self.bookmarksMenu = wx.Menu()
		self.bookmarksMenu.Append(self.ID_ADDBOOKMARK, _("&Add/Remove Bookmark\tCtrl+D"), "", wx.ITEM_NORMAL)
		self.bookmarksMenu.AppendSeparator()
		self.mainMenu.Append(self.bookmarksMenu, _("&Bookmarks"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_HELP, _("&Help\tF1"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ABOUT, _(u"&About…\tCtrl+F1"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, _("&Help"))
		self.SetMenuBar(self.mainMenu)
		# Menu Bar end
		
		# Tool Bar
		self.mainToolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE)
		self.SetToolBar(self.mainToolbar)
		self.mainToolbar.AddLabelTool(self.ID_NEW, _(u"New…"), wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Create new wiki…"), "")
		self.mainToolbar.AddLabelTool(self.ID_OPEN, _(u"Open…"), wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Open wiki…"), "")
		self.mainToolbar.AddLabelTool(self.ID_SAVE, _("Save"), wx.Bitmap(os.path.join (self.imagesDir, "save.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Save wiki"), "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_RELOAD, _("Reload"), wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Reload wiki"), "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_ADDPAGE, _(u"Add sibling page…"), wx.Bitmap(os.path.join (self.imagesDir, "sibling.ico"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Add sibling page…"), "")
		self.mainToolbar.AddLabelTool(self.ID_ADDCHILD, _(u"Add child Page…"), wx.Bitmap(os.path.join (self.imagesDir, "child.ico"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Add child Page…"), "")
		self.mainToolbar.AddLabelTool(self.ID_REMOVE_PAGE, _("Remove page"), wx.Bitmap(os.path.join (self.imagesDir, "remove.ico"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Remove page…"), "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_ATTACH, _(u"Attach files…"), wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Attach files…"), "")
		self.mainToolbar.AddLabelTool(self.ID_EDIT, _("Edit page"), wx.Bitmap(os.path.join (self.imagesDir, "edit.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Edit page's properties"), "")
		self.mainToolbar.AddLabelTool(self.ID_GLOBAL_SEARCH, _(u"Global search…"), wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Global search…"), "")
		self.mainToolbar.AddSeparator()
		# Tool Bar end
		self.mainPanel = wx.Panel(self, -1)
		self.statusbar = wx.StatusBar(self, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_MENU, self.onNew, id=self.ID_NEW)
		self.Bind(wx.EVT_MENU, self.onOpen, id=self.ID_OPEN)
		self.Bind(wx.EVT_MENU, self.onOpenReadOnly, id=self.ID_OPEN_READONLY)
		self.Bind(wx.EVT_MENU, self.onSave, id=self.ID_SAVE)
		self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_REDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_CUT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_COPY)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.onPreferences, id=self.ID_PREFERENCES)
		self.Bind(wx.EVT_MENU, self.onAddSiblingPage, id=self.ID_ADDPAGE)
		self.Bind(wx.EVT_MENU, self.onAddChildPage, id=self.ID_ADDCHILD)
		self.Bind(wx.EVT_MENU, self.onRename, id=self.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.onRemovePage, id=self.ID_REMOVE_PAGE)
		self.Bind(wx.EVT_MENU, self.onEditPage, id=self.ID_EDIT)
		self.Bind(wx.EVT_MENU, self.onGlobalSearch, id=self.ID_GLOBAL_SEARCH)
		self.Bind(wx.EVT_MENU, self.onAttach, id=self.ID_ATTACH)
		self.Bind(wx.EVT_MENU, self.onCopyTitle, id=self.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.onCopyPath, id=self.ID_COPYPATH)
		self.Bind(wx.EVT_MENU, self.onCopyAttaches, id=self.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.onCopyLink, id=self.ID_COPY_LINK)
		self.Bind(wx.EVT_MENU, self.onReload, id=self.ID_RELOAD)
		self.Bind(wx.EVT_MENU, self.onBookmark, id=self.ID_ADDBOOKMARK)
		self.Bind(wx.EVT_MENU, self.onHelp, id=self.ID_HELP)
		self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)
		self.Bind(wx.EVT_TOOL, self.onNew, id=self.ID_NEW)
		self.Bind(wx.EVT_TOOL, self.onOpen, id=self.ID_OPEN)
		self.Bind(wx.EVT_TOOL, self.onReload, id=self.ID_RELOAD)
		self.Bind(wx.EVT_TOOL, self.onAddSiblingPage, id=self.ID_ADDPAGE)
		self.Bind(wx.EVT_TOOL, self.onAddChildPage, id=self.ID_ADDCHILD)
		self.Bind(wx.EVT_TOOL, self.onRemovePage, id=self.ID_REMOVE_PAGE)
		self.Bind(wx.EVT_TOOL, self.onAttach, id=self.ID_ATTACH)
		self.Bind(wx.EVT_TOOL, self.onEditPage, id=self.ID_EDIT)
		self.Bind(wx.EVT_TOOL, self.onGlobalSearch, id=self.ID_GLOBAL_SEARCH)
		# end wxGlade

		self.auiManager = wx.aui.AuiManager(self.mainPanel)

		self.tree = WikiTree(self.mainPanel, -1)
		self.pagePanel = CurrentPagePanel(self.mainPanel, -1)
		self.attachPanel = AttachPanel (self.mainPanel, -1)

		self.__initAuiManager (self.auiManager)

		self.__setMenuBitmaps()
		
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.Bind (wx.EVT_ICONIZE, self.onIconize)
		self.Bind (wx.EVT_MENU, self.onRestore, id=self.ID_RESTORE)
		self.Bind (wx.EVT_IDLE, self.onIdle)

		self.mainPanel.Bind (wx.EVT_CLOSE, self.onMainPanelClose)

		self._dropTarget = DropFilesTarget (self)

		self.SetDropTarget (self._dropTarget)
		self.__enableGui()
		self. __createTrayIcon()

		self.statusbar.SetFieldsCount(1)
		self.pagePanel.Disable()

		aTable = wx.AcceleratorTable([
			(wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
			(wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
			(wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
		self.SetAcceleratorTable(aTable)
	

	def onMainPanelClose (self, event):
		self.tree.Close()
		self.pagePanel.Close()
		self.attachPanel.Close()
		
		self.mainPanel.Destroy()


	def __initAuiManager(self, auiManager):
		self.__initTreePane (self.auiManager)
		self.__initAttachesPane (self.auiManager)

		auiManager.AddPane(self.pagePanel, wx.CENTER)
		auiManager.Update()

		self.tree.SetMinSize ((Application.config.treeWidthOption.value, 
			Application.config.treeHeightOption.value))
		
		self.attachPanel.SetMinSize ((Application.config.attachesWidthOption.value, 
			Application.config.attachesHeightOption.value))
		

	def __initTreePane (self, auiManager):
		"""
		Загрузить настройки окошка с деревом
		"""
		config = Application.config
		
		pane = self.__loadPaneInfo (config.treePaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name(("treePane")).Caption(_("Notes")).Gripper(False).CaptionVisible(True).Layer(2).Position(0).CloseButton(False).MaximizeButton(False).Left().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		auiManager.AddPane(self.tree, pane, _('Notes') )
	

	def __initAttachesPane (self, auiManager):
		"""
		Загрузить настройки окошка с прикрепленными файлами
		"""
		config = Application.config
		
		pane = self.__loadPaneInfo (config.attachesPaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name("attachesPane").Caption(_("Attaches")).Gripper(False).CaptionVisible(True).Layer(1).Position(0).CloseButton(False).MaximizeButton(False).Bottom().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		auiManager.AddPane(self.attachPanel, pane, _('Attaches') )
	

	def __loadPaneInfo (self, param):
		"""
		Загрузить из конфига и вернуть информацию о dockable-панели (AuiPaneInfo)
		"""
		string_info = param.value

		if len (string_info) == 0:
			return

		pane = wx.aui.AuiPaneInfo()
		try:
			self.auiManager.LoadPaneInfo (string_info, pane)
		except Exception, e:
			return

		return pane


	def __savePaneInfo (self, param, paneInfo):
		"""
		Сохранить в конфиг информацию о dockable-панели (AuiPaneInfo)
		"""
		string_info = self.auiManager.SavePaneInfo (paneInfo)
		param.value = string_info


	def __savePanesParams (self):
		"""
		Сохранить параметры панелей
		"""
		self.__savePaneInfo (Application.config.treePaneOption, self.auiManager.GetPane (self.tree))
		self.__savePaneInfo (Application.config.attachesPaneOption, self.auiManager.GetPane (self.attachPanel))
		
		Application.config.treeWidthOption.value = self.tree.GetSizeTuple()[0]
		Application.config.treeHeightOption.value = self.tree.GetSizeTuple()[1]
			
		Application.config.attachesWidthOption.value = self.attachPanel.GetSizeTuple()[0]
		Application.config.attachesHeightOption.value = self.attachPanel.GetSizeTuple()[1]


	def onPageSelect (self, newpage):
		self.__updateTitle()
	

	def __updateTitle (self):
		template = Application.config.titleFormatOption.value

		if Application.wikiroot == None:
			self.SetTitle (u"OutWiker")
			return

		pageTitle = u"" if Application.wikiroot.selectedPage == None else Application.wikiroot.selectedPage.title
		filename = os.path.basename (Application.wikiroot.path)

		result = template.replace ("{file}", filename).replace ("{page}", pageTitle)
		self.SetTitle (result)
	

	def onRestore (self, event):
		self.__restoreWindow()
	

	def __createTrayIcon (self):
		self.taskBarIcon = OutwikerTrayIcon()
		self.taskBarIcon.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.OnTrayLeftClick)
		self.taskBarIcon.Bind(wx.EVT_MENU, self.onRestore, id=self.taskBarIcon.ID_RESTORE)
		self.taskBarIcon.Bind(wx.EVT_MENU, self.onExit, id=self.taskBarIcon.ID_EXIT)


	def OnTrayLeftClick (self, event):
		self.__restoreWindow()


	def __enableGui (self):
		"""
		Проверить открыта ли вики и включить или выключить кнопки на панели
		"""
		enabled = Application.wikiroot != None
		self.__enableTools (enabled)
		self.__enableMenu (enabled)
		self.pagePanel.Enable()

	
	def __enableTools (self, enabled):
		for toolId in self.disabledTools:
			if self.mainToolbar.FindById (toolId) != None:
				self.mainToolbar.EnableTool (toolId, enabled)

	
	def __enableMenu (self, enabled):
		for toolId in self.disabledTools:
			if self.mainMenu.FindItemById (toolId) != None:
				self.mainMenu.Enable (toolId, enabled)


	def __setMenuBitmaps (self):
		newItem = self.fileMenu.FindItemById (self.ID_NEW)
		newBitmap = wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY)
		newItem.SetBitmap (newBitmap)


	def onIdle (self, event):
		if self.firstEvent:
			self.firstEvent = False
			self._loadParams()
			self._loadRecentWiki()
			self.__iconizeAfterStart ()

			if len (sys.argv) > 1:
				self._openFromCommandLine()
			else:
				# Открыть последний открытый файл (если установлена соответствующая опция)
				self.__openRecentWiki ()

	

	def __openRecentWiki (self):
		"""
		Открыть последнюю вики, если установлена соответствующая опция
		"""
		openRecent = Application.config.historyLengthOption.value

		if openRecent and len (self.recentWiki) > 0:
			self.openWiki (self.recentWiki[0])


	def __iconizeAfterStart (self):
		"""
		Свернуться при запуске, если установлена соответствующая опция
		"""
		iconize = Application.config.startIconizedOption.value

		if iconize:
			self.Iconize(True)

	
	def _openFromCommandLine (self):
		"""
		Открыть вики, путь до которой передан в командной строке
		"""
		fname = unicode (sys.argv[1], core.system.getOS().filesEncoding)
		if not os.path.isdir (fname):
			fname = os.path.split (fname)[0]

		try:
			wikiroot = WikiDocument.load (fname)
		except IOError:
			wx.MessageBox (_(u"Can't load wiki '%s'") % self._recentId[event.Id], _(u"Error"), wx.ICON_ERROR | wx.OK)
			return

		self._openLoadedWiki(wikiroot)

	
	def _loadRecentWiki (self):
		self._removeMenuItemsById (self.fileMenu, self._recentId.keys())
		self._recentId = {}

		self.recentWiki = RecentWiki (Application.config)

		self._recentId = {}

		for n in range (len (self.recentWiki)):
			id = wx.NewId()
			path = self.recentWiki[n]
			self._recentId[id] = path

			title = path if n + 1 > 9 else u"&{n}. {path}".format (n=n + 1, path=path)

			self.fileMenu.Append (id, title, "", wx.ITEM_NORMAL)
			
			self.Bind(wx.EVT_MENU, self.onRecent, id=id)
	

	def _loadBookmarks (self):
		self._removeMenuItemsById (self.bookmarksMenu, self._bookmarksId.keys())
		self._bookmarksId = {}

		if Application.wikiroot != None:
			for n in range (len (Application.wikiroot.bookmarks)):
				id = wx.NewId()
				page = Application.wikiroot.bookmarks[n]
				if page == None:
					continue

				subpath = page.subpath
				self._bookmarksId[id] = subpath

				# Найдем родителя
				parent = page.parent

				if parent.parent != None:
					label = "%s [%s]" % (page.title, parent.subpath)
				else:
					label = page.title

				self.bookmarksMenu.Append (id, label, "", wx.ITEM_NORMAL)
				self.Bind(wx.EVT_MENU, self.onSelectBookmark, id=id)


	def _removeMenuItemsById (self, menu, keys):
		"""
		Удалить все элементы меню по идентификаторам
		"""
		for key in keys:
			menu.Delete (key)
			self.Unbind (wx.EVT_MENU, id = key)


	def onRecent (self, event):
		"""
		Выбор меню с недавно открытыми файлами
		"""
		self.openWiki (self._recentId[event.Id])


	def openWiki (self, path, readonly=False):
		Controller.instance().onStartTreeUpdate(Application.wikiroot)
		
		try:
			if Application.wikiroot != None:
				Controller.instance().onWikiClose (Application.wikiroot)
			
			wikiroot = core.commands.openWiki (path, readonly)
			self._openLoadedWiki(wikiroot, addToRecent = not readonly)
		except IOError:
			wx.MessageBox (_(u"Can't load wiki '%s'") % path, _(u"Error"), wx.ICON_ERROR | wx.OK)

		finally:
			Controller.instance().onEndTreeUpdate(Application.wikiroot)


	
	def onSelectBookmark (self, event):
		subpath = self._bookmarksId[event.Id]
		page = Application.wikiroot[subpath]

		if page != None:
			Application.wikiroot.selectedPage = Application.wikiroot[subpath]
	

	def _loadParams(self):
		"""
		Загрузить параметры из конфига
		"""
		config = Application.config
		self.Freeze()

		width = config.WidthOption.value
		height = config.HeightOption.value

		xpos = config.XPosOption.value
		ypos = config.YPosOption.value
		
		self.SetSize ( (width, height) )
		self.SetPosition ( (xpos, ypos) )

		self.Thaw()
	

	def __saveParams (self):
		"""
		Сохранить параметры в конфиг
		"""
		config = Application.config

		try:
			if not self.IsIconized():
				(width, height) = self.GetSizeTuple()
				config.WidthOption.value = width
				config.HeightOption.value = height

				(xpos, ypos) = self.GetPositionTuple()
				config.XPosOption.value = xpos
				config.YPosOption.value = ypos

				self.__savePanesParams()
		except Exception, e:
			wx.MessageBox (_(u"Can't save config\n%s") % (unicode (e)), 
					_(u"Error"), wx.ICON_ERROR | wx.OK)
	

	def __set_properties(self):
		# begin wxGlade: MainWindow.__set_properties
		self.SetTitle(_("OutWiker"))
		_icon = wx.EmptyIcon()
		_icon.CopyFromBitmap(wx.Bitmap(os.path.join (self.imagesDir, "icon.ico"), wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)
		self.SetSize((800, 680))
		self.mainToolbar.Realize()
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: MainWindow.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		mainSizer.Add(self.mainPanel, 1, wx.EXPAND, 0)
		mainSizer.Add(self.statusbar, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		self.Layout()
		# end wxGlade


	def onClose (self, event):
		askBeforeExit = Application.config.askBeforeExitOption.value

		if (not askBeforeExit or 
				wx.MessageBox (_(u"Really exit?"), _(u"Exit"), wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES):
			if Application.wikiroot != None:
				Controller.instance().onWikiClose (Application.wikiroot)

			self.__saveParams()

			self.auiManager.UnInit()
			self.mainPanel.Close()

			self.__removeTrayIcon()

			self.Destroy()
		else:
			event.Veto()
	

	def __removeTrayIcon (self):
		"""
		Удалить иконку из трея
		"""
		if self.taskBarIcon.IsIconInstalled():
			self.taskBarIcon.RemoveIcon()


	def onMainWindowConfigChange (self):
		self.__updateTitle()


	def onTreeUpdate (self, sender):
		"""
		Событие при обновлении дерева
		"""
		Application.wikiroot = sender.root
		self._loadBookmarks()


	def onNew(self, event): # wxGlade: MainWindow.<event_handler>
		dlg = wx.FileDialog (self, style = wx.FD_SAVE)

		if dlg.ShowModal() == wx.ID_OK:
			if Application.wikiroot != None:
				Controller.instance().onWikiClose (Application.wikiroot)

			Application.wikiroot = WikiDocument.create (dlg.GetPath ())
			Application.wikiroot.selectedPage = None
			self.recentWiki.add (Application.wikiroot.path)
			self._loadRecentWiki()

		dlg.Destroy()
		self.__enableGui()


	def onOpen(self, event): # wxGlade: MainWindow.<event_handler>
		wikiroot = core.commands.openWikiWithDialog (self, Application.wikiroot)
		self._openLoadedWiki(wikiroot)
	

	def _openLoadedWiki (self, wikiroot, addToRecent=True):
		"""
		Обновить окно после того как загрузили вики
		"""
		if wikiroot != None:
			Application.wikiroot = wikiroot

			if addToRecent:
				self.recentWiki.add (wikiroot.path)
				self._loadRecentWiki()
			self.__enableGui()


	def onSave(self, event): # wxGlade: MainWindow.<event_handler>
		self.pagePanel.Save()


	def onSaveAs(self, event): # wxGlade: MainWindow.<event_handler>
		print "Event handler `onSaveAs' not implemented"
		event.Skip()
	

	def onReload(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None:
			Controller.instance().onWikiClose (Application.wikiroot)
			Controller.instance().onStartTreeUpdate(Application.wikiroot)

			if (wx.MessageBox (_(u"Save current page before reload?"), 
				_(u"Save?"), 
				wx.YES_NO  | wx.ICON_QUESTION ) == wx.NO):
				self.pagePanel.destroyWithoutSave()
			else:
				self.pagePanel.destroyPageView()
				
			try:
				wikiroot = core.commands.openWiki (Application.wikiroot.path)
			except IOError:
				wx.MessageBox (_(u"Can't load wiki '%s'") % self._recentId[event.Id], _(u"Error"), wx.ICON_ERROR | wx.OK)
				return
			finally:
				Controller.instance().onEndTreeUpdate(Application.wikiroot)

			self._openLoadedWiki (Application.wikiroot)


	def onAddSiblingPage(self, event): # wxGlade: MainWindow.<event_handler>
		"""
		Создание страницы на уровне текущей страницы
		"""
		if Application.wikiroot == None:
			return

		currPage = Application.wikiroot.selectedPage

		if currPage == None or currPage.parent == None:
			parentpage = Application.wikiroot
		else:
			parentpage = currPage.parent

		core.commands.createPageWithDialog (self, parentpage)

	
	def onAddChildPage(self, event): # wxGlade: MainWindow.<event_handler>
		"""
		Создание дочерней страницы
		"""
		if Application.wikiroot == None:
			return

		currPage = Application.wikiroot.selectedPage

		if currPage == None:
			currPage = Application.wikiroot

		core.commands.createPageWithDialog (self, currPage)


	def onAttach(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.attachFilesWithDialog (self, Application.wikiroot.selectedPage)

	def onAbout(self, event): # wxGlade: MainWindow.<event_handler>
		version = core.commands.getCurrentVersion()
		dlg = AboutDialog (version, self)
		dlg.ShowModal()
		dlg.Destroy()


	def onExit(self, event): # wxGlade: MainWindow.<event_handler>
		self.Close()


	def onCopyPath(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.copyPathToClipboard (Application.wikiroot.selectedPage)


	def onCopyAttaches(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.copyAttachPathToClipboard (Application.wikiroot.selectedPage)

	
	def onCopyLink(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.copyLinkToClipboard (Application.wikiroot.selectedPage)

	
	def onCopyTitle(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.copyTitleToClipboard (Application.wikiroot.selectedPage)
	

	def onBookmarksChanged (self, event):
		self._loadBookmarks()


	def onBookmark(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			selectedPage = Application.wikiroot.selectedPage

			if not Application.wikiroot.bookmarks.pageMarked (selectedPage):
				Application.wikiroot.bookmarks.add (Application.wikiroot.selectedPage)
			else:
				Application.wikiroot.bookmarks.remove (Application.wikiroot.selectedPage)


	def onEditPage(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.editPage (self, Application.wikiroot.selectedPage)


	def onRemovePage(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			core.commands.removePage (Application.wikiroot.selectedPage)


	def onGlobalSearch(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None:
			if Application.wikiroot.readonly:
				wx.MessageBox (_(u"Wiki is opened as read-only"), _(u"Error"), wx.ICON_ERROR | wx.OK)
				return
			else:
				try:
					pages.search.searchpage.GlobalSearch.create (Application.wikiroot)
				except IOError:
					wx.MessageBox (_(u"Can't create page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


	def onStdEvent(self, event): # wxGlade: MainWindow.<event_handler>
		if not self.stdEventLoop:
			self.stdEventLoop = True
			target = wx.Window.FindFocus()
			target.ProcessEvent (event)
		self.stdEventLoop = False


	def onRename(self, event): # wxGlade: MainWindow.<event_handler>
		self.tree.beginRename()


	def onHelp(self, event): # wxGlade: MainWindow.<event_handler>
		help_dir = u"help"
		current_help = "help_rus"
		path = os.path.join (core.system.getCurrentDir(), help_dir, current_help)
		self.openWiki (path, readonly=True)


	def onOpenReadOnly(self, event): # wxGlade: MainWindow.<event_handler>
		wikiroot = core.commands.openWikiWithDialog (self, Application.wikiroot, readonly=True)
		self._openLoadedWiki(wikiroot, addToRecent=False)


	def onPreferences(self, event): # wxGlade: MainWindow.<event_handler>
		dlg = PrefDialog (self)

		if dlg.ShowModal() == wx.ID_OK:
			pass

		dlg.Destroy()
	

	def onIconize (self, event):
		if self.IsIconized():
			# Окно свернули
			self.__minimizeWindow ()


	def __restoreWindow (self):
		self.Show ()
		self.Iconize (False)
		self.__removeTrayIcon()


	def __minimizeWindow (self):
		"""
		Свернуть окно
		"""
		if Application.config.minimizeOption.value:
			# В трей добавим иконку, а окно спрячем
			self.taskBarIcon.ShowIcon()
			self.Hide()
		

# end of class MainWindow


class DropFilesTarget (wx.FileDropTarget):
	def __init__ (self, mainWindow):
		wx.FileDropTarget.__init__ (self)
		self._mainWindow = mainWindow
	
	
	def OnDropFiles (self, x, y, files):
		if (Application.wikiroot != None and
				Application.wikiroot.selectedPage != None):
			core.commands.attachFiles (self._mainWindow, 
						Application.wikiroot.selectedPage, 
						files)
			return True
