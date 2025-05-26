from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex


class CheckListModel(QAbstractListModel):
    CheckerIdRole = Qt.UserRole + 1
    CheckerNameRole = Qt.UserRole + 2
    CheckerValueRole = Qt.UserRole + 3

    def __init__(self, data: list[dict[str, bool | str]] | None = None):
        super().__init__()
        self._checker = data or []

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._checker)

    def data(self, index: QModelIndex, role: int) -> str | bool | None:
        if not index.isValid():
            return None

        item = self._checker[index.row()]

        if role == self.CheckerIdRole:
            return item["checkerId"]
        elif role == self.CheckerNameRole:
            return item["checkerName"]
        elif role == self.CheckerValueRole:
            return item["checkerValue"]

    def roleNames(self) -> dict[int, bytes]:
        return {
            self.CheckerIdRole: b"checkerId",
            self.CheckerNameRole: b"checkerName",
            self.CheckerValueRole: b"checkerValue",
        }

    def setData(self, index: QModelIndex, value: bool, role: int):
        if role == self.CheckerValueRole:
            self._checker[index.row()]["checkerValue"] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def serialize(self) -> dict[str, bool]:
        """Helper to access the serializable version of the authors

        Returns
        -------
        list
            the list of authors in the serializable way (i.e., python objects)
        """

        to_return = {}
        for item in self._checker:
            if item["checkerValue"]:
                to_return[item["checkerId"]] = item["checkerValue"]
        return to_return

    def __str__(self) -> str:
        return str(self._checker)

    def __repr__(self) -> str:
        return str(self._checker)
