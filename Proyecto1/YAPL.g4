grammar YAPL;

/*Reglas Lexicas*/

// espacios en blanco
WHITESPACE: [ \t\r\n\f]+ -> skip; 

// comentarios
BLOCK_COMMENT: '(*' (BLOCK_COMMENT|.)*? '*)'   -> channel(HIDDEN);
LINE_COMMENT: '--' .*? '\n'                   -> channel(HIDDEN);

// palabras reservadas
CLASS: 'CLASS' | 'class';
ELSE: 'ELSE' | 'else';
FALSE: 'false';
FI: 'FI' | 'fi';
IF: 'IF' | 'if';
IN: 'IN' | 'in';
INHERITS: 'INHERITS' | 'inherits';
ISVOID: 'ISVOID' | 'isvoid';
LET: 'LET' | 'let';
LOOP: 'LOOP' | 'loop';
POOL: 'POOL' | 'pool';
THEN: 'THEN' | 'then';
WHILE: 'WHILE' | 'while';
CASE: 'CASE' | 'case';
ESAC: 'ESAC' | 'esac';
NEW: 'NEW' | 'new';
OF: 'OF' | 'of';
NOT: 'NOT' | 'not';
TRUE: 'true';

// tipos de variables
STRING: '"' (ESC | ~ ["\\])* '"';
INT: [0-9]+;
TYPE: [A-Z][_0-9A-Za-z]*;
ID: [a-z][_0-9A-Za-z]*;
ASSIGNMENT: '<-';
IMPLY: '=>';

fragment ESC: '\\' (["\\/bfnrt] | UNICODE);
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEX: [0-9a-fA-F];

// errores
ERROR: .;

// Catch-all rule for unrecognized characters
UNRECOGNIZED: . -> channel(HIDDEN), type(ERROR);

/*Reglas Sintacticas*/

program: (classDefine ';')+ EOF;

classDefine: CLASS TYPE (INHERITS TYPE)? '{' (feature_list ';')* '}';

feature_list: method | property;

method: ID '(' (formal (',' formal)*)* ')' ':' TYPE '{' expr '}';

property:	formal (ASSIGNMENT expr)?;

varDeclaration: ID ASSIGNMENT expr; 

formal: ID ':' TYPE;  /* method argument */

expr: expr ('@' TYPE)? '.' ID '(' (expr (',' expr)*)* ')' #dispatchExplicit
          | ID '(' (expr (',' expr)*)* ')'                #dispatchImplicit
          | IF expr THEN expr ELSE expr FI                #if
          | WHILE expr LOOP expr POOL                     #while
          | '{' (expr ';')+ '}'                           #block
          | CASE expr OF (formal IMPLY expr ';')+ ESAC    #case
          | NEW TYPE                                      #new
          | '~' expr                                      #negative
          | ISVOID expr                                   #isvoid
          | expr op=('*' | '/') expr                      #arithmetic
          | expr op=('+' | '-') expr                      #arithmetic
          | expr op=('<=' | '<' | '=') expr               #comparisson
          | NOT expr                                      #boolNot
          | '(' expr ')'                                  #parentheses
          | ID                                            #id
          | INT                                           #int
          | STRING                                        #string
          | value=(TRUE | FALSE)                          #boolean
          | varDeclaration					        #assignment
          | LET property (',' property)* IN expr		   #letIn
		;