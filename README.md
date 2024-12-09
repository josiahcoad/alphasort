### Setup
#### Pre-setup for pipx, poetry
```
brew install pipx
pipx ensurepath
pipx install poetry
poetry config virtualenvs.in-project true
```

```
poetry install
poetry shell
```

#### to update version
`poetry version patch/minor/major`

#### create_user_jwt.sh

- Find MARKY_JWT_SECRET [here](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/%252Fmarky%252Fprod%252FSECRET/description?region=us-east-1&tab=Table#list_parameter_filters=Name:Contains:secret)
- you may have to do `brew install jq` (will work on mac if you have homebrew installed)

#### deploying project
```
poetry config repositories.test-pypi https://test.pypi.org/legacy
poetry config pypi-token.test-pypi <token>
poetry build
poetry publish -r test-pypi
```