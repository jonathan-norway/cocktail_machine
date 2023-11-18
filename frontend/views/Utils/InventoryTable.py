
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt6.QtWidgets import QTableView, QStyledItemDelegate, QWidget, QMessageBox, QVBoxLayout, QHeaderView, QAbstractItemView
from backend.cocktail_machine import CocktailMachine
from backend.datatypes import ExternalIngredient, ValidIngredientUnits
from typing import List
from dataclasses import fields

COLUMNS_TO_SHOW = [
    "AMOUNT",
    "NAME",
    "Date Added",
    "Update"
]


class TableModel(QAbstractTableModel):
    def __init__(self, data: List[ExternalIngredient]):
        super(TableModel, self).__init__()
        self._data = data
        self.headers = {
            0: "Name",
            1: "Amount",
            2: "Unit",
            3: "Date Added",
            4: ""
        }
        self._data.insert(0, ExternalIngredient())

    def data(self, index, role):
        item = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            if index.column() == 0:
                return item.name
            if index.column() == 1:
                if item.amount == 0:
                    return ""
                return item.amount
            if index.column() == 2:
                return item.unit
            if index.column() == 3:
                return item.date_added
            return ""

        if role == Qt.ItemDataRole.BackgroundRole:
            if item.unit != "mL" or index.row() == 0:
                return QColor("#EFEFEFEF")
            return

        if role == Qt.ItemDataRole.FontRole:
            font = QFont()
            font.setPointSize(16)
            return font

    def setData(self, index, value, role):
        edited_item = self._data[index.row()]
        if index.column() == 0:
            edited_item.name = value
        elif index.column() == 1:
            edited_item.amount = value
        elif index.column() == 2:
            try:
                validated_unit = ValidIngredientUnits(value)
                edited_item.unit = validated_unit.value
            except Exception as e:
                print(e)
                QMessageBox.warning(None, "Invalid Unit", "Please enter 'mL' or 'pcs'")
        if index.row() != 0:
            CocktailMachine.update_ingredient(edited_item)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        flags = super().flags(index)
        if index.column() != 3:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]

    def sort(self, column, order):
        if column == 4:
            return
        self.layoutAboutToBeChanged.emit()
        self._data.sort(
            key=lambda ingredient: getattr(
                ingredient,
                "_".join(self.headers[column].lower().split(" "))),
            reverse=order == Qt.SortOrder.DescendingOrder)
        self.layoutChanged.emit()

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(fields(self._data[0])) + 1

    def get_item_at_row(self, row: int) -> ExternalIngredient:
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def update_data(self, new_data: List[ExternalIngredient]) -> None:
        self.beginResetModel()
        self._data = [ExternalIngredient(), *new_data]
        self.endResetModel()


class InventoryTable(QWidget):
    def __init__(self):
        super(InventoryTable, self).__init__()

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.SortOrder.DescendingOrder)
        data = CocktailMachine.get_ingredients()

        self.model = TableModel(data)
        self.table.setModel(self.model)

        button_delegate = ButtonDelegate(self)
        button_delegate.removeIngredient.connect(self._remove_ingredient)
        button_delegate.addIngredient.connect(self._add_ingredient)
        self.table.setItemDelegateForColumn(4, button_delegate)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.table)

    def _remove_ingredient(self, ingredient_to_remove: str) -> None:
        CocktailMachine.remove_ingredient(ingredient_to_remove)
        print(f"Clicked remove on '{ingredient_to_remove}'")
        self._force_update_data()

    def _add_ingredient(self, item_to_add: ExternalIngredient):
        CocktailMachine.update_ingredient(item_to_add)
        print(f"Clicked add on '{item_to_add}'")
        self._force_update_data()

    def _force_update_data(self):
        print("Force updating data")
        self.model.update_data(CocktailMachine.get_ingredients())


class ButtonDelegate(QStyledItemDelegate):
    addIngredient = pyqtSignal(ExternalIngredient)
    removeIngredient = pyqtSignal(str)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.column() == 4:
            button_rect = option.rect.adjusted(5, 5, -5, -5)
            if index.row() == 0:
                painter.fillRect(button_rect, QColor("#4CAF50"))
                painter.drawText(button_rect, Qt.AlignmentFlag.AlignCenter, "Add")
            else:
                painter.fillRect(button_rect, QColor("#FF5050"))
                painter.drawText(button_rect, Qt.AlignmentFlag.AlignCenter, "Remove")

    def editorEvent(self, event, model: TableModel, option, index):
        if event.type() == event.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            if index.column() == 4 and option.rect.contains(event.pos()):
                ingredient: ExternalIngredient = model.get_item_at_row(index.row())
                if index.row() == 0:
                    # top row
                    self.addIngredient.emit(ingredient)
                else:
                    self.removeIngredient.emit(ingredient.name)
                return True
        return False
