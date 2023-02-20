# merge and test branches
 In this file process of merging and testing of the merged branches is
 described.
## General steps
1. copy of the main > main_temp_feature 
2. check the difference of the branch to the main/main_temp via a diff-tool
  - possible at the "new merge request" procedure
  - check every file
  - understand the differences 
3. merge branch into the main_temp
4. check main_temp branch
  - run the project
  - check following *and document it*
    - for the documentation we need a template or something?
    - every page is working
    - check admin area
    - check search functions
      - tools
      - data
    - check new features
5. merge main_temp into the main branch
6. check the main like "check main_temp branch"
  - here no errors should occur
7. delete main_temp
