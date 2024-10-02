from my_token import Token


class Parameter():

    def __init__(self, value: str, is_id: bool):
        self.value = value
        self.is_id = is_id

    def to_string(self):
        return self.value


class Predicate():
    def __init__(self, name: str, parameters: list[Parameter]):
        self.name = name
        self.parameters = parameters
    
    def to_string(self):
        parameters_str: str = [param.to_string() for param in self.parameters]
        parameters_str = ','.join(parameters_str)
        return(f'{self.name}({parameters_str})')
    

class Rule():

    def __init__(self, headpredicate: Predicate, parameters: list[Predicate]) -> None:
        self.head_predicate: Predicate = headpredicate
        self.predicates: list[Predicate] = parameters

    def to_string(self):
        predicates_str = ','.join(pred.to_string() for pred in self.predicates)
        return f'{self.head_predicate.to_string()} :- {predicates_str}'
    

class DatalogProgram():

    def __init__(self, schemes: list[Predicate], facts: list[Predicate], rules: list[Rule], queries: list[Predicate]):
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries
        

    def to_string(self):
        string: str = "Success!\n"
        string += ("Schemes(" + str(len(self.schemes)) + '):\n')
        for i in range(len(self.schemes)):
            string += ("  " + self.schemes[i].to_string() + '\n')
        string += ("Facts(" + str(len(self.facts)) + "):\n")
        for i in range(len(self.facts)):
            string += ("  " + self.facts[i].to_string() + '.\n')
        string += ("Rules(" + str(len(self.rules)) + "):\n")
        for i in range(len(self.rules)):
            string += ("  " + self.rules[i].to_string() + '.\n')
        string += ("Queries(" + str(len(self.queries)) + "):\n")
        for i in range(len(self.queries)):
            string += ("  " + self.queries[i].to_string() + '?\n')
        domain = set()
        for i in range(len(self.facts)):
            for j in range(len(self.facts[i].parameters)):
                domain.add(self.facts[i].parameters[j].to_string())
        domain = sorted(domain)
        string += ("Domain(" + str(len(domain)) + "):\n")
        for i in range(len(domain)):
            string += ("  " + domain[i] + '\n')
        return string
        


class Parser():
    def __init__(self):
        self.first: dict[str, set[str]] = dict()
        self.follow: dict[str, set[str]] = dict()
        self.datalogprogram = None

    def throw_error(self):
        raise ValueError(self.get_curr_token().to_string())

    def get_curr_token(self) -> Token:
        if (self.index >= len(self.tokens)):
            self.index = len(self.tokens) - 1
            self.throw_error()
        return self.tokens[self.index]
        
    def get_prev_token_val(self) -> str:
        return self.tokens[self.index - 1].value

    def advance(self):
        self.index += 1

    def skipComments(self):
        while(self.get_curr_token().token_type == "COMMENT"):
            self.advance()

    def match(self, expected_type: str):
        self.skipComments()
        if (self.get_curr_token().token_type == expected_type):
            self.advance()
        else:
            self.throw_error()


    def run(self, tokens: list[Token]) -> DatalogProgram:
        self.index: int = 0
        self.tokens: list[Token] = tokens
        #self.datalogprogram = DatalogProgram()
        try:
            self.datalogprogram = self.parse_datalog_program()
            return self.datalogprogram.to_string()
        except ValueError as error_msg:
            return f"Failure!\n  {error_msg}"

    def get_program(self):
        return self.datalogprogram

    def parse_datalog_program(self) -> DatalogProgram:
        self.skipComments()
        self.match("SCHEMES")
        self.match("COLON")
        scheme: list[Predicate] = []
        scheme.append(self.parse_scheme())
        scheme += self.parse_Scheme_list()
        self.match("FACTS")
        self.match("COLON")
        facts: list[Predicate] = []
        facts += self.parse_Fact_list()
        self.match("RULES")
        self.match("COLON")
        rules: list[Rule] = []
        rules += self.parse_Rule_list()
        self.match("QUERIES")
        self.match("COLON")
        queries: list[Predicate] = []
        queries.append(self.parse_query())
        queries += self.parse_Query_list()
        self.match("EOF")
        return DatalogProgram(scheme, facts, rules, queries)

    def parse_Scheme_list(self) -> Predicate:
        self.follow["schemeList"] = {"FACTS"}
        self.first["schemeList"] = {"ID"}
        schemes: list[Predicate] = []

        self.skipComments()
        if self.get_curr_token().token_type in self.first["schemeList"]:
            schemes.append(self.parse_scheme())
            schemes += self.parse_Scheme_list()
        elif self.get_curr_token().token_type in self.follow["schemeList"]: 
            return schemes
        else:
            self.throw_error()
        return schemes
        
    def parse_Rule_list(self) -> Rule:
        self.follow["ruleList"] = {"QUERIES"}
        self.first["ruleList"] = {"ID"}
        rule: list[Rule] = []

        self.skipComments()
        if self.get_curr_token().token_type in self.first["ruleList"]:
            rule.append(self.parse_rule())
            rule += self.parse_Rule_list()
        elif self.get_curr_token().token_type in self.follow["ruleList"]:
            return rule
        else:
            self.throw_error()
        return rule
        
    def parse_Query_list(self) -> Predicate:
        self.follow["queryList"] = {"EOF"}
        self.first["queryList"] = {"ID"}
        query: list[Predicate] = []

        self.skipComments()
        if self.get_curr_token().token_type in self.first["queryList"]:
            query.append(self.parse_query())
            query += self.parse_Query_list()
        elif self.get_curr_token().token_type in self.follow["queryList"]:
            return []
        else:
            self.throw_error()
        return query
        
    def parse_Fact_list(self) -> Predicate:
        self.follow["factList"] = {"RULES"}
        self.first["factList"] = {"ID"}
        fact: list[Predicate] = []

        self.skipComments()
        if self.get_curr_token().token_type in self.first["factList"]:
            fact.append(self.parse_fact())
            fact += self.parse_Fact_list()
        elif self.get_curr_token().token_type in self.follow["factList"]:
            return []
        else:
            self.throw_error()
        return fact

