OctoSalt: OctoPrint Salt Modules
================================
This is a collection of Salt modules for the OctoPrint 3D printing server. It
allows an OctoPrint installation to function as a Salt minion, by way of Salt's
proxy minion setup, using OctoPrint's built-in API.

Introduction
------------
OctoSalt uses a proxy minion module, configured via pillar and designed to run
from another minion which has access to the OctoPrint server.

For those not familiar with the concepts, here's a quick rundown.

*Salt* is a remote automation platform popular in data centers whose size ranges
from just a handful of servers to tens of thousands. Its use is not limited to
data centers, however. Its very nature makes it a perfect tool for the maker
community, particularly on small Linux-based devices such as the Raspberry Pi.

A *Salt master* is the server which controls Salt minions.

A *Salt minion* is a device, usually a server running a full-blown OS such as
Linux or Windows, which is managed by Salt. These devices are typically able
to run the ``salt-minion`` service, which runs in Python.

In the event that a device is unable to run Python or otherwise run the
``salt-minion`` service, a *proxy minion* may be configured on either the
master or one of the minions, to provide an interface which makes the device
behave like any other minion.

The *Salt pillar* subsystem allows for minions to be configured from the Salt
master instead of directly on the minion. Because a proxy minion is unable
to store its own configuration, the pillar subsystem is usually used to
configure it.

Installation
------------
The files for this package must be installed on the minion which will host the
proxy minion. The ``salt/`` directory in this package may be placed directly
in the ``/srv/`` directory on that minion. This will create a directory tree
that looks like:

:: 

  /srv/
  +-- salt/
      +-- _modules/
      +-- _proxy/

Configuration
-------------
The following assumes some familiarity with Salt. A more in-depth discussion
of Salt itself can be found in the `Getting Started guide
<https://docs.saltstack.com/en/getstarted/>`_.

First, configure ``/srv/pillar/top.sls`` on the Salt master:

.. code-block:: yaml

    base:
      octominion:
        - octosalt

In this example, ``octominion`` is the minion name by which Salt will refer to
the printer. It is _not_ the name of the minion which will actually host the
proxy module and perform the connection.

The ``octosalt`` line refers to ``/srv/pillar/octosalt.sls`` on the Salt master.
Create that file with the following content:

.. code-block:: yaml

    proxy:
      proxytype: octoprint
      url: http://192.168.11.38

In this file, the only value that needs changing is the URL, which points to
the OctoPrint server.

Unless the hostname for your Salt master is ``salt``, you will also need to
update the ``/etc/salt/proxy`` file on the minion which is hosting the proxy
minion.

.. code-block:: yaml

    master: salt.mydomain.com

Finally, to start the proxy minion, create ``/srv/salt/octosalt.sls`` on the
Salt master with the following content:

.. code-block:: yaml

    octosalt-configure:
      salt_proxy.configure_proxy:
        - proxyname: octominion
        - start: True

In this example, ``octominion`` refers to the minion name by which Salt will
refer to the OctoPrint server, and _not_ the minion which will host the proxy.

In order to start the proxy minion on the host minion, issue the following
command from the Salt master:

.. code-block:: bash

    # salt octopi state.sls octosalt

In this example, ``octopi`` refers to the minion which will host the proxy.

Then accept the key for the new proxy minion:

.. code-block:: bash

    # salt-key -ya octominion
