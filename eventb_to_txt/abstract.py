# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.


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

    def _print_comment(self, data, f):
        if 'comment' in data:
            if data['comment'].strip():
                f.write(' // ')
                f.write(data['comment'].replace('\n', ' '))
            else:
                f.write(data['comment'])

        f.write('\n')
