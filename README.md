Development Standards
Python

Version: 3.12.4

Code Style

Formatter: black

Import Sorter: isort

Linter (optional): flake8

Commit Convention

We use Conventional Commits, examples:

feat(core): add candle model
fix(api): correct response format
chore: setup black and isort
docs: update README
infra: update docker configs

Naming Conventions

Files: snake_case

Variables: snake_case

Classes: PascalCase

Constants: UPPER_CASE

Dependencies

Each service has its own requirements.txt

A requirements-dev.txt will be added later for development tooling