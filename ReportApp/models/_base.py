from RoomAccounting.settings import ADMIN_PRIORITY


def verbose_name_plural(model_name):
    for model in ADMIN_PRIORITY:
        if model_name in model:
            return ' ' * ADMIN_PRIORITY[::-1].index(model_name) + model_name
    return 'ERROR: TABLE NAME NOT FOUND IN settings'


class DefaultZeroDict(dict):
    
    def __getitem__(self, key):
        if key not in list(self.keys()):
            return 0
        
        return super().__getitem__(key)
