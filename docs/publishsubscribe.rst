.. Publishing & Subscription

******************************
Publishing & Subscription
******************************

=======
Classes
=======

.. autoclass:: expatriate.publishsubscribe.Publisher
    :members: subscribe, _publish_added, _publish_updated, _publish_deleted
.. autoclass:: expatriate.publishsubscribe.Subscriber
    :members: _data_added, _data_deleted, _data_updated

================================================================================
Structural Types
================================================================================

These types subclass the basic python structural types and allow publishing
changes to the structure.

.. autoclass:: expatriate.publishsubscribe.PublishingDict
    :members:
    :inherited-members:
.. autoclass:: expatriate.publishsubscribe.PublishingList
    :members:
    :inherited-members:

===========
Exceptions
===========

Exceptions are available by::

    from expatriate.model.exceptions import *

.. py:exception:: expatriate.model.exceptions.SubscriberException
