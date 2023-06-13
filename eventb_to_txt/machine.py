# Copyright (c) 2018 Ilya Shchepetkov
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import os
import xml.etree.ElementTree as ET

from eventb_to_txt.abstract import EventBComponent


class Machine(EventBComponent):
    VARIABLE = 'org.eventb.core.variable'
    INVARIANT = 'org.eventb.core.invariant'
    VARIANT = 'org.eventb.core.variant'
    EXPRESSION = 'org.eventb.core.expression'
    EVENT = 'org.eventb.core.event'
    CONVERGENCE = 'org.eventb.core.convergence'
    EXTENDED = 'org.eventb.core.extended'
    PARAMETER = 'org.eventb.core.parameter'
    GUARD = 'org.eventb.core.guard'
    ACTION = 'org.eventb.core.action'
    ASSIGNMENT = 'org.eventb.core.assignment'
    SEES = 'org.eventb.core.seesContext'
    REFINES_MACHINE = 'org.eventb.core.refinesMachine'
    REFINES_EVENT = 'org.eventb.core.refinesEvent'
    WITNESS = 'org.eventb.core.witness'

    def __init__(self, machine):
        super().__init__(machine)
        self.sees = []
        self.refines = ''
        self.variables = []
        self.invariants = []
        self.variant = dict()
        self.events = []

        self.__parse()

    def __parse(self):
        root = ET.parse(self.path).getroot()

        if self.COMMENT in root.attrib:
            self.head['comment'] = root.attrib[self.COMMENT]

        for child in root:
            tag = child.tag
            attrs = child.attrib

            if tag == self.REFINES_MACHINE:
                self.__parse_refines_machine(attrs)
            elif tag == self.SEES:
                self.__parse_sees(attrs)
            elif tag == self.VARIABLE:
                self.__parse_variable(attrs)
            elif tag == self.INVARIANT:
                self.__parse_invariant(attrs)
            elif tag == self.VARIANT:
                self.__parse_variant(attrs)
            elif tag == self.EVENT:
                self.__parse_event(attrs, child)

    def __parse_refines_machine(self, attrs):
        self.refines = attrs[self.TARGET]

    def __parse_sees(self, attrs):
        self.sees.append(attrs[self.TARGET])

    def __parse_variable(self, attrs):
        var = {'id': attrs[self.ID]}

        if self.COMMENT in attrs:
            var['comment'] = attrs[self.COMMENT]

        self.variables.append(var)

    def __parse_invariant(self, attrs):
        inv = {
            'label': attrs[self.LABEL],
            'predicate': attrs[self.PREDICATE]
        }

        if self.THEOREM in attrs:
            inv['theorem'] = attrs[self.THEOREM]
        if self.COMMENT in attrs:
            inv['comment'] = attrs[self.COMMENT]

        self.invariants.append(inv)

    def __parse_variant(self, attrs):
        self.variant['expression'] = attrs[self.EXPRESSION]

        if self.COMMENT in attrs:
            self.variant['comment'] = attrs[self.COMMENT]

    def __parse_event(self, attrs, child):
        event = {
            'label': attrs[self.LABEL],
            'convergence': attrs[self.CONVERGENCE],
            'extended': attrs[self.EXTENDED]
        }

        if self.COMMENT in attrs:
            event['comment'] = attrs[self.COMMENT]

        for grandchild in child:
            grand_tag = grandchild.tag
            grand_attrs = grandchild.attrib

            if grand_tag == self.REFINES_EVENT:
                self.__parse_refines(event, grand_attrs)
            elif grand_tag == self.PARAMETER:
                self.__parse_parameter(event, grand_attrs)
            elif grand_tag == self.GUARD:
                self.__parse_guard(event, grand_attrs)
            elif grand_tag == self.WITNESS:
                self.__parse_witness(event, grand_attrs)
            elif grand_tag == self.ACTION:
                self.__parse_action(event, grand_attrs)

        self.events.append(event)

    def __parse_refines(self, event, attrs):
        event['refines'] = attrs[self.TARGET]

    def __parse_parameter(self, event, attrs):
        parameter = {'id': attrs[self.ID]}

        if self.COMMENT in attrs:
            parameter['comment'] = attrs[self.COMMENT]

        if 'parameters' not in event:
            event['parameters'] = []

        event['parameters'].append(parameter)

    def __parse_guard(self, event, attrs):
        guard = {
            'label': attrs[self.LABEL],
            'predicate': attrs[self.PREDICATE]
        }

        if self.THEOREM in attrs:
            guard['theorem'] = attrs[self.THEOREM]
        if self.COMMENT in attrs:
            guard['comment'] = attrs[self.COMMENT]

        if 'guards' not in event:
            event['guards'] = []

        event['guards'].append(guard)

    def __parse_witness(self, event, attrs):
        witness = {
            'label': attrs[self.LABEL],
            'predicate': attrs[self.PREDICATE]
        }

        if self.COMMENT in attrs:
            witness['comment'] = attrs[self.COMMENT]

        if 'witnesses' not in event:
            event['witnesses'] = []

        event['witnesses'].append(witness)

    def __parse_action(self, event, attrs):
        action = {
            'label': attrs[self.LABEL],
            'assignment': attrs[self.ASSIGNMENT]
        }

        if self.COMMENT in attrs:
            action['comment'] = attrs[self.COMMENT]

        if 'actions' not in event:
            event['actions'] = []

        event['actions'].append(action)

    def __str__(self):
        res = (self.__to_str_machine_head() +
               self.__to_str_variables() +
               self.__to_str_invariants() +
               self.__to_str_variant() +
               self.__to_str_events() +
               'end\n')
        return self._post_process_str(res)

    def to_txt(self, out_path, merge=False):
        exists = os.path.exists(out_path)

        with open(out_path, 'a', encoding="utf8") as f:
            if merge and exists:
                f.write('\n\n')

            f.write(str(self))

    def __to_str_machine_head(self):
        res = ('machine ' + self.get_component_name() +
               self._to_str_comment(self.head))

        if self.refines:
            res += self.TAB + 'refines ' + self.refines + '\n'

        if self.sees:
            res += self.TAB + 'sees ' + ' '.join(self.sees) + '\n'

        res += '\n'
        return res

    def __to_str_variables(self):
        if not self.variables:
            return ''

        pr_line = lambda x: self.TAB + x['id'] + self._to_str_comment(x)
        return ('variables\n' +
                ''.join(map(pr_line, self.variables)) + '\n')

    def __to_str_invariants(self):
        if not self.invariants:
            return ''

        return ('invariants\n' +
                ''.join(map(lambda x: self.__to_str_invariant(x),
                            self.invariants)) + '\n')

    def __to_str_invariant(self, inv):
        predicate = inv['predicate'].replace('\r\n', '\n')
        predicate = predicate.replace('\n', '\n' + self.TAB * 2)
        predicate = predicate.replace('\t', self.TAB)

        res = self.TAB

        if 'theorem' in inv:
            res += 'theorem '

        res += '@' + inv['label'] + ':\n' + self.TAB * 2 + predicate
        res += self._to_str_comment(inv)
        return res

    def __to_str_variant(self):
        if not self.variant:
            return ''

        return ('variant\n' +
                self.TAB + self.variant["expression"] +
                self._to_str_comment(self.variant) + '\n')

    def __to_str_events(self):
        if not self.events:
            return ''

        return ('events\n' +
                ''.join(map(lambda x: self.__to_str_event(x),
                            self.events)))

    def __to_str_event(self, event):
        res = self.__to_str_event_head(event)

        if 'parameters' in event:
            res += (self.TAB + self.HALFTAB + 'any\n' +
                    ''.join(map(lambda x:
                                self.TAB * 2 + x['id'] + self._to_str_comment(x),
                                event['parameters'])))

        if 'guards' in event:
            res += (self.TAB + self.HALFTAB + 'where\n' +
                    ''.join(map(lambda x: self.__to_str_guard(x),
                                event['guards'])))

        if 'witnesses' in event:
            res += (self.TAB + self.HALFTAB + 'with\n' +
                    ''.join(map(lambda x: self.__to_str_witness(x),
                                event['witnesses'])))

        if 'actions' in event:
            res += (self.TAB + self.HALFTAB + 'then\n' +
                    ''.join(map(lambda x: self.__to_str_action(x),
                                event['actions'])))

        res += self.TAB + 'end\n\n'
        return res

    def __to_str_event_head(self, event):
        res = self.TAB

        if event['convergence'] == '1':
            res += "convergent "
        elif event['convergence'] == '2':
            res += "anticipated "

        res += 'event ' + event['label']

        if 'refines' in event:
            if event['extended'] == 'true':
                res += ' extends ' + event['refines']
            else:
                res += ' refines ' + event['refines']
        else:
            if event['extended'] == 'true':
                res += ' extends ' + event['label']

        res += self._to_str_comment(event)
        return res

    def __to_str_guard(self, guard):
        res = self.TAB * 2

        if 'theorem' in guard:
            res += 'theorem '

        res += '@' + guard['label'] + ': '

        additional_tab = len(guard['label']) + 2
        if 'theorem' in guard:
            additional_tab += len('theorem ')

        replacement = '\n' + self.TAB * 2 + ' ' * additional_tab
        predicate = guard['predicate'].replace('\r\n', '\n')
        predicate = predicate.replace('\n', replacement)
        predicate = predicate.replace('\t', self.TAB)

        res += predicate

        res += self._to_str_comment(guard)
        return res

    def __to_str_witness(self, witness):
        res = self.TAB * 2 + '@' + witness['label'] + ': '

        additional_tab = len(witness['label']) + 2

        replacement = '\n' + self.TAB * 2 + ' ' * additional_tab
        predicate = witness['predicate'].replace('\r\n', '\n')
        predicate = predicate.replace('\n', replacement)
        predicate = predicate.replace('\t', self.TAB)

        res += predicate

        res += self._to_str_comment(witness)
        return res

    def __to_str_action(self, action):
        res = self.TAB * 2 + '@' + action['label'] + ': '

        additional_tab = len(action['label']) + 2

        replacement = '\n' + self.TAB * 2 + ' ' * additional_tab
        assignment = action['assignment'].replace('\r\n', '\n')
        assignment = assignment.replace('\n', replacement)
        assignment = assignment.replace('\t', self.TAB)

        res += assignment

        res += self._to_str_comment(action)
        return res
