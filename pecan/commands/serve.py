"""
PasteScript serve command for Pecan.
"""
from paste.script.serve import ServeCommand as _ServeCommand

from base               import Command
import re


class ServeCommand(_ServeCommand, Command):
    """
    Serves a Pecan web application.

    This command serves a Pecan web application using the provided
    configuration file for the server and application.

    If start/stop/restart is given, then --daemon is implied, and it will
    start (normal operation), stop (--stop-daemon), or do both.
    """

    # command information
    usage = 'CONFIG_FILE [start|stop|restart|status]'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
    description = '\n'.join(
        map(lambda s: s.rstrip(), __doc__.strip().splitlines()[2:])
    )

    # command options/arguments
    max_args = 2

    # command parser
    parser = _ServeCommand.parser
    parser.remove_option('-n')
    parser.remove_option('-s')
    parser.remove_option('--server-name')

    # configure scheme regex
    _scheme_re = re.compile(r'.*')

    def command(self):

        # set defaults for removed options
        setattr(self.options, 'app_name', None)
        setattr(self.options, 'server', None)
        setattr(self.options, 'server_name', None)

        # run the base command
        _ServeCommand.command(self)

    def loadserver(self, server_spec, name, relative_to, **kw):
        return (lambda app: WSGIRefServer(app.config.server.host, app.config.server.port, app))
    
    def loadapp(self, app_spec, name, relative_to, **kw):
        return self.load_app()


def WSGIRefServer(host, port, app, **options):
    """
    A very simple approach for a WSGI server.
    """
    from wsgiref.simple_server import make_server
    port = int(port)
    srv = make_server(host, port, app, **options)
    srv.serve_forever()
