.. _get\_template\_template\_num:

Get Template Num Count
======================

This sample code shows how to get the number of templates registered in
the module flash library. The flash library has a total of 255 locations
to store templates. The examples code searches all 255 locations and
returns the total number of locations that has a template stored in them.
Good for knowing how many fingerprints have been
:ref:`enrolled <enroll_to_flash_library>` into the flash library.

.. literalinclude:: ../../../examples/get_template_num_count.py
    :language: python