import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "authors"

GroupBox {
    id: authorPanel
    title: "<b>Author</b>"
    property var paper
    property var columnWidths: [40, 180, 150, 150, 300]
    property int tableWidth: {
        var w = 0;
        for (var i = 0; i < columnWidths.length; ++i)
            w += columnWidths[i];
        return w + columnWidths.length * 9;
    }

    ColumnLayout {
        anchors.fill: parent

        Flickable {
            id: hFlick

            Layout.fillWidth: true
            Layout.fillHeight: true
            contentWidth: table.width
            contentHeight: height
            clip: true

            // Support scrollbar
            flickableDirection: Flickable.HorizontalFlick
            ScrollBar.horizontal: ScrollBar {
                policy: ScrollBar.AsNeeded
            }

            //
            Column {
                id: table
                width: authorPanel.tableWidth
                height: hFlick.height
                spacing: 5

                // Fake the header of the table
                Rectangle {
                    id: header
                    clip: true
                    width: parent.width
                    height: 40

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 5
                        spacing: 10

                        Repeater {
                            model: ["", "Email", "First Name", "Last Name", "Affiliation"]

                            Rectangle {
                                width: authorPanel.columnWidths[index]
                                height: parent.height
                                radius: 6
                                border.color: index == 0 ? Material.background : Material.foreground
                                color: Material.background

                                Label {
                                    anchors.centerIn: parent
                                    text: modelData
                                    font.bold: true
                                    color: Material.foreground
                                }
                            }
                        }
                    }
                }

                ListView {
                    id: listView
                    y: header.height
                    width: parent.width
                    height: parent.height - header.height
                    model: authorPanel.paper ? authorPanel.paper.authors : []
                    clip: true
                    delegate: AuthorItem {}

                    move: Transition {
                        NumberAnimation {
                            properties: "x,y"
                            duration: 200
                            easing.type: Easing.OutQuad
                        }
                    }

                    moveDisplaced: Transition {
                        NumberAnimation {
                            properties: "x,y"
                            duration: 200
                            easing.type: Easing.OutQuad
                        }
                    }

                    addDisplaced: Transition {
                        NumberAnimation {
                            properties: "x,y"
                            duration: 200
                        }
                    }

                    removeDisplaced: Transition {
                        NumberAnimation {
                            properties: "x,y"
                            duration: 200
                        }
                    }

                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }
                }
            }
        }

        // =========================
        // BUTTONS
        // =========================
        RowLayout {
            Layout.alignment: Qt.AlignHCenter

            Button {
                id: add_button
                text: "Add Author"
                onClicked: {
                    authorPanel.paper.authors.addAuthor()
                    remove_button.enabled = true
                }
            }

            Button {
                id: remove_button
                text: "Remove"
                onClicked: {
                    authorPanel.paper.authors.removeAuthor(listView.currentIndex)
                    if (authorPanel.paper.authors.rowCount() == 0) {
                        remove_button.enabled = false
                    }
                }
            }
        }
    }
}
