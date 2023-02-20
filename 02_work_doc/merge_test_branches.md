# merge and test branches
 In this file process of merging and testing of the merged branches is
 described.
## General steps
1. clean up feature branch
  - delete everything not needed for this feature (not used code and not necessary comments)
  - use style guide
  - check grammar and spelling
  - for every file including changes regarding style guide and spell and grammar check at least commit
  - run project and check feature
2. copy of the main > main_temp_feature 
3. check the difference of the branch to the main/main_temp_feature  via a diff-tool
  - possible at the "new merge request" procedure
  - check every file
  - understand the differences
4. merge branch into the main_temp_feature 
5. check main_temp_feature branch
  - run the project
    - always use new environment and build it via requirement.txt
  - check following
    - check database structure fits
     - migrate and make migration, when needed 
    - every page is working
    - check admin area
    - check search functions
      - tools
      - data
    - check new features
6. merge main_temp_feature  into the main branch
7. check the main like "check main_temp branch"
  - here no errors should occur
8. delete main_temp_feature 
