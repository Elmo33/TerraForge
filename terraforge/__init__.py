"""
TerraForge: A library for generating and manipulating Terraform configurations in HCL.
"""

__version__ = "0.1.0"

from .core import HCLExpression, HCLBlock, TerraformConfig

__all__ = ["HCLExpression", "HCLBlock", "TerraformConfig"]
