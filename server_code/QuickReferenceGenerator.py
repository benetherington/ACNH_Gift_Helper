import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

'''
These methods shouldn't be used in production.
Use when the database gets updated from tinyurl.com/acnh-sheet. Copy the output into Globals.
'''

def generate_clothing_list():
  print(list(set( [ i['name'] for i in app_tables.items.search() ] )))

def generate_villagers_dict_list():
  print([ {'name': v['name'], 'icon_image': v['icon_image']} for v in app_tables.villagers.search() ])
