import openpyxl


class ExcelHandler:  # excel文件处理类
    __book = None
    __sheet = None

    def __init__(self):
        self.book = None
        self.sheet = None
        pass

    # 获取工作簿并获得工作表的引用
    def startHandleExcel(self):
        self.book = openpyxl.Workbook()
        self.sheet = self.book.active

    # 为A、B、C、D、E列的指定行添加数据
    def handleExcel(self, row, A, B, C, D, E):
        self.sheet["A" + str(row)] = str(A).strip()
        self.sheet["B" + str(row)] = str(B).strip()
        self.sheet["C" + str(row)] = str(C).strip()
        self.sheet["D" + str(row)] = str(D).strip()
        self.sheet["E" + str(row)] = str(E).strip()
        return True

    # 处理完成保存excel
    def endHandleExcel(self, fileName):
        self.book.save(fileName)

    # 读取excel并获得工作表的引用
    def startReadExcel(self, fileName):
        self.book = openpyxl.load_workbook(fileName)
        self.sheet = self.book.active

    # 读取excel指定位置的数据
    def readExcel(self, coordinate):
        return str(self.sheet[coordinate].value)

    # 读取完成
    def endReadExcel(self):
        pass
