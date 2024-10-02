from Relation import Relation
from Row import Row
from Header import Header
from typing import Dict
from parser_1 import DatalogProgram
from parser_1 import Predicate
from parser_1 import Parameter
from parser_1 import Rule

class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Dict[str, Relation] = {}
        pass
    
    def run(self, datalog_program: DatalogProgram) -> str:
        self.datalog_program: DatalogProgram = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        self.interpret_rules()
        self.interpret_queries()
        return self.output_str
    
    def interpret_schemes(self) -> None:
        self.database: Dict[str, Relation] = {}
        for scheme in self.datalog_program.schemes:
            name = scheme.name
            header = Header([param.to_string() for param in scheme.parameters])
            rows = set()
            self.database[name] = Relation(name,header,rows)
        pass
    
    def interpret_facts(self) -> None:
        for fact in self.datalog_program.facts:
            relationadd = self.database[fact.name]
            row = Row([param.to_string() for param in fact.parameters])
            relationadd.add_row(row)
        pass
    
    def interpret_queries(self) -> None:
        for query in self.datalog_program.queries:
            self.output_str += f"{query.to_string()}? "
            result = self.evaluate_predicate(query)
            if len(result.rows) == 0:
                self.output_str += "No\n"
            else:
                self.output_str += f"Yes({len(result.rows)})\n"
                self.output_str += str(result)
            print (sorted(self.output_str))
        pass
    
    def evaluate_predicate(self, predicate: Predicate) -> Relation:
        curr_relation = self.database[predicate.name]
        vars_used = {}
        locations: list[int] = []
        attributes: list[Parameter] = []

        for i, param in enumerate(predicate.parameters):
            if param.to_string()[0] == "\'":
                curr_relation = curr_relation.select1(param.to_string(), i)

            elif param.to_string() in vars_used:
                curr_relation = curr_relation.select2(vars_used[param.to_string()], i)

            else:
                vars_used[param.to_string()] = i
                attributes.append(param)
                locations.append(i)

        curr_relation = curr_relation.project(locations)
        curr_relation = curr_relation.rename(Row([param.to_string() for param in attributes]))
        return curr_relation
    
    def interpret_rules(self) -> None:
        new_rules: int = None
        swapped: bool = True
        passes: int = 0
        self.output_str += "Rule Evaluation\n"
        while swapped:
            swapped = False
            for rule in self.datalog_program.rules:
                self.output_str += rule.to_string() + ".\n"
                new_rules = self.evaluate_rule(rule)
                if new_rules != 0:
                    swapped = True
            passes += 1
        self.output_str += f"\nSchemes populated after {passes} passes through the Rules.\n\nQuery Evaluation\n"
    

    
    def evaluate_rule(self, rule: Rule) -> int:
        evaluated_relations: list[Relation] = []
        for body_preds in rule.predicates:
            evaluated_relations.append(self.evaluate_predicate(body_preds))

        joined_relation = evaluated_relations[0]
        if len(evaluated_relations) > 1:
            for i in range(1, len(evaluated_relations)):
                joined_relation = joined_relation.natural_join(evaluated_relations[i])

        # Step 3:
        # Project the columns that appear in the head predicate:
        header: Predicate = rule.head_predicate
        variables: list[Parameter] = header.parameters
        col_indexes = [joined_relation.header.values.index(variable.to_string()) for variable in variables]
        joined_relation = joined_relation.project(col_indexes)

        header_list: list[str] = []
        for x in variables:
            header_list.append(x.to_string())
        new_header = Header(header_list)
        joined_relation.rename(new_header)

        data_relation = self.database[rule.head_predicate.name]
        size_before: int = len(data_relation.rows)

        # Create a copy of the data_relation rows before union
        data_relation_rows_before = data_relation.rows.copy()

        data_relation.rows = data_relation.rows.union(joined_relation.rows)

        # Get the new rows that were added
        new_rows = data_relation.rows - data_relation_rows_before

        # Save the size of the database relation after calling union
        size_after: int = len(data_relation.rows)

        # Check if new rows were added and update output_str
        added_rows = size_after - size_before
        if added_rows != 0:
            # Create a new relation with the new rows
            added_data_relation = Relation(data_relation.name, data_relation.header, new_rows)
            self.output_str += f"{added_data_relation.__str__()}"
        return added_rows