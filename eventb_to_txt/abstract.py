# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import io
import os


class EventBComponent():
    COMMENT = 'org.eventb.core.comment'
    ID = 'org.eventb.core.identifier'
    LABEL = 'org.eventb.core.label'
    PREDICATE = 'org.eventb.core.predicate'
    THEOREM = 'org.eventb.core.theorem'
    TARGET = 'org.eventb.core.target'

    # Tab size must be even
    TAB_SIZE = 4
    TAB = ' ' * TAB_SIZE
    HALFTAB = ' ' * int(TAB_SIZE / 2)

    def __init__(self, component):
        self.path = component
        self.head = {'name': os.path.basename(os.path.splitext(self.path)[0])}

    def get_component_name(self):
        return self.head['name']

    def _print_comment(self, data, f):
        if data.get('comment'):
            if data['comment'].strip():
                f.write(' // ')
                comment = data['comment'].replace('\r\n', '\n')
                comment = comment.replace('\n', ' ')
                f.write(comment)
            else:
                comment = data['comment'].replace('\r\n', '\n')
                f.write(comment)

        f.write('\n')

    def _post_process_file(self, path):
        # trim trailing whitespaces
        lines = ''.join([line.rstrip() + '\n' for line in open(path).readlines()])

        # save file with LF line endings
        with io.open(path, 'w', newline='\n') as f:
            f.writelines(lines)
