import os


class FileStorage(object):
    def __init__(self, db: str = None) -> None:
        if db is None:
            self.db = os.path.abspath('controllers/car/config')
        else:
            self.db = db

    def get(self, name: str, defaultValue=None):
        try:
            conf = open(self.db, 'r')
            lines = conf.readlines()
            conf.close()
            file_len = len(lines) - 1
            flag = False
            # Find the argument and set the value
            for i in range(file_len):
                if lines[i][0] != '#':
                    if lines[i].split('=')[0].strip() == name:
                        value = lines[i].split('=')[1].replace(' ', '').strip()
                        flag = True
            if flag:
                return value
            else:
                return defaultValue
        except:
            return defaultValue

    def set(self, name: str, value) -> None:
        conf = open(self.db, 'r')
        lines = conf.readlines()
        conf.close()
        file_len = len(lines) - 1
        flag = False
        # Find the argument and set the value
        for i in range(file_len):
            if lines[i][0] != '#':
                if lines[i].split('=')[0].strip() == name:
                    lines[i] = '%s = %s\n' % (name, value)
                    flag = True
        # If argument does not exist, create one
        if not flag:
            lines.append('%s = %s\n\n' % (name, value))

        # Save the file
        conf = open(self.db, 'w')
        conf.writelines(lines)
        conf.close()
