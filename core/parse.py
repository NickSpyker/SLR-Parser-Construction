from core.grammar.context_free_grammar import ContextFreeGrammar
from core.grammar.production import Production
from core.grammar.actions import ActionsTable
from core.lexer.lexer import Lexer, ScanState
from core.grammar.goto import GotoTable
from core.lexer.token import TokenType
from core.error.error import Error
from typing import List


PRODUCTIONS: List[Production] = [
    Production('Program', ('DeclList',)),  # 1
    Production('DeclList', ('Decl', 'DeclList')),  # 2
    Production('DeclList', ()),  # 3
    Production('Decl', ('VarDecl',)),  # 4
    Production('Decl', ('FuncDecl',)),  # 5
    Production('VarDecl', (TokenType.TYPE, TokenType.IDENTIFIER, TokenType.SEMICOLON)),  # 6
    Production('VarDecl', (TokenType.TYPE, TokenType.IDENTIFIER, TokenType.ASSIGN, 'Expr', TokenType.SEMICOLON)),  # 7
    Production('FuncDecl', (TokenType.TYPE, TokenType.IDENTIFIER, TokenType.LEFT_PAREN, 'ParamList', TokenType.RIGHT_PAREN, 'Block')),  # 8
    Production('ParamList', ('Param', 'ParamTail')),  # 9
    Production('ParamList', ()),  # 10
    Production('ParamTail', (TokenType.COMMA, 'Param', 'ParamTail')),  # 11
    Production('ParamTail', ()),  # 12
    Production('Param', (TokenType.TYPE, TokenType.IDENTIFIER)),  # 13
    Production('Block', (TokenType.LEFT_BRACE, 'StmtList', TokenType.RIGHT_BRACE)),  # 14
    Production('StmtList', ('Stmt', 'StmtList')),  # 15
    Production('StmtList', ()),  # 16
    Production('Stmt', ('MatchedStmt',)),  # 17
    Production('Stmt', ('UnmatchedStmt',)),  # 18
    Production('MatchedStmt', (TokenType.IF, TokenType.LEFT_PAREN, 'Expr', TokenType.RIGHT_PAREN, 'MatchedStmt', TokenType.ELSE, 'MatchedStmt')),  # 19
    Production('MatchedStmt', (TokenType.WHILE, TokenType.LEFT_PAREN, 'Expr', TokenType.RIGHT_PAREN, 'MatchedStmt')),  # 20
    Production('MatchedStmt', (TokenType.FOR, TokenType.LEFT_PAREN, 'Expr', TokenType.SEMICOLON, 'Expr', TokenType.SEMICOLON, 'Expr', TokenType.RIGHT_PAREN, 'MatchedStmt')),  # 21
    Production('MatchedStmt', (TokenType.RETURN, 'Expr', TokenType.SEMICOLON)),  # 22
    Production('MatchedStmt', ('VarDecl',)),  # 23
    Production('MatchedStmt', ('ExprStmt',)),  # 24
    Production('MatchedStmt', ('Block',)),  # 25
    Production('UnmatchedStmt', (TokenType.IF, TokenType.LEFT_PAREN, 'Expr', TokenType.RIGHT_PAREN, 'Stmt')),  # 26
    Production('UnmatchedStmt', (TokenType.IF, TokenType.LEFT_PAREN, 'Expr', TokenType.RIGHT_PAREN, 'MatchedStmt', TokenType.ELSE, 'UnmatchedStmt')),  # 27
    Production('UnmatchedStmt', (TokenType.WHILE, TokenType.LEFT_PAREN, 'Expr', TokenType.RIGHT_PAREN, 'UnmatchedStmt')),  # 28
    Production('UnmatchedStmt', (TokenType.FOR, TokenType.LEFT_PAREN, 'Expr', TokenType.SEMICOLON, 'Expr', TokenType.SEMICOLON, 'Expr', TokenType.RIGHT_PAREN, 'UnmatchedStmt')),  # 29
    Production('ExprStmt', (TokenType.IDENTIFIER, TokenType.ASSIGN, 'Expr', TokenType.SEMICOLON)),  # 30
    Production('Expr', ('EqualityExpr',)),  # 31
    Production('EqualityExpr', ('AdditiveExpr',)),  # 32
    Production('EqualityExpr', ('AdditiveExpr', TokenType.COMPARE, 'EqualityExpr')),  # 33
    Production('AdditiveExpr', ('MultiplicativeExpr',)),  # 34
    Production('AdditiveExpr', ('AdditiveExpr', TokenType.PLUS, 'MultiplicativeExpr')),  # 35
    Production('MultiplicativeExpr', ('UnaryExpr',)),  # 36
    Production('MultiplicativeExpr', ('MultiplicativeExpr', TokenType.MULTIPLY, 'UnaryExpr')),  # 37
    Production('UnaryExpr', (TokenType.MINUS, 'UnaryExpr')),  # 38
    Production('UnaryExpr', ('PrimaryExpr',)),  # 39
    Production('PrimaryExpr', (TokenType.IDENTIFIER, TokenType.LEFT_PAREN, 'ArgList', TokenType.RIGHT_PAREN)),  # 40
    Production('PrimaryExpr', (TokenType.IDENTIFIER,)),  # 41
    Production('PrimaryExpr', (TokenType.NUMBER,)),  # 42
    Production('PrimaryExpr', (TokenType.LEFT_PAREN, 'Expr', TokenType.RIGHT_PAREN)),  # 43
    Production('ArgList', ('Expr', TokenType.COMMA, 'ArgList')),  # 44
    Production('ArgList', ('Expr',)),  # 45
    Production('ArgList', ()),  # 46
]


SMALL_PRODUCTIONS: List[Production] = [
    Production('S', ('E',)),
    Production('E', ('E', TokenType.PLUS, 'T')),
    Production('E', ('T',)),
    Production('T', ('T', TokenType.MULTIPLY, 'F')),
    Production('T', ('F',)),
    Production('F', (TokenType.LEFT_PAREN, 'E', TokenType.RIGHT_PAREN)),
    Production('F', (TokenType.IDENTIFIER,)),
]


def parse(buffer: str) -> str:
    lexer = Lexer(buffer)
    tokens = lexer.scan()
    if lexer.scan_state == ScanState.FAILURE:
        return Error.build_lexer_error_msg(lexer)
    cfg = ContextFreeGrammar(start_symbol="S", productions=SMALL_PRODUCTIONS)
    actions_table = ActionsTable(cfg)
    goto_table = GotoTable(cfg)
    return f"{actions_table}\n\n{goto_table}"
