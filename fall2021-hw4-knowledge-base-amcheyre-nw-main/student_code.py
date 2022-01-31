import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None

        An asserted fact should only be removed if it is unsupported.
        An asserted rule should never be removed.
        Use the supports_rules and supports_facts fields to find and adjust facts and rules that are supported by
        a retracted fact.
        The supported_by lists in each fact/rule that it supports needs to be adjusted accordingly.
        If a supported fact/rule is no longer supported as a result of retracting this fact (and is not asserted),
         it should also be removed.
        """
        printv("Retracting {!r}", 0, verbose, [fact])

        # For Fact
        if isinstance(fact, Fact):
            # Remove asserted fact if it is unsupported
            for i in self.facts:
                if fact.statement == i.statement:
                    fact = i

            if fact in self.facts and fact.supported_by == []:
                self.facts.remove(fact)

        # Search if in supports_facts some are supported by a retracted fact
        for f in fact.supports_facts:
            for s in f.supported_by:
                if fact in s:
                    f.supported_by.remove(s)
            if f.supported_by == []:
                self.kb_retract(f)

        # For Rule
        if isinstance(fact, Rule):
            # Remove rule if it is unsupported and not asserted
            if fact in self.rules and fact.supported_by == []:
                self.rules.remove(fact)

        # Search if in supports_rules some are supported by a retracted fact
        for r in fact.supports_rules:
            # Adjust supported_by
            for x in r.supported_by:
                if fact in x:
                    r.supported_by.remove(x)
            if r.supported_by == []:
                self.kb_retract(r)

        return None

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing

            Use the util.match function to do unification and create possible bindings.
            Use the util.instantiate function to bind a variable in the rest of a rule.
            Rules and Facts have fields for supported_by, supports_facts, and supports_rules. Use them to track
            inferences! For example, imagine that a fact F and rule R matched to infer a new fact/rule fr.
            fr is supported by F and R. Add them to fr's supported_by list - you can do this by passing them as a
            constructor argument when creating fr.
            F and R now support fr. Add fr to the supports_rules and supports_facts lists (as appropriate) in F and R.
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])

        # Check binding, use the util.match function to do unification and create possible bindings.
        binding = match(rule.lhs[0], fact.statement)
        lhs_length = len(rule.lhs)

        if binding == False:
            return None


        # One LHS -> Fact
        if lhs_length == 1 and binding != False:
            new_f = Fact(instantiate(rule.rhs, binding), [[rule, fact]])

            if new_f != None:
                kb.kb_add(new_f)
                rule.supports_facts.append(new_f)
                fact.supports_facts.append(new_f)


        # Multiple LHS -> Rule
        elif lhs_length > 1 and binding != False:
            lhs_aux = []
            rule_aux = []

            for i in range(1, lhs_length):
                lhs_aux.append(instantiate(rule.lhs[i], binding))

            rule_aux.append(lhs_aux)
            rule_aux.append(instantiate(rule.rhs, binding))

            new_r = Rule(rule_aux, [[rule, fact]])

            if new_r != None:
                kb.kb_add(new_r)
                rule.supports_rules.append(new_r)
                fact.supports_rules.append(new_r)


        return None
