import csv
import chardet
import logging
import configparser
config_mapping = configparser.ConfigParser(allow_no_value=True)
config_mapping.read(['config_default.ini', 'config.ini'])


class BankFile:

    def __init__(self, file_path):
        self.file_path = file_path

        self.all_rows = []
        self.all_rows_lower = []

        self.encoding = 'utf-8'
        self.minimum_money = None
        self.header_mapping = config_mapping['COLUMNS']

        self._get_encoding()
        self._read_lines()

    def _get_encoding(self):
        raw_data = open(self.file_path, "rb").read()
        result = chardet.detect(raw_data)
        self.encoding = result['encoding']
        logging.debug(self.encoding)

    def _remap_column_names(self, row):
        # cant change an iterating dictionary, enforce a cached list with the currently present keys
        for column_name in list(row.keys()):
            if column_name in self.header_mapping:
                # yes, we got the value twice now, who cares
                row[self.header_mapping[column_name]] = row[column_name]

    def _read_lines(self):
        with open(self.file_path, newline='', encoding=self.encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')

            try:
                for row in reader:
                    self._remap_column_names(row)
                    self.all_rows.append(row)
            except Exception as ex:
                logging.error('cant read: ', self.file_path)
                logging.debug(ex)

    def _make_all_rows_lower(self, enforce=False):
        if len(self.all_rows_lower) == 0 or enforce:

            for row in self.all_rows:
                lower_row = {}
                for key in row.keys():
                    lower_row[key.lower()] = row[key].lower()
                self.all_rows_lower.append(lower_row)

    def search(self, txt: str, column_name: str = ''):
        self._make_all_rows_lower()

        found_rows = []

        txt = txt.lower()
        for row in self.all_rows_lower:
            if self.minimum_money is not None:
                if int(row['amount'].replace(',', '').replace('.', '')) > self.minimum_money:
                    continue

            if txt == '*':
                found_rows.append(row)
            elif column_name != '':
                if txt in row[column_name]:
                    logging.debug(row)
                    found_rows.append(row)
            else:
                for value in row.values():
                    if txt in value:
                        logging.debug(row)
                        found_rows.append(row)
                        break

        return found_rows
