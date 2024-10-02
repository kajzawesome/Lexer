from fsa_classes.fsa import FSA
from fsa_classes.colon_dash_fsa import ColonDashFSA
from fsa_classes.colon_dash_fsa import ColonFSA
from fsa_classes.colon_dash_fsa import LeftParenFSA
from fsa_classes.colon_dash_fsa import RightParenFSA
from fsa_classes.colon_dash_fsa import CommaFSA
from fsa_classes.colon_dash_fsa import PeriodFSA
from fsa_classes.colon_dash_fsa import QMarkFSA
from fsa_classes.colon_dash_fsa import MultiplyFSA
from fsa_classes.colon_dash_fsa import AddFSA
from fsa_classes.colon_dash_fsa import SchemesFSA
from fsa_classes.colon_dash_fsa import FactsFSA
from fsa_classes.colon_dash_fsa import RulesFSA
from fsa_classes.colon_dash_fsa import QueriesFSA
from fsa_classes.colon_dash_fsa import IDFSA
from fsa_classes.colon_dash_fsa import StringFSA
from fsa_classes.colon_dash_fsa import CommentFSA
from my_token import Token

class LexerFSM:
    tokens: list[Token]
    automata: list[FSA]

    def __init__(self):
        self.tokens: list[Token] = []
        self.automata: list[FSA] = [ColonDashFSA(),ColonFSA(),LeftParenFSA(),RightParenFSA(),CommaFSA(),PeriodFSA(),QMarkFSA(),
                                    MultiplyFSA(),AddFSA(),SchemesFSA(),FactsFSA(),RulesFSA(),QueriesFSA(),IDFSA(),StringFSA(),CommentFSA()]
        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA()
        self.colon_fsa: ColonFSA = ColonFSA()
        self.left_paren_fsa: LeftParenFSA = LeftParenFSA()
        self.right_paren_fsa: RightParenFSA = RightParenFSA()
        self.comma_fsa: CommaFSA = CommaFSA()
        self.period_fsa: PeriodFSA = PeriodFSA()
        self.qmark_fsa: QMarkFSA = QMarkFSA()
        self.multiply_fsa: MultiplyFSA = MultiplyFSA()
        self.add_fsa: AddFSA = AddFSA()
        self.schemes_fsa: SchemesFSA = SchemesFSA ()
        self.facts_fsa: FactsFSA = FactsFSA()
        self.rules_fsa: RulesFSA = RulesFSA()
        self.queries_fsa: QueriesFSA = QueriesFSA()
        self.id_fsa: IDFSA = IDFSA()
        self.string_fsa: StringFSA = StringFSA()
        self.comment_fsa: CommentFSA = CommentFSA()

        # other FSA classes and any other member variables you need
    
    def run(self, input: str) -> str:
        for automaton in self.automata:
            automaton.reset()
        line_num: int = 1
        undefined = False
        while(input):
            if(input[0].isspace()):
                if(input[0] == "\n"):
                    line_num += 1
                input = input[1:]
                continue

            max_read: int = 0
            max_automaton: FSA = None
            for automaton in self.automata:
                check_run = automaton.run(input)
                num_read: int = automaton.get_num_read()
                if ((num_read > max_read) and (check_run)):
                    max_read = num_read
                    max_automaton = automaton
            if (max_read == 0):
                self.tokens.append(Token("UNDEFINED",input[max_read],line_num))
                break
            else:
                self.tokens.append(Token(max_automaton.get_name(),input[:max_read],line_num))
            input = input[max_read:]
            for automaton in self.automata:
                automaton.reset()
        if undefined == False:
            self.tokens.append(Token("EOF","",line_num))
        else:
            self
        return self.tokens
        
    def reset(self) -> None:
        self.colon_dash_fsa.reset(self)
        self.colon_fsa.reset(self)
        self.left_paren_fsa.reset(self)
        self.right_paren_fsa.reset(self)
        self.comma_fsa.reset(self)
        self.period_fsa.reset(self)
        self.qmark_fsa.reset(self)
        self.multiply_fsa.reset(self)
        self.add_fsa.reset(self)
        self.schemes_fsa.reset(self)
        self.facts_fsa.reset(self)
        self.rules_fsa.reset(self)
        self.queries_fsa.reset(self)
        self.id_fsa.reset(self)
        self.string_fsa.reset(self)
    
    def to_string(self) -> str:
        output: str = ''
        j: int = 0
        for i in self.tokens:
            output = output + i.to_string() + '\n'
            if (i.token_type == "UNDEFINED"):
                output = output + "\nTotal Tokens = Error on line " + str(i.line)
                break
            j += 1  
        else:
            output = output + "Total Tokens = " + str(j)
        return output