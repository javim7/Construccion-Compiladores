# Generated from YAPL.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete listener for a parse tree produced by YAPLParser.
class YAPLListener(ParseTreeListener):

    # Enter a parse tree produced by YAPLParser#program.
    def enterProgram(self, ctx:YAPLParser.ProgramContext):
        pass

    # Exit a parse tree produced by YAPLParser#program.
    def exitProgram(self, ctx:YAPLParser.ProgramContext):
        pass


    # Enter a parse tree produced by YAPLParser#classDefine.
    def enterClassDefine(self, ctx:YAPLParser.ClassDefineContext):
        pass

    # Exit a parse tree produced by YAPLParser#classDefine.
    def exitClassDefine(self, ctx:YAPLParser.ClassDefineContext):
        pass


    # Enter a parse tree produced by YAPLParser#feature.
    def enterFeature(self, ctx:YAPLParser.FeatureContext):
        pass

    # Exit a parse tree produced by YAPLParser#feature.
    def exitFeature(self, ctx:YAPLParser.FeatureContext):
        pass


    # Enter a parse tree produced by YAPLParser#method.
    def enterMethod(self, ctx:YAPLParser.MethodContext):
        pass

    # Exit a parse tree produced by YAPLParser#method.
    def exitMethod(self, ctx:YAPLParser.MethodContext):
        pass


    # Enter a parse tree produced by YAPLParser#property.
    def enterProperty(self, ctx:YAPLParser.PropertyContext):
        pass

    # Exit a parse tree produced by YAPLParser#property.
    def exitProperty(self, ctx:YAPLParser.PropertyContext):
        pass


    # Enter a parse tree produced by YAPLParser#formal.
    def enterFormal(self, ctx:YAPLParser.FormalContext):
        pass

    # Exit a parse tree produced by YAPLParser#formal.
    def exitFormal(self, ctx:YAPLParser.FormalContext):
        pass


    # Enter a parse tree produced by YAPLParser#new.
    def enterNew(self, ctx:YAPLParser.NewContext):
        pass

    # Exit a parse tree produced by YAPLParser#new.
    def exitNew(self, ctx:YAPLParser.NewContext):
        pass


    # Enter a parse tree produced by YAPLParser#parentheses.
    def enterParentheses(self, ctx:YAPLParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by YAPLParser#parentheses.
    def exitParentheses(self, ctx:YAPLParser.ParenthesesContext):
        pass


    # Enter a parse tree produced by YAPLParser#letIn.
    def enterLetIn(self, ctx:YAPLParser.LetInContext):
        pass

    # Exit a parse tree produced by YAPLParser#letIn.
    def exitLetIn(self, ctx:YAPLParser.LetInContext):
        pass


    # Enter a parse tree produced by YAPLParser#string.
    def enterString(self, ctx:YAPLParser.StringContext):
        pass

    # Exit a parse tree produced by YAPLParser#string.
    def exitString(self, ctx:YAPLParser.StringContext):
        pass


    # Enter a parse tree produced by YAPLParser#isvoid.
    def enterIsvoid(self, ctx:YAPLParser.IsvoidContext):
        pass

    # Exit a parse tree produced by YAPLParser#isvoid.
    def exitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        pass


    # Enter a parse tree produced by YAPLParser#assignment.
    def enterAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by YAPLParser#assignment.
    def exitAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by YAPLParser#arithmetic.
    def enterArithmetic(self, ctx:YAPLParser.ArithmeticContext):
        pass

    # Exit a parse tree produced by YAPLParser#arithmetic.
    def exitArithmetic(self, ctx:YAPLParser.ArithmeticContext):
        pass


    # Enter a parse tree produced by YAPLParser#while.
    def enterWhile(self, ctx:YAPLParser.WhileContext):
        pass

    # Exit a parse tree produced by YAPLParser#while.
    def exitWhile(self, ctx:YAPLParser.WhileContext):
        pass


    # Enter a parse tree produced by YAPLParser#dispatchImplicit.
    def enterDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        pass

    # Exit a parse tree produced by YAPLParser#dispatchImplicit.
    def exitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        pass


    # Enter a parse tree produced by YAPLParser#int.
    def enterInt(self, ctx:YAPLParser.IntContext):
        pass

    # Exit a parse tree produced by YAPLParser#int.
    def exitInt(self, ctx:YAPLParser.IntContext):
        pass


    # Enter a parse tree produced by YAPLParser#negative.
    def enterNegative(self, ctx:YAPLParser.NegativeContext):
        pass

    # Exit a parse tree produced by YAPLParser#negative.
    def exitNegative(self, ctx:YAPLParser.NegativeContext):
        pass


    # Enter a parse tree produced by YAPLParser#boolNot.
    def enterBoolNot(self, ctx:YAPLParser.BoolNotContext):
        pass

    # Exit a parse tree produced by YAPLParser#boolNot.
    def exitBoolNot(self, ctx:YAPLParser.BoolNotContext):
        pass


    # Enter a parse tree produced by YAPLParser#boolean.
    def enterBoolean(self, ctx:YAPLParser.BooleanContext):
        pass

    # Exit a parse tree produced by YAPLParser#boolean.
    def exitBoolean(self, ctx:YAPLParser.BooleanContext):
        pass


    # Enter a parse tree produced by YAPLParser#block.
    def enterBlock(self, ctx:YAPLParser.BlockContext):
        pass

    # Exit a parse tree produced by YAPLParser#block.
    def exitBlock(self, ctx:YAPLParser.BlockContext):
        pass


    # Enter a parse tree produced by YAPLParser#comparisson.
    def enterComparisson(self, ctx:YAPLParser.ComparissonContext):
        pass

    # Exit a parse tree produced by YAPLParser#comparisson.
    def exitComparisson(self, ctx:YAPLParser.ComparissonContext):
        pass


    # Enter a parse tree produced by YAPLParser#id.
    def enterId(self, ctx:YAPLParser.IdContext):
        pass

    # Exit a parse tree produced by YAPLParser#id.
    def exitId(self, ctx:YAPLParser.IdContext):
        pass


    # Enter a parse tree produced by YAPLParser#if.
    def enterIf(self, ctx:YAPLParser.IfContext):
        pass

    # Exit a parse tree produced by YAPLParser#if.
    def exitIf(self, ctx:YAPLParser.IfContext):
        pass


    # Enter a parse tree produced by YAPLParser#case.
    def enterCase(self, ctx:YAPLParser.CaseContext):
        pass

    # Exit a parse tree produced by YAPLParser#case.
    def exitCase(self, ctx:YAPLParser.CaseContext):
        pass


    # Enter a parse tree produced by YAPLParser#dispatchExplicit.
    def enterDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        pass

    # Exit a parse tree produced by YAPLParser#dispatchExplicit.
    def exitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        pass



del YAPLParser