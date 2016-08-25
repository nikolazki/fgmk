
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from fgmk import base_model, current_project, fifl, actions_wdgt

item_categories=['none','consumable','collectible','weapon','armor']
default_equipable = False
default_unique = False
default_reusable = False
default_usable = False
default_effect = None
default_statMod = None
default_description = ''
default_icon = None
default_category = None
default_action = None

class base_item:
    def __init__(self,name, equipable=default_equipable,
                            unique=default_unique,
                            reusable=default_reusable,
                            usable=default_usable,
                            effect=default_effect,
                            statMod=default_statMod,
                            description=default_description,
                            icon=default_icon,
                            category=default_category,
                            action=default_action,
                            jsonTree=None):
        normalized_name = str(name)
        normalized_name = normalized_name.title()
        normalized_name = normalized_name.replace(" ", "")

        self.name = name
        self.equipable = equipable
        self.unique = unique
        self.reusable = reusable
        self.usable = usable
        self.effect = effect
        self.statMod = statMod
        self.description = description
        self.icon = icon
        self.category = category
        self.action = action
        if(jsonTree!=None):
            self.loadjsontree(jsonTree)

    def setname(self,name):
        self.name = name

    def setequipable(self, equipable=True):
        self.equipable = equipable

    def setunique(self, unique=True):
        self.unique = unique

    def setreusable(self, reusable=True):
        self.reusable = reusable

    def setusable(self,usable=True):
        self.usable = usable

    def seteffect(self,effect=default_effect):
        self.effect = effect

    def setstatmod(self,statMod=default_statMod):
        self.statMod = statMod

    def setdescription(self, description=default_description):
        self.description = description

    def seticon(self, icon=default_icon):
        self.icon = icon

    def setcategory(self, category=default_category):
        self.category = category

    def setaction(self,action=default_action):
        self.action = action

    def getnormalname(self):
        normalized_name = str(self.name)
        normalized_name = normalized_name.replace(" ", "")
        return normalized_name

    def new(self):
        self.equipable=default_equipable
        self.unique=default_unique
        self.reusable=default_reusable
        self.usable=default_usable
        self.effect=default_effect
        self.statMod=default_statMod
        self.description=default_description
        self.icon=default_icon
        self.category=default_category
        self.action=default_action

    def loadjsontree(self,jsonTree):
        self.new()
        if('name' in jsonTree):
            self.name = jsonTree['name']
        if('equipable' in jsonTree):
            self.equipable = jsonTree['equipable']
        if('usable' in jsonTree):
            self.usable = jsonTree['usable']
        if('unique' in jsonTree):
            self.unique = jsonTree['unique']
        if('reusable' in jsonTree):
            self.reusable = jsonTree['reusable']
        if('effect' in jsonTree):
            self.effect = jsonTree['effect']
        if('statMod' in jsonTree):
            self.statMod = jsonTree['statMod']
        if('description' in jsonTree):
            self.description = jsonTree['description']
        if('icon' in jsonTree):
            self.icon = jsonTree['icon']
        if('category' in jsonTree):
            self.category = jsonTree['category']
        if('action' in jsonTree):
            self.action = jsonTree['action']

    def getjsontree(self):
        jsonTree = {}
        jsonTree['name'] = self.name
        if(self.equipable):
            jsonTree['equipable'] = True
        if(self.usable):
            jsonTree['usable'] = True
        if(self.unique):
            jsonTree['unique'] = True
        if(self.reusable):
            jsonTree['reusable'] = True
        if(self.effect != None):
            jsonTree['effect'] = self.effect
        if(self.statMod != None):
            jsonTree['statMod'] = self.statMod
        if(self.description != False or self.description != ''):
            jsonTree['description'] = self.description
        if(self.icon != None):
            jsonTree['icon'] = self.icon
        if(self.category != None):
            jsonTree['category'] = self.category
        if(self.action != None):
            jsonTree['action'] = self.action

        return jsonTree


