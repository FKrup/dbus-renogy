import os
import platform
import sys

import dbus
from gi.repository import GLib

# import Victron Energy packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "ext", "velib_python"))
from vedbus import VeDbusService


class DbusDevice(object):
    def __init__(self, serviceName, deviceName, paths):
        self._dbusservice = VeDbusService(serviceName, dbusconnection())
        self._paths = paths

        # Create management objects, as specified in the ccgx dbus-api document
        self._dbusservice.add_path("/Mgmt/Connection", "Not implemented")
        self._dbusservice.add_path("/Mgmt/ProcessName", __file__)
        self._dbusservice.add_path(
            "/Mgmt/ProcessVersion",
            "1.0.0, running on Python " + platform.python_version(),
        )

        # Create mandatory objects
        self._dbusservice.add_path("/ProductName", deviceName)
        self._dbusservice.add_path("/Connected", 1)
        self._dbusservice.add_path("/DeviceInstance", 0)
        self._dbusservice.add_path("/ProductId", 0)
        self._dbusservice.add_path("/HardwareVersion", 0)
        self._dbusservice.add_path("/FirmwareVersion", 0)

        # Create optional objects
        self._dbusservice.add_path("/CustomName", deviceName)
        self._dbusservice.add_path("/Serial", 0)

        # Add all paths
        for path, settings in self._paths.items():
            self._dbusservice.add_path(
                path,
                settings.get("initial"),
                writeable=settings.get("writeable", False),
                onchangecallback=settings.get("onchangecallback", None),
            )

        GLib.timeout_add(1000, self._update)

    def _update(self):
        with self._dbusservice as s:
            for path, settings in self._paths.items():
                if "update" in settings:
                    update = settings["update"]
                    if callable(update):
                        s[path] = update(path, s[path])
                    else:
                        s[path] += update
        return True

    def _handlechangedvalue(self, path, value):
        return True


class SystemBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SYSTEM)


class SessionBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SESSION)


def dbusconnection():
    return SessionBus() if "DBUS_SESSION_BUS_ADDRESS" in os.environ else SystemBus()
