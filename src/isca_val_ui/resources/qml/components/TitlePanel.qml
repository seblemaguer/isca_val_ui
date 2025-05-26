import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import Qt.labs.qmlmodels

GroupBox {
    id: title_panel
    title: "<b>Title</b>"
    property var paper

    TextField {
        id: titleField
        text: title_panel.paper?.title ?? ""
        anchors.fill: parent
        color: Material.foreground
        background: Rectangle{
            color:"white"
            radius: 6
            border.color: Material.foreground
        }

        onEditingFinished: function() {
            if (title_panel.paper) {
                title_panel.paper.title = text
            }
        }
        Connections {
            target: title_panel

            function onPaperChanged() {
                Qt.callLater(() => titleField.cursorPosition = 0)
            }
        }
    }
}
