import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from htmlEdit import htmlEdit

reload(sys)
sys.setdefaultencoding('utf-8')

qtCreatorFile = "htmlEdit.ui" # Enter file here.
Ui_Window , QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_Window):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Window.__init__(self)
        self.setupUi(self)

        self.btn_do.clicked.connect(self.htmlEdit)

    def htmlEdit(self):
        txt = self.txt_input.toPlainText()
        #print txt
        editHTML = htmlEdit()
        txtHTML,counter = editHTML.spanTagCleaner(txt)
        #print "Deleted %s SPAN tag" %counter
        self.txt_report.setPlainText("Deleted %s <span></span> TAG."%counter)
        txtHTML,counter = editHTML.linkOpenNewTag(txtHTML)
        #print "Added %s BLANK target" %counter
        self.txt_report.append("Added %s BLANK target."%counter)
        txtHTML,counter,youtube_notallow_embed,youtube_broken_links = editHTML.youtubeEmbeddedMaker(txtHTML)
        #print "Added %s Embedded Youtube" %counter
        self.txt_report.append("Added %s Embedded Youtube Videos."%counter)
        if youtube_notallow_embed:
            #print "Following links are not allowed to embed: ", youtube_notallow_embed
            self.txt_report.append("Following links are not allowed to embed: %s"%youtube_notallow_embed)
        if youtube_broken_links:
            # print "Following YOUTUBE links are broken links: ", youtube_broken_links
            self.txt_report.append("Following YOUTUBE links are broken links: %s"%youtube_broken_links)
        self.txt_output.setPlainText(txtHTML)
      







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
