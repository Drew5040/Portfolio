#!/bin/bash

# shellcheck source=/dev/null

activate_venv() {
  # Prompt user input: project name
  read -r -p "Enter the project name: " project_name
  # Construct path to venv as a local variable
  local venv_path="$HOME/.pyenv/pyenv/versions/${project_name}/bin/activate"
  # Perform path check for existence
  if [ -f "$venv_path" ]; then
    # Source venv path
    source "$venv_path"
    # Print results if venv exists
    echo "Activated virtual environment: $project_name"
  else
    # Print results if venv does not exist
    echo "Could not find virtual environment: $project_name at $venv_path"
  fi
}

# Call the function
activate_venv






