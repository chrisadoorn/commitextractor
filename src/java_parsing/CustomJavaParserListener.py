# Generated from JavaParser.g4 by ANTLR 4.13.0
from antlr4 import *

from .JavaParserListener import JavaParserListener

POINT = '.'

NEWLINE = '\n'

if "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser


# This class defines a complete listener for a parse tree produced by JavaParser.
class CustomJavaParserListener(JavaParserListener):

    def __init__(self, zoekterm, packagenaam, output:str):
        self.zoekterm = zoekterm
        self.packagenaam = packagenaam
        self.output = output
        # zoekterm
        # package
        # alleen zoekterm vinden? ( Thread
        #     maar dan geen import Thread
        # zoekterm vinden?
        #    dan ook import vinden van classe
        #    of import van package.*
        # alleen gebruik van bibliotheek/framework?
        #   dan moet package geïmporteerd zijn
        #   niet verder zoeken naar gebuik class names

        # resultaat velden
        self.geimporteerd = False
        self.instance_declaratie = False
        self.lokale_declaratie = False
        self.is_argument = False
        self.is_resultaat = False
        self.is_parameter = False
        self.gebruikt = False

        # switches voor de afhandeling
        self.import_busy = False
        self.field_decl_busy = False



    def is_gevonden_in(self):
        return(self.geimporteerd, self.instance_declaratie, self.lokale_declaratie, self.is_argument, self.is_resultaat,
        self.is_parameter, self.gebruikt)

    # Enter a parse tree produced by JavaParser#compilationUnit.
    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaParser#compilationUnit.
    def exitCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        pass

    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#packageDeclaration.
    def exitPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        statement = str(ctx.getText())
        if statement.__eq__('package' + self.packagenaam + ';'):
            self.geimporteerd = True
            self.output += 'import ' + NEWLINE

    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        self.import_busy = True

    # Exit a parse tree produced by JavaParser#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        statement = str(ctx.getText())
        if statement.__eq__('import' + self.packagenaam + '.' + self.zoekterm + ';'):
            self.geimporteerd = True
            self.output += 'import ' + NEWLINE
        if statement.__eq__('import' + self.packagenaam + '.*;'):
            self.geimporteerd = True
            self.output += 'import ' + NEWLINE
        self.import_busy = False

    # Enter a parse tree produced by JavaParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx: JavaParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx: JavaParser.TypeDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#modifier.
    def enterModifier(self, ctx: JavaParser.ModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#modifier.
    def exitModifier(self, ctx: JavaParser.ModifierContext):
        pass

    # Enter a parse tree produced by JavaParser#classOrInterfaceModifier.
    def enterClassOrInterfaceModifier(self, ctx: JavaParser.ClassOrInterfaceModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#classOrInterfaceModifier.
    def exitClassOrInterfaceModifier(self, ctx: JavaParser.ClassOrInterfaceModifierContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ClassOrInterfaceModifier ' + NEWLINE
#            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#variableModifier.
    def enterVariableModifier(self, ctx: JavaParser.VariableModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#variableModifier.
    def exitVariableModifier(self, ctx: JavaParser.VariableModifierContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'VariableModifier ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classDeclaration.
    def exitClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#typeParameters.
    def enterTypeParameters(self, ctx: JavaParser.TypeParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameters.
    def exitTypeParameters(self, ctx: JavaParser.TypeParametersContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeParameters ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#typeParameter.
    def enterTypeParameter(self, ctx: JavaParser.TypeParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameter.
    def exitTypeParameter(self, ctx: JavaParser.TypeParameterContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeParameter ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#typeBound.
    def enterTypeBound(self, ctx: JavaParser.TypeBoundContext):
        pass

    # Exit a parse tree produced by JavaParser#typeBound.
    def exitTypeBound(self, ctx: JavaParser.TypeBoundContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeBound ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#enumDeclaration.
    def enterEnumDeclaration(self, ctx: JavaParser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#enumDeclaration.
    def exitEnumDeclaration(self, ctx: JavaParser.EnumDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#enumConstants.
    def enterEnumConstants(self, ctx: JavaParser.EnumConstantsContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstants.
    def exitEnumConstants(self, ctx: JavaParser.EnumConstantsContext):
        pass

    # Enter a parse tree produced by JavaParser#enumConstant.
    def enterEnumConstant(self, ctx: JavaParser.EnumConstantContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstant.
    def exitEnumConstant(self, ctx: JavaParser.EnumConstantContext):
        pass

    # Enter a parse tree produced by JavaParser#enumBodyDeclarations.
    def enterEnumBodyDeclarations(self, ctx: JavaParser.EnumBodyDeclarationsContext):
        pass

    # Exit a parse tree produced by JavaParser#enumBodyDeclarations.
    def exitEnumBodyDeclarations(self, ctx: JavaParser.EnumBodyDeclarationsContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx: JavaParser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx: JavaParser.InterfaceDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#classBody.
    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#classBody.
    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceBody.
    def enterInterfaceBody(self, ctx: JavaParser.InterfaceBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBody.
    def exitInterfaceBody(self, ctx: JavaParser.InterfaceBodyContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceBody ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#classBodyDeclaration.
    def enterClassBodyDeclaration(self, ctx: JavaParser.ClassBodyDeclarationContext):
        self.field_decl_busy = True

    # Exit a parse tree produced by JavaParser#classBodyDeclaration.
    def exitClassBodyDeclaration(self, ctx: JavaParser.ClassBodyDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ClassBodyDeclaration ' + NEWLINE
            self.output += statement + NEWLINE
        self.field_decl_busy = False

    # Enter a parse tree produced by JavaParser#memberDeclaration.
    def enterMemberDeclaration(self, ctx: JavaParser.MemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#memberDeclaration.
    def exitMemberDeclaration(self, ctx: JavaParser.MemberDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'MemberDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'MethodDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#methodBody.
    def enterMethodBody(self, ctx: JavaParser.MethodBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#methodBody.
    def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'MethodBody ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#typeTypeOrVoid.
    def enterTypeTypeOrVoid(self, ctx: JavaParser.TypeTypeOrVoidContext):
        pass

    # Exit a parse tree produced by JavaParser#typeTypeOrVoid.
    def exitTypeTypeOrVoid(self, ctx: JavaParser.TypeTypeOrVoidContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeTypeOrVoid ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#genericMethodDeclaration.
    def enterGenericMethodDeclaration(self, ctx: JavaParser.GenericMethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#genericMethodDeclaration.
    def exitGenericMethodDeclaration(self, ctx: JavaParser.GenericMethodDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'GenericMethodDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#genericConstructorDeclaration.
    def enterGenericConstructorDeclaration(self, ctx: JavaParser.GenericConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#genericConstructorDeclaration.
    def exitGenericConstructorDeclaration(self, ctx: JavaParser.GenericConstructorDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'GenericConstructorDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ConstructorDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#compactConstructorDeclaration.
    def enterCompactConstructorDeclaration(self, ctx: JavaParser.CompactConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#compactConstructorDeclaration.
    def exitCompactConstructorDeclaration(self, ctx: JavaParser.CompactConstructorDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'CompactConstructorDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'FieldDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def enterInterfaceBodyDeclaration(self, ctx: JavaParser.InterfaceBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def exitInterfaceBodyDeclaration(self, ctx: JavaParser.InterfaceBodyDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceBodyDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def enterInterfaceMemberDeclaration(self, ctx: JavaParser.InterfaceMemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def exitInterfaceMemberDeclaration(self, ctx: JavaParser.InterfaceMemberDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceMemberDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#constDeclaration.
    def enterConstDeclaration(self, ctx: JavaParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#constDeclaration.
    def exitConstDeclaration(self, ctx: JavaParser.ConstDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#constantDeclarator.
    def enterConstantDeclarator(self, ctx: JavaParser.ConstantDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#constantDeclarator.
    def exitConstantDeclarator(self, ctx: JavaParser.ConstantDeclaratorContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def enterInterfaceMethodDeclaration(self, ctx: JavaParser.InterfaceMethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def exitInterfaceMethodDeclaration(self, ctx: JavaParser.InterfaceMethodDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceMethodDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#interfaceMethodModifier.
    def enterInterfaceMethodModifier(self, ctx: JavaParser.InterfaceMethodModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodModifier.
    def exitInterfaceMethodModifier(self, ctx: JavaParser.InterfaceMethodModifierContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceMethodModifier ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#genericInterfaceMethodDeclaration.
    def enterGenericInterfaceMethodDeclaration(self, ctx: JavaParser.GenericInterfaceMethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#genericInterfaceMethodDeclaration.
    def exitGenericInterfaceMethodDeclaration(self, ctx: JavaParser.GenericInterfaceMethodDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'GenericInterfaceMethodDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#interfaceCommonBodyDeclaration.
    def enterInterfaceCommonBodyDeclaration(self, ctx: JavaParser.InterfaceCommonBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceCommonBodyDeclaration.
    def exitInterfaceCommonBodyDeclaration(self, ctx: JavaParser.InterfaceCommonBodyDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InterfaceCommonBodyDeclaration ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#variableDeclarators.
    def enterVariableDeclarators(self, ctx: JavaParser.VariableDeclaratorsContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarators.
    def exitVariableDeclarators(self, ctx: JavaParser.VariableDeclaratorsContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'VariableDeclarators ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'VariableDeclarator ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#variableDeclaratorId.
    def enterVariableDeclaratorId(self, ctx: JavaParser.VariableDeclaratorIdContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclaratorId.
    def exitVariableDeclaratorId(self, ctx: JavaParser.VariableDeclaratorIdContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'VariableDeclaratorid ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#variableInitializer.
    def enterVariableInitializer(self, ctx: JavaParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#variableInitializer.
    def exitVariableInitializer(self, ctx: JavaParser.VariableInitializerContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'VariableInitializer ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#arrayInitializer.
    def enterArrayInitializer(self, ctx: JavaParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayInitializer.
    def exitArrayInitializer(self, ctx: JavaParser.ArrayInitializerContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ArrayInitializer ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#classOrInterfaceType.
    def enterClassOrInterfaceType(self, ctx: JavaParser.ClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#classOrInterfaceType.
    def exitClassOrInterfaceType(self, ctx: JavaParser.ClassOrInterfaceTypeContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ClassOrInterfaceType ' + NEWLINE
#            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#typeArgument.
    def enterTypeArgument(self, ctx: JavaParser.TypeArgumentContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgument.
    def exitTypeArgument(self, ctx: JavaParser.TypeArgumentContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeArgument ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#qualifiedNameList.
    def enterQualifiedNameList(self, ctx: JavaParser.QualifiedNameListContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedNameList.
    def exitQualifiedNameList(self, ctx: JavaParser.QualifiedNameListContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'QualifiedNameList ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#formalParameters.
    def enterFormalParameters(self, ctx: JavaParser.FormalParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameters.
    def exitFormalParameters(self, ctx: JavaParser.FormalParametersContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'FormalParameters ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#receiverParameter.
    def enterReceiverParameter(self, ctx: JavaParser.ReceiverParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#receiverParameter.
    def exitReceiverParameter(self, ctx: JavaParser.ReceiverParameterContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'receiverParameter ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#formalParameterList.
    def enterFormalParameterList(self, ctx: JavaParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameterList.
    def exitFormalParameterList(self, ctx: JavaParser.FormalParameterListContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'FormalParameterList ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#formalParameter.
    def enterFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameter.
    def exitFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'FormalParameter ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#lastFormalParameter.
    def enterLastFormalParameter(self, ctx: JavaParser.LastFormalParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#lastFormalParameter.
    def exitLastFormalParameter(self, ctx: JavaParser.LastFormalParameterContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LastFormalParameter ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#lambdaLVTIList.
    def enterLambdaLVTIList(self, ctx: JavaParser.LambdaLVTIListContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaLVTIList.
    def exitLambdaLVTIList(self, ctx: JavaParser.LambdaLVTIListContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LambdaLVTIList ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#lambdaLVTIParameter.
    def enterLambdaLVTIParameter(self, ctx: JavaParser.LambdaLVTIParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaLVTIParameter.
    def exitLambdaLVTIParameter(self, ctx: JavaParser.LambdaLVTIParameterContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LambdaLVTIParameter ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#qualifiedName.
    def enterQualifiedName(self, ctx: JavaParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedName.
    def exitQualifiedName(self, ctx: JavaParser.QualifiedNameContext):
        if not self.import_busy:
            statement = str(ctx.getText())
            if statement.__eq__(self.packagenaam + POINT + self.zoekterm):
                self.gebruikt = True
                self.output += 'QualifiedName ' + NEWLINE

    # Enter a parse tree produced by JavaParser#literal.
    def enterLiteral(self, ctx: JavaParser.LiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#literal.
    def exitLiteral(self, ctx: JavaParser.LiteralContext):
        pass

    # Enter a parse tree produced by JavaParser#integerLiteral.
    def enterIntegerLiteral(self, ctx: JavaParser.IntegerLiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#integerLiteral.
    def exitIntegerLiteral(self, ctx: JavaParser.IntegerLiteralContext):
        pass

    # Enter a parse tree produced by JavaParser#floatLiteral.
    def enterFloatLiteral(self, ctx: JavaParser.FloatLiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#floatLiteral.
    def exitFloatLiteral(self, ctx: JavaParser.FloatLiteralContext):
        pass

    # Enter a parse tree produced by JavaParser#altAnnotationQualifiedName.
    def enterAltAnnotationQualifiedName(self, ctx: JavaParser.AltAnnotationQualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#altAnnotationQualifiedName.
    def exitAltAnnotationQualifiedName(self, ctx: JavaParser.AltAnnotationQualifiedNameContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AltAnnotationQualifiedName ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#annotation.
    def enterAnnotation(self, ctx: JavaParser.AnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotation.
    def exitAnnotation(self, ctx: JavaParser.AnnotationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Annotation ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#elementValuePairs.
    def enterElementValuePairs(self, ctx: JavaParser.ElementValuePairsContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValuePairs.
    def exitElementValuePairs(self, ctx: JavaParser.ElementValuePairsContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ElementValuePairs ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#elementValuePair.
    def enterElementValuePair(self, ctx: JavaParser.ElementValuePairContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValuePair.
    def exitElementValuePair(self, ctx: JavaParser.ElementValuePairContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ElementValuePair ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#elementValue.
    def enterElementValue(self, ctx: JavaParser.ElementValueContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValue.
    def exitElementValue(self, ctx: JavaParser.ElementValueContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ElementValue ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#elementValueArrayInitializer.
    def enterElementValueArrayInitializer(self, ctx: JavaParser.ElementValueArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValueArrayInitializer.
    def exitElementValueArrayInitializer(self, ctx: JavaParser.ElementValueArrayInitializerContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ElementValueArrayInitializer ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#annotationTypeDeclaration.
    def enterAnnotationTypeDeclaration(self, ctx: JavaParser.AnnotationTypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeDeclaration.
    def exitAnnotationTypeDeclaration(self, ctx: JavaParser.AnnotationTypeDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationTypeDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#annotationTypeBody.
    def enterAnnotationTypeBody(self, ctx: JavaParser.AnnotationTypeBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeBody.
    def exitAnnotationTypeBody(self, ctx: JavaParser.AnnotationTypeBodyContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationTypeBody ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#annotationTypeElementDeclaration.
    def enterAnnotationTypeElementDeclaration(self, ctx: JavaParser.AnnotationTypeElementDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeElementDeclaration.
    def exitAnnotationTypeElementDeclaration(self, ctx: JavaParser.AnnotationTypeElementDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationTypeElementDeclaration ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#annotationTypeElementRest.
    def enterAnnotationTypeElementRest(self, ctx: JavaParser.AnnotationTypeElementRestContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeElementRest.
    def exitAnnotationTypeElementRest(self, ctx: JavaParser.AnnotationTypeElementRestContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationTypeElementRest ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#annotationMethodOrConstantRest.
    def enterAnnotationMethodOrConstantRest(self, ctx: JavaParser.AnnotationMethodOrConstantRestContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationMethodOrConstantRest.
    def exitAnnotationMethodOrConstantRest(self, ctx: JavaParser.AnnotationMethodOrConstantRestContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationMethodOrConstantRest ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#annotationMethodRest.
    def enterAnnotationMethodRest(self, ctx: JavaParser.AnnotationMethodRestContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationMethodRest.
    def exitAnnotationMethodRest(self, ctx: JavaParser.AnnotationMethodRestContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationMethodRest ' + NEWLINE
            self.output += statement + NEWLINE
    # Enter a parse tree produced by JavaParser#annotationConstantRest.
    def enterAnnotationConstantRest(self, ctx: JavaParser.AnnotationConstantRestContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationConstantRest.
    def exitAnnotationConstantRest(self, ctx: JavaParser.AnnotationConstantRestContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'AnnotationConstantRest ' + NEWLINE
            self.output += statement + NEWLINE
    # Enter a parse tree produced by JavaParser#defaultValue.
    def enterDefaultValue(self, ctx: JavaParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by JavaParser#defaultValue.
    def exitDefaultValue(self, ctx: JavaParser.DefaultValueContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'DefaultValue ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#moduleDeclaration.
    def enterModuleDeclaration(self, ctx: JavaParser.ModuleDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleDeclaration.
    def exitModuleDeclaration(self, ctx: JavaParser.ModuleDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ModuleDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#moduleBody.
    def enterModuleBody(self, ctx: JavaParser.ModuleBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleBody.
    def exitModuleBody(self, ctx: JavaParser.ModuleBodyContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ModuleBody ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#moduleDirective.
    def enterModuleDirective(self, ctx: JavaParser.ModuleDirectiveContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleDirective.
    def exitModuleDirective(self, ctx: JavaParser.ModuleDirectiveContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ModuleDirective ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#requiresModifier.
    def enterRequiresModifier(self, ctx: JavaParser.RequiresModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#requiresModifier.
    def exitRequiresModifier(self, ctx: JavaParser.RequiresModifierContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'RequiresModifier ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx: JavaParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx: JavaParser.RecordDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'RecordDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#recordHeader.
    def enterRecordHeader(self, ctx: JavaParser.RecordHeaderContext):
        pass

    # Exit a parse tree produced by JavaParser#recordHeader.
    def exitRecordHeader(self, ctx: JavaParser.RecordHeaderContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'RecordHeader ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#recordComponentList.
    def enterRecordComponentList(self, ctx: JavaParser.RecordComponentListContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponentList.
    def exitRecordComponentList(self, ctx: JavaParser.RecordComponentListContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'RecordComponentList ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#recordComponent.
    def enterRecordComponent(self, ctx: JavaParser.RecordComponentContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponent.
    def exitRecordComponent(self, ctx: JavaParser.RecordComponentContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'RecordComponent ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#recordBody.
    def enterRecordBody(self, ctx: JavaParser.RecordBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#recordBody.
    def exitRecordBody(self, ctx: JavaParser.RecordBodyContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'RecordBody ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#block.
    def enterBlock(self, ctx: JavaParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaParser#block.
    def exitBlock(self, ctx: JavaParser.BlockContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Block ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#blockStatement.
    def enterBlockStatement(self, ctx: JavaParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#blockStatement.
    def exitBlockStatement(self, ctx: JavaParser.BlockStatementContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'BlockStatement ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#localVariableDeclaration.
    def enterLocalVariableDeclaration(self, ctx: JavaParser.LocalVariableDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#localVariableDeclaration.
    def exitLocalVariableDeclaration(self, ctx: JavaParser.LocalVariableDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LocalVariableDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#identifier.
    def enterIdentifier(self, ctx: JavaParser.IdentifierContext):
        pass

    # Exit a parse tree produced by JavaParser#identifier.
    def exitIdentifier(self, ctx: JavaParser.IdentifierContext):
        if not self.import_busy:
            statement = str(ctx.getText())
            if statement.__eq__(self.zoekterm):
                self.gebruikt = True
                self.output += 'Identifier ' + NEWLINE

    # Enter a parse tree produced by JavaParser#typeIdentifier.
    def enterTypeIdentifier(self, ctx: JavaParser.TypeIdentifierContext):
        pass

    # Exit a parse tree produced by JavaParser#typeIdentifier.
    def exitTypeIdentifier(self, ctx: JavaParser.TypeIdentifierContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeIdentifier ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#localTypeDeclaration.
    def enterLocalTypeDeclaration(self, ctx: JavaParser.LocalTypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#localTypeDeclaration.
    def exitLocalTypeDeclaration(self, ctx: JavaParser.LocalTypeDeclarationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LocalTypeDeclaration ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#statement.
    def enterStatement(self, ctx: JavaParser.StatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statement.
    def exitStatement(self, ctx: JavaParser.StatementContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'statement ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#catchClause.
    def enterCatchClause(self, ctx: JavaParser.CatchClauseContext):
        pass

    # Exit a parse tree produced by JavaParser#catchClause.
    def exitCatchClause(self, ctx: JavaParser.CatchClauseContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'CatchClause ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#catchType.
    def enterCatchType(self, ctx: JavaParser.CatchTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#catchType.
    def exitCatchType(self, ctx: JavaParser.CatchTypeContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'CatchType ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#finallyBlock.
    def enterFinallyBlock(self, ctx: JavaParser.FinallyBlockContext):
        pass

    # Exit a parse tree produced by JavaParser#finallyBlock.
    def exitFinallyBlock(self, ctx: JavaParser.FinallyBlockContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'FinallyBlock ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#resourceSpecification.
    def enterResourceSpecification(self, ctx: JavaParser.ResourceSpecificationContext):
        pass

    # Exit a parse tree produced by JavaParser#resourceSpecification.
    def exitResourceSpecification(self, ctx: JavaParser.ResourceSpecificationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ResourceSpecification ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#resources.
    def enterResources(self, ctx: JavaParser.ResourcesContext):
        pass

    # Exit a parse tree produced by JavaParser#resources.
    def exitResources(self, ctx: JavaParser.ResourcesContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Resources ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#resource.
    def enterResource(self, ctx: JavaParser.ResourceContext):
        pass

    # Exit a parse tree produced by JavaParser#resource.
    def exitResource(self, ctx: JavaParser.ResourceContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Resource ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#switchBlockStatementGroup.
    def enterSwitchBlockStatementGroup(self, ctx: JavaParser.SwitchBlockStatementGroupContext):
        pass

    # Exit a parse tree produced by JavaParser#switchBlockStatementGroup.
    def exitSwitchBlockStatementGroup(self, ctx: JavaParser.SwitchBlockStatementGroupContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'SwitchBlockStatementGroup ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#switchLabel.
    def enterSwitchLabel(self, ctx: JavaParser.SwitchLabelContext):
        pass

    # Exit a parse tree produced by JavaParser#switchLabel.
    def exitSwitchLabel(self, ctx: JavaParser.SwitchLabelContext):
        pass

    # Enter a parse tree produced by JavaParser#forControl.
    def enterForControl(self, ctx: JavaParser.ForControlContext):
        pass

    # Exit a parse tree produced by JavaParser#forControl.
    def exitForControl(self, ctx: JavaParser.ForControlContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ForControl ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#forInit.
    def enterForInit(self, ctx: JavaParser.ForInitContext):
        pass

    # Exit a parse tree produced by JavaParser#forInit.
    def exitForInit(self, ctx: JavaParser.ForInitContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ForInit ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#enhancedForControl.
    def enterEnhancedForControl(self, ctx: JavaParser.EnhancedForControlContext):
        pass

    # Exit a parse tree produced by JavaParser#enhancedForControl.
    def exitEnhancedForControl(self, ctx: JavaParser.EnhancedForControlContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'EnhancedForControl ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#parExpression.
    def enterParExpression(self, ctx: JavaParser.ParExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#parExpression.
    def exitParExpression(self, ctx: JavaParser.ParExpressionContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ParExpression ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#expressionList.
    def enterExpressionList(self, ctx: JavaParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionList.
    def exitExpressionList(self, ctx: JavaParser.ExpressionListContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ExpressionList ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#methodCall.
    def enterMethodCall(self, ctx: JavaParser.MethodCallContext):
        pass

    # Exit a parse tree produced by JavaParser#methodCall.
    def exitMethodCall(self, ctx: JavaParser.MethodCallContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'MethodCall ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#expression.
    def enterExpression(self, ctx: JavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#expression.
    def exitExpression(self, ctx: JavaParser.ExpressionContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Expression ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#pattern.
    def enterPattern(self, ctx: JavaParser.PatternContext):
        pass

    # Exit a parse tree produced by JavaParser#pattern.
    def exitPattern(self, ctx: JavaParser.PatternContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Pattern ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#lambdaExpression.
    def enterLambdaExpression(self, ctx: JavaParser.LambdaExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaExpression.
    def exitLambdaExpression(self, ctx: JavaParser.LambdaExpressionContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LambdaExpression ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#lambdaParameters.
    def enterLambdaParameters(self, ctx: JavaParser.LambdaParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParameters.
    def exitLambdaParameters(self, ctx: JavaParser.LambdaParametersContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LambdaParameters ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#lambdaBody.
    def enterLambdaBody(self, ctx: JavaParser.LambdaBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaBody.
    def exitLambdaBody(self, ctx: JavaParser.LambdaBodyContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'LambdaBody ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#primary.
    def enterPrimary(self, ctx: JavaParser.PrimaryContext):
        pass

    # Exit a parse tree produced by JavaParser#primary.
    def exitPrimary(self, ctx: JavaParser.PrimaryContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Primary ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#switchExpression.
    def enterSwitchExpression(self, ctx: JavaParser.SwitchExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#switchExpression.
    def exitSwitchExpression(self, ctx: JavaParser.SwitchExpressionContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'SwitchExpression ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#switchLabeledRule.
    def enterSwitchLabeledRule(self, ctx: JavaParser.SwitchLabeledRuleContext):
        pass

    # Exit a parse tree produced by JavaParser#switchLabeledRule.
    def exitSwitchLabeledRule(self, ctx: JavaParser.SwitchLabeledRuleContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'SwitchLabeledRule ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#guardedPattern.
    def enterGuardedPattern(self, ctx: JavaParser.GuardedPatternContext):
        pass

    # Exit a parse tree produced by JavaParser#guardedPattern.
    def exitGuardedPattern(self, ctx: JavaParser.GuardedPatternContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'GuardedPattern ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#switchRuleOutcome.
    def enterSwitchRuleOutcome(self, ctx: JavaParser.SwitchRuleOutcomeContext):
        pass

    # Exit a parse tree produced by JavaParser#switchRuleOutcome.
    def exitSwitchRuleOutcome(self, ctx: JavaParser.SwitchRuleOutcomeContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'SwitchRuleOutcome ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#classType.
    def enterClassType(self, ctx: JavaParser.ClassTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#classType.
    def exitClassType(self, ctx: JavaParser.ClassTypeContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ClassType ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#creator.
    def enterCreator(self, ctx: JavaParser.CreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#creator.
    def exitCreator(self, ctx: JavaParser.CreatorContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'Creator ' + NEWLINE
            self.output += statement + NEWLINE


    # Enter a parse tree produced by JavaParser#createdName.
    def enterCreatedName(self, ctx: JavaParser.CreatedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#createdName.
    def exitCreatedName(self, ctx: JavaParser.CreatedNameContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'CreatedName ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#innerCreator.
    def enterInnerCreator(self, ctx: JavaParser.InnerCreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#innerCreator.
    def exitInnerCreator(self, ctx: JavaParser.InnerCreatorContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'InnerCreator ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#arrayCreatorRest.
    def enterArrayCreatorRest(self, ctx: JavaParser.ArrayCreatorRestContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayCreatorRest.
    def exitArrayCreatorRest(self, ctx: JavaParser.ArrayCreatorRestContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ArrayCreatorRest ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#classCreatorRest.
    def enterClassCreatorRest(self, ctx: JavaParser.ClassCreatorRestContext):
        pass

    # Exit a parse tree produced by JavaParser#classCreatorRest.
    def exitClassCreatorRest(self, ctx: JavaParser.ClassCreatorRestContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ClassCreatorRest ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#explicitGenericInvocation.
    def enterExplicitGenericInvocation(self, ctx: JavaParser.ExplicitGenericInvocationContext):
        pass

    # Exit a parse tree produced by JavaParser#explicitGenericInvocation.
    def exitExplicitGenericInvocation(self, ctx: JavaParser.ExplicitGenericInvocationContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ExplicitGenericInvocation ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def enterTypeArgumentsOrDiamond(self, ctx: JavaParser.TypeArgumentsOrDiamondContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def exitTypeArgumentsOrDiamond(self, ctx: JavaParser.TypeArgumentsOrDiamondContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeArgumentsOrDiamond ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#nonWildcardTypeArgumentsOrDiamond.
    def enterNonWildcardTypeArgumentsOrDiamond(self, ctx: JavaParser.NonWildcardTypeArgumentsOrDiamondContext):
        pass

    # Exit a parse tree produced by JavaParser#nonWildcardTypeArgumentsOrDiamond.
    def exitNonWildcardTypeArgumentsOrDiamond(self, ctx: JavaParser.NonWildcardTypeArgumentsOrDiamondContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'NonWildcardTypeArgumentsOrDiamond ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#nonWildcardTypeArguments.
    def enterNonWildcardTypeArguments(self, ctx: JavaParser.NonWildcardTypeArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#nonWildcardTypeArguments.
    def exitNonWildcardTypeArguments(self, ctx: JavaParser.NonWildcardTypeArgumentsContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'NonWildcardTypeArguments ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#typeList.
    def enterTypeList(self, ctx: JavaParser.TypeListContext):
        pass

    # Exit a parse tree produced by JavaParser#typeList.
    def exitTypeList(self, ctx: JavaParser.TypeListContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeList ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#typeType.
    def enterTypeType(self, ctx: JavaParser.TypeTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#typeType.
    def exitTypeType(self, ctx: JavaParser.TypeTypeContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeType ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#primitiveType.
    def enterPrimitiveType(self, ctx: JavaParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#primitiveType.
    def exitPrimitiveType(self, ctx: JavaParser.PrimitiveTypeContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'PrimitiveType ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#typeArguments.
    def enterTypeArguments(self, ctx: JavaParser.TypeArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArguments.
    def exitTypeArguments(self, ctx: JavaParser.TypeArgumentsContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'TypeArguments ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#superSuffix.
    def enterSuperSuffix(self, ctx: JavaParser.SuperSuffixContext):
        pass

    # Exit a parse tree produced by JavaParser#superSuffix.
    def exitSuperSuffix(self, ctx: JavaParser.SuperSuffixContext):
        pass

    # Enter a parse tree produced by JavaParser#explicitGenericInvocationSuffix.
    def enterExplicitGenericInvocationSuffix(self, ctx: JavaParser.ExplicitGenericInvocationSuffixContext):
        pass

    # Exit a parse tree produced by JavaParser#explicitGenericInvocationSuffix.
    def exitExplicitGenericInvocationSuffix(self, ctx: JavaParser.ExplicitGenericInvocationSuffixContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'ExplicitGenericInvocationSuffix ' + NEWLINE
            self.output += statement + NEWLINE

    # Enter a parse tree produced by JavaParser#arguments.
    def enterArguments(self, ctx: JavaParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#arguments.
    def exitArguments(self, ctx: JavaParser.ArgumentsContext):
        statement = str(ctx.getText())
        if statement.__contains__(self.zoekterm):
            self.gebruikt = True
            self.output += 'arguments ' + NEWLINE
            self.output += statement + NEWLINE


del JavaParser
