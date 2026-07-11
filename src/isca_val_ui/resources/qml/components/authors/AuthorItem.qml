import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import QtQuick.Controls.Material

Item {
    id: root
    width: listView.width
    height: 60

    required property var authorModel
    required property string email
    required property string firstName
    required property string lastName
    required property string affiliation
    required property int index

    property bool dragging: dragHandler.active
    property int startIndex
    z: dragging ? 1000 : 0

    Rectangle {
        anchors.fill: parent
        width: authorPanel.columnWidths[0]
        radius: 6
        color: dragging ? "#d0e6ff" : Material.background
        border.color: Material.foreground
    }

    Row {
        anchors.fill: parent
        anchors.margins: 5
        spacing: 10

        Rectangle {
            id: handle
            width: authorPanel.columnWidths[0]
            height: parent.height
            color: "transparent"
            // color: Material.foreground

            Text {
                anchors.centerIn: parent
                text: "\u2630"
                font.pixelSize: 18
            }

            HoverHandler {
                id: hoverHandler
                cursorShape: Qt.OpenHandCursor
            }

            DragHandler {
                id: dragHandler
                target: root
                yAxis.enabled: true
                xAxis.enabled: false

                onActiveChanged: {
                    if (active) {
                        hoverHandler.cursorShape = Qt.ClosedHandCursor
                        root.startIndex = index
                    } else {
                        hoverHandler.cursorShape = Qt.OpenHandCursor

                        let newIndex = Math.round(root.y / (root.height + listView.spacing))
                        newIndex = Math.max(0, Math.min(listView.count - 1, newIndex))

                        if (newIndex !== root.startIndex) {
                            listView.model.moveItem(root.startIndex, newIndex)
                        }

                        root.y = 0
                    }
                }
            }
        }

        Rectangle {
            width: authorPanel.columnWidths[1]
            height: parent.height

            TextField {
                id: email_textfield
                anchors.fill: parent
                text: root.email
                validator: RegularExpressionValidator { regularExpression:/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/ }
                color: acceptableInput ? Material.foreground : "red"
                onActiveFocusChanged: {
                    if (activeFocus) {
                        listView.currentIndex = root.index
                    }
                }
                onEditingFinished: function() {
                    authorModel.setRole(index, "email", text)
                }

                Component.onCompleted: {
                    cursorPosition = 0
                }
            }
        }

        Rectangle {
            width: authorPanel.columnWidths[2]
            height: parent.height

            TextField {
                anchors.fill: parent
                color: Material.foreground
                text: root.firstName

                onActiveFocusChanged: {
                    if (activeFocus) {
                        listView.currentIndex = root.index
                    }
                }
                onEditingFinished: function() {
                    authorModel.setRole(index, "firstName", text)
                }

                Component.onCompleted: {
                    cursorPosition = 0
                }
            }
        }

        Rectangle {
            width: authorPanel.columnWidths[3]
            height: parent.height

            TextField {
                anchors.fill: parent
                color: Material.foreground
                text: root.lastName

                onActiveFocusChanged: {
                    if (activeFocus) {
                        listView.currentIndex = root.index
                    }
                }
                onEditingFinished: function() {
                    authorModel.setRole(index, "lastName", text)
                }
                Component.onCompleted: {
                    cursorPosition = 0
                }
            }
        }

        Rectangle {
            width: authorPanel.columnWidths[4] - 5
            height: parent.height

            TextField {
                anchors.fill: parent
                color: Material.foreground
                text: root.affiliation

                onActiveFocusChanged: {
                    if (activeFocus) {
                        listView.currentIndex = root.index
                    }
                }
                onEditingFinished: function() {
                    authorModel.setRole(index, "affiliation", text)
                }
                Component.onCompleted: {
                    cursorPosition = 0
                }
            }
        }
    }
}
