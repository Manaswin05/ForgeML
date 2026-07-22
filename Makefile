# ForgeML Makefile for easy development

.PHONY: dev prod setup test clean reset install help

# Default target
dev: ## Start development server
	@python run.py dev

prod: ## Start production server
	@python run.py prod

setup: ## Install dependencies
	@python run.py setup

install: setup ## Alias for setup

test: ## Run tests
	@python run.py test

clean: ## Clean cache files
	@python run.py clean

reset: ## Reset models and datasets
	@python run.py reset

help: ## Show this help message
	@echo "ForgeML - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick start:"
	@echo "  make setup    # Install dependencies"
	@echo "  make dev      # Start development server"