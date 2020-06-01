from dateutil import parser
import csv
import chardet
import logging
import hashlib
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

        self.date_field = 'booking_day'

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
                    self._prepare_row(row)
                    self.all_rows.append(row)
            except Exception as ex:
                logging.error('cant read: ', self.file_path)
                logging.debug(ex)

    def _make_all_rows_lower(self, enforce=False):
        if len(self.all_rows_lower) == 0 or enforce:

            for row in self.all_rows:
                lower_row = {}
                for key in row.keys():
                    if type(row[key]) is str:
                        lower_row[key.lower()] = row[key].lower()
                    else:
                        lower_row[key.lower()] = row[key]

                self.all_rows_lower.append(lower_row)

    @staticmethod
    def get_uuid_from_dict(_dict):
        """
        exported banking rows usually NEVER have any sort of UUID
        so we make one!
        :param _dict: dict full row to generate a UUID for
        :return: str UUID
        """

        _hash = hashlib.sha1()

        all_values = ''
        for values in _dict.values():
            all_values += values + '|'
        _hash.update(all_values.encode())

        return _hash.digest()

    def _prepare_row(self, row):
        uuid = BankFile.get_uuid_from_dict(row)
        row['uuid'] = uuid

        # TODO: implement date_format
        if config_mapping.get('DATE_PARSING', 'date_format', fallback='') != '':
            logging.error('date_format is NOT implemented yet')

        row[self.date_field] = parser.parse(
            row[self.date_field],
            dayfirst=config_mapping.getboolean('DATE_PARSING', 'day_first', fallback=True)
        )

    def _row_has_year_month(self, row, year_month):
        if not year_month:
            return True

        if row['booking_day'].strftime("%Y-%m") == year_month:
            return True

        return False

    def _row_has_text(self, row, txt, column_name):
        if txt == '*':
            return True
        elif column_name != '':
            if txt in row[column_name]:
                logging.debug(row)
                return True
        else:
            for value in row.values():
                if txt in str(value):
                    logging.debug(row)
                    return True

        return False

    def search(self, txt: str, column_name: str = '', year_month: str = ''):
        self._make_all_rows_lower()

        found_rows = []

        txt = txt.lower()
        for row in self.all_rows_lower:
            if self.minimum_money is not None:
                if int(row['amount'].replace(',', '').replace('.', '')) > self.minimum_money:
                    continue

            found_text = self._row_has_text(row, txt, column_name)
            found_year_month = self._row_has_year_month(row, year_month)

            if found_text and found_year_month:
                found_rows.append(row)

        return found_rows
