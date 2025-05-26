"""Module containing the helpers to bridge the paper in Qt"""

from typing import Any
import re
import pathlib

from ruamel.yaml import YAML
from PySide6.QtCore import Qt, QObject, Property, QAbstractListModel, QModelIndex, Slot, Signal

from .authors import AuthorModel
from .checklist import CheckListModel


def extract_color_spans(full_html: str) -> str:
    """Helper to strip all the HTML code except the span information required for the diff

    Parameters
    ----------
    full_html : str
        The full HTML string

    Returns
    -------
    str
        the cleaned string
    """

    # Extract body
    start = full_html.find("<body")
    start = full_html.find(">", start) + 1
    end = full_html.find("</body>")
    body = full_html[start:end]

    # Remove all tags except span
    body = re.sub(r"<(?![/]?span\b)[^>]+>", "", body)

    # Clean span styles to keep only color
    body = re.sub(
        r'<span[^>]*style="[^"]background-color:\s*([^;"]+)[^"]*"[^>]*>', r'<span style="background-color:\1">', body
    )

    return body.strip()


class Paper(QObject):
    """QT interface to represent a paper

    Attributes
    ----------
    id: str
        The paper identifier
    title: str
        The title of the paper
    abstract: str
        The abstract of the paepr
    authors: AuthorModel
        The authors of the paper
    pdf_file: str
        The path to the PDF of the paper
    """

    titleChanged = Signal()
    abstractChanged = Signal()
    authorsChanged = Signal()
    checkListChanged = Signal()
    checkedChanged = Signal()

    def __init__(self, paper_id: str, paper_info: dict, desc: dict[str, str]):
        """Initialisation

        Parameters
        ----------
        paper_id : str
            The paper identifier
        paper_info : dict
            The information of the paper
        """

        super().__init__()

        self._id: str = paper_id
        self._title: str = paper_info["title"]
        self._abstract: str = paper_info["abstract"]
        self._authors: AuthorModel = AuthorModel(paper_info["authors"])
        self._pdf_file: str = paper_info["pdf_file"]
        self._checked: bool = False if "checked" not in paper_info else paper_info["checked"]
        self._checkList: CheckListModel = CheckListModel([
            {
                "checkerId": id,
                "checkerName": name,
                "checkerValue": paper_info["issues"][id] if id in paper_info["issues"] else False
            }
            for id, name in desc.items()
        ])

    @Property(str, constant=True)
    def id(self) -> str:
        """Getter of the paper identifier

        This value cannot be changed, so it is defined as a constant

        Returns
        -------
        str
            The paper identifier
        """

        return self._id

    @Property(str, constant=True)
    def pdf_file(self) -> str:
        """Getter of the PDF path of the paper

        This value cannot be changed, so it is defined as a constant

        Returns
        -------
        str
            The path of the PDF of the paper
        """

        return self._pdf_file

    @Property(str, notify=titleChanged)
    def title(self) -> str:
        """Getter of the title of the paper

        Returns
        -------
        str
            The title of the paper
        """
        return self._title

    @title.setter
    def title(self, value: str):
        """Setter of the title of the paper

        The setter emits the signal titleChanged

        Parameters
        ----------
        value: str
            The new title of the paper
        """
        if self._title != value:
            self._title = value
            self.titleChanged.emit()

    @Property(str, notify=abstractChanged)
    def abstract(self) -> str:
        """Getter of the abstract of the paper

        Returns
        -------
        str
            The abstract of the paper
        """
        return self._abstract

    @abstract.setter
    def abstract(self, value: str):
        """Setter of the abstract of the paper

        The setter emits the signal abstractChanged

        Parameters
        ----------
        value: str
            The new abstract of the paper
        """
        if self._abstract != value:
            self._abstract = value
            self.abstractChanged.emit()

    @Property(QObject, notify=authorsChanged)
    def authors(self) -> AuthorModel:
        """Getter of the authors of the paper

        Returns
        -------
        str
            The authors of the paper
        """
        return self._authors

    @authors.setter
    def authors(self, value: AuthorModel):
        """Setter of the authors of the paper

        The setter emits the signal authorsChanged

        Parameters
        ----------
        value: str
            The new authors of the paper
        """
        if self._authors != value:
            self._authors = value
            self.authorsChanged.emit()

    @Property(QObject, notify=checkListChanged)
    def checkList(self) -> CheckListModel:
        """Getter of the checkList of the paper

        Returns
        -------
        str
            The checkList of the paper
        """
        return self._checkList

    @checkList.setter
    def checkList(self, value: CheckListModel):
        """Setter of the checkList of the paper

        The setter emits the signal checkListChanged

        Parameters
        ----------
        value: str
            The new checkList of the paper
        """
        if self._checkList != value:
            self._checkList = value
            self.checkListChanged.emit()

    @Property(bool, notify=checkedChanged)
    def checked(self) -> bool:
        """Getter of the checked of the paper

        Returns
        -------
        str
            The checked of the paper
        """
        return self._checked

    @checked.setter
    def checked(self, value: bool):
        """Setter of the checked of the paper

        The setter emits the signal checkedChanged

        Parameters
        ----------
        value: str
            The new checked of the paper
        """
        if self._checked != value:
            self._checked = value
            self.checkedChanged.emit()



