import rdflib
import os

# graph for Rule base
g_rb = rdflib.Graph()
RB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RB_V3.n3") 
g_rb.parse(file=open(RB_path, mode="r"), format="text/n3")

# graph for Knowledge base
g_kb = rdflib.Graph()
KB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KB_V3.n3") 
g_kb.parse(file=open(KB_path, mode="r"), format="text/n3")


def rb_sparql_query(condition='owl:oneOf'):
    middle_rules = ['rdf:type', 'a', 'owl:oneOf', 'owl:propertyDisjointWith', 
                    'owl:SourceIndividual', 'owl:AssertionProperty', 'owl:TargetValue', 
                    'rdfs:domain', 'rdfs:range' 
                    ]
    right_rules = ['owl:IrreflexiveProperty', 'owl:AsymmetricProperty', 
                       'owl:TransitiveProperty', 'owl:NegativePropertyAssertion' 
                    ]
    
    if condition in middle_rules:
        prompt = f"""SELECT DISTINCT ?ind_name ?ind_instances WHERE {{?ind_name {condition} ?ind_instances .}}"""
        flag = 'middle_rules'
    elif condition in right_rules:
        prompt = f"""SELECT DISTINCT ?ind_name WHERE {{?ind_name a {condition} .}}"""
        flag = 'right_rules'
    else:
        print(f"!!!!!!!!!!!!!!!!! Condition: '{condition}' not found, need to add to list (middle_rules, right_rules) !!!!!!!!!!!!!")
        prompt = None

    base_query = g_rb.query(prompt)

    inds_list=[]
    ind_instances_list=[]
    for row in base_query:
        if flag == 'middle_rules':
            ind_found = str(row.asdict()['ind_name'].toPython())
            inds_list.append(ind_found)
            ind_instances_found = str(row.asdict()['ind_instances'].toPython())
            ind_instances_list.append(ind_instances_found)
        elif flag == 'right_rules':
            ind_found = str(row.asdict()['ind_name'].toPython())
            inds_list.append(ind_found)

    return inds_list, ind_instances_list


def kb_sparql_query(condition='prop:hasKPI'):
    middle_rules = ['prop:SubProcess', 'rdf:type', 'a', 'rdfs:label', 'rdf:isDefinedBy', 
                    'prop:hasKPI', 'prop:hasInput', 'prop:hasResource', 'hasOutput', 
                    ]
    if condition in middle_rules:
        prompt = f"""SELECT DISTINCT ?ind_name ?ind_instances WHERE {{?ind_name {condition} ?ind_instances .}}"""
    else:
        print(f"!!!!!!!!!!!!!!!!! Condition: '{condition}' not found, need to add to list (middle_rules, right_rules) !!!!!!!!!!!!!")
        prompt = None

    base_query = g_kb.query(prompt)

    inds_list=[]
    ind_instances_list=[]
    for row in base_query:
        ind_found = str(row.asdict()['ind_name'].toPython())
        inds_list.append(ind_found)
        ind_instances_found = str(row.asdict()['ind_instances'].toPython())
        ind_instances_list.append(ind_instances_found)

    return inds_list, ind_instances_list

print('\n', "---------------------New Case owl:oneOf---------------------------")
print("========== RULE owl:oneOf =========")
ind_oneOf, all_oneOf = rb_sparql_query('owl:oneOf')
print(f"List of 'ind:name': {sorted(set(ind_oneOf))}")
print(f"List of 'ind:all_instances': {sorted(set(all_oneOf))}")

print('\n', "========== KB prop:hasKPI =========")
ind_hasKPI, all_hasKPI = kb_sparql_query(condition='prop:hasKPI')
print(f"List of 'ind:name': {sorted(set(ind_hasKPI))}")
print(f"List of 'ind:all_instances': {sorted(set(all_hasKPI))}")

print('\n', "========== KB prop:hasResource =========")
ind_hasResource, all_hasResource = kb_sparql_query(condition='prop:hasResource')
print(f"List of 'ind:name': {sorted(set(ind_hasResource))}")
print(f"List of 'ind:all_instances': {sorted(set(all_hasResource))}")
print()

kb_union = set.union(set(all_hasKPI), set(all_hasResource))
items_in_all_lists = sorted(set.intersection(set(all_oneOf), kb_union))
print(f"Elements in all lists: {items_in_all_lists}")

