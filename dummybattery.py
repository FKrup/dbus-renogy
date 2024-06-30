from dbus_device import DbusDevice


class DummyBattery(DbusDevice):
    def __init__(self):
        paths = {
            "/Dc/0/Voltage": {"initial": 54.0},
            "/Dc/0/Current": {"initial": 0.926},
            "/Dc/0/Power": {"initial": 50.0},
        }
        super(DummyBattery, self).__init__(
            "com.victronenergy.battery.dummy",
            "Dummy Battery",
            paths,
        )

    def _update(self):
        super(DummyBattery, self)._update()

    def _handlechangedvalue(self, path, value):
        super(DummyBattery, self)._handlechangedvalue()
