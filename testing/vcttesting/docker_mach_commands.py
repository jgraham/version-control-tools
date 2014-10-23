# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

from mach.decorators import (
    CommandArgument,
    CommandProvider,
    Command,
)

from vcttesting.docker import (
    Docker,
    params_from_env,
)

@CommandProvider
class DockerCommands(object):
    def __init__(self, context):
        if 'DOCKER_STATE_FILE' in os.environ:
            state_file = os.environ['DOCKER_STATE_FILE']

        # When running from Mercurial tests, use a per-test state file.
        # We can't use HGTMP because it is shared across many tests. We
        # use HGRCPATH as a base, since it is in a test-specific directory.
        elif 'HGRCPATH' in os.environ:
            state_file = os.path.join(os.path.dirname(os.environ['HGRCPATH']),
                                     'docker-state.json')
        else:
            print('Do not know where to put a Docker state file.')
            sys.exit(1)

        docker_url, tls = params_from_env(os.environ)
        d = Docker(state_file, docker_url, tls=tls)

        if not d.is_alive():
            print('Docker is not available!')
            sys.exit(1)

        self.d = d

    @Command('build-bmo', category='docker',
        description='Build bugzilla.mozilla.org Docker images')
    def build_bmo(self):
        self.d.build_bmo(verbose=True)

    @Command('start-bmo', category='docker',
        description='Start a bugzilla.mozilla.org instance')
    @CommandArgument('cluster', help='Name to give to this instance')
    @CommandArgument('http_port',
        help='HTTP port the server should be exposed on')
    def start_bmo(self, cluster, http_port):
        db_image = os.environ.get('DOCKER_BMO_DB_IMAGE')
        web_image = os.environ.get('DOCKER_BMO_WEB_IMAGE')

        self.d.start_bmo(cluster=cluster, hostname=None, http_port=http_port,
                db_image=db_image, web_image=web_image)

    @Command('stop-bmo', category='docker',
        description='Stop a bugzilla.mozilla.org instance')
    @CommandArgument('cluster', help='Name of instance to stop')
    def stop_bmo(self, cluster):
        self.d.stop_bmo(cluster)

    @Command('prune-images', category='docker',
        description='Prune old Docker images')
    def prune_images(self):
        self.d.prune_images()
