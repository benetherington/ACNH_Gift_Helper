from ._anvil_designer import DatabaseViewerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ItemsDisplay import ItemsDisplay
from .VillagersDisplay import VillagersDisplay

if anvil.app.branch == 'published':
  raise PermissionError("If you're seeing this, please let ben.j.etherington@gmail.com know he's a moron." )

class DatabaseViewer(DatabaseViewerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    anvil.server.call('generate_villagers_dict_list')

  def items_button_click(self, **event_args):
    self.column_panel.clear()
    item_display = ItemsDisplay(item=app_tables.items.search())
    self.column_panel.add_component(item_display)

  def villagers_button_click(self, **event_args):
    self.column_panel.clear()
    villager_display = VillagersDisplay(item=app_tables.villagers.search())
    self.column_panel.add_component(villager_display)


