# Git
```sh
git reset --soft HEAD~1
git branch -d branch_name
git push -u origin <branch>
git push origin <branch> --force

# Remote tracking management
git fetch upstream
git merge upstream/master
git checkout [--theirs,--ours] <file>

git remote add - upstream

# creates local tracking branch from remote.
git checkout --track origin/<branch_name>

git ls-files . --ignored --exclude-standard --others
git ls-files . --exclude-standard --others

git push -f

## clean pull
git fetch origin/
git checkout <branch>
git reset --hard origin/<branch>
```