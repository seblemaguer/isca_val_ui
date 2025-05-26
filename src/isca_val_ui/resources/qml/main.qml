import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import QtQuick.Controls.Material
import Qt.labs.qmlmodels
import "components"

ApplicationWindow {
    id: app
    visible: true
    width: 1200
    height: 1200
    title: "PDF Reviewing"

    property var papers: paperModel

    Material.theme: Material.Light
    Material.primary: Material.BlueGrey
    Material.accent: Material.Blue

    RowLayout {
        anchors.fill: parent

        // === PDF Browser ===
        PdfBrowser {
            id: pdfBrowser
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: app.papers
        }

        AnnotationPanel {
            id: annotationPanel
            Layout.preferredWidth: parent.width * 0.4
            Layout.alignment: Qt.AlignTop
        }
    }
}
