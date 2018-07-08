import sys
from KeywordCalculator import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'TF-IDF'
        self.left = 100
        self.top = 100
        self.width = 2000
        self.height = 1400
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon('assets/book.png'))
        QFontDatabase.addApplicationFont('assets/Segoe.ttf')
        self.setStyleSheet(open('assets/styles.qss').read())
        self.initUI()

        self.corpus_filenames = []
        self.filename = ""
        self.args = []

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initDocumentNameText(800, 65, 100, 100)
        self.initUploadDocumentButton(950, 100)

        self.initUploadCorpusButton(100, 250)
        self.initClearCorpusListButton(1480, 250)        
        self.initDocumentsTable(100, 350, 1750, 400)
                                
        self.initComboBox(100, 800, 75, 60)
        self.initGetKeywordsButton(200, 800)
        self.initTextOutput(100, 900, 1750, 400)

        self.show()

    def initUploadDocumentButton(self, left, top):
        d_upload_button = QPushButton('UPLOAD DOCUMENT', self)
        d_upload_button.adjustSize()
        d_upload_button.resize(
            d_upload_button.width() + 20,
            d_upload_button.height()
        )
        d_upload_button.move(left, top)

        self.d_upload_button = d_upload_button
        self.d_upload_button.clicked.connect(self.onDocumentUpload)

    def initDocumentNameText(self, width, height, left, top):
        document_name = QPlainTextEdit(self)
        document_name.setDisabled(True)
        document_name.setPlaceholderText('Select document')
        document_name.move(left, top)
        document_name.resize(width, height)

        self.document_name = document_name

    def initUploadCorpusButton(self, left, top):
        c_upload_button = QPushButton('UPLOAD CORPUS DOCUMENTS', self)
        c_upload_button.adjustSize()
        c_upload_button.resize(
            c_upload_button.width() + 20,
            c_upload_button.height()
        )
        c_upload_button.move(left, top)

        self.c_upload_button = c_upload_button
        self.c_upload_button.clicked.connect(self.onCorpusUpload)


    def initClearCorpusListButton(self, left, top):
        clear_button = QPushButton('CLEAR DOCUMENTS LIST', self)
        clear_button.adjustSize()
        clear_button.resize(
            clear_button.width() + 20,
            clear_button.height()
        )
        clear_button.move(left, top)
        clear_button.setStyleSheet('background-color: #a95c61; color: white;')

        self.clear_button = clear_button
        self.clear_button.clicked.connect(self.onClear)

    def initGetKeywordsButton(self, left, top):
        keywords_button = QPushButton(f'GET {self.combo.currentText()} KEYWORDS', self)
        keywords_button.adjustSize()
        keywords_button.resize(
            keywords_button.width() + 20,
            keywords_button.height()
        )
        keywords_button.move(left, top)

        self.keywords_button = keywords_button
        self.keywords_button.clicked.connect(self.onGetKeywords)

    def initComboBox(self, left, top, width, height):
        combo = QComboBox(self)
        combo.addItems(map(lambda x: str(x), range(1, 15)))
        combo.move(left, top)
        combo.resize(width, height)

        self.combo = combo
        self.combo.activated[str].connect(self.onActivated)

    def initDocumentsTable(self, left, top, width, height):
        documents_table = QTableWidget(self)
        documents_table.setColumnCount(1)
        documents_table.setRowCount(0)
        documents_table.resize(width, height)
        documents_table.move(left, top)
        documents_table.setHorizontalHeaderLabels(['CORPUS DOCUMENTS:'])
        documents_table.verticalHeader().setVisible(False)
        header = documents_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft)

        self.documents_table = documents_table

    def initTextOutput(self, left, top, width, height):
        text_output = QPlainTextEdit(self)
        text_output.setPlaceholderText('Keywords')
        text_output.setDisabled(True)
        text_output.move(left, top)
        text_output.resize(width, height)

        self.text_output = text_output

    def onActivated(self, text):
        self.keywords_button.setText(f'GET {text} KEYWORDS')

    def onCorpusUpload(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select Documents", "", "Text Files (*.txt)", options=options)
        if files:
            for i, filename in enumerate(files):
                self.corpus_filenames.append(filename)
                item = QTableWidgetItem(filename)
                item.setFlags(Qt.ItemIsEnabled)
                self.documents_table.setRowCount(self.documents_table.rowCount() + 1)
                current_row_index = self.documents_table.rowCount() - 1
                self.documents_table.setItem(current_row_index, 0, item)

    def onDocumentUpload(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Select Document", "", "Text Files (*.txt)", options=options)
        self.document_name.setPlainText(file)

    def onGetKeywords(self):
        args = [self.document_name.toPlainText(),
                self.corpus_filenames,
                int(self.combo.currentText())]

        calculator = KeywordsCalculator(*args)
        self.text_output.setPlainText(', '.join(
            map(lambda p: p[0], calculator.getKeywords()))
        )

    def onClear(self):
        for i in range(self.documents_table.rowCount()):
            self.documents_table.removeRow(0)
            self.corpus_filenames.clear()
