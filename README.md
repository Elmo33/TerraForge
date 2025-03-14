
# TerraGen

TerraGen is a Python library for generating and manipulating Terraform configurations in HCL format. It provides an intuitive, programmatic interface to create and manage Terraform files, making it easier to build, modify, and maintain infrastructure-as-code configurations.

## Features

- **HCL Generation**: Create HCL expressions, blocks, and entire Terraform configurations.
- **Flexible Configuration**: Easily add providers, variables, resources, and modules.
- **Simple API**: Designed to be used as a Python module for quick integration into your projects.

## Installation

TerraGen is available on PyPI. You can install it using pip:

```bash
pip install terragen
```

Alternatively, install it from source:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/terragen.git
    ```
2. Change to the project directory:
    ```bash
    cd terragen
    ```
3. Install the package:
    ```bash
    pip install .
    ```

## Usage

Here is a simple example that demonstrates how to create a Terraform configuration with TerraGen:

```python
from terragen import TerraformConfig

# Create a new Terraform configuration
config = TerraformConfig()

# Add a provider configuration
config.add_provider("aws", region="us-west-2")

# Add a variable
config.add_variable("instance_type", default="t2.micro")

# Add a resource
config.add_resource("aws_instance", "example", ami="ami-0abcdef1234567890", instance_type="t2.micro")

# Format the configuration as HCL and print it
hcl_config = config.format_config()
print(hcl_config)

# Save the configuration to a file
config.save("main.tf")
```

This example creates a basic Terraform configuration with:
- An AWS provider configured for the `us-west-2` region.
- A variable called `instance_type` with a default value.
- A resource (AWS EC2 instance) with specified attributes.

## API Overview

### Core Classes

- **HCLExpression**  
  Wraps a raw HCL expression so that it is output without quotes when rendered.

- **HCLBlock**  
  Represents a generic HCL block. This class supports:
  - Adding attributes (key/value pairs)
  - Nesting blocks (useful for complex configurations)

- **TerraformConfig**  
  A configuration builder that provides methods to:
  - `add_required_provider(provider_name, source, version)`: Specify a required provider.
  - `add_provider(provider_name, **kwargs)`: Add a provider block.
  - `add_variable(var_name, **kwargs)`: Define a variable.
  - `add_resource(resource_type, resource_name, **kwargs)`: Define a resource.
  - `add_module(module_name, source, **kwargs)`: Add a module.
  - `format_config()`: Render the complete configuration as an HCL string.
  - `save(filename)`: Write the configuration to a file.

### Utility Functions

- **render_value(value, indent=0)**  
  Recursively renders a Python value (strings, numbers, booleans, lists, dicts, etc.) into an HCL-formatted string.

- **is_simple_scalar(value)**  
  Returns `True` if the value is a simple scalar (int, float, bool, str, or HCLExpression) that can be rendered inline.

## Running Tests

To run the tests, execute the following command from the root of the project:

```bash
python -m unittest discover
```

This command will discover and run all tests located in the `tests/` directory.

## Contributing

Contributions are welcome! If you have suggestions or improvements:
- Open an issue or submit a pull request on [GitHub](https://github.com/yourusername/terragen).
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
- Include tests for any new features or bug fixes.

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Contact

For questions or feedback, please open an issue in the GitHub repository.

---

Happy Terraforming!
