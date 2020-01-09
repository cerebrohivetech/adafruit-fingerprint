Adafruit Fingerprint Core Library Documentation
===============================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    core
    interface
    exceptions
    responses
    utils

This part documents the library itself.

Now, the `interface` and `responses` module are most likely the only ones
you'll have to deal with to implement code for your use case.

The `Core`, `Exceptions` and `Utils` modules are internal modules used
internally by the `adafruit_fingerprint` package itself to build up the
interface. The interface exposes the ``AdafruitFingerprint`` class,
which can be imported directly from the package like so
``from adafruit_fingerprint import AdafruitFingerprint``. This class is
the only object exposed by the package's `__init__` file.

And the responses can be imported like so
``from adafruit_fingerprint.responses import *``.
You can also decide to import only a particular response like so
``from adafruit_fingerprint.responses import FINGERPRINT_OK``.

And this is basically all you need from the library to get started.
See the :ref:`example_codes` section to get an idea of how this works.
