"""Module containing the helpers to bridge the authors in Qt"""

from typing import Any
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, Slot


class AuthorModel(QAbstractListModel):
    """The Qt Model of the author"""

    EmailRole = Qt.UserRole + 1
    FirstNameRole = Qt.UserRole + 2
    LastNameRole = Qt.UserRole + 3
    AffiliationRole = Qt.UserRole + 4

    def __init__(self, authors: list | None = None):
        """Initialisation

        Parameters
        ----------
        authors : list, optional
            the list of authors
        """

        super().__init__()
        self._authors = authors or []

    def rowCount(self, parent=QModelIndex()) -> int:
        """Count the number of authors

        Parameters
        ----------
        parent : QModelIndex
            the parent of the model

        Returns
        -------
        int
            the number of authors
        """
        return len(self._authors)

    def roleNames(self) -> dict[Any, bytes]:
        """Get the role names

        Returns
        -------
        dict[Any, bytes]
            The association of the role identifier and its string (in bytes) representation
        """
        return {
            self.EmailRole: b"email",
            self.FirstNameRole: b"firstName",
            self.LastNameRole: b"lastName",
            self.AffiliationRole: b"affiliation",
        }

    def roleFromName(self, name:str) -> int:
        """Get the role names

        Returns
        -------
        dict[Any, bytes]
            The association of the role identifier and its string (in bytes) representation
        """
        name2role = {
            "email": self.EmailRole,
            "firstName": self.FirstNameRole,
            "lastName": self.LastNameRole,
            "affiliation": self.AffiliationRole,
        }

        return name2role[name]


    def data(self, index, role=Qt.DisplayRole):
        """Access the data

        Parameters
        ----------
        index : ???
            The QML index object
        role : int
            The role required for the access

        Returns
        -------
        Any | None
            If the role is valid, any required information else None
        """

        if not index.isValid():
            return None

        person = self._authors[index.row()]
        if role == self.EmailRole:
            return person["email"]
        elif role == self.FirstNameRole:
            return person["first_name"]
        elif role == self.LastNameRole:
            return person["last_name"]
        elif role == self.AffiliationRole:
            return person["affiliation"] if "affiliation" in person else ""
        return None

    @Slot(int, str, "QVariant", result=bool)
    def setRole(self, row, role_name, value):
        idx = self.index(row, 0)
        return self.setData(idx, value, self.roleFromName(role_name))

    def setData(self, index, value, role=Qt.EditRole) -> bool:
        if not index.isValid():
            return False

        person = self._authors[index.row()]
        if role == self.EmailRole:
            person["email"] = value
        elif role == self.FirstNameRole:
            person["first_name"] = value
        elif role == self.LastNameRole:
            person["last_name"] = value
        elif role == self.AffiliationRole:
            person["affiliation"] = value
        else:
            return False

        self.dataChanged.emit(index, index, role)
        return True


    @Slot(int, int)
    def moveItem(self, from_row_index: int, to_row_index: int) -> bool:
        """Slot to move an author in the list

        Parameters
        ----------
        from_row_index : int
            The index of the author to move
        to_row_index : int
            The index where to move the author to

        Returns
        -------
        bool
            True if the move happens, False else
        """

        # Equality,
        if from_row_index == to_row_index:
            return False

        # Check boundaries
        count = len(self._authors)
        if not (0 <= from_row_index < count):
            return False
        if not (0 <= to_row_index < count):
            return False

        # Important: Qt destination index rules
        destination = to_row_index
        if to_row_index > from_row_index:
            destination += 1

        # # For debug purposes
        # print("#########################################################")
        # print(f"> {from_row}, {to_row} ({destination})")
        # print("")

        # And now move!
        self.beginMoveRows(QModelIndex(), from_row_index, from_row_index, QModelIndex(), destination)
        author = self._authors.pop(from_row_index)
        self._authors.insert(to_row_index, author)
        self.endMoveRows()

        # # For debug purposes, print the the current status of the database
        # for i_author, author in enumerate(self._authors):
        #     print(f"{i_author:02d}: {author}")
        # print("=========================================================")

        return True

    @Slot()
    def addAuthor(self):
        """Slot to create an author at the end of the list"""

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._authors.append({"email": "", "first_name": "", "last_name": "", "affiliation": ""})
        self.endInsertRows()

    @Slot(int)
    def removeAuthor(self, author_index: int):
        """Slot to remove an author

        Parameters
        ----------
        author_index : int
            The index of the author to remove

        """

        if 0 <= author_index < self.rowCount():
            self.beginRemoveRows(QModelIndex(), author_index, author_index)
            self._authors.pop(author_index)
            self.endRemoveRows()

    def serialize(self) -> list:
        """Helper to access the serializable version of the authors

        Returns
        -------
        list
            the list of authors in the serializable way (i.e., python objects)
        """

        return self._authors.copy()
