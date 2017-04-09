

class Pip(object):

    def main(self, packages, system, state):
        import pip

        cmd = []

        if state == 'present':
            cmd.append('install')

            if not system:
                cmd.append('--user')
        else:
            cmd.append('uninstall')

        cmd.extend(packages)

        return pip.main(cmd)
