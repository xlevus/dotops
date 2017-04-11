

class Pip(object):

    def main(self, *, packages, user=True, state='present', version=3):
        import pip

        cmd = []

        if state == 'present':
            cmd.append('install')

            if not user:
                cmd.append('--user')
        else:
            cmd.append('uninstall')

        cmd.extend(packages)

        return pip.main(cmd)
