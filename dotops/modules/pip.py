from plumbum import local


class Pip(object):
    state_map = {
        'present': 'install',
        'absent': 'uninstall -y',
        'latest': 'install -U',
        'reinstall': 'install -I'
    }

    def get_pip(self, version):
        return local['pip' + str(version)]

    def main(self, *, packages, user=True, state='present', version=3):
        pip = self.get_pip(version)
        pip = pip['--isolated']
        pip = pip[self.state_map[state]]

        if user:
            pip = pip['--user']

        pip = pip[packages]

        pip()
