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

class HCLBlockDef(dict):
    """
    A dictionary subclass used to signal that this dictionary represents the
    arguments for a nested HCL block, rather than a map value.
    """
    pass


class HCLBlock:
    """
    Represents a generic HCL block.
    """
    def __init__(self, block_type, labels=None, **kwargs):
        self.block_type = block_type
        self.labels = labels or []
        self.attributes = {}
        self.nested_blocks = []

        for key, value in kwargs.items():
            if isinstance(value, HCLBlockDef):
                nested_block = HCLBlock(key, **value)
                self.add_nested_block(nested_block)
            else:
                self.add_attribute(key, value)

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def add_nested_block(self, block):
        self.nested_blocks.append(block)

    def get_nested_block(self, block_type):
        for nb in self.nested_blocks:
            if nb.block_type == block_type:
                return nb
        return None

    def to_hcl(self, indent=0):
        indent_str = "  " * indent
        header = indent_str + self.block_type
        for label in self.labels:
            header += f' "{label}"'
        header += " {"
        lines = [header]

        for key, value in sorted(self.attributes.items()):
            rendered_value = render_value(value, indent + 1)
            lines.append("  " * (indent + 1) + f"{key} = {rendered_value}")

        if self.attributes and self.nested_blocks:
            lines.append("")

        for nb in self.nested_blocks:
            lines.append(nb.to_hcl(indent + 1))
        lines.append(indent_str + "}")
        return "\n".join(lines)

class TerraformConfig:
    def __init__(self):
        self.blocks = []

    def _get_block(self, block_type):
        for b in self.blocks:
            if b.block_type == block_type:
                return b
        return None

    def add_required_provider(self, provider_name, source, version):
        terraform_block = self._get_block("terraform")
        if not terraform_block:
            terraform_block = HCLBlock("terraform")
            self.blocks.append(terraform_block)
        rp_block = terraform_block.get_nested_block("required_providers")
        if not rp_block:
            rp_block = HCLBlock("required_providers")
            terraform_block.add_nested_block(rp_block)
        rp_block.add_attribute(provider_name, {"source": source, "version": version})

    def add_provider(self, provider_name, **kwargs):
        block = HCLBlock("provider", [provider_name], **kwargs)
        self.blocks.append(block)

    def add_variable(self, var_name, **kwargs):
        block = HCLBlock("variable", [var_name], **kwargs)
        self.blocks.append(block)

    def add_resource(self, resource_type, resource_name, **kwargs):
        block = HCLBlock("resource", [resource_type, resource_name], **kwargs)
        self.blocks.append(block)

    def add_module(self, module_name, **kwargs):
        block = HCLBlock("module", [module_name], **kwargs)
        self.blocks.append(block)

    def format_config(self):
        return "\n\n".join(block.to_hcl() for block in self.blocks)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.format_config())
