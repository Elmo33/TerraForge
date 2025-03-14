import os
import tempfile
import unittest
from terragen import HCLExpression, HCLBlock, TerraformConfig
from terragen.utils import render_value, is_simple_scalar

class TestHCLExpression(unittest.TestCase):
    def test_str(self):
        expr = HCLExpression("example")
        self.assertEqual(str(expr), "example")

class TestRenderValue(unittest.TestCase):
    def test_render_string(self):
        self.assertEqual(render_value("test"), '"test"')

    def test_render_number(self):
        self.assertEqual(render_value(42), "42")

    def test_render_boolean(self):
        self.assertEqual(render_value(True), "true")
        self.assertEqual(render_value(False), "false")

    def test_render_list_inline(self):
        # All simple scalars should render inline
        result = render_value([1, 2, "three", False])
        expected = '[1, 2, "three", false]'
        self.assertEqual(result, expected)

    def test_render_list_multiline(self):
        # If a list contains a nested list, it should force multiline formatting
        result = render_value([1, [2, "three"], "four"])
        self.assertIn("\n", result)

    def test_render_dict(self):
        result = render_value({"a": 1, "b": "two"})
        self.assertIn("a = 1", result)
        self.assertIn('b = "two"', result)

class TestHCLBlock(unittest.TestCase):
    def test_simple_block(self):
        block = HCLBlock("test_block", ["label"])
        block.add_attribute("key", "value")
        hcl = block.to_hcl()
        self.assertIn('test_block "label" {', hcl)
        self.assertIn('key = "value"', hcl)
        self.assertTrue(hcl.strip().endswith("}"))

    def test_nested_blocks(self):
        parent = HCLBlock("parent")
        child = HCLBlock("child")
        child.add_attribute("c_key", 123)
        parent.add_nested_block(child)
        hcl = parent.to_hcl()
        self.assertIn("child {", hcl)
        self.assertIn("c_key = 123", hcl)

class TestTerraformConfig(unittest.TestCase):
    def test_add_provider_and_format(self):
        config = TerraformConfig()
        config.add_provider("aws", region="us-east-1")
        output = config.format_config()
        self.assertIn('provider "aws" {', output)
        self.assertIn('region = "us-east-1"', output)

    def test_add_required_provider(self):
        config = TerraformConfig()
        config.add_required_provider("aws", "hashicorp/aws", "~> 3.0")
        output = config.format_config()
        self.assertIn("terraform {", output)
        self.assertIn("required_providers {", output)
        # Depending on how dictionaries are rendered, check for key parts
        self.assertIn("aws", output)
        self.assertIn("hashicorp/aws", output)
        self.assertIn("~> 3.0", output)

    def test_save_function(self):
        config = TerraformConfig()
        config.add_provider("aws", region="us-east-1")
        # Create a temporary file to test the save method
        with tempfile.NamedTemporaryFile(delete=False, mode="w+") as tmp:
            filename = tmp.name
        try:
            config.save(filename)
            with open(filename, "r") as f:
                content = f.read()
            self.assertIn('provider "aws" {', content)
        finally:
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
