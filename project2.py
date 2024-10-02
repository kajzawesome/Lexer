from my_token import Token
from parser_1 import Parser
from lexer_fsm import LexerFSM
from parser_1 import DatalogProgram
#Return your program output here for grading (can treat this function as your "main")
def project2(input: str) -> str:
    tokens: list[Token] = LexerFSM().run(input)
    datalog_program = Parser().run(tokens)

    #if isinstance(datalog_program, DatalogProgram):
    #    return datalog_program.to_string()
    #else:
    return datalog_program

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("Path to input file goes here")
    project2(input_contents)
