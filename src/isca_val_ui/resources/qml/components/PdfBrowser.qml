import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import QtQuick.Pdf 6.2
import QtQuick.Shapes 6.2


Item {
    id: paperNavigator
    property var currentPaper :  fileSelector.currentIndex >= 0 ? fileSelector.currentValue : null
    property var model
    property real zoom: 1.0
    property real default_zoom : 1.0

    onWidthChanged: pdfRenderer.resetZoom()
    onHeightChanged: pdfRenderer.resetZoom()


    ColumnLayout {
        anchors.fill: parent

        // --- Navigation Toolbar (Centered) ---
        Item {
            Layout.fillWidth: true
            height: 50
            Layout.alignment: Qt.AlignCenter


            RowLayout {
                height: 40
                anchors.centerIn: parent

                ToolButton {
                    Layout.fillHeight: true
                    text: "|<";
                    onClicked: function () {
                        pdfRenderer.goToPage(0)
                    }
                }
                ToolButton {
                    Layout.fillHeight: true
                    text: "<";
                    onClicked: function () {
                        if (pdfRenderer.currentPage > 0) {
                            pdfRenderer.goToPage(pdfRenderer.currentPage-1)
                        }
                    }
                }
                TextField {
                    id: pageNumber
                    Layout.fillHeight: true
                    Layout.preferredWidth: 50
                    Layout.alignment: Qt.AlignCenter
                    text: pdfRenderer.currentPage + 1
                    background: Rectangle{
                        color:"white"
                        radius: 6
                        border.color: Material.foreground
                    }

                    onEditingFinished: pdfRenderer.goToPage(parseInt(text)-1)
                }
                Label {
                    Layout.fillHeight: true
                    verticalAlignment: Qt.AlignVCenter
                    text: "/";
                }
                Label {
                    Layout.fillHeight: true
                    verticalAlignment: Qt.AlignVCenter
                    text: pdfRenderer.document ? pdfRenderer.document.pageCount : 0
                }
                ToolButton {
                    Layout.fillHeight: true
                    text: ">";
                    onClicked: function () {
                        if (pdfRenderer.currentPage < pdfRenderer.document.pageCount-1) {
                            pdfRenderer.goToPage(pdfRenderer.currentPage+1)
                        }
                    }
                }
                ToolButton {
                    Layout.fillHeight: true
                    text: ">|";
                    onClicked: function () {
                        pdfRenderer.goToPage(pdfRenderer.document.pageCount-1)
                    }
                }

                // --- zoom controls ---
                ToolSeparator {}
                Slider {
                    id: zoomSlider
                    from: 0.25
                    value: 1.0
                    to: 3.0

                    onMoved: {
                        paperNavigator.zoom = zoomSlider.value
                    }
                }
                ToolButton { text: "1:1"; onClicked: pdfRenderer.resetZoom() }                 // reset
            }
        }

        ScrollView {
            id: pdfViewer
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            Rectangle {
                id: container
                width: Math.max(pdfRenderer.width, pdfViewer.width)
                height: Math.max(pdfRenderer.height, pdfViewer.height)
                color: pdfRenderer.activeFocus ? "#dceeff" : "#f0f0f0"

                PdfPageView {
                    id: pdfRenderer
                    anchors.centerIn: parent
                    renderScale: paperNavigator.zoom
                    focus: true

                    document: PdfDocument {
                        id: pdfDocument
                        source: paperNavigator.currentPaper ? paperNavigator.currentPaper.pdf_file : ""
                        onSourceChanged: {
                            if (source !== "") {
                                pdfRenderer.goToPage(0)
                            }
                        }
                    }

                    onCurrentPageChanged: resetZoom()

                    function resetZoom () {
                        var size = document.pagePointSize(currentPage)
                        paperNavigator.default_zoom = pdfViewer.height / size.height
                        paperNavigator.zoom = paperNavigator.default_zoom
                        zoomSlider.value = paperNavigator.zoom
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            parent.forceActiveFocus()
                        }

                        onDoubleClicked: {
                            pdfRenderer.selectAll()
                        }
                    }

                    Shortcut {
                        sequences: [StandardKey.Copy]
                        onActivated: function () {
                            pdfRenderer.copySelectionToClipboard()
                        }
                    }
                }
            }
        }

        // --- File Navigation Toolbar (Centered) ---
        Item {
            Layout.fillWidth: true
            height: 50

            RowLayout {
                height: 40
                anchors.centerIn: parent
                Layout.bottomMargin: 5
                spacing: 10

                ToolButton {
                    Layout.fillHeight: true
                    text: "|<";
                    onClicked: function () {
                        fileSelector.currentIndex = 0
                    }
                }

                ToolButton {
                    Layout.fillHeight: true
                    text: "<<";
                    onClicked: function () {
                        if (fileSelector.currentIndex > 0) {
                            fileSelector.currentIndex = fileSelector.model.previousItem(fileSelector.currentIndex)
                        }
                    }
                }

                ToolButton {
                    Layout.fillHeight: true
                    text: "<";
                    onClicked: function () {
                        if (fileSelector.currentIndex > 0) {
                            fileSelector.currentIndex -= 1
                        }
                    }
                }

                // SearchableComboBox {
                ComboBox {
                    Layout.minimumWidth: 300
                    Layout.preferredWidth: 300
                    Layout.fillHeight: true
                    id: fileSelector
                    model: paperNavigator.model
                    textRole: "id"
                    valueRole: "paper"

                    Component.onCompleted: {
                        if (count > 0) {
                            currentIndex = fileSelector.model.nextItem(0)
                        }
                    }
                }

                Label {
                    text: fileSelector.currentIndex + 1
                }

                Label {
                    text: "/"
                }

                Label {
                    text: fileSelector.count
                }

                ToolButton {
                    Layout.fillHeight: true
                    text: ">";
                    onClicked: function () {
                        if (fileSelector.currentIndex < (fileSelector.count - 1)) {
                            fileSelector.currentIndex += 1
                        }
                    }
                }

                ToolButton {
                    Layout.fillHeight: true
                    text: ">>";
                    onClicked: function () {
                        if (fileSelector.currentIndex < (fileSelector.count - 1)) {
                            fileSelector.currentIndex = fileSelector.model.nextItem(fileSelector.currentIndex)
                        }
                    }
                }

                ToolButton {
                    Layout.fillHeight: true
                    text: ">|";
                    onClicked: function () {
                        fileSelector.currentIndex = fileSelector.count - 1
                    }
                }
            }
        }
    }
}
