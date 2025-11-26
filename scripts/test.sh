#!/bin/bash

# Test Runner Script
# Runs various test suites with different configurations

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

echo "🧪 Sentinel - Test Runner"
echo "========================="
echo ""

# Parse command line arguments
TEST_TYPE=${1:-all}

run_unit_tests() {
    echo "📝 Running Unit Tests..."
    pytest tests/unit/ -v --tb=short
}

run_integration_tests() {
    echo "🔗 Running Integration Tests..."
    pytest tests/integration/ -v --tb=short
}

run_with_coverage() {
    echo "📊 Running Tests with Coverage..."
    pytest --cov=src --cov-report=html --cov-report=term
    echo ""
    echo "📄 Coverage report generated: htmlcov/index.html"
}

run_lint() {
    echo "🔍 Running Code Quality Checks..."
    echo ""
    echo "Black (formatting)..."
    black --check src/ tests/ || true
    echo ""
    echo "Flake8 (linting)..."
    flake8 src/ tests/ --max-line-length=100 --exclude=venv || true
    echo ""
    echo "MyPy (type checking)..."
    mypy src/ --ignore-missing-imports || true
}

case "$TEST_TYPE" in
    unit)
        run_unit_tests
        ;;
    integration)
        run_integration_tests
        ;;
    coverage)
        run_with_coverage
        ;;
    lint)
        run_lint
        ;;
    all)
        run_unit_tests
        echo ""
        run_integration_tests
        echo ""
        run_with_coverage
        ;;
    *)
        echo "Usage: $0 [unit|integration|coverage|lint|all]"
        echo ""
        echo "Options:"
        echo "  unit         - Run unit tests only"
        echo "  integration  - Run integration tests only"
        echo "  coverage     - Run all tests with coverage report"
        echo "  lint         - Run code quality checks"
        echo "  all          - Run all tests (default)"
        exit 1
        ;;
esac

echo ""
echo "✅ Tests complete!"
