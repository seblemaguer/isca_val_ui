import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2


GroupBox {
    id: abstractPanel
    title: "<b>Abstract</b>"
    property var paper

    ScrollView {
        id: scroller
        anchors.fill: parent
        topPadding: 10
        background: Rectangle{
            color:"white"
            radius: 6
            border.color: Material.foreground
        }

        ScrollBar.vertical: ScrollBar {
            id: abstractVerticalBar
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            hoverEnabled: true
            active: hovered || pressed

            property bool showIt: hovered || pressed
        }

        TextArea {
            id: textArea
            textFormat: Text.RichText
            wrapMode: TextArea.Wrap

            background: Rectangle{
                color:"transparent"
            }

            text: abstractPanel.paper?.abstract ?? ""
            onEditingFinished: {
                if (abstractPanel.paper) {
                    abstractPanel.paper.abstract = text
                }
            }
        }
    }
}
