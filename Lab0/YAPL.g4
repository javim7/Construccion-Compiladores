grammar YAPL;


/*Reglas Lexicas*/

// espacios en blanco
WHITESPACE      :   [ \t\r\n\f]+ -> skip; 

// comentarios
BLOCK_COMMENT   :   '(*' (BLOCK_COMMENT|.)*? '*)'   -> channel(HIDDEN);
LINE_COMMENT    :   '--' .*? '\n'                   -> channel(HIDDEN);

// palabras reservadas
CLASS: 'class' | 'CLASS';
ELSE: 'else' | 'ELSE';
FALSE: 'false';
FI: 'FI' | 'fi' ;
IF: 'if' | 'IF';
IN: 'in' | 'IN';
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
STRING              :           '"' (ESC | ~ ["\\])* '"';
INT                 :           [0-9]+;
TYPE                :           [A-Z][_0-9A-Za-z]*;
ID                  :           [a-z][_0-9A-Za-z]*;
ASSIGNMENT          :           '<-';
IMPLY               :           '=>';

fragment ESC: '\\' (["\\/bfnrt] | UNICODE);
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEX: [0-9a-fA-F];

/*Reglas Sintacticas*/

program			:       (classDefine ';')+ EOF
				;

classDefine     :       CLASS TYPE (INHERITS TYPE)? '{' (feature ';')* '}'
                ;

feature         :       method
                |       property
                ;

method			:		ID '(' (formal (',' formal)*)* ')' ':' TYPE '{' expression '}'
				;

property		:		formal (ASSIGNMENT expression)?
				;

formal          :       ID ':' TYPE;  /* method argument */

expression      :       expression ('@' TYPE)? '.' ID '(' (expression (',' expression)*)* ')'                                       #dispatchExplicit
                |       ID '(' (expression (',' expression)*)* ')'                                                                  #dispatchImplicit
                |       IF expression THEN expression ELSE expression FI                                                            #if
                |       WHILE expression LOOP expression POOL                                                                       #while
                |       '{' (expression ';')+ '}'                                                                                   #block
                |       CASE expression OF (formal IMPLY expression ';')+ ESAC														#case
                |       NEW TYPE                                                                                                    #new
                |       '~' expression                                                                                              #negative
                |       ISVOID expression                                                                                           #isvoid
                |       expression op=('*' | '/') expression                                                                        #arithmetic
                |       expression op=('+' | '-') expression                                                                        #arithmetic
                |       expression op=('<=' | '<' | '=') expression                                                                 #comparisson
                |       NOT expression                                                                                              #boolNot
                |       '(' expression ')'                                                                                          #parentheses
                |       ID                                                                                                          #id
                |       INT                                                                                                         #int
                |       STRING                                                                                                      #string
                |       value=(TRUE | FALSE)                                                                                        #boolean
                |       ID ASSIGNMENT expression																					#assignment
                |       LET property (',' property)* IN expression																	#letIn
			;

// errores
ERROR: .;