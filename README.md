# DependencyChecker
Dependency checker is a utility that check application dependencies in simplest way. Only json configure you need

#Install recipes from gist (Not recommended on production)

 If the recipe is in a gist file, you can use the Dependency checker command ```./updater get GIST_ID```, and it will copy all the files in place. Be sure to check out the gist's README to see if you need to do any extra configuration.

#Save as system command
Try to create symlink to executable file 
Execute from directory
```
chmod u+x updater
sudo ln -s updater /usr/bin
```