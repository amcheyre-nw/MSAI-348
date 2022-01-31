from bayesnet import BayesNet, BayesNode

def ask(var, value, evidence, bn):
	'''
	This function needs to return the probability of a hypothesis given some evidence: P(H|E)
	var: is the name of the hyptothesis variable.
	value: indicates whether the hypothesis being asked about is True or False.
	evidence: set of variables known to be True or False.
	bn: BayesNet (in the provided module) pertaining to the problem (bn.variables -> all the variables in the Bayes net)
	P (H|E), ask should calculate and return P (H,E)/alfa
	P (b,e,a) = P(b)*P(e,a|b)
	To implement this recursion you may want to introduce a new function. That function takes the list of variables in
	the joint probability and the collection of all known variable values. Conditions:
		• Recursion is done (i.e., it can end) if there are no more variables in the list.
		• The next variable in the list has a known value (it is in the evidence) ->  lookup the probability in the
		Conditional Probabibility Table (CPT) using the function probability in BayesNode
		• The value of the next variable is not known.

	αlpha = P (a, b) + P (¬a, b) -> alpha of P(a|b)
	BayesNet -> variables field, which is an iterator of all of the variables in the net
	BayesNode -> name and evidence, also probability function
	'''
	chain = evaluate_chain(var, value, evidence, bn)
	a = calculate_alpha(var, value, evidence, bn)
	probability_hypothesis = chain * a

	return probability_hypothesis

def evidence_known(var, value, evidence, bn):
       evidence_dict = {}
       evidence_dict[var]=value
       if evidence != {}:
              for i,j in evidence.items():
                     evidence_dict[i]=j
       return evidence_dict

def evidence_all(var, value, evidence, bn):
       evidence_dict = {}
       evidence_dict[var]=value
       if evidence != {}:
              for i,j in evidence.items():
                     evidence_dict[i]=j
       for variable in bn.variables:
              if variable.name not in evidence_dict.keys():
                     evidence_dict[variable.name] = 'Unknown'
       return evidence_dict


def chain_rule(var, value, evidence, bn):
       chain_dictionary = {}
       known_evidence = evidence_known(var, value, evidence,bn)

       for x in known_evidence.keys():
              for y in bn.variables:
                     if x == y.name:
                            chain_dictionary[y.name] = y.parents


       # Check parents of parents ROUND 1
       aux1={}
       for key, value in chain_dictionary.items():
              if value != None:
                     for parent in value:
                            for y in bn.variables:
                                   if parent == y.name and parent not in chain_dictionary.keys():
                                          aux1[y.name] = y.parents
       # Check parents of parents ROUND 2
       aux2={}
       for key, value in aux1.items():
              if value != None:
                     for parent in value:
                            for y in bn.variables:
                                   if parent == y.name and parent not in chain_dictionary.keys() and parent not in aux1.keys():
                                          aux2[y.name] = y.parents

       for key, value in aux1.items():
              chain_dictionary[key] = value

       for key, value in aux2.items():
              chain_dictionary[key] = value

       return chain_dictionary

def evaluate_chain(var, value, evidence, bn):
       all_evidence = evidence_all(var, value, evidence, bn)
       chain = chain_rule(var, value, evidence, bn)
       relevant_variables = list(chain.keys())
       relevant_evidence = {}
       for x in relevant_variables:
              for i,j in all_evidence.items():
                     if x == i:
                            relevant_evidence[i]=j

       # For Unknown we are going to make different scenarios to calculate probabilities
       scenarios = []
       scenarios.append(relevant_evidence)

       stop = False
       while stop == False:
              aux_scenarios = []
              for s in scenarios:
                     aux_true = s.copy()
                     aux_false = s.copy()
                     unknown = 0
                     for i, j in s.items():
                            if j == 'Unknown':
                                   unknown = unknown + 1
                                   aux_true[i] = True
                                   aux_false[i] = False
                                   aux_scenarios.append(aux_true)
                                   aux_scenarios.append(aux_false)
                                   break
                     if unknown == 0:
                            stop = True
              if aux_scenarios != []:
                     scenarios = aux_scenarios

       print(scenarios, "This is final scenarios")

       # Now we calculate the probabilities
       print(chain)
       probabilities = []

       for sc in scenarios:
              prob_scenario = []
              for x, y in chain.items():
                     for v in sc:
                            for variable in bn.variables:
                                   if x == variable.name and v == variable.name:
                                          v_boolean = sc[v]
                                          prob = variable.probability(v_boolean, sc)
                                          prob_scenario.append(prob)
              probabilities.append(prob_scenario)

       probability_chain = 0
       for i in probabilities:
              prob_scen = 1
              for j in i:
                     prob_scen = prob_scen * j
              probability_chain = prob_scen + probability_chain

       return probability_chain



def calculate_alpha(var, value, evidence, bn):
       chain_1 = evaluate_chain(var, value, evidence, bn)
       if value == True: value2 = False
       if value == False: value2 = True
       chain_2 = evaluate_chain(var, value2, evidence, bn)

       alpha = 1 / (chain_1 + chain_2)

       return alpha


