# AUTO PROJECT DETECTION

On activation, scan working directory for:

## DETECT STACK
- package.json → Node.js, check for react/vue/svelte/next
- requirements.txt / pyproject.toml → Python
- Cargo.toml → Rust
- go.mod → Go
- Gemfile → Ruby
- composer.json → PHP
- *.csproj → .NET
- Makefile / CMakeLists.txt → C/C++

## DETECT PROJECT TYPE
- src/ + tests/ → standard app
- lib/ → library
- cmd/ → CLI tool
- api/ / routes/ → web service
- infrastructure/ / terraform/ → IaC
- .github/workflows/ → has CI/CD

## DETECT CONVENTIONS
- .editorconfig → formatting rules
- .eslintrc / .prettierrc → JS style
- pyproject.toml [tool.black] → Python style
- existing code patterns → match them

## AUTO-CONFIGURE
Store detected config in memory/short-term/project-context.json
Apply relevant expertise automatically
Match existing code style in all outputs

