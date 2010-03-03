# -*- coding: utf-8 -*-

import os
import shutil

import iw.recipe.template
import zc.buildout

TRUE_VALUES = set(['yes', 'true', '1', 'on'])
TEMPLATE_DIR = os.path.dirname(__file__)

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.name, self.options, self.buildout = name, options, buildout
        self.part_dir = os.path.join(buildout['buildout']['parts-directory'], name)

        options['host'] = options.get('host','localhost').strip()
        options['port'] = options.get('port', '8070').strip()
        options['section-name'] = options.get('section-name', 'hudson').strip()

        options['jetty-location'] = options['jetty-location'].strip()
        options['hudson-location'] = options['hudson-location'].strip()

        options['jetty-destination'] = options.get(
            'jetty-destination',
            os.path.join(self.part_dir, 'etc'))

        options['vardir'] = options.get(
            'vardir',
            os.path.join(buildout['buildout']['directory'], 'var', 'hudson'))

        options['script'] = options.get('script', 'hudson').strip()

        # Java startup commands
        options['java_opts'] = options.get('java_opts', '')

    def parse_java_opts(self):
        """Parsed the java opts from `options`. """
        cmd_opts = []
        _start = ['java', '-jar']
        _jar = 'start.jar'
        _opts = []
        if not self.options['java_opts']:
            cmd_opts = _start
        else:
            _opts = self.options['java_opts'].strip().splitlines()
            cmd_opts = _start + _opts
        cmd_opts.append(_jar)
        return cmd_opts

    def generate_jetty(self, **kwargs):
        iw.recipe.template.Template(
            self.buildout,
            'jetty.xml',
            kwargs).install()

    def create_bin_scripts(self, **kwargs):
        """ Create a runner for our hudson instance """
        if self.options['script']:
            iw.recipe.template.Script(
                self.buildout,
                self.options['script'],
                kwargs).install()

    def install(self):
        """installer"""
        parts = [self.part_dir]

        if os.path.exists(self.part_dir):
            raise zc.buildout.UserError(
                'Target directory %s already exists. Please remove it.' % self.part_dir)

        vardir = self.options['vardir']
        datadir = os.path.join(vardir, 'data')
        logdir = os.path.join(vardir, 'log')

        for path in datadir, logdir:
            if not os.path.exists(path):
                os.makedirs(path)

        # Copy the jetty files
        shutil.copytree(self.options['jetty-location'], self.part_dir)

        # Copy the hudson files
        war = os.path.join(self.options['hudson-location'], 'hudson.war')
        webapps = os.path.join(self.part_dir, 'webapps')
        shutil.copyfile(war, os.path.join(webapps, 'hudson.war'))

        # Clean up default garbage
        test_war = os.path.join(webapps, 'test.war')
        if os.path.exists(test_war):
            os.remove(test_war)

        for xml in ('test.xml', 'demo.xml', 'javadoc.xml'):
            xml_file = os.path.join(self.part_dir, 'contexts', xml)
            if os.path.exists(xml_file):
                os.remove(xml_file)

        self.generate_jetty(
            source='%s/templates/jetty.xml.tmpl' % TEMPLATE_DIR,
            logdir=logdir,
            serverport=self.options['port'],
            destination=self.options['jetty-destination'])

        self.create_bin_scripts(
            source='%s/templates/hudson.tmpl' % TEMPLATE_DIR,
            pidfile=os.path.join(vardir, 'hudson.pid'),
            logfile=os.path.join(logdir, 'hudson.log'),
            destination=self.buildout['buildout']['bin-directory'],
            basedir=self.part_dir,
            startcmd=self.parse_java_opts())

        # returns installed files
        return parts

    def update(self):
        """updater"""
        pass