import logging
import configparser
config_mapping = configparser.ConfigParser(allow_no_value=True)
config_mapping.read(['config_default.ini', 'config.ini'])


class BankGui:

    def __init__(self):
        self.all_rows = []
        self.order_by = 'booking_day'
        self.date_field = 'booking_day'
        self.print_fields = [
            'booking_day',
            # 'valutadatum',
            'amount',
            'from',
            'usage_text'
        ]

        if 'SHOW_COLUMNS' in config_mapping:
            self.print_fields = []
            for value in config_mapping['SHOW_COLUMNS']:
                self.print_fields.append(value)

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)

    def add_row(self, row):
        skipped = False
        for _row in self.all_rows:
            if _row['uuid'] == row['uuid']:
                logging.debug('SKIPPING')
                skipped = True
                break

        if not skipped:
            self.all_rows.append(row)

    def print_gui2(self):
        self.sort(self.order_by)
        table_data = [[]]

        for field_name in self.print_fields:
            table_data[0].append(field_name)

        for row in self.all_rows:
            table_data.append([])
            for field_name in self.print_fields:
                table_data[len(table_data)-1].append(row[field_name])

        import terminaltables
        table = terminaltables.ascii_table.AsciiTable(table_data)
        table.title = 'Search Results'
        print(table.table)
        self.print_stats()

    def print_gui(self):
        self.sort(self.order_by)
        output = ''

        for field_name in self.print_fields:
            output += field_name.ljust(len(field_name) + 3)
        output += "\n"

        for row in self.all_rows:
            for field_name in self.print_fields:
                output += row[field_name].ljust(len(field_name) + 3)
            output += "\n"

        print(output)
        self.print_stats()

    def print_stats(self):
        moneyz = 0
        for row in self.all_rows:
            moneyz += int(row['amount'].replace(',', '').replace('.', ''))

        print('Entries:', len(self.all_rows), 'Money:', moneyz / 100)

    def sort(self, order_by):
        from operator import itemgetter
        self.all_rows = sorted(self.all_rows, key=itemgetter(order_by))
