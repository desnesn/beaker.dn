# -*- coding: utf-8 -*-

"""
bkr update-prefs: Update user preferences
============================================================

.. program:: bkr update-prefs

Synopsis
--------

| :program:`bkr update-prefs` [*options*]
|       [--email=<email_address> ...]

Description
-----------

Update user preferences

Options
-------

.. option:: --email <email_address>

   Update user's email address

Common :program:`bkr` options are described in the :ref:`Options
<common-options>` section of :manpage:`bkr(1)`.

Exit status
-----------

Non-zero on error, otherwise zero.

Examples
--------

Update user's email address

    bkr update-prefs --email=foobar@example.com

See also
--------

:manpage:`bkr(1)`
"""


from bkr.client import BeakerCommand
import sys

class Update_Prefs(BeakerCommand):
    """Update user preferences"""
    enabled = True

    def options(self):
        self.parser.usage = "%%prog %s [options]" % self.normalized_name
        self.parser.add_option(
            "--email",
            help="New email address for user",
        )

    def run(self, *args, **kwargs):

        username = kwargs.pop("username", None)
        password = kwargs.pop("password", None)

        self.set_hub(username, password)

        if len(kwargs) < 1:
            self.parser.error("Please specify at least one user preferences option")

        email_address = kwargs.pop("email", None)

        self.hub.prefs.update(email_address)
