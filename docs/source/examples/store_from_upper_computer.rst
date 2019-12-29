.. _store\_from\_upper\_computer:

Store From Upper Computer
=========================

This sample code shows how to store a fingerprint from upper computer
into a location in the flash library of the module.

The first part of the code makes use of :ref:`enroll_to_upper_computer
<enroll_to_upper_computer>` function exposed in the sample code from the
:ref:`Enroll to upper computer <enroll_to_upper_computer>` example, as
seen in line `13` where it is imported and line `37` where it is used.

This saves us the stress of having to always copy and paste a previously
stored template into the command line when the program is been ran.

.. literalinclude:: ../../../examples/store_from_upper_computer.py
    :language: python
    :linenos: