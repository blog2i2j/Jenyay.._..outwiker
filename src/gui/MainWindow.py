# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Mar 23 21:59:58 2010

import os.path
import sys

import wx

from core.controller import Controller
from core.tree import WikiDocument, RootWikiPage
from WikiTree import WikiTree
from gui.CurrentPagePanel import CurrentPagePanel
import core.commands
from core.recent import RecentWiki
import pages.search.searchpage
import core.system
from gui.preferences.PrefDialog import PrefDialog

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

version = "1.0"

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

		# Секция конфига, где будут храниться все настройки для главного окна
		self._configSection = "MainWindow"

		# Флаг, который отмечает, что пришло первое событие onIdle.
		# Используется для определения момента, когда окно только загрузилось
		self.firstEvent = True

		# Размеры окна по умолчанию
		self.defaultWidth = 800
		self.defaultHeiht = 680

		# Ширина дерева по умолчанию
		self.defaultSash = 200

		Controller.instance().onTreeUpdate += self.onTreeUpdate
		Controller.instance().onPageSelect += self.onPageSelect
		Controller.instance().onBookmarksChanged += self.onBookmarksChanged
		Controller.instance().onMainWindowConfigChange += self.onMainWindowConfigChange
		
		# Ссылка на корень открытой в данный момент вики
		self.wikiroot = None

		# Путь к директории с программой/скриптом
		self.imagesDir = core.system.getImagesDir()

		# begin wxGlade: MainWindow.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER|wx.SP_LIVE_UPDATE)
		self.rightPane = wx.Panel(self.splitter, -1)
		self.leftPane = wx.Panel(self.splitter, -1)
		
		# Menu Bar
		self.mainMenu = wx.MenuBar()
		self.fileMenu = wx.Menu()
		self.fileMenu.Append(self.ID_NEW, "&New\tCtrl+N", "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN, u"&Open…\tCtrl+O", "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN_READONLY, "Open &Read-only...\tCtrl+Shift+O", "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_SAVE, "&Save\tCtrl+S", "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_EXIT, u"&Exit…\tAlt+F4", "", wx.ITEM_NORMAL)
		self.fileMenu.AppendSeparator()
		self.mainMenu.Append(self.fileMenu, "&File")
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_REDO, "&Redo\tCtrl+Y", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(wx.ID_CUT, "Cu&t\tCtrl+X", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_COPY, "&Copy\tCtrl+C", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_PASTE, "&Paste\tCtrl+V", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_PREFERENCES, "Pr&eferences...\tCtrl+F8", "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, "&Edit")
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_ADDPAGE, u"Add &sibling page…\tCtrl+T", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ADDCHILD, u"Add &child Page…\tCtrl+Shift+T", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_RENAME, "Rename page\tF2", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_REMOVE_PAGE, u"Remove page…\tCtrl+Shift+Del", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_EDIT, u"Edit page…\tCtrl+E", "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, "&Tree")
		self.toolsMenu = wx.Menu()
		self.toolsMenu.Append(self.ID_GLOBAL_SEARCH, u"&Global search…\tCtrl+Shift+F", "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_ATTACH, u"&Attach Files…\tCtrl+Alt+A", "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_COPY_TITLE, "Copy page's title to clipboard\tCtrl+Shift+D", "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPYPATH, "Copy &page's path to clipboard\tCtrl+Shift+P", "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_ATTACH_PATH, "Copy a&ttaches path to clipboard\tCtrl+Shift+A", "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_LINK, "Copy page link to clipboard\tCtrl+Shift+L", "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_RELOAD, "Reload wiki\tCtrl+R", "", wx.ITEM_NORMAL)
		self.mainMenu.Append(self.toolsMenu, "T&ools")
		self.bookmarksMenu = wx.Menu()
		self.bookmarksMenu.Append(self.ID_ADDBOOKMARK, "Add/Remove Bookmark\tCtrl+D", "", wx.ITEM_NORMAL)
		self.bookmarksMenu.AppendSeparator()
		self.mainMenu.Append(self.bookmarksMenu, "Bookmarks")
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_HELP, "Help\tF1", "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ABOUT, u"&About…\tCtrl+F1", "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, "&Help")
		self.SetMenuBar(self.mainMenu)
		# Menu Bar end
		
		# Tool Bar
		self.mainToolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE)
		self.SetToolBar(self.mainToolbar)
		self.mainToolbar.AddLabelTool(self.ID_NEW, u"New…", wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Create new wiki…", "")
		self.mainToolbar.AddLabelTool(self.ID_OPEN, u"Open…", wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Open wiki…", "")
		self.mainToolbar.AddLabelTool(self.ID_SAVE, "Save", wx.Bitmap(os.path.join (self.imagesDir, "save.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Save wiki", "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_RELOAD, "Reload", wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Reload wiki", "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_ADDPAGE, u"Add sibling page…", wx.Bitmap(os.path.join (self.imagesDir, "sibling.ico"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Add sibling page…", "")
		self.mainToolbar.AddLabelTool(self.ID_ADDCHILD, u"Add child Page…", wx.Bitmap(os.path.join (self.imagesDir, "child.ico"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Add child Page…", "")
		self.mainToolbar.AddLabelTool(self.ID_REMOVE_PAGE, "Remove page", wx.Bitmap(os.path.join (self.imagesDir, "remove.ico"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Remove page…", "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_ATTACH, u"Attach files…", wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Attach files…", "")
		self.mainToolbar.AddLabelTool(self.ID_EDIT, "Edit page", wx.Bitmap(os.path.join (self.imagesDir, "edit.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Edit page's properties", "")
		self.mainToolbar.AddLabelTool(self.ID_GLOBAL_SEARCH, u"Global search…", wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Global search…", "")
		self.mainToolbar.AddSeparator()
		# Tool Bar end
		self.tree = WikiTree(self.leftPane, -1)
		self.pagePanel = CurrentPagePanel(self.rightPane, -1)
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

		self.__setMenuBitmaps()
		
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.Bind (wx.EVT_ICONIZE, self.onIconize)
		self.Bind (wx.EVT_MENU, self.onRestore, id=self.ID_RESTORE)

		self.Bind (wx.EVT_IDLE, self.onIdle)
		#self._hideElements()

		self._dropTarget = DropFilesTarget (self)

		self.SetDropTarget (self._dropTarget)
		self.__enableGui()
		self. __createTrayIcon()

		self.minPaneSize = 30
		self.splitter.SetMinimumPaneSize (self.minPaneSize)

		self.statusbar.SetFieldsCount(1)
		self.pagePanel.Disable()

		aTable = wx.AcceleratorTable([
			(wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
			(wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
			(wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
		self.SetAcceleratorTable(aTable)
	

	def onPageSelect (self, newpage):
		self.__updateTitle()
	

	def __updateTitle (self):
		try:
			template =  wx.GetApp().getConfig().get (u"MainWindow", u"Title")
		except:
			template = u"{file} - OutWiker"

		if self.wikiroot == None:
			self.SetTitle (u"OutWiker")
			return

		pageTitle = u"" if self.wikiroot.selectedPage == None else self.wikiroot.selectedPage.title
		filename = os.path.basename (self.wikiroot.path)

		result = template.replace ("{file}", filename).replace ("{page}", pageTitle)
		self.SetTitle (result)
	

	def onRestore (self, event):
		self.__restoreWindow()
	

	def __createTrayMenu (self, taskBarIcon):
		self.trayMenu = wx.Menu()
		self.trayMenu.Append (self.ID_RESTORE, u"Restore")
		self.trayMenu.Append (self.ID_EXIT, u"Exit")

		self.taskBarIcon.Bind(wx.EVT_MENU, self.onRestore, id=self.ID_RESTORE)
		self.taskBarIcon.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)


	def __createTrayIcon (self):
		self.icon = wx.EmptyIcon()
		self.icon.CopyFromBitmap(wx.Bitmap(os.path.join (self.imagesDir, "outwiker_16.png"), wx.BITMAP_TYPE_ANY))

		self.taskBarIcon = wx.TaskBarIcon()
		self.taskBarIcon.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.OnTrayLeftClick)
		self.taskBarIcon.Bind (wx.EVT_TASKBAR_RIGHT_DOWN, self.OnTrayRightClick)

		self.__createTrayMenu(self.taskBarIcon)


	def OnTrayLeftClick (self, event):
		self.__restoreWindow()


	def OnTrayRightClick (self, event):
		self.taskBarIcon.PopupMenu (self.trayMenu)
	

	def __enableGui (self):
		"""
		Проверить открыта ли вики и включить или выключить кнопки на панели
		"""
		enabled = self.wikiroot != None
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
		try:
			openRecent = wx.GetApp().getConfig().getbool (u"RecentWiki", u"AutoOpen")
		except:
			return

		if openRecent and len (self.recentWiki) > 0:
			self.openWiki (self.recentWiki[0])


	def __iconizeAfterStart (self):
		"""
		Свернуться при запуске, если установлена соответствующая опция
		"""
		try:
			iconize = wx.GetApp().getConfig().getbool (u"General", u"StartIconized")
		except:
			return

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
			wx.MessageBox (u"Can't load wiki '%s'" % self._recentId[event.Id], u"Error", wx.ICON_ERROR | wx.OK)
			return

		self._openLoadedWiki(wikiroot)

	
	def _loadRecentWiki (self):
		self._removeMenuItemsById (self.fileMenu, self._recentId.keys())
		self._recentId = {}

		self.recentWiki = RecentWiki (wx.GetApp().getConfig())

		self._recentId = {}

		for n in range (len (self.recentWiki)):
			id = wx.NewId()
			path = self.recentWiki[n]
			self._recentId[id] = path

			self.fileMenu.Append (id, path, "", wx.ITEM_NORMAL)
			
			self.Bind(wx.EVT_MENU, self.onRecent, id=id)
	

	def _loadBookmarks (self):
		self._removeMenuItemsById (self.bookmarksMenu, self._bookmarksId.keys())
		self._bookmarksId = {}

		if self.wikiroot != None:
			for n in range (len (self.wikiroot.bookmarks)):
				id = wx.NewId()
				page = self.wikiroot.bookmarks[n]
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
		Controller.instance().onStartTreeUpdate(self.wikiroot)
		
		try:
			if self.wikiroot != None:
				Controller.instance().onWikiClose (self.wikiroot)
			
			wikiroot = core.commands.openWiki (path, readonly)
			self._openLoadedWiki(wikiroot)
		except IOError:
			wx.MessageBox (u"Can't load wiki '%s'" % path, u"Error", wx.ICON_ERROR | wx.OK)

		finally:
			Controller.instance().onEndTreeUpdate(self.wikiroot)


	
	def onSelectBookmark (self, event):
		subpath = self._bookmarksId[event.Id]
		page = self.wikiroot[subpath]

		if page != None:
			self.wikiroot.selectedPage = self.wikiroot[subpath]
	

	def _loadParams(self):
		"""
		Загрузить параметры из конфига
		"""
		config = wx.GetApp().getConfig()
		self._showElements()
		
		try:
			width = config.getint (self._configSection, "width")
			height = config.getint (self._configSection, "height")

			xpos = config.getint (self._configSection, "xpos")
			ypos = config.getint (self._configSection, "ypos")
		except Exception as e:
			width = self.defaultWidth
			height = self.defaultHeiht
			(dx, dy) = wx.GetDisplaySize()

			# Чтобы окно умещалось на экране
			if dx < width:
				width = dx

			if dy < height:
				height = dy

			# Координаты окна
			xpos = (dx - width) / 2
			ypos = (dy - height) / 2
		
		self.SetSize ( (width, height) )
		self.SetPosition ( (xpos, ypos) )
		self.__loadSashPosition()
	

	def __loadSashPosition (self):
		try:
			sash = wx.GetApp().getConfig().getint (self._configSection, "sash")
		except:
			sash = self.defaultSash

		self.splitter.SetSashPosition (sash)

	
	def _saveParams (self):
		"""
		Сохранить параметры в конфиг
		"""
		config = wx.GetApp().getConfig()

		try:
			if not self.IsIconized():
				(width, height) = self.GetSizeTuple()
				config.set (self._configSection, "width", width)
				config.set (self._configSection, "height", height)

				(xpos, ypos) = self.GetPositionTuple()
				config.set (self._configSection, "xpos", xpos)
				config.set (self._configSection, "ypos", ypos)

			self.__saveSashPosition()
		except Exception as e:
			wx.MessageBox (u"Can't save config\n" + unicode (e), u"Error", wx.ICON_ERROR | wx.OK)
	

	def __saveSashPosition(self):
		"""
		Сохранить положение перетаскиваемой линии между деревом и заметкой
		"""
		wx.GetApp().getConfig().set (self._configSection, "sash", self.splitter.GetSashPosition())

	
	def _hideElements (self):
		pass
		self.tree.Hide()
		self.pagePanel.Hide()

	def _showElements (self):
		self.tree.Show()
		self.pagePanel.Show()


	def __set_properties(self):
		# begin wxGlade: MainWindow.__set_properties
		self.SetTitle("OutWiker")
		_icon = wx.EmptyIcon()
		_icon.CopyFromBitmap(wx.Bitmap(os.path.join (self.imagesDir, "icon.ico"), wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)
		self.SetSize((800, 680))
		self.mainToolbar.Realize()
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: MainWindow.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		rightSizer = wx.FlexGridSizer(1, 1, 0, 0)
		treeSizer = wx.FlexGridSizer(1, 1, 0, 0)
		treeSizer.Add(self.tree, 1, wx.EXPAND|wx.FIXED_MINSIZE, 0)
		self.leftPane.SetSizer(treeSizer)
		treeSizer.AddGrowableRow(0)
		treeSizer.AddGrowableCol(0)
		rightSizer.Add(self.pagePanel, 1, wx.EXPAND, 0)
		self.rightPane.SetSizer(rightSizer)
		rightSizer.AddGrowableRow(0)
		rightSizer.AddGrowableCol(0)
		self.splitter.SplitVertically(self.leftPane, self.rightPane, 181)
		mainSizer.Add(self.splitter, 1, wx.EXPAND, 0)
		mainSizer.Add(self.statusbar, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		self.Layout()
		# end wxGlade


	def onClose (self, event):
		try:
			askBeforeExit = wx.GetApp().getConfig().getbool (u"General", u"AskBeforeExit")
		except:
			askBeforeExit = True

		if (not askBeforeExit or 
				wx.MessageBox (u"Really exit?", u"Exit", wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES):
			if self.wikiroot != None:
				Controller.instance().onWikiClose (self.wikiroot)
			self._saveParams()
			self.pagePanel.Close()

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
		self.wikiroot = sender.root
		self._loadBookmarks()

		if self.wikiroot == None:
			self._hideElements()
		else:
			self._showElements()


	def onNew(self, event): # wxGlade: MainWindow.<event_handler>
		dlg = wx.FileDialog (self, style = wx.FD_SAVE)

		if dlg.ShowModal() == wx.ID_OK:
			if self.wikiroot != None:
				Controller.instance().onWikiClose (self.wikiroot)

			self.wikiroot = WikiDocument.create (dlg.GetPath ())
			self.wikiroot.selectedPage = None
			self.recentWiki.add (self.wikiroot.path)
			self._loadRecentWiki()

		dlg.Destroy()
		self.__enableGui()


	def onOpen(self, event): # wxGlade: MainWindow.<event_handler>
		wikiroot = core.commands.openWikiWithDialog (self, self.wikiroot)
		self._openLoadedWiki(wikiroot)
	

	def _openLoadedWiki (self, wikiroot):
		"""
		Обновить окно после того как загрузили вики
		"""
		if wikiroot != None:
			self.wikiroot = wikiroot
			self.recentWiki.add (wikiroot.path)
			self._loadRecentWiki()
			self.__enableGui()


	def onSave(self, event): # wxGlade: MainWindow.<event_handler>
		self.pagePanel.Save()


	def onSaveAs(self, event): # wxGlade: MainWindow.<event_handler>
		print "Event handler `onSaveAs' not implemented"
		event.Skip()
	

	def onReload(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None:
			Controller.instance().onWikiClose (self.wikiroot)
			Controller.instance().onStartTreeUpdate(self.wikiroot)

			if (wx.MessageBox (u"Save current page before reload?", 
				u"Save?", 
				wx.YES_NO  | wx.ICON_QUESTION ) == wx.NO):
				self.pagePanel.destroyWithoutSave()
			else:
				self.pagePanel.destroyPageView()
				
			try:
				wikiroot = core.commands.openWiki (self.wikiroot.path)
			except IOError:
				wx.MessageBox (u"Can't load wiki '%s'" % self._recentId[event.Id], u"Error", wx.ICON_ERROR | wx.OK)
				return
			finally:
				Controller.instance().onEndTreeUpdate(self.wikiroot)

			self._openLoadedWiki (self.wikiroot)


	def onAddSiblingPage(self, event): # wxGlade: MainWindow.<event_handler>
		"""
		Создание страницы на уровне текущей страницы
		"""
		if self.wikiroot == None:
			return

		currPage = self.tree.selectedPage

		if currPage == None or currPage.parent == None:
			parentpage = self.wikiroot
		else:
			parentpage = currPage.parent

		core.commands.createPageWithDialog (self, parentpage)

	
	def onAddChildPage(self, event): # wxGlade: MainWindow.<event_handler>
		"""
		Создание дочерней страницы
		"""
		if self.wikiroot == None:
			return

		currPage = self.tree.selectedPage
		if currPage == None:
			currPage = self.wikiroot

		core.commands.createPageWithDialog (self, currPage)


	def onAttach(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.attachFilesWithDialog (self, self.wikiroot.selectedPage)

	def onAbout(self, event): # wxGlade: MainWindow.<event_handler>
		info = wx.AboutDialogInfo()
		info.AddDeveloper (u"Ilin E.V. (aka Jenyay)")
		info.SetCopyright (u"(c) 2010 Ilin E.V. (aka Jenyay)")
		info.SetName (u"OutWiker")
		info.SetDescription (u"Outliner + personal wiki = OutWiker")

		# Version:
		info.SetVersion (version)
		info.SetWebSite ("http://jenyay.net")
		#icon = wx.Icon(os.path.join (os.path.dirname(sys.argv[0]),
		#								os.path.join (self.imagesDir, "texgui.ico")), wx.BITMAP_TYPE_ICO)
		#info.SetIcon (icon)
		
		wx.AboutBox(info)

	def onExit(self, event): # wxGlade: MainWindow.<event_handler>
		self.Close()


	def onCopyPath(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.copyPathToClipboard (self.wikiroot.selectedPage)


	def onCopyAttaches(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.copyAttachPathToClipboard (self.wikiroot.selectedPage)

	
	def onCopyLink(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.copyLinkToClipboard (self.wikiroot.selectedPage)

	
	def onCopyTitle(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.copyTitleToClipboard (self.wikiroot.selectedPage)
	

	def onBookmarksChanged (self, event):
		self._loadBookmarks()


	def onBookmark(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			selectedPage = self.wikiroot.selectedPage

			if not self.wikiroot.bookmarks.pageMarked (selectedPage):
				self.wikiroot.bookmarks.add (self.wikiroot.selectedPage)
			else:
				self.wikiroot.bookmarks.remove (self.wikiroot.selectedPage)


	def onEditPage(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.editPage (self, self.wikiroot.selectedPage)


	def onRemovePage(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None and self.wikiroot.selectedPage != None:
			core.commands.removePage (self.wikiroot.selectedPage)


	def onGlobalSearch(self, event): # wxGlade: MainWindow.<event_handler>
		if self.wikiroot != None:
			if self.wikiroot.readonly:
				wx.MessageBox (u"Wiki is opened as read-only", u"Error", wx.ICON_ERROR | wx.OK)
				return
			else:
				try:
					pages.search.searchpage.GlobalSearch.create (self.wikiroot)
				except IOError:
					wx.MessageBox (u"Can't create page", u"Error", wx.ICON_ERROR | wx.OK)


	def onStdEvent(self, event): # wxGlade: MainWindow.<event_handler>
		if not self.stdEventLoop:
			self.stdEventLoop = True
			target = wx.Window.FindFocus()
			#print target
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
		wikiroot = core.commands.openWikiWithDialog (self, self.wikiroot, readonly=True)
		self._openLoadedWiki(wikiroot)


	def onPreferences(self, event): # wxGlade: MainWindow.<event_handler>
		dlg = PrefDialog (self)

		if dlg.ShowModal() == wx.ID_OK:
			pass

		dlg.Destroy()
	

	def onIconize (self, event):
		if self.IsIconized():
			# Окно свернули
			self.__minimizeWindow ()

			try:
				self.__saveSashPosition()
			except Exception as e:
				wx.MessageBox (u"Can't save config\n" + unicode (e), u"Error", wx.ICON_ERROR | wx.OK)


	def __restoreWindow (self):
		self.Show ()
		self.Iconize (False)
		self.__removeTrayIcon()
		self.__loadSashPosition()


	def __minimizeWindow (self):
		"""
		Свернуть окно
		"""
		try:
			minimize = wx.GetApp().config.getbool (u"General", u"MinimizeToTray")
		except:
			return

		if minimize:
			# В трей добавим иконку, а окно спрячем
			self.taskBarIcon.SetIcon(self.icon)
			self.Hide()
		

# end of class MainWindow


class DropFilesTarget (wx.FileDropTarget):
	def __init__ (self, mainWindow):
		wx.FileDropTarget.__init__ (self)
		self._mainWindow = mainWindow
	
	
	def OnDropFiles (self, x, y, files):
		if (self._mainWindow.wikiroot != None and
				self._mainWindow.wikiroot.selectedPage != None):
			core.commands.attachFiles (self._mainWindow, 
						self._mainWindow.wikiroot.selectedPage, 
						files)
			return True
