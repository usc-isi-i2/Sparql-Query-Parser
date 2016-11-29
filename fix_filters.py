import codecs
import json
import pprint


def is_filters_constraint_object(filters):
    if len(filters) == 1:
        first_filter = filters[0]
        return isinstance(first_filter, dict) and 'constraint' in first_filter
    return False

def is_filters_in_array_format(filters):
    if len(filters) == 1:
        first_filter = filters[0]
        if 'clauses' in first_filter:
            clauses = first_filter['clauses']
            if isinstance(clauses, list):
                for c in clauses:
                    if isinstance(c, list) and len(c) == 3:
                        return True
    return False

def create_fixed_filter_for_constraint_object(filters):
    new_filters = list()
    new_filters_dict = dict()
    new_filters_dict['clauses'] = list()
    new_filters_dict['clauses'].append(filters[0])
    new_filters_dict['operator'] = ['and']
    new_filters.append(new_filters_dict)
    return new_filters


def create_fixed_filter_for_array_clauses(filters):
    new_filters = list()
    new_filters_dict = dict()
    new_filters_dict['clauses'] = list()
    for filter_array in filters[0]['clauses']:
        new_filter_object = {
            'constraint': filter_array[1],
            'operator': filter_array[2],
            'variable': filter_array[0]
        }
        new_filters_dict['clauses'].append(new_filter_object)
    new_filters_dict['operator'] = filters[0]['operator']
    new_filters.append(new_filters_dict)
    return new_filters


def fix_queries_in_file(file_path, output_path):
    sparql_file = codecs.open(file_path, 'r', 'utf-8')

    queries = json.load(sparql_file)
    new_queries = list()
    for q in queries:
        where = q['SPARQL']['where']
        if 'filters' in where:
            filters = where['filters']
            if is_filters_constraint_object(filters):
                new_filters = create_fixed_filter_for_constraint_object(filters)
                where['filters'] = new_filters
            elif is_filters_in_array_format(filters):
                new_filters = create_fixed_filter_for_array_clauses(filters)
                where['filters'] = new_filters
        new_queries.append(q)

    output_file = codecs.open(output_path, 'w', 'utf-8')
    output_file.write(json.dumps(new_queries, indent=True))
    output_file.write('\n')
    output_file.close()



if __name__ == '__main__':
    pp = pprint.PrettyPrinter()

    files = [
        'post_aggregate_parsed',
        'post_cluster_identification-parsed',
        'post_point_fact_parsed',
        'post_cluster_facet_parsed'
    ]

    sparql_root_path = '/Users/pszekely/memex-nov-query/nov-queries-parsed/'

    for file in files:
        input_path = sparql_root_path + file + ".json"
        output_path = sparql_root_path + file + "_fixed.json"
        new_queries = fix_queries_in_file(input_path, output_path)


