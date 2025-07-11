# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a blog project using Hugo with the Terminal theme. The repository contains:
- A Python project structure (pyproject.toml) but appears to be primarily a Hugo static site
- The Terminal Hugo theme as a submodule/directory (`hugo-theme-terminal/`)
- Empty README.md (needs content)

## Development Commands

### Hugo Site Development
```bash
# Run the development server
hugo server -t terminal

# Build the site
hugo

# Create new posts using archetype
hugo new posts/your-post-name.md
```

The site will be available at `localhost:1313` during development.

### Theme Development (if modifying the Terminal theme)
```bash
# Navigate to theme directory
cd hugo-theme-terminal/

# Install theme dependencies
yarn install

# Test theme (basic test only)
yarn test
```

## Architecture

### Hugo Site Structure
- **Content**: Posts go in `content/posts/` directory
- **Configuration**: Site config should be in `config.toml` or `hugo.toml` in root
- **Theme**: Uses the Terminal theme (v4.2.0) located in `hugo-theme-terminal/`
- **Static files**: Place in `static/` directory
- **Layouts**: Custom layouts can override theme defaults

### Terminal Theme Features
- Fully responsive with customizable color schemes
- Built-in shortcodes: `image` and `code`
- Fira Code font for monospaced text
- Chroma syntax highlighting
- Requires Hugo Extended v0.90.x or higher

### Theme Configuration
Key configuration options in `config.toml`:
- `contentTypeName = "posts"` - Main content directory
- `showMenuItems = 2` - Number of menu items to show
- `fullWidthTheme = false` - Theme width setting
- `autoCover = true` - Automatic cover image detection

## Important Notes

- The Hugo theme requires **Hugo Extended** version 0.90.x or higher
- Theme can be installed as Hugo Module, local directory, or git submodule
- Custom styles can be added via `static/style.css` to override theme defaults
- The Python project structure (pyproject.toml) suggests this might be a hybrid project or the Python components are not yet implemented