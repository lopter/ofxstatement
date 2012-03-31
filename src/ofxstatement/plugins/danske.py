from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement import statement

class DanskeCsvStatementParser(CsvStatementParser):
    mappings = {"date": 0,
                "payee": 4,
                "memo": 5,
                "amount": 8
                }
    dateFormat = "%Y:%m:%d"

    def parse(self):
        stmt = super(DanskeCsvStatementParser, self).parse()
        statement.recalculate_balance(stmt)
        return stmt

    def parseLine(self, line):
        if self.currentLine == 1:
            return None

        # fill statement line according to mappings
        sl = super(DanskeCsvStatementParser, self).parseLine(line)

        # generate transaction id out of available data
        sl.id = statement.generate_transaction_id(sl)
        return sl


class DanskePlugin(Plugin):
    name = "danske"

    def get_parser(self, fin):
        encoding = self.settings.get('charset', 'utf-8')
        f = open(fin, 'r', encoding=encoding)
        parser = DanskeCsvStatementParser(f)
        parser.statement.currency = self.settings['currency']
        parser.statement.accountId = self.settings['account']
        parser.statement.bankId = self.settings.get('bank', 'Danske')
        return parser
