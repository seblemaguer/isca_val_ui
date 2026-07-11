import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import Qt.labs.qmlmodels

GroupBox {
    id: checked_panel
    property var paper
    label: CheckBox {
        id: checkBox
        checked: checked_panel.paper?.checked ?? false
        text: "<b>PDF Validated</b>"

        onClicked: function() {
            if (checked_panel.paper) {
                checked_panel.paper.checked = checkBox.checked
            }
        }
    }

    GridView {
        id: checkListView
        anchors.fill: parent
        cellWidth: 170; cellHeight: 40
        clip: true
        model: checked_panel.paper?.checkList

        ScrollBar.vertical: ScrollBar {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            hoverEnabled: true
            active: hovered || pressed
        }

        delegate: Column {
            height: implicitHeight

            CheckBox {
                text: checkerName
                checked: checkerValue

                onClicked: function() {
                    checkerValue = checked
                }
            }
        }
    }
}