class PaperModel(QAbstractListModel):
    IDRole = Qt.UserRole + 1
    TitleRole = Qt.UserRole + 2
    AbstractRole = Qt.UserRole + 3
    AuthorsRole = Qt.UserRole + 4
    PDFFileRole = Qt.UserRole + 5
    CheckedRole = Qt.UserRole + 6
    CheckListRole = Qt.UserRole + 7
    PaperRole = Qt.UserRole + 8

    def __init__(self, papers: dict, desc: dict[str, str]):
        """Initialisation

        Parameters
        ----------
        papers : dict
            The dictionnary containing the papers (paper_id -> paper_info)

        """

        super().__init__()

        # Now fill the database of papers
        self._papers = []
        for paper_id, paper_info in papers.items():
            self._papers.append(Paper(paper_id, paper_info, desc))

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

        if not index.isValid() or index.row() >= len(self._papers):
            return None

        paper = self._papers[index.row()]
        if role == self.IDRole:
            return paper.id
        elif role == self.TitleRole:
            return paper.title
        elif role == self.AbstractRole:
            return paper.abstract
        elif role == self.AuthorsRole:
            return paper.authors
        elif role == self.PDFFileRole:
            return paper.pdf_file
        elif role == self.CheckedRole:
            return paper.checked
        elif role == self.CheckListRole:
            return paper.checkList
        elif role == self.PaperRole:
            return paper

        return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Count the number of papers

        Parameters
        ----------
        parent : QModelIndex
            the parent of the model

        Returns
        -------
        int
            the number of papers
        """

        return len(self._papers)

    @Slot(int, result=int)
    def previousItem(self, index: int) -> int:
        return_index = 0
        for cur_index in range(index-1, 0, -1):
            if not self._papers[cur_index].checked:
                return_index = cur_index
                break
        return return_index

    @Slot(int, result=int)
    def nextItem(self, index: int) -> int:
        return_index = len(self._papers) - 1
        for cur_index in range(index, len(self._papers) - 1):
            if not self._papers[cur_index].checked:
                return_index = cur_index
                break
        return return_index

    def roleNames(self) -> dict[Any, bytes]:
        """Get the role names

        Returns
        -------
        dict[Any, bytes]
            The association of the role identifier and its string (in bytes) representation
        """

        return {
            self.IDRole: b"id",
            self.TitleRole: b"title",
            self.AbstractRole: b"abstract",
            self.AuthorsRole: b"authors",
            self.PDFFileRole: b"pdf_file",
            self.CheckedRole: b"checked",
            self.CheckListRole: b"checkList",
            self.PaperRole: b"paper",
        }

    @Slot(str)
    def save(self, file_uri: str):
        """Slot to save the paper model to a YAML report

        Parameters
        ----------
        file_uri : str
            The URI of the target file
        """

        papers = {}
        for paper in self._papers:
            papers[paper.id] = {
                "title": paper.title,
                "authors": paper.authors.serialize(),
                "abstract": extract_color_spans(paper.abstract),
                "pdf_file": paper.pdf_file,
                "checked": paper.checked,
                "issues": paper.checkList.serialize(),
            }

        yaml_io = YAML(typ="rt", pure=True)
        yaml_io.preserve_quotes = True
        yaml_io.indent(mapping=2, sequence=4, offset=2)
        file_path = pathlib.Path(file_uri.replace("file://", ""))
        with open(file_path, "w") as f_out:
            yaml_io.dump({"papers": papers}, f_out)
