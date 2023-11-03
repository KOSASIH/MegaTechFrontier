import os
import re
import ast
from typing import List, Dict

def extract_functions(file_path: str) -> List[Dict[str, str]]:
    """
    Extracts function information from a given file.

    Args:
        file_path (str): Path to the file.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing function information.
    """
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function = {
                'name': node.name,
                'parameters': [arg.arg for arg in node.args.args],
                'docstring': ast.get_docstring(node),
                'examples': extract_examples(code, node.lineno)
            }
            functions.append(function)

    return functions

def extract_examples(code: str, function_line: int) -> List[str]:
    """
    Extracts usage examples for a given function.

    Args:
        code (str): Code content.
        function_line (int): Line number of the function definition.

    Returns:
        List[str]: List of usage examples.
    """
    examples = []
    lines = code.split('\n')

    for i, line in enumerate(lines):
        if line.strip().startswith('def') and i > function_line:
            break

        if re.search(r'(?:\b|_)example(?:\b|_)', line, re.IGNORECASE):
            examples.append(line.strip())

    return examples

def generate_markdown_documentation(file_path: str) -> str:
    """
    Generates markdown documentation for a given software project.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Markdown documentation.
    """
    functions = extract_functions(file_path)

    markdown = ''
    for function in functions:
        markdown += f'## {function["name"]}\n\n'
        markdown += f'**Parameters:** {", ".join(function["parameters"])}\n\n'
        markdown += f'**Description:**\n\n{function["docstring"]}\n\n'

        if function["examples"]:
            markdown += '**Usage Examples:**\n\n'
            for example in function["examples"]:
                markdown += f'- {example}\n'
            markdown += '\n'

        markdown += '---\n\n'

    return markdown

# Example usage
file_path = 'path/to/your/code.py'
documentation = generate_markdown_documentation(file_path)
print(documentation)
