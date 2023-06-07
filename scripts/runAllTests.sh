#!/bin/bash

echo "Executing Docker build/execution Tests..."
./runSystemTests.sh

echo "Executing Database Tests..."
./runDBImportTests.sh

echo "Executing Selenium Tests..."
cd ../02_work_doc/10_test/06_seleniumSystemTests
. ../testingVenv/bin/activate
python 