class ItemsFormat(base_model.BaseFormat):
    def __init__(self,filename=''):
        base_model.BaseFormat.__init__(self)
        if(filename==''):
            self.filename = os.path.join(current_project.settings['gamefolder'],fifl.ITEMSFILE)
        else:
            self.filename = filename
        self.new()

    def new(self):
        self.jsonTree = {"Items":{}}

    def additem(self, item):
        newitem=False
        if(not item.getnormalname() in self.jsonTree['Items']):
            newitem=True

        self.jsonTree['Items'][item.getnormalname()] = item.getjsontree()
        return newitem

    def removebyname(self, name):
        it = base_item(name)
        del self.jsonTree['Items'][it.getnormalname()]
        return self.jsonTree

    def getitems(self):
        return self.jsonTree['Items']

    def getitem(self,item):
        tempjson = self.jsonTree['Items'][item]
        if not 'name' in tempjson:
            tempjson['name']=item

        return tempjson

    def getitemsname(self):
        return sorted(self.jsonTree['Items'])

class StatModWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)
        #elements
        titleLabel = QtWidgets.QLabel('stat modification')
        self.clearButton = QtWidgets.QPushButton('clear all',self)
        self.stSpinbox = QtWidgets.QSpinBox(self)
        self.dxSpinbox = QtWidgets.QSpinBox(self)
        self.iqSpinbox = QtWidgets.QSpinBox(self)
        stLabel = QtWidgets.QLabel('st')
        dxLabel = QtWidgets.QLabel('dx')
        iqLabel = QtWidgets.QLabel('iq')

        #logic
        self.clearButton.clicked.connect(self.clearAll)
        self.stSpinbox.setToolTip('How much the item will modify strenght.')
        self.stSpinbox.setMinimum(-250)
        self.stSpinbox.setMaximum(250)
        self.stSpinbox.setSingleStep(1)
        self.dxSpinbox.setToolTip('How much the item will modify dexterity.')
        self.dxSpinbox.setMinimum(-250)
        self.dxSpinbox.setMaximum(250)
        self.dxSpinbox.setSingleStep(1)
        self.iqSpinbox.setToolTip('How much the item will modify intelligence.')
        self.iqSpinbox.setMinimum(-250)
        self.iqSpinbox.setMaximum(250)
        self.iqSpinbox.setSingleStep(1)

        #layout and appearance
        titleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        stLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        dxLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        iqLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        VBox = QtWidgets.QVBoxLayout(self)
        statsHBox = QtWidgets.QHBoxLayout()
        statsHBox.addWidget(stLabel)
        statsHBox.addWidget(self.stSpinbox)
        statsHBox.addWidget(dxLabel)
        statsHBox.addWidget(self.dxSpinbox)
        statsHBox.addWidget(iqLabel)
        statsHBox.addWidget(self.iqSpinbox)
        titleHBox = QtWidgets.QHBoxLayout()
        titleHBox.addWidget(titleLabel)
        titleHBox.addWidget(self.clearButton)
        VBox.addLayout(titleHBox)
        VBox.addLayout(statsHBox)

    def clearAll(self):
        self.stSpinbox.setValue(0)
        self.dxSpinbox.setValue(0)
        self.iqSpinbox.setValue(0)

    def setValue(self,stat={'st':0,'dx':0,'iq':0}):
        if stat == default_statMod:
            self.clearAll()
            return

        if 'st' in stat:
            self.stSpinbox.setValue(stat['st'])
        else:
            self.stSpinbox.setValue(0)

        if 'dx' in stat:
            self.dxSpinbox.setValue(stat['dx'])
        else:
            self.dxSpinbox.setValue(0)

        if 'iq' in stat:
            self.iqSpinbox.setValue(stat['iq'])
        else:
            self.iqSpinbox.setValue(0)

    def getValue(self):
        stat = {}
        st = self.stSpinbox.value()
        dx = self.dxSpinbox.value()
        iq = self.iqSpinbox.value()
        if st != 0:
            stat['st']=st
        if dx != 0:
            stat['dx']=st
        if iq != 0:
            stat['iq']=iq

        if('st' in stat or 'dx' in stat or 'iq' in stat):
            return stat
        else:
            return default_statMod


