import os
import BankFile
import BankGui
import logging
import configparser
config_mapping = configparser.ConfigParser(allow_no_value=True)
config_mapping.read(['config_default.ini', 'config.ini'])

#if 'SETTINGS' in config_mapping:
#    settings = config_mapping['SETTINGS']
#    if settings.getboolean('debug'):
#        logging.basicConfig(level=logging.DEBUG)
if config_mapping.getboolean('SETTINGS', 'debug', fallback=False):
    logging.basicConfig(level=logging.DEBUG)

path = config_mapping.get('SETTINGS', 'path', fallback='bank_exports')

search_for = input('enter a text to search for (ENTER for everything): ')
if not search_for:
    search_for = '*'

money = input('enter min money (no cents!): ')
if money == '':
    money = None
else:
    money = int(money) * 100

year_month = input('enter year-month: ')

gui = BankGui.BankGui()

for file_name in os.listdir(path):
    if file_name.lower().endswith('.csv'):
        bf = BankFile.BankFile(os.path.join(path, file_name))
        bf.minimum_money = money
        gui.add_rows(bf.search(search_for, year_month=year_month))

print()
gui.print_gui2()
