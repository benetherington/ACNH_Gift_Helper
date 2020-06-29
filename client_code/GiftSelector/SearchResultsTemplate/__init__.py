from ._anvil_designer import SearchResultsTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class SearchResultsTemplate(SearchResultsTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def select_button_click(self, **event_args):
    self.parent.raise_event('x-search-results-select-clicked', item_name=self.item)