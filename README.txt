Overview
========

This is a recipe to set up and configure Hudson_ in a Jetty_ servlet container.

.. _Hudson : http://hudson-ci.org/
.. _Jetty : http://www.eclipse.org/jetty/


Basic setup
-----------

A basic buildout configuration using this recipe looks like this::

    [buildout]

    parts =
        jetty-download
        hudson-download
        hudson

    [jetty-download]
    recipe = gocept.download
    url = http://download.eclipse.org/jetty/stable-7/dist/jetty-distribution-7.0.1.v20091125.tar.gz
    md5sum = b29813029fbbf94d05e1f28d9592813f
    strip-top-level-dir = true

    [hudson-download]
    recipe = gocept.download
    url = http://download.hudson-labs.org/war/1.375/hudson.war
    md5sum = c9bd2515f5b01e46eed2f740aef5e145

    [hudson]
    recipe = collective.recipe.hudson
    jetty-location = ${jetty-download:location}
    hudson-location = ${hudson-download:location}


This will download both Jetty and Hudson and create an executable Jetty
environment in ``parts/hudson``. It will also create a control script in
``bin/hudson``. The name of the script is the name of the section.

To test the setup run ``bin/hudson fg`` and check the console output. By default
this will run a Jetty server on port 8070. The hudson instance is accessible in
a browser at ``http://127.0.0.1:8070/hudson/``.

Hudson will write all its log files into ``var/hudson/log``. All its
configuration including jobs and past runs will go into ``var/hudson/data``.
The directory name in ``var`` will have the name of the recipe section.


Options
-------

The recipe supports the following options:

host
    Name or IP address of the Jetty server, e.g. ``some.server.com``.
    Defaults to ``127.0.0.1``.

port
    Server port. Defaults to ``8070``.

java-opts
    Optional. Parameters to pass to the Java Virtual Machine (JVM) used to
    run Jetty. Each option is specified on a separated line.
    If you run into memory problems it's typical to pass::

        [hudson]
        ...
        java-opts =
          -Xms512M
          -Xmx1024M
        ...