class ItemCfgWidget(QtWidgets.QWidget):
    def __init__(self, itemd=None, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, **kwargs)

        self.parent = parent
        if(itemd==None):
            self.itemd = base_item('')
        else:
            self.itemd = itemd

        VBox = QtWidgets.QVBoxLayout(self)

        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setMaxLength(22)
        self.radioEquipable = QtWidgets.QRadioButton('equipable',self)
        self.radioUsable = QtWidgets.QRadioButton('usable', self)
        self.radioNone = QtWidgets.QRadioButton('none', self)
        self.checkboxUnique =  QtWidgets.QCheckBox('unique', self)
        self.checkboxReusable =  QtWidgets.QCheckBox('reusable', self)
        self.descriptionLineEdit = QtWidgets.QLineEdit(self)
        self.comboboxCategory = QtWidgets.QComboBox(self)

        self.statModWidget = StatModWidget(self)
        self.actionWidget = actions_wdgt.tinyActionsWdgt(self,current_project.settings,True,True)

        self.actionWidget.setEnabled(False)
        self.statModWidget.setEnabled(False)
        self.checkboxReusable.setEnabled(False)

        self.radioUsable.toggled.connect(self.radioUsableChanged)
        self.radioEquipable.toggled.connect(self.radioEquipableChanged)

        for i in range(len(item_categories)):
            category = item_categories[i]
            self.comboboxCategory.insertItem(i,category)

        self.loadItem()

        VBox.addWidget(QtWidgets.QLabel('Item name:'))
        VBox.addWidget(self.nameLineEdit)
        VBox.addWidget(QtWidgets.QLabel('Item properties:'))
        VBox.addWidget(self.radioEquipable)
        VBox.addWidget(self.radioUsable)
        VBox.addWidget(self.radioNone)
        VBox.addWidget(self.checkboxUnique)
        VBox.addWidget(self.checkboxReusable)
        VBox.addWidget(QtWidgets.QLabel('Item description:'))
        VBox.addWidget(self.descriptionLineEdit)
        VBox.addWidget(QtWidgets.QLabel('Item category:'))
        VBox.addWidget(self.comboboxCategory)
        VBox.addWidget(self.statModWidget)
        VBox.addWidget(self.actionWidget)

    def radioUsableChanged(self,abool):
        self.actionWidget.setEnabled(abool)
        self.checkboxReusable.setEnabled(abool)

    def radioEquipableChanged(self,abool):
        self.statModWidget.setEnabled(abool)

    def newItem(self):
        self.itemd = base_item('')
        self.loadItem()

    def loadItem(self,item=None):
        if(item!=None):
            self.itemd = item

        self.nameLineEdit.setText(self.itemd.name)
        self.descriptionLineEdit.setText(self.itemd.description)
        self.radioNone.setChecked(True)
        if(self.itemd.equipable != default_equipable):
            self.radioEquipable.setChecked(True)

        if(self.itemd.usable != default_usable):
            self.radioUsable.setChecked(True)
        if(self.itemd.unique != default_unique):
            self.checkboxUnique.setChecked(True)
        else:
            self.checkboxUnique.setChecked(False)

        if(self.itemd.reusable != default_reusable):
            self.checkboxReusable.setChecked(True)
        else:
            self.checkboxReusable.setChecked(False)

        self.comboboxCategory.setCurrentIndex(0)
        if(self.itemd.category != default_category):
            category_index = item_categories.index(self.itemd.category)
            self.comboboxCategory.setCurrentIndex(category_index)

        if(self.itemd.action != default_action):
            self.actionWidget.setList(self.itemd.action)
        else:
            self.actionWidget.setList([])

        if(self.itemd.statMod != default_statMod):
            self.statModWidget.setValue(self.itemd.statMod)
        else:
            self.statModWidget.setValue(default_statMod)

    def getItem(self,item=None):
        if(item!=None):
            self.itemd = item

        self.itemd.setname(self.nameLineEdit.text())
        self.itemd.setdescription(self.descriptionLineEdit.text())

        if(self.statModWidget.getValue() == default_statMod):
            self.itemd.setstatmod()
        else:
            self.itemd.setstatmod(self.statModWidget.getValue())

        if(self.actionWidget.getValue() == []):
            self.itemd.setaction()
        else:
            self.itemd.setaction(self.actionWidget.getValue())

        if(self.checkboxReusable.isChecked()):
            self.itemd.setreusable(True)
        else:
            self.itemd.setreusable(False)

        if(self.radioEquipable.isChecked()):
            self.itemd.setequipable(True)
            self.itemd.setaction()
            self.itemd.seteffect()
            self.itemd.setreusable(False)
        else:
            self.itemd.setequipable(False)

        if(self.radioUsable.isChecked()):
            self.itemd.setusable(True)
            self.itemd.setstatmod()
        else:
            self.itemd.setusable(False)

        if(self.checkboxUnique.isChecked()):
            self.itemd.setunique(True)
        else:
            self.itemd.setunique(False)


        if(self.comboboxCategory.currentIndex()!=0):
            self.itemd.setcategory(self.comboboxCategory.currentText())
        else:
            self.itemd.setcategory()

        return self.itemd

