
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt6.QtWidgets import QTableView, QStyledItemDelegate, QWidget, QMessageBox, QVBoxLayout, QHeaderView, QAbstractItemView
from backend.cocktail_machine import CocktailMachine
from backend.datatypes import ExternalIngredient, ValidIngredientUnits
from typing import List
from dataclasses import fields
from backend.pump import Pump
from datetime import datetime

pump_header_mapping = {
    "Content": "contains",
    "Amount": "amount",
    "Pump Code": "pump_code",
    "Date Added": "date_added",
    "Runs": "internal",
    "Tube Volume": "tube_volume"
}


class PumpModel(QAbstractTableModel):
    def __init__(self, data: List[Pump]):
        super(PumpModel, self).__init__()
        self._data = data
        self.headers = {
            0: "Content",
            1: "Amount",
            2: "Pump Code",
            3: "Date Added",
            4: "Runs",
            5: "Tube Volume",
            6: ""
        }

    def data(self, index, role):
        item: Pump = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            # if item.contains == "":
            #    return ""
            if index.column() == 0:
                return item.contains
            if index.column() == 1:
                return item.amount
            if index.column() == 2:
                return item.pump_code
            if index.column() == 3:
                return item.date_added
            if index.column() == 4:
                if item.internal:
                    return "Internal"
                return "External"
            if index.column() == 5:
                return item.tube_volume
            return ""

        if role == Qt.ItemDataRole.BackgroundRole:
            if not item.internal:
                return QColor("#EFEFEFEF")
            return

        if role == Qt.ItemDataRole.FontRole:
            font = QFont()
            font.setPointSize(16)
            return font

    def setData(self, index, value, role):
        edited_item = self._data[index.row()]
        if index.column() == 0:
            edited_item.contains = value
        elif index.column() == 1:
            edited_item.amount = value
        elif index.column() == 2:
            raise Exception("ILLEGAL TO UPDATE PUMP CODE!")
            edited_item.pump_code = value
        elif index.column() == 3:
            print("Date Added should be automatically generated")
            edited_item.date_added = datetime.now().date().strftime("%Y-%m-%d")
        elif index.column() == 5:
            edited_item.tube_volume = value

        # CocktailMachine.update_pump(edited_item)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        flags = super().flags(index)
        if index.column() in [0, 1, 3, 5]:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(
            key=lambda pump: getattr(
                pump,
                pump_header_mapping[self.headers[column]]),
            reverse=order == Qt.SortOrder.DescendingOrder)
        self.layoutChanged.emit()

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return 7

    def get_item_at_row(self, row: int) -> Pump:
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def update_data(self, new_data: List[Pump]) -> None:
        self.beginResetModel()
        self._data = [*new_data]
        self.endResetModel()


class PumpTable(QWidget):
    def __init__(self):
        super(PumpTable, self).__init__()

        self.table = QTableView()

        self.table.sortByColumn(4, Qt.SortOrder.AscendingOrder)
        data = CocktailMachine.get_pumps()

        self.model = PumpModel(data)
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        button_delegate = ButtonDelegate(self)
        button_delegate.update_pump.connect(self._update_pump)
        self.table.setItemDelegateForColumn(6, button_delegate)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.table)

    def _update_pump(self, updated_pump: Pump):
        CocktailMachine.update_pump(updated_pump)
        print(f"Clicked add on '{updated_pump}'")
        self._force_update_data()

    def _force_update_data(self):
        print("Force updating pump data")
        self.model.update_data(CocktailMachine.get_pumps())


class ButtonDelegate(QStyledItemDelegate):
    update_pump = pyqtSignal(Pump)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.column() == 6:
            button_rect = option.rect.adjusted(5, 5, -5, -5)
            painter.fillRect(button_rect, QColor("yellow"))
            painter.drawText(button_rect, Qt.AlignmentFlag.AlignCenter, "Update")

    def editorEvent(self, event, model: PumpModel, option, index):
        if event.type() == event.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            if index.column() == 6 and option.rect.contains(event.pos()):
                pump: Pump = model.get_item_at_row(index.row())
                self.update_pump.emit(pump)
                return True
        return False
