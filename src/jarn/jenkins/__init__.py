# -*- coding: utf-8 -*-

import os
import shutil

import iw.recipe.template

TEMPLATE_DIR = os.path.dirname(__file__)

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.name, self.options, self.buildout = name, options, buildout
        self.part_dir = os.path.join(buildout['buildout']['parts-directory'], name)

        options['host'] = options.get('host', '127.0.0.1').strip()
        options['port'] = options.get('port', '8070').strip()

        options['jetty-location'] = options['jetty-location'].strip()
        options['jenkins-location'] = options['jenkins-location'].strip()

        # Java startup commands
        options['java-opts'] = options.get('java-opts', '')

    def parse_java_opts(self):
        """Parsed the java opts from `options`. """
        cmd_opts = []
        _start = ['java', '-jar']
        _jar = 'start.jar'
        _opts = []
        if not self.options['java-opts']:
            cmd_opts = _start
        else:
            _opts = self.options['java-opts'].strip().splitlines()
            cmd_opts = _start + _opts
        cmd_opts.append(_jar)
        return cmd_opts

    def generate_jetty(self, **kwargs):
        iw.recipe.template.Template(
            self.buildout,
            'jetty.xml',
            kwargs).install()

    def create_bin_scripts(self, **kwargs):
        """ Create a runner for our jenkins instance """
        iw.recipe.template.Script(
            self.buildout,
            self.name,
            kwargs).install()

    def install(self, update=False):
        """installer"""
        parts = [self.part_dir]

        vardir = os.path.join(
            self.buildout['buildout']['directory'], 'var', self.name)

        datadir = os.path.join(vardir, 'data')
        logdir = os.path.join(vardir, 'log')
        webapps = os.path.join(self.part_dir, 'webapps')

        for path in datadir, logdir:
            if not os.path.exists(path):
                os.makedirs(path)

        if not update:
            if os.path.exists(self.part_dir):
                shutil.rmtree(self.part_dir)

            # Copy the jetty files
            shutil.copytree(self.options['jetty-location'], self.part_dir)

            # Clean up default garbage
            war = os.path.join(webapps, 'test.war')
            if os.path.exists(war):
                os.remove(war)

        # Copy the jenkins file
        source = os.path.join(self.options['jenkins-location'], 'jenkins.war')
        destination = os.path.join(webapps, 'jenkins.war')
        shutil.copyfile(source, destination)

        self.generate_jetty(
            source='%s/templates/jetty.xml.tmpl' % TEMPLATE_DIR,
            logdir=logdir,
            serverhost=self.options['host'],
            serverport=self.options['port'],
            datadir=datadir,
            destination=os.path.join(self.part_dir, 'etc'))

        self.create_bin_scripts(
            source='%s/templates/jenkins.tmpl' % TEMPLATE_DIR,
            pidfile=os.path.join(vardir, 'jenkins.pid'),
            logfile=os.path.join(logdir, 'jenkins.log'),
            destination=self.buildout['buildout']['bin-directory'],
            basedir=self.part_dir,
            startcmd=self.parse_java_opts())

        # returns installed files
        return parts

    def update(self):
        """updater"""
        self.install(update=True)
