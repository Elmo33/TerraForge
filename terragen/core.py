# core.py

from .utils import render_value

class HCLExpression:
    """
    Wraps a raw HCL expression. When rendered, the expression is output without quotes.
    """
    def __init__(self, expression: str):
        self.expression = expression

    def __str__(self):
        return self.expression

class HCLBlock:
    """
    Represents a generic HCL block.
    A block has:
      - a type (e.g., "provider", "resource", etc.)
      - optional labels (like resource names)
      - attributes (key/value pairs)
      - nested blocks (for constructs such as exec { ... }).
    """
    def __init__(self, block_type, labels=None):
        self.block_type = block_type
        self.labels = labels or []  # e.g., provider "aws"  ==> labels=["aws"]
        self.attributes = {}        # key-value pairs
        self.nested_blocks = []     # list of HCLBlock instances

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def add_nested_block(self, block):
        self.nested_blocks.append(block)

    def get_nested_block(self, block_type):
        """Return the first nested block of a given type (if any)."""
        for nb in self.nested_blocks:
            if nb.block_type == block_type:
                return nb
        return None

    def to_hcl(self, indent=0):
        indent_str = '  ' * indent
        # Build header: e.g., provider "aws" { ... }
        header = indent_str + self.block_type
        for label in self.labels:
            header += f' "{label}"'
        header += " {"
        lines = [header]

        # Render attributes
        for key, value in self.attributes.items():
            rendered_value = render_value(value, indent + 1)
            lines.append('  ' * (indent + 1) + f"{key} = {rendered_value}")

        # Render nested blocks
        for nb in self.nested_blocks:
            lines.append(nb.to_hcl(indent + 1))
        lines.append(indent_str + "}")
        return "\n".join(lines)

class TerraformConfig:
    """
    A universal Terraform configuration builder.
    Provides methods to add required providers, providers, variables, resources, and modules.
    """
    def __init__(self):
        self.blocks = []  # top-level blocks

    def _get_block(self, block_type):
        for b in self.blocks:
            if b.block_type == block_type:
                return b
        return None

    def add_required_provider(self, provider_name, source, version):
        """
        Add an entry in terraform { required_providers { ... } }.
        """
        terraform_block = self._get_block("terraform")
        if not terraform_block:
            terraform_block = HCLBlock("terraform")
            self.blocks.append(terraform_block)
        rp_block = terraform_block.get_nested_block("required_providers")
        if not rp_block:
            rp_block = HCLBlock("required_providers")
            terraform_block.add_nested_block(rp_block)
        rp_block.attributes[provider_name] = {"source": source, "version": version}

    def add_provider(self, provider_name, **kwargs):
        block = HCLBlock("provider", [provider_name])
        for k, v in kwargs.items():
            block.add_attribute(k, v)
        self.blocks.append(block)

    def add_variable(self, var_name, **kwargs):
        block = HCLBlock("variable", [var_name])
        for k, v in kwargs.items():
            block.add_attribute(k, v)
        self.blocks.append(block)

    def add_resource(self, resource_type, resource_name, **kwargs):
        block = HCLBlock("resource", [resource_type, resource_name])
        for k, v in kwargs.items():
            block.add_attribute(k, v)
        self.blocks.append(block)

    def add_module(self, module_name, source, **kwargs):
        block = HCLBlock("module", [module_name])
        block.add_attribute("source", source)
        for k, v in kwargs.items():
            block.add_attribute(k, v)
        self.blocks.append(block)

    def format_config(self):
        """Render the entire Terraform configuration as HCL."""
        return "\n\n".join(block.to_hcl() for block in self.blocks)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.format_config())
