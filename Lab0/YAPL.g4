grammar YAPL;

/*Lexer Rules*/

// skip spaces, tabs, newlines.
WS: [ \t\r\n\f]+ -> skip; 

// comments
LINE_COMMENT:   '--' .*? '\n' -> channel(HIDDEN);
BLOCK_COMMENT:   '(*' (BLOCK_COMMENT|.)*? '*)' -> channel(HIDDEN);

// key words
CLASS : 'CLASS' | 'class';
ELSE : 'ELSE' | 'else';
FI : 'FI' | 'fi';
IF : 'IF' | 'if';
IN : 'IN' | 'in';
INHERITS : 'INHERITS' | 'inherits';
ISVOID : 'ISVOID' | 'isvoid';
LOOP : 'LOOP' | 'loop';
POOL : 'POOL' | 'pool';
THEN : 'THEN' | 'then';
WHILE : 'WHILE' | 'while';
NEW : 'NEW' | 'new';
NOT : 'NOT' | 'not';
TRUE : 'TRUE' | 'true';
FALSE : 'FALSE' | 'false';

// tokens
LET : 'LET' | 'let';
CASE : 'CASE' | 'case';
ESAC : 'ESAC' | 'esac';
OF : 'OF' | 'of';

STRING: '"' (ESC | ~ ["\\])* '"';
INT: [0-9]+;
TYPE: [A-Z][_0-9A-Za-z]*;
ID:[a-z][_0-9A-Za-z]*;
ASSIGNMENT: '<-';
IMPLY: '=>';

fragment ESC: '\\' (["\\/bfnrt] | UNICODE);
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEX: [0-9a-fA-F];

/*Parser Rules*/

program: (classDefine ';')+ EOF;

classDefine: CLASS TYPE (INHERITS TYPE)? '{' (feature ';')* '}';

feature:method | property;

method: ID '(' (formal (',' formal)*)* ')' ':' TYPE '{' expr '}';

property:	formal (ASSIGNMENT expr)?;

formal:ID ':' TYPE;  /* method argument */

expr: expr ('@' TYPE)? '.' ID '(' (expr (',' expr)*)* ')'    #dispatchExplicit
     | ID '(' (expr (',' expr)*)* ')'                        #dispatchImplicit
     | IF expr THEN expr ELSE expr FI                        #if
     | WHILE expr LOOP expr POOL                             #while
     | '{' (expr ';')+ '}'                                   #block
     | CASE expr OF (formal IMPLY expr ';')+ ESAC			 #case
     | NEW TYPE                                              #new
     | '~' expr                                              #negative
     | ISVOID expr                                           #isvoid
     | expr op=('*' | '/') expr                              #arithmetic
     | expr op=('+' | '-') expr                              #arithmetic
     | expr op=('<=' | '<' | '=') expr                       #comparisson
     | NOT expr                                              #boolNot
     | '(' expr ')'                                          #parentheses
     | ID                                                    #id
     | INT                                                   #int
     | STRING                                                #string
     | value=(TRUE | FALSE)                                  #boolean
     | ID ASSIGNMENT expr							 #assignment
     | LET property (',' property)* IN expr				 #letIn
     ;

