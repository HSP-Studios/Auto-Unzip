GENERAL DEVELOPMENT RULES:
- Keep only function calls and main functions in the #file:auto-unzip.py and then make a folder called "modules" and have a file FOR EACH FUNCTION. 
- use thorough commenting
- explain what each file does at the top of each file in multi line comments
- split the prompt into tasks, one for each different feature or bugfix, then work on tasks one at a time. before starting a task, make sure to git push any unsaved changes, git pull to pull remote changes, and then create a branch for the task which should be appropriately named. after creating a branch, switch to that branch and verify that you are on that branch. then you can begin working on the task. throughout the task, run git add . and git commit to keep backups stored of your progress. when finished a task, run git add . to add all changes to the commit and then git commit to save changes. run git push and git pull, then merge the working branch into the main branch. make sure to verify that changes have been merged, then you may delete the old branch. finally, run git push and then git pull one more time and then move on to the next task.
- any dependencies that are added should be documented in the requirements.txt file
- any dependencies that are added should be checked 
- WHEN USING GIT MERGE, USE THE -M SWITCH FOR THE COMMIT MESSAGE. YOU MUST INCLUDE -m WITH A COMMIT MESSAGE FOLLOWING
- when naming branches, use either "fix/[name]" or "feature/[name]" or "debug/[name]"
- when naming commits, use either "fix: [description]" or "feature: [description]" or "debug: [description]" or "refactor: [description]"