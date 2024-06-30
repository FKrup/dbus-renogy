import _thread as thread
import logging

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from dbus_renogy import DbusRenogy
from dummybattery import DummyBattery


def main():
    logging.basicConfig(level=logging.DEBUG)
    thread.daemon = True

    DBusGMainLoop(set_as_default=True)

    DbusRenogy()
    DummyBattery()

    logging.info(
        "Connected to dbus, and switching over to GLib.MainLoop() (= event based)"
    )
    mainloop = GLib.MainLoop()
    mainloop.run()


if __name__ == "__main__":
    main()
