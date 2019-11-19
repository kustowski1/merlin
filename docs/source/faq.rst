.. _faq:

Frequently Asked Questions
==========================
.. contents:: FAQs
  :local:

General
-------
What is Merlin?
~~~~~~~~~~~~~~~
Merlin is a distributed task queue system
designed to facilitate the large scale
execution of HPC ensembles, like those
needed to build machine learning models
of complex simulations.

Where can I get help with Merlin?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In addition to this :doc:`documentation <./index>`,
the Merlin developers can be reached at
merlin@llnl.gov.
You can also reach out to the merlin user
group mailing list: merlin-users@listserv.llnl.gov.

Setup & Installation
--------------------

How can I build Merlin?
~~~~~~~~~~~~~~~~~~~~~~~
Merlin can be installed via
`pip <https://pypi.org/project/pip/>`_ in a python
:doc:`virtual environment <./virtualenv>`
or via :doc:`spack <./spack>`.

See :doc:`Getting started <./getting_started>`.

Do I have to build Merlin?
~~~~~~~~~~~~~~~~~~~~~~~~~~
If you're at LLNL and want to run on LC, you
can use one of the public deployments.
For more information, check out the LLNL access page
in confluence.

What are the setup instructions at LLNL?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
See "Do I have to build Merlin"

How do I reconfigure for different servers?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The server configuration is set in ``~/.merlin/app.yaml``.
Details can be found :doc:`here <./merlin_config>`.

Component Technology
--------------------
What underlying libraries does Merlin use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Celery
    * :ref:`what-is-celery`
* Maestro
    * :ref:`what-is-maestro`

What security features are in Merlin?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Merlin encrypts network traffic of step results,
implying that all results are encrypted with a
unique user-based key, which is auto-generated
and placed in ``~/.merlin/``. This allows
for multiple users to share a results database.
This is important since some backends, like
redis do not allow for multiple distinct users.

.. _what-is-celery:

What is celery?
~~~~~~~~~~~~~~~
Celery is an asynchronous task/job queue based on distributed message passing.
It is focused on real-time operation, but supports scheduling as well.
See `Celery's GitHub page
<https://github.com/celery/celery>`_
and `Celery's website
<http://www.celeryproject.org/>`_ for more details.

.. _what-is-maestro:

What is maestro?
~~~~~~~~~~~~~~~~
Maestro is a tool and library for specifying and conducting
general workflows.
See `Maestro's GitHub page
<https://github.com/LLNL/maestrowf>`_
for more details.

What is flux?
~~~~~~~~~~~~~
Flux is a hierarchical scheduler and launcher for parallel simulations. It allows the user
to specifiy the same launch command that will work on different HPC clusters with different 
default schedulers such as SLURM or LSF.
More information can be found at the `Flux web page <http://flux-framework.org/docs/home/>`_.

Designing and Building Workflows
--------------------------------
:doc:`yaml specification file <./merlin_specification>`

Where are some example workflows?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``merlin-templates``

How do I launch a workflow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~
To launch a workflow locally, use ``merlin run --local <spec>``.
To launch a distributed workflow, use ``merlin run-workers <spec>``,
and ``merlin run <spec>``.
These may be done in any order.

How do I describe workflows in Merlin?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Merlin workflow is described with a :doc:`yaml specification file <./merlin_specification>`.

What is a DAG?
~~~~~~~~~~~~~~
DAG is an acronym for 'directed acyclic graph'.
This is the way your workflow steps are represented as tasks.

What if my workflow can't be described by a DAG?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are certain workflows that cannot be explicitly defined by a single DAG; however, in our experience, many can.
Furthermore, those workflows that cannot usually do employ DAG sub-components.
You probably can gain much of the functionality you want by combining a DAG with control logic return features (like step restart and additional calls to ``merlin run``).


How do I implement workflow looping / iteration?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Combining ``exit $(MERLIN_RESTART)`` with ``max_retries`` can allow you to loop a single step.
Entire workflow looping / iteration can be accomplished by finishing off your DAG with a final step that makes another call to ``merlin run``.


Can steps be restarted?
~~~~~~~~~~~~~~~~~~~~~~~
Yes. To build this into a workflow, use ``exit $(MERLIN_RESTART)`` within a step to restart it.
To restart failed steps after a workflow has run, see :ref:`restart`.

The max number of retries in given step can be specified with the ``max_retries`` field.

How do I mark a step failure?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each step is ultimately designated as:
* a success ``$(MERLIN_SUCCESS)`` -- writes a ``MERLIN_FINISHED`` file to the step's workspace directory
* a soft failure ``$(MERLIN_SOFT_FAIL)`` -- allows the workflow to continue
* a hard failure ``$(MERLIN_HARD_FAIL)`` -- stops the whole workflow

Normally this happens behinds the scenes, so you don't need to worry about it.
To hard-code this into your step logic, use a shell command such as ``exit $(MERLIN_HARD_FAIL)``.

To rerun all failed steps in a workflow, see :ref:`restart`.
If you really want a previously successful step to be re-run, you can first manually remove the ``MERLIN_FINISHED`` file.


What fields can be added to steps?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Steps have a ``name``, ``description``, and ``run`` field, as shown below.

.. code:: yaml

    name: ...
    description: ...
    run:
        cmd: ...
        depends: ...
        task_queue: ...
        shell: ...
        max_retries: ...

Optional fields are ``depends``, ``task_queue``, and ``shell``.

How do I specify the language used in a step?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can add the field ``shell`` under the ``run`` portion of your step
to change the language you write your step in. The default is ``/bin/bash``,
but you can do things like ``/usr/bin/env python`` as well.
See the ``basic_ensemble.yaml`` for an example.

Running Workflows
-----------------
``merlin run <yaml file>``

For more details, see :doc:`Merlin commands<./merlin_commands>`.

How do I set up a workspace without executing step scripts?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``merlin run --dry <yaml file>``

How do I start workers?
~~~~~~~~~~~~~~~~~~~~~~~
``merlin run-workers <yaml file>``

How do I see what workers are connected?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``merlin query-workers``

.. _stop-workers:

How do I stop workers?
~~~~~~~~~~~~~~~~~~~~~~~~~~~
``merlin stop-workers``

.. _restart:

How do I re-run failed steps in a workflow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``merlin restart <spec>``

What tasks are in my queue?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

How do I purge tasks?
~~~~~~~~~~~~~~~~~~~~~
``merlin purge <yaml file>``

Why is stuff still running after I purge?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You probably have workers executing tasks. Purging
removes them from the server queue, but any currently
running or reserved tasks are being held by the workers.
You need to shut down these workers first:

.. code:: bash

   (merlin3_7) merlin stop-workers
   (merlin3_7) merlin purge <yaml file>

Why am I running old tasks?
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You might have old tasks in your queues. Try ``merlin purge <yaml>``.
You might also have rogue workers. To find out, try ``merlin query-workers``.

Where do tasks get run?
~~~~~~~~~~~~~~~~~~~~~~~