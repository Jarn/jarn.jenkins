Overview
========

This is a recipe to set up and configure Jenkins_ in a Jetty_ servlet
container.

.. _Jenkins : http://jenkins-ci.org/
.. _Jetty : http://www.eclipse.org/jetty/


Note
----

The recipe is currently not compatible with Python 2.7 due to an
incompatibility in the ``iw.recipe.template`` recipe used internally.


Basic setup
-----------

A basic buildout configuration using this recipe looks like this::

    [buildout]

    parts =
        jetty-download
        jenkins-download
        jenkins

    [jetty-download]
    recipe = hexagonit.recipe.download
    url = http://download.eclipse.org/jetty/7.2.2.v20101205/dist/jetty-distribution-7.2.2.v20101205.tar.gz
    strip-top-level-dir = true

    [jenkins-download]
    recipe = hexagonit.recipe.download
    url = http://mirrors.jenkins-ci.org/war/1.397/jenkins.war
    download-only = true

    [jenkins]
    recipe = jarn.jenkins
    jetty-location = ${jetty-download:location}
    jenkins-location = ${jenkins-download:location}


This will download both Jetty and Jenkins and create an executable Jetty
environment in ``parts/jenkins``. It will also create a control script in
``bin/jenkins``. The name of the script is the name of the section.

To test the setup run ``bin/jenkins fg`` and check the console output. By
default this will run a Jetty server on port 8070. The jenkins instance is
accessible in a browser at ``http://127.0.0.1:8070/jenkins/``.

Jenkins will write all its log files into ``var/jenkins/log``. All its
configuration including jobs and past runs will go into ``var/jenkins/data``.
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

        [jenkins]
        ...
        java-opts =
          -Xms512M
          -Xmx1024M
        ...
