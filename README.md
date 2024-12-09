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


#### deploying project
```
poetry config repositories.pypi https://pypi.org
poetry config pypi-token.pypi <token>
poetry build
poetry publish
```
