.. _enroll\_to\_upper\_computer:

Enroll To Upper Computer
========================

This sample code shows how to enroll a fingerprint, but instead of
storing the template in a particular location in the module flash
library, we return the template back to upper computer.

The template could then be stored in a database or something, and could
be retrieved later into the module for verification. There's an example
that shows how to store templates from upper computer back into a
location in the flash library in order to perform a search.

.. literalinclude:: ../../../examples/enroll_to_upper_computer.py
    :language: python