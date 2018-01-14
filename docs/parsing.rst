.. Basic XML Parsing

.. toctree::
   :maxdepth: 2
   :caption: Contents:

*****************
Basic XML Parsing
*****************

================================================================================
Classes
================================================================================

.. autoclass:: expatriate.Document
    :members:
    :inherited-members:

.. autoclass:: expatriate.Attribute
      :members:
      :inherited-members:

.. autoclass:: expatriate.CharacterData
    :members:
    :inherited-members:

.. autoclass:: expatriate.Comment
    :members:
    :inherited-members:

.. autoclass:: expatriate.Element
    :members:
    :inherited-members:

.. autoclass:: expatriate.Namespace
    :members:
    :inherited-members:

.. autoclass:: expatriate.ProcessingInstruction
    :members:
    :inherited-members:

============================
Support Classes
============================

.. autoclass:: expatriate.Node.Node
    :members:
    :inherited-members:

.. autoclass:: expatriate.Parent.Parent
    :members:
    :inherited-members:

===========
Exceptions
===========

Exceptions are available by::

    from expatriate.exceptions import *

.. py:exception:: expatriate.exceptions.NamespaceRedefineException
.. py:exception:: expatriate.exceptions.PrefixRedefineException
.. py:exception:: expatriate.exceptions.UnattachedElementException
.. py:exception:: expatriate.exceptions.UnknownNamespaceException
.. py:exception:: expatriate.exceptions.UnknownPrefixException
