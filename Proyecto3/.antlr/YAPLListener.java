// Generated from c:/Users/rjmom/OneDrive/Documentos/GitHub/Construccion-Compiladores/Proyecto3/YAPL.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link YAPLParser}.
 */
public interface YAPLListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link YAPLParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(YAPLParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(YAPLParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link YAPLParser#classDefine}.
	 * @param ctx the parse tree
	 */
	void enterClassDefine(YAPLParser.ClassDefineContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#classDefine}.
	 * @param ctx the parse tree
	 */
	void exitClassDefine(YAPLParser.ClassDefineContext ctx);
	/**
	 * Enter a parse tree produced by {@link YAPLParser#feature_list}.
	 * @param ctx the parse tree
	 */
	void enterFeature_list(YAPLParser.Feature_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#feature_list}.
	 * @param ctx the parse tree
	 */
	void exitFeature_list(YAPLParser.Feature_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link YAPLParser#method}.
	 * @param ctx the parse tree
	 */
	void enterMethod(YAPLParser.MethodContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#method}.
	 * @param ctx the parse tree
	 */
	void exitMethod(YAPLParser.MethodContext ctx);
	/**
	 * Enter a parse tree produced by {@link YAPLParser#property}.
	 * @param ctx the parse tree
	 */
	void enterProperty(YAPLParser.PropertyContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#property}.
	 * @param ctx the parse tree
	 */
	void exitProperty(YAPLParser.PropertyContext ctx);
	/**
	 * Enter a parse tree produced by {@link YAPLParser#varDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterVarDeclaration(YAPLParser.VarDeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#varDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitVarDeclaration(YAPLParser.VarDeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link YAPLParser#formal}.
	 * @param ctx the parse tree
	 */
	void enterFormal(YAPLParser.FormalContext ctx);
	/**
	 * Exit a parse tree produced by {@link YAPLParser#formal}.
	 * @param ctx the parse tree
	 */
	void exitFormal(YAPLParser.FormalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code new}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNew(YAPLParser.NewContext ctx);
	/**
	 * Exit a parse tree produced by the {@code new}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNew(YAPLParser.NewContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parentheses}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParentheses(YAPLParser.ParenthesesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parentheses}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParentheses(YAPLParser.ParenthesesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code letIn}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterLetIn(YAPLParser.LetInContext ctx);
	/**
	 * Exit a parse tree produced by the {@code letIn}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitLetIn(YAPLParser.LetInContext ctx);
	/**
	 * Enter a parse tree produced by the {@code string}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterString(YAPLParser.StringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code string}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitString(YAPLParser.StringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code isvoid}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIsvoid(YAPLParser.IsvoidContext ctx);
	/**
	 * Exit a parse tree produced by the {@code isvoid}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIsvoid(YAPLParser.IsvoidContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignment}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(YAPLParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignment}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(YAPLParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by the {@code arithmetic}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterArithmetic(YAPLParser.ArithmeticContext ctx);
	/**
	 * Exit a parse tree produced by the {@code arithmetic}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitArithmetic(YAPLParser.ArithmeticContext ctx);
	/**
	 * Enter a parse tree produced by the {@code while}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterWhile(YAPLParser.WhileContext ctx);
	/**
	 * Exit a parse tree produced by the {@code while}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitWhile(YAPLParser.WhileContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dispatchImplicit}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterDispatchImplicit(YAPLParser.DispatchImplicitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dispatchImplicit}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitDispatchImplicit(YAPLParser.DispatchImplicitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code int}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterInt(YAPLParser.IntContext ctx);
	/**
	 * Exit a parse tree produced by the {@code int}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitInt(YAPLParser.IntContext ctx);
	/**
	 * Enter a parse tree produced by the {@code negative}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNegative(YAPLParser.NegativeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code negative}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNegative(YAPLParser.NegativeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code boolNot}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterBoolNot(YAPLParser.BoolNotContext ctx);
	/**
	 * Exit a parse tree produced by the {@code boolNot}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitBoolNot(YAPLParser.BoolNotContext ctx);
	/**
	 * Enter a parse tree produced by the {@code boolean}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterBoolean(YAPLParser.BooleanContext ctx);
	/**
	 * Exit a parse tree produced by the {@code boolean}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitBoolean(YAPLParser.BooleanContext ctx);
	/**
	 * Enter a parse tree produced by the {@code block}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterBlock(YAPLParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by the {@code block}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitBlock(YAPLParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by the {@code comparisson}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterComparisson(YAPLParser.ComparissonContext ctx);
	/**
	 * Exit a parse tree produced by the {@code comparisson}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitComparisson(YAPLParser.ComparissonContext ctx);
	/**
	 * Enter a parse tree produced by the {@code id}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterId(YAPLParser.IdContext ctx);
	/**
	 * Exit a parse tree produced by the {@code id}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitId(YAPLParser.IdContext ctx);
	/**
	 * Enter a parse tree produced by the {@code if}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIf(YAPLParser.IfContext ctx);
	/**
	 * Exit a parse tree produced by the {@code if}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIf(YAPLParser.IfContext ctx);
	/**
	 * Enter a parse tree produced by the {@code case}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterCase(YAPLParser.CaseContext ctx);
	/**
	 * Exit a parse tree produced by the {@code case}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitCase(YAPLParser.CaseContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dispatchExplicit}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterDispatchExplicit(YAPLParser.DispatchExplicitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dispatchExplicit}
	 * labeled alternative in {@link YAPLParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitDispatchExplicit(YAPLParser.DispatchExplicitContext ctx);
}