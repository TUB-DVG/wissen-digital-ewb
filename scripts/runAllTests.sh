#!/bin/bash

echo "Executing Docker build/execution Tests..."
bash scripts/runSystemTests.sh

echo "Executing Database Tests..."
bash scripts/runDBImportTests.sh

echo "Executing Selenium Tests..."
bash scripts/runSeleniumTests.sh