#-------

    # scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_scheme(self) -> Predicate:
        name = ""
        parameters_list: list[Parameter] = []

        self.skipComments()
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters_list.append(Parameter(self.get_prev_token_val(), True))
        parameters_list += self.parse_id_list()  # Use += to concatenate lists

        self.match("RIGHT_PAREN")
        return Predicate(name, parameters_list)
    
    def parse_fact(self) -> Predicate:
        name = ""
        parameters_list: list[Parameter] = []

        self.skipComments()
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("STRING")
        parameters_list.append(Parameter(self.get_prev_token_val(),False))
        parameters_list += self.parse_string_list()
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        return Predicate(name, parameters_list) 
    
    def parse_rule(self) -> Rule:
        parameters: list[Predicate] = []

        self.skipComments()
        name: Predicate = self.head_predicate()
        self.match("COLON_DASH")
        parameters.append(self.parse_predicate())
        parameters += self.parse_predicate_list()
        self.match("PERIOD")
        
        return Rule(name, parameters)
    
    def parse_query(self) -> Predicate:
        self.skipComments()
        predicatequery = self.parse_predicate()  #how to call this right? is correct return type?
        self.match("Q_MARK")
        return predicatequery

#------------

    def head_predicate(self) -> Predicate:
        name = ""
        parameters: list[Parameter] = []

        self.skipComments()
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(Parameter(self.get_prev_token_val(),True))
        parameters += self.parse_id_list()
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)
    
    def parse_predicate(self) -> Predicate:
        parameters: list[Parameter] = []
        name: str = ''

        self.skipComments()
        self.match("ID")
        name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        parameters.append(self.parse_parameter())
        parameters += self.parse_parameter_list()
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)

#------------

# idList  	-> 	COMMA ID idList | lambda
    def parse_id_list(self) -> list[Parameter]:
        self.skipComments()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("ID")
            current_id = [Parameter(self.get_prev_token_val(), is_id=True)]
            rest_ids = self.parse_id_list()
            return current_id + rest_ids
        else:
            return []

    def parse_string_list(self) -> list[Parameter]:
        self.skipComments()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            current_string = [Parameter(self.get_prev_token_val(), is_id=False)]
            rest_strings = self.parse_string_list()
            return current_string + rest_strings
        else:
            return []

    def parse_predicate_list(self):
        predicates: list[Predicate]
        self.follow["predicateList"] = {"PERIOD"}
        self.skipComments()
        if self.get_curr_token().token_type in self.follow["predicateList"]:
            return []
        else:
            self.match("COMMA")
            predicates = [self.parse_predicate()]
            predicates += self.parse_predicate_list()
            return predicates

    def parse_parameter_list(self):
        self.follow["parameterList"] = {"RIGHT_PAREN"}
        parameters: list[Parameter] = []
        
        if(self.get_curr_token().token_type == "COMMA"): 
            self.match("COMMA")
            parameters = [self.parse_parameter()]
            parameters += self.parse_parameter_list()
            return parameters
        
        elif self.get_curr_token().token_type in self.follow["parameterList"]:
            return parameters

    def parse_parameter(self) -> Parameter:
        self.skipComments()
        if(self.get_curr_token().token_type == "STRING"):
            self.match("STRING")
            is_id = False
            return Parameter(self.get_prev_token_val(), is_id)
        elif(self.get_curr_token().token_type == "ID"):
            self.match("ID")
            is_id = True
            return Parameter(self.get_prev_token_val(), is_id)