kb_differences = set.symmetric_difference(set(all_hasKPI), set(all_hasResource))
inconsistencies_list = sorted(set.symmetric_difference(set(all_oneOf), kb_differences))
print(f"INCONSISTENCIES in 'prop:hasKPI' and 'prop:hasResource' by owl:oneOf if exist: {inconsistencies_list}")

print()
print("---------------------New Case owl:IrreflexiveProperty---------------------------")
print("========== RULE owl:IrreflexiveProperty =========")
ind_oneOftest, all_oneOftest = rb_sparql_query(condition='owl:IrreflexiveProperty')
print(f"List of 'ind:name': {sorted(set(ind_oneOftest))}")
print(f"List of 'ind:all_instances': {sorted(set(all_oneOftest))}")

print('\n', "========== KB prop:SubProcess =========")
ind_SubProcess, all_SubProcess = kb_sparql_query(condition='prop:SubProcess')
print(f"List of 'ind:name': {ind_SubProcess}")
print(f"List of 'ind:all_instances': {all_SubProcess}")
inconsistencies_SubProcess = sorted([item[i] for i in range(len(ind_SubProcess)) if ind_SubProcess[i] == all_SubProcess[i]])
print(f"INCONSISTENCIES in 'prop:SubProcess' by owl:IrreflexiveProperty if exist: {inconsistencies_SubProcess}")

print('\n', "========== KB prop:hasKPI =========")
ind_hasKPI, all_hasKPI = kb_sparql_query(condition='prop:hasKPI')
print(f"List of 'ind:name': {ind_hasKPI}")
print(f"List of 'ind:all_instances': {all_hasKPI}")
inconsistencies_hasKPI = sorted([item[i] for i in range(len(ind_SubProcess)) if ind_SubProcess[i] == all_SubProcess[i]])
print(f"INCONSISTENCIES in 'prop:SubProcess' by owl:IrreflexiveProperty if exist: {inconsistencies_hasKPI}")


print()
print("---------------------New Case owl:propertyDisjointWith---------------------------")
print("========== RULE owl:propertyDisjointWith =========")
ind_oneOftest, all_oneOftest = rb_sparql_query(condition='owl:propertyDisjointWith')
print(f"List of 'ind:name': {sorted(set(ind_oneOftest))}")
print(f"List of 'ind:all_instances': {sorted(set(all_oneOftest))}")

print('\n', "========== KB prop:hasKPI =========")
ind_hasKPI, all_hasKPI = kb_sparql_query(condition='prop:hasKPI')
print(f"List of 'ind:name': {sorted(set(ind_hasKPI))}")
print(f"List of 'ind:all_instances': {sorted(set(all_hasKPI))}")

print('\n', "========== KB prop:hasResource =========")
ind_hasResource, all_hasResource = kb_sparql_query(condition='prop:hasResource')
print(f"List of 'ind:name': {sorted(set(ind_hasResource))}")
print(f"List of 'ind:all_instances': {sorted(set(all_hasResource))}")

inconsistencies_hasKPI_DisjointWith = [item for item in all_hasKPI if item in all_hasResource]
inconsistencies_hasResource_DisjointWith = [item for item in ind_hasResource if item in all_hasKPI]
print(f"INCONSISTENCIES ('prop:hasKPI' 'owl:propertyDisjointWith' 'prop:hasResource') if exist: {inconsistencies_hasKPI_DisjointWith + inconsistencies_hasResource_DisjointWith}")


print()
print("---------------------New Case rdfs:domain---------------------------")
print("========== RULE rdfs:domain =========")
ind_domain, all_domain = rb_sparql_query(condition='rdfs:domain')
print(f"List of 'ind:name': {sorted(set(ind_domain))}")
print(f"List of 'ind:all_instances': {sorted(set(all_domain))}")

print('\n', "========== KB a(rdf:type) =========")
ind_type, all_type = kb_sparql_query(condition='rdf:type')
print(f"List of 'ind:name': {ind_type}")
print(f"List of 'ind:all_instances': {all_type}")

inconsistencies_domain_type = [item for item in ind_domain if item not in ind_type]
inconsistencies_domain_type_all = [item for item in all_domain if item not in all_type]
print(f"INCONSISTENCIES ('rdfs:domain' 'rdf:type' ) if exist: {inconsistencies_domain_type + inconsistencies_domain_type_all}")

print()

