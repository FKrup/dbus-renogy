from dbus_device import DbusDevice


class DbusRenogy(DbusDevice):
    def __init__(self):
        paths = {
            "/NrOfTrackers": {"initial": 1},
            "/Pv/V": {"initial": 15.0},
            "/Yield/Power": {"initial": 50.0},
            "/MppOperationMode": {"initial": 2},
            "/Dc/0/Voltage": {"initial": 54.0},
            "/Dc/0/Current": {"initial": 0.926},
        }
        super(DbusRenogy, self).__init__(
            "com.victronenergy.solarcharger.renogy",
            "Renogy Rover Boost 10A MPPT",
            paths,
        )

    def _update(self):
        super(DbusRenogy, self)._update()

    def _handlechangedvalue(self, path, value):
        super(DbusRenogy, self)._handlechangedvalue()
