import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import QtQuick.Dialogs
import QtQuick.Controls.Material

import "authors"

Item {
    FileDialog {
        id: saveFileDialog
        modality: Qt.ApplicationModal
        fileMode: FileDialog.SaveFile
        nameFilters: ["Report (*.yaml *.yml)"]
        onAccepted: {
            app.papers.save(selectedFile)
        }
    }

    ColumnLayout {
        width: parent.width * 0.99
        height: parent.height
        spacing: 5

        TitlePanel {
            paper: pdfBrowser.currentPaper
            Layout.fillWidth: true
        }

        AuthorPanel {
            paper: pdfBrowser.currentPaper
            Layout.fillWidth: true
            Layout.preferredHeight: 400
        }

        AbstractPanel {
            Layout.fillWidth: true
            Layout.preferredHeight: 300
            paper: pdfBrowser.currentPaper
        }

        CheckingStatusPanel {
            Layout.fillWidth: true
            Layout.preferredHeight: 160
            paper: pdfBrowser.currentPaper
        }

        Button {
            Layout.alignment: Qt.AlignCenter
            text: "Save"
            onClicked: saveFileDialog.open()
        }
    }
}
