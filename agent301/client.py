from telethon.types import InputBotAppShortName
from bots.base.base import BaseFarmer
from bots.agent301.strings import *
from bots.agent301.task import process_do_task, process_do_wheel_task
from bots.agent301.spin import process_spin_wheel
from bots.agent301.info import get_info

class BotFarmer(BaseFarmer):

    name = "Agent301Bot"
    app_extra = "onetime5115285864"
    codes_to_refresh = (401,)
    refreshable_token = True

    @property
    def initialization_data(self):
        return dict(peer=self.name, 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "app"),
                    start_param=self.app_extra)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        self.headers['Authorization'] = auth_data

    def refresh_token(self, *args, **kwargs):
        self.authenticate()

    def farm(self):
        get_info(self)
        process_do_task(self)
        process_do_wheel_task(self)
        process_spin_wheel(self)
