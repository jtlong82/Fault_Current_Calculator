from menus import zbusmenu
from Classes import ZBus

def get_relay_scheme(dataframes):
    zbus_choice = zbusmenu(dataframes)
    zbus_selection = ZBus(zbus_choice)

    for key, value in connection_types.items():
        print(f"{key}. {value}")
    choice = input("Enter (1-4): ")
    return connection_types.get(choice, None)