class ItemsList(QtWidgets.QWidget):
    currentItemChanged = QtCore.pyqtSignal(base_item, 'QString')
    def __init__(self,itemsfname=None, parent=None, ssettings={}, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.itemf = ItemsFormat()
        self.itemsList = QtWidgets.QListWidget(self)
        self.itemsList.currentItemChanged.connect(self.currentChanged)

        self.load(itemsfname)
        VBox = QtWidgets.QVBoxLayout(self)
        VBox.addWidget(self.itemsList)
        self.setLayout(VBox)

    def getFileName(self):
        return self.itemf.filename

    def new(self):
        self.itemf.new()
        self.load()

    def load(self,itemsfname=None):
        self.itemsList.clear()
        if(itemsfname != None):
            self.itemf.load(itemsfname)

        items = self.itemf.getitemsname()
        for i in range(len(items)):
            item = items[i]
            self.itemsList.addItem(item)

    def newItem(self):
        item = base_item('newItem')
        needsrefresh = self.itemf.additem(item)
        if(needsrefresh):
            self.load()

        items = self.itemf.getitemsname()
        for i in range(len(items)):
            itemname = items[i]
            if(itemname=='newItem'):
                self.itemsList.setCurrentRow(i)
                return

    def saveItem(self,item):
        needsrefresh = self.itemf.additem(item)
        if(needsrefresh):
            self.load()

    def removeByName(self,itemname):
        self.itemf.removebyname(itemname)
        self.load()

    def save(self,filename=None):
        if(filename!=None):
            self.itemf.save(filename)
        else:
            self.itemf.save()

    def currentItem(self):
        listitem = self.itemsList.currentItem()
        if(listitem != None):
            return listitem.text()
        else:
            return None

    def getCurrentItemDescriptor(self):
        itemname = self.currentItem()
        if(itemname!=None):
            itemjson = self.itemf.getitem(itemname)
            item = base_item(itemname,jsonTree=itemjson)
            return item

    def currentChanged(self,current,previous):
        if(current == previous):
            return

        previousname = ''
        if(previous != None):
            previousname = previous.text()

        if(current != None):
            itemname = current.text()
            itemjson = self.itemf.getitem(itemname)
            item = base_item(itemname,jsonTree=itemjson)
            self.currentItemChanged.emit(item,previousname)

class itemsEditorWidget(QtWidgets.QDialog):
    def __init__(self,itemsfname=None, parent=None, ssettings={}, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, **kwargs)

        self.itemsList = ItemsList(itemsfname)
        self.itemsList.currentItemChanged.connect(self.itemChanged)
        self.itemCfg = ItemCfgWidget()

        LVBox = QtWidgets.QVBoxLayout()
        if(parent==None):
            self.toolbarMain = QtWidgets.QToolBar()
            self.toolbarMain.addAction("new\nitems.json",self.newItems)
            self.toolbarMain.addAction("open\nitems.json", self.openItems)
            self.toolbarMain.addAction("save\nitems.json", self.saveItems)
            LVBox.addWidget(self.toolbarMain)

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.addAction("+new",self.newItem)
        self.toolbar.addAction("-delete", self.deleteItem)
        self.toolbar.addAction("save", self.saveCurrentItem)
        self.toolbar.addAction("reload", self.reloadCurrentItem)
        LVBox.addWidget(self.toolbar)

        LVBox.addWidget(self.itemsList)

        HBox = QtWidgets.QHBoxLayout(self)
        HBox.addLayout(LVBox)
        HBox.addWidget(self.itemCfg)

    def newItem(self):
        self.itemsList.newItem()

    def deleteItem(self):
        itemname = self.itemsList.currentItem()
        if(itemname != None):
            self.itemsList.removeByName(itemname)

    def saveCurrentItem(self):
        itemname = self.itemsList.currentItem()
        item = self.itemCfg.getItem()
        if(item.name == itemname):
            self.itemsList.saveItem(item)
        else:
            self.itemsList.removeByName(itemname)
            self.itemsList.saveItem(item)

    def reloadCurrentItem(self):
        currentItem = self.itemsList.getCurrentItemDescriptor()
        self.itemCfg.loadItem(currentItem)

    def saveNewItem(self):
        item = self.itemCfg.getItem()
        self.itemsList.saveItem(item)

    def itemChanged(self,currentItem,previousName):
        if(previousName!=None and previousName != ''):
            item = self.itemCfg.getItem()
            if(item.name == previousName):
                self.itemsList.saveItem(item)
            else:
                self.itemsList.removeByName(previousName)
                self.itemsList.saveItem(item)

        if(currentItem!=None):
            self.itemCfg.loadItem(currentItem)
            self.itemCfg.setEnabled(True)
        else:
            self.itemCfg.setEnabled(False)

    def newItems(self):
        self.itemsList.new()

    def openItems(self):
        folder_to_open_to=''
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.DESCRIPTORS)

        filename = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        folder_to_open_to,
                        "JSON Items (items.json);;All Files (*)")[0]
        if(filename!=''):
            self.itemsList.load(filename)

    def saveItems(self,filename=''):
        if(filename==''):
            filename = self.itemsList.getFileName()

        print(os.path.dirname(filename))
        if os.path.exists(os.path.dirname(filename)):
            self.saveCurrentItem()
            self.itemsList.save(filename)
        else:
            self.saveItemsAs()

    def saveItemsAs(self):
        if(current_project.settings['gamefolder'] == ''):
            folder_to_open_to = os.path.expanduser('~')
        else:
            folder_to_open_to = os.path.join(current_project.settings['gamefolder'], fifl.DESCRIPTORS)

        filename, extension = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save File', folder_to_open_to, 'JSON Items (items.json)')

        if filename != "":
            if filename[-10:] != 'items.json':
                filename = os.path.join(os.path.dirname(filename),'items.json')

            self.saveItems(filename)


def main(filelist=None):
    filetoopen=None

    if (isinstance(filelist, str)):
        if ("items.json" in filelist):
            filetoopen = filelist

    else:
        matching = [s for s in filelist if "items.json" in s]
        if len(matching) > 0:
            filetoopen = matching[0]

    if(filetoopen==None):
        return itemsEditorWidget()
    else:
        current_project.settings['gamefolder'] = os.path.join(os.path.dirname(filetoopen),'../')
        return itemsEditorWidget(itemsfname=filetoopen)

if __name__ == "__main__":
    from sys import argv, exit

    a = QtWidgets.QApplication(argv)
    m = main(argv)
    a.processEvents()
    m.show()
    m.raise_()
    exit(a.exec_())