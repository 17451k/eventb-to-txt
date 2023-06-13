# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import os
import xml.etree.ElementTree as ET

from eventb_to_txt.abstract import EventBComponent


class Context(EventBComponent):
    EXTENDS = 'org.eventb.core.extendsContext'
    SET = 'org.eventb.core.carrierSet'
    AXIOM = 'org.eventb.core.axiom'
    CONSTANT = 'org.eventb.core.constant'

    def __init__(self, context):
        super().__init__(context)
        self.extends = []
        self.sets = []
        self.axioms = []
        self.constants = []

        self.__parse()

    def __parse(self):
        root = ET.parse(self.path).getroot()

        if self.COMMENT in root.attrib:
            self.head['comment'] = root.attrib[self.COMMENT]

        for child in root:
            tag = child.tag
            attrs = child.attrib

            if tag == self.EXTENDS:
                self.extends.append(attrs[self.TARGET])
            elif tag == self.SET:
                self.__parse_set(attrs)
            elif tag == self.CONSTANT:
                self.__parse_constant(attrs)
            elif tag == self.AXIOM:
                self.__parse_axiom(attrs)

    def __parse_set(self, attrs):
        st = {'id': attrs[self.ID]}

        if self.COMMENT in attrs:
            st['comment'] = attrs[self.COMMENT]

        self.sets.append(st)

    def __parse_constant(self, attrs):
        const = {'id': attrs[self.ID]}

        if self.COMMENT in attrs:
            const['comment'] = attrs[self.COMMENT]

        self.constants.append(const)

    def __parse_axiom(self, attrs):
        axiom = {
            'label': attrs[self.LABEL],
            'predicate': attrs[self.PREDICATE]
        }

        if self.THEOREM in attrs:
            axiom['theorem'] = attrs[self.THEOREM]
        if self.COMMENT in attrs:
            axiom['comment'] = attrs[self.COMMENT]

        self.axioms.append(axiom)

    def __str__(self):
        res = (self.__to_str_context_head() +
               self.__to_str_sets() +
               self.__to_str_constants() +
               self.__to_str_axioms() +
               'end\n')
        return self._post_process_str(res)

    def to_txt(self, out_path, merge=False):
        exists = os.path.exists(out_path)

        with open(out_path, 'a', encoding="utf8") as f:
            if merge and exists:
                f.write('\n\n')

            f.write(str(self))

    def __to_str_context_head(self):
        res = ('context ' + self.get_component_name() +
               self._to_str_comment(self.head))

        if self.extends:
            res += self.TAB + 'extends ' + ' '.join(self.extends) + '\n'

        res += '\n'
        return res

    def __to_str_sets(self):
        if not self.sets:
            return ''

        pr_line = lambda x: self.TAB + x['id'] + self._to_str_comment(x)
        return 'sets\n' + ''.join(map(pr_line, self.sets)) + '\n'

    def __to_str_constants(self):
        if not self.constants:
            return ''

        pr_line = lambda x: self.TAB + x['id'] + self._to_str_comment(x)
        return 'constants\n' + ''.join(map(pr_line, self.constants)) + '\n'

    def __to_str_axioms(self):
        if not self.axioms:
            return ''

        return ('axioms\n' +
                ''.join(map(lambda x: self.__to_str_axiom(x),
                            self.axioms)) +
                '\n')

    def __to_str_axiom(self, axiom):
        predicate = axiom['predicate'].replace('\r\n', '\n')
        predicate = predicate.replace('\n', '\n' + self.TAB * 2)
        predicate = predicate.replace('\t', self.TAB)

        res = self.TAB

        if 'theorem' in axiom:
            res += 'theorem '

        res += ('@' + axiom['label'] + ':\n' + self.TAB * 2 + predicate)
        res += self._to_str_comment(axiom)
        return res
