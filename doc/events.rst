Event Bus
=========
Both OctoPrint and Salt have their own event bus. It is possible to connect
some or all of the events fired from OctoPrint to the Salt event bus, making
the Salt Reactor available to issue commands based on printer activity.

More information on the OctoPrint event bus can be found here, including more
detailed descriptions of the events and what they mean:

http://docs.octoprint.org/en/master/events/index.html

OctoPrint events are configured in the ``config.yaml`` file, in the ``events``
section. This section will look something like:

.. code-block:: yaml

    events:
      enabled: True
      subscriptions:
        - command: <some command>
          event: <some event>
          type: system

This section, including all of the available events in OctoPrint, is in the
``events.yaml`` file included with OctoSalt. This file looks like:

.. code-block:: yaml

    events:
      enabled: true
      subscriptions:
      - command: 'salt-call event.fire_master ''{{"status": "The server has started."}}'' octoprint/server/Startup'
        event: Startup
        type: system
      - command: 'salt-call event.fire_master ''{{"status": "The server is shutting down."}}'' octoprint/server/Shutdown'
        event: Shutdown
        type: system

...and so on. Each list item is a dictionary containing a command, an event,
and the type. For OctoSalt, the type will always be ``system``. The event key
refers to the OctoPrint event. The command key contains a ``salt-call`` command
which will fire that event on the Salt event bus.

Breaking down the command we have the following components:

* ``salt-call event.fire_master``: This starts the call to the Salt event bus.
* ``''{{"status": "..."}}''``: The data to send to the event bus.
* ``octoprint/<type>/<event>``: A tag namespaced to the Salt event bus.

Any or all of these list items may be added to OctoPrint's ``config.yaml`` file
as is. You may want to select only the events you plan to use in order to keep
the noise down on the Salt event bus, or you may just want to add everything,
just in case you need it later.

Salt Permissions
----------------
In order to use the above commands, the user which runs OctoPrint must have
access to the ``salt-call`` command. This not only means the ability to run
the command, but also appropriate file permissions to certain directories.
These directories, and instructions on changing permissions, are listed at:

https://docs.saltstack.com/en/latest/ref/configuration/nonroot.html

Changing Events
---------------
The ``salt-call`` command to fire an event to the master contains two primary
compents: payload data and a tag.

Payload Data
````````````
``salt-call`` expects the data to be a dictionary in JSON format. This can be
tricky with the OctoPrint event bus for two reasons:

* The ``config.yaml`` file is in YAML format, which has subtle nuances.
* The ``command`` definition is processed using Python's string processing functionality, which has its own rules.

Encasing the dictionary inside two sets of single quotes will allow the
double quotes inside JSON to be read properly by the YAML engine. Using double
braces for dictionary definitions will distinguish them from placeholders,
which use single braces.

The Upload event is one example of an event which uses placeholders (single
braces) inside double braces:

.. code-block:: yaml

    - command: 'salt-call event.fire_master ''{{"status": "A file has been uploaded through the web interface.", "name": "{name}", "path": "{path}", "target": "{target}"}}'' octoprint/file/Upload'
      event: Upload
      type: system

In this event, the ``{name}`` placeholder will be replaced with the name of the
file (hence the single braces). But the dictionary that it resides in is
defined with double braces.

Tags
````
Events in the Salt event bus contain a tag. These tags are namespaced to
certain areas of salt. For instance, ``salt/auth`` events are related to Salt's
authentication subsystem. ``salt/job/<jid>/ret/<minion>`` contains return data
for a job (specified by a Job ID, or JID) that was processed by a specific
minion.

The events defined in ``events.yaml`` are intended to provide a standard
namespace inside of Salt for events originating from OctoPrint. The beginning
of a tag contains ``octoprint/`` for this reason. Next is the type of event
(``file/``). OctoPrint doesn't include these types programmatically, but for
improved readability they have been included as found in OctoPrint's event
documentation. The last part of the tag is the event name as defined by
OctoPrint itself, such as ``Upload``.

Together, the resulting tag will look like:

.. code-block:: yaml

    octoprint/file/Upload

While you are able to change these tags, it is strongly discouraged. The events
defined by OctoSalt are intended to be used as a standard inside the
Salt/OctoPrint space.
