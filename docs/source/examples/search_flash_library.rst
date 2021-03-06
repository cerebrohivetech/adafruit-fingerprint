.. _search\_flash\_library:

Search Flash Library
====================

This sample code shows how to search the module flash library for a
print (template) match. It is based on a confidence score. The search
could be for a previously generated template
:ref:`enrolled directly in the flash library <enroll_to_flash_library>`
or one
:ref:`stored from upper computer <store_from_upper_computer>` to module
flash library.

The template could then be stored in a database or something, and could
be retrieved later into the module for verification. There's an example
that shows how to store templates from upper computer back into a
location in the flash library in order to perform a search.

.. literalinclude:: ../../../examples/search.py
    :language: python