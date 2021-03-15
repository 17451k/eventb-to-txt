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

    def to_txt(self, out_path, merge=False):
        exists = os.path.exists(out_path)

        with open(out_path, 'a', encoding="utf8") as f:
            if merge and exists:
                f.write('\n\n')

            self.__print_context_head(f)
            self.__print_sets(f)
            self.__print_constants(f)
            self.__print_axioms(f)

            f.write('end\n')

        self._post_process_file(out_path)

    def __print_context_head(self, f):
        f.write('context ' + self.get_component_name())

        self._print_comment(self.head, f)

        if self.extends:
            f.write(self.TAB + 'extends')

            for extenders in self.extends:
                f.write(' ' + extenders)

            f.write('\n')

        f.write('\n')

    def __print_sets(self, f):
        if not self.sets:
            return

        f.write('sets\n')

        for st in self.sets:
            f.write(self.TAB + st['id'])

            self._print_comment(st, f)
        f.write('\n')

    def __print_constants(self, f):
        if not self.constants:
            return

        f.write('constants\n')

        for const in self.constants:
            f.write(self.TAB + const['id'])

            self._print_comment(const, f)
        f.write('\n')

    def __print_axioms(self, f):
        if not self.axioms:
            return

        f.write('axioms\n')

        for axiom in self.axioms:
            self.__print_axiom(axiom, f)
        f.write('\n')

    def __print_axiom(self, axiom, f):
        predicate = axiom['predicate'].replace('\r\n', '\n')
        predicate = predicate.replace('\n', '\n' + self.TAB * 2)
        predicate = predicate.replace('\t', self.TAB)

        f.write(self.TAB)

        if 'theorem' in axiom:
            f.write('theorem ')

        f.write('@' + axiom['label'] + ':\n' + self.TAB * 2 + predicate)

        self._print_comment(axiom, f)
