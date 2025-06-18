# utils.py

def is_simple_scalar(value):
    """Return True if value is a scalar that should be rendered inline."""
    from .core import HCLExpression
    return isinstance(value, (HCLExpression, int, float, bool, str)) or value is None

def render_value(value, indent=0):
    """
    Recursively render a Python value into an HCL-formatted string.
    If a value is an instance of HCLExpression, it is rendered as-is (without quotes).
    Lists of simple scalars are rendered inline.
    """
    indent_str = '  ' * indent
    from .core import HCLExpression  # local import to avoid circular dependency
    if isinstance(value, HCLExpression):
        return value.expression
    elif value is None:
        return "null"
    elif isinstance(value, str):
        # Normal strings are quoted
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        if not value:
            return "[]"
        # If every element is a simple scalar, render inline.
        if all(is_simple_scalar(item) for item in value):
            items = [render_value(item, 0) for item in value]
            return "[" + ", ".join(items) + "]"
        else:
            items = []
            for item in value:
                items.append('  ' * (indent + 1) + render_value(item, indent + 1))
            return "[\n" + ",\n".join(items) + "\n" + indent_str + "]"
    elif isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append('  ' * (indent + 1) + f"{k} = {render_value(v, indent + 1)}")
        return "{\n" + "\n".join(lines) + "\n" + indent_str + "}"
    else:
        return str(value)
