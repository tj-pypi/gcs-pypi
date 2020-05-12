
gcspypi
=======

gcspypi is a CLI for creating a Python Package Repository in an GCS bucket.

Getting started
---------------

Installation
^^^^^^^^^^^^

Install gcspypi using pip:

.. code-block:: bash

   pip install gcspypi

SET cache-control header for index.html

.. code-block:: bash

   $ gsutil setmeta -h "cache-control:public, must-revalidate, proxy-revalidate, max-age=0" gs://[BUCKET]/index.html

Usage
-----

Distributing packages
^^^^^^^^^^^^^^^^^^^^^

You can now use ``gcspypi`` to create Python packages and upload them to your GCS bucket. 
To hide packages from the public, you can use the ``--private`` option to prevent the packages from 
being accessible directly via the GCS bucket (they will only be accessible via Cloudfront and you can 
use WAF rules to protect them), or alternatively you can specify a secret subdirectory using the ``--secret`` option:

.. code-block:: bash

   cd /path/to/your-project/
   gcspypi --bucket mybucket [--private] [--secret SECRET]

Installing packages
^^^^^^^^^^^^^^^^^^^

Install your packages using ``pip`` by pointing the ``--extra-index-url`` to your CloudFront distribution (optionally followed by a secret subdirectory):

.. code-block:: bash

   pip install your-project --extra-index-url https://pypi.example.com/SECRET/

Alternatively, you can configure the index URL in ``~/.pip/pip.conf``\ :

.. code-block::

   [global]
   extra-index-url = https://pypi.example.com/SECRET/
