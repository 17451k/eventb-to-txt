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
        self.path = machine
        self.sees = []
        self.refines = ''
        self.variables = []
        self.invariants = []
        self.variant = dict()
        self.events = []

        self.machine_head = dict()
        self.machine_head['name'] = os.path.basename(os.path.splitext(self.path)[0])

        self.__parse()

    def __parse(self):
        root = ET.parse(self.path).getroot()

        if self.COMMENT in root.attrib:
            self.machine_head['comment'] = root.attrib[self.COMMENT]

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
        var = dict()
        var['id'] = attrs[self.ID]

        if self.COMMENT in attrs:
            var['comment'] = attrs[self.COMMENT]

        self.variables.append(var)

    def __parse_invariant(self, attrs):
        inv = dict()
        inv['label'] = attrs[self.LABEL]
        inv['predicate'] = attrs[self.PREDICATE]

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
        event = dict()
        event['label'] = attrs[self.LABEL]
        event['convergence'] = attrs[self.CONVERGENCE]
        event['extended'] = attrs[self.EXTENDED]

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
        parameter = dict()
        parameter['id'] = attrs[self.ID]

        if self.COMMENT in attrs:
            parameter['comment'] = attrs[self.COMMENT]

        if 'parameters' not in event:
            event['parameters'] = []

        event['parameters'].append(parameter)

    def __parse_guard(self, event, attrs):
        guard = dict()
        guard['label'] = attrs[self.LABEL]
        guard['predicate'] = attrs[self.PREDICATE]

        if self.THEOREM in attrs:
            guard['theorem'] = attrs[self.THEOREM]
        if self.COMMENT in attrs:
            guard['comment'] = attrs[self.COMMENT]

        if 'guards' not in event:
            event['guards'] = []

        event['guards'].append(guard)

    def __parse_witness(self, event, attrs):
        witness = dict()
        witness['label'] = attrs[self.LABEL]
        witness['predicate'] = attrs[self.PREDICATE]

        if self.COMMENT in attrs:
            witness['comment'] = attrs[self.COMMENT]

        if 'witnesses' not in event:
            event['witnesses'] = []

        event['witnesses'].append(witness)

    def __parse_action(self, event, attrs):
        action = dict()
        action['label'] = attrs[self.LABEL]
        action['assignment'] = attrs[self.ASSIGNMENT]

        if self.COMMENT in attrs:
            action['comment'] = attrs[self.COMMENT]

        if 'actions' not in event:
            event['actions'] = []

        event['actions'].append(action)

    def to_txt(self, out_path, merge=False):
        exists = os.path.exists(out_path)

        with open(out_path, 'a') as f:
            if merge and exists:
                f.write('\n\n')

            self.__print_machine_head(f)
            self.__print_variables(f)
            self.__print_invariants(f)
            self.__print_variant(f)
            self.__print_events(f)

            f.write('end\n')

    def __print_machine_head(self, f):
        f.write('machine ' + self.machine_head['name'])

        self._print_comment(self.machine_head, f)

        if self.refines:
            f.write(self.TAB + 'refines ' + self.refines + '\n')

        if self.sees:
            f.write(self.TAB + 'sees')

            for seers in self.sees:
                f.write(' ' + seers)

            f.write('\n')

        f.write('\n')

    def __print_variables(self, f):
        if not self.variables:
            return

        f.write('variables' + '\n')

        for var in self.variables:
            f.write(self.TAB + var['id'])

            self._print_comment(var, f)

        f.write('\n')

    def __print_invariants(self, f):
        if not self.invariants:
            return

        f.write('invariants' + '\n')

        for inv in self.invariants:
            self.__print_invariant(inv, f)

        f.write('\n')

    def __print_invariant(self, inv, f):
        predicate = str.replace(inv['predicate'], '\n', '\n' + self.TAB * 2)
        predicate = str.replace(predicate, '\t', self.TAB)

        f.write(self.TAB)

        if 'theorem' in inv:
            f.write('theorem ')

        f.write('@' + inv['label'] + '\n' + self.TAB * 2 + predicate)

        self._print_comment(inv, f)

    def __print_variant(self, f):
        if not self.variant:
            return

        f.write('variant\n')
        f.write(self.TAB + self.variant["expression"])

        self._print_comment(self.variant, f)

        f.write('\n')

    def __print_events(self, f):
        if not self.events:
            return

        f.write('events' + '\n')

        for event in self.events:
            self.__print_event(event, f)

    def __print_event(self, event, f):
        self.__print_event_head(event, f)

        if 'parameters' in event:
            f.write(self.TAB + self.HALFTAB + 'any\n')

            for param in event['parameters']:
                f.write(self.TAB * 2 + param['id'])

                self._print_comment(param, f)

        if 'guards' in event:
            f.write(self.TAB + self.HALFTAB + 'where\n')

            for guard in event['guards']:
                self.__print_guard(guard, f)

        if 'witnesses' in event:
            f.write(self.TAB + self.HALFTAB + 'with\n')

            for witness in event['witnesses']:
                self.__print_witness(witness, f)

        if 'actions' in event:
            f.write(self.TAB + self.HALFTAB + 'then\n')

            for action in event['actions']:
                self.__print_action(action, f)

        f.write(self.TAB + 'end\n\n')

    def __print_event_head(self, event, f):
        f.write(self.TAB)

        if event['convergence'] == '1':
            f.write("convergent ")
        elif event['convergence'] == '2':
            f.write("anticipated ")

        f.write('event ' + event['label'])

        if 'refines' in event:
            if event['extended'] == 'true':
                f.write(' extends ' + event['refines'])
            else:
                f.write(' refines ' + event['refines'])
        else:
            if event['extended'] == 'true':
                f.write(' extends ' + event['label'])

        self._print_comment(event, f)

    def __print_guard(self, guard, f):
        f.write(self.TAB * 2)

        if 'theorem' in guard:
            f.write('theorem ')

        f.write('@' + guard['label'] + ' ')

        additional_tab = len(guard['label']) + 2
        if 'theorem' in guard:
            additional_tab += len('theorem ')

        replacement = '\n' + self.TAB * 2 + ' ' * additional_tab
        predicate = str.replace(guard['predicate'], '\n', replacement)
        predicate = str.replace(predicate, '\t', self.TAB)

        f.write(predicate)

        self._print_comment(guard, f)

    def __print_witness(self, witness, f):
        f.write(self.TAB * 2 + '@' + witness['label'] + ' ')

        additional_tab = len(witness['label']) + 2

        replacement = '\n' + self.TAB * 2 + ' ' * additional_tab
        predicate = str.replace(witness['predicate'], '\n', replacement)
        predicate = str.replace(predicate, '\t', self.TAB)

        f.write(predicate)

        self._print_comment(witness, f)

    def __print_action(self, action, f):
        f.write(self.TAB * 2 + '@' + action['label'] + ' ')

        additional_tab = len(action['label']) + 2

        replacement = '\n' + self.TAB * 2 + ' ' * additional_tab
        assignment = str.replace(action['assignment'], '\n', replacement)
        assignment = str.replace(assignment, '\t', self.TAB)

        f.write(assignment)

        self._print_comment(action, f)
