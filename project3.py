#from Relation import Relation
#from Header import Header
#from Row import Row
from Interpreter import Interpreter
from lexer_fsm import LexerFSM
from my_token import Token
from parser_1 import Parser
from parser_1 import DatalogProgram

#Return your program output here for grading (can treat this function as your "main")
def project3(input: str) -> str:
    lexer: LexerFSM = LexerFSM()
    lexer.run(input)
    tokens: list[Token] = lexer.tokens

    parser: Parser = Parser()
    parser.run(tokens)
    datalog_program: DatalogProgram = parser.get_program()

    interpreter: Interpreter = Interpreter()
    result = interpreter.run(datalog_program)
    return result

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("Path to input file goes here")
    project3(input_contents)
