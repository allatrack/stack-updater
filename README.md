# What is it?
Stack updater check dependency and update your app stack in a simplest way. 
This is DevOps tool for lazy programmers. Only json and bash file configure you need.
This application allows you to deploy you projects and not worry about breaking your project due to outdated package on the server.

# Table of contents
- [Goals](#goals)
- [Why not Puppet, Chef, SaltStack or Ansible?](#how-does-it-work)
- [Why not Puppet or Chef or etc?](#why-not)
- [Getting started](#start)
  - [Dependencies](#dependencies)
  - [Configuration](#configuration)
  - [Running the application](#running)
  - [Command line options](#cli-options)
  - [Install recipes from Gist](#install-recipes)
  - [Save as system command](#save-systemd-command)
  - [Logging](#logging)
- [Native and Third party recipes](#recipes)
- [Customizing](#customizing)
- [Contributing](#contributing)
- [Recipes and log filesystem](#filesystem)
- [License](#license)

# <a name="goals"></a> Goals
Sometimes you'r deploying your app on server and it won't work. You work hard to debug your code but it turns out that the problem was in an obsolete software on the server.
Crap!!!

Sounds Familiar?

That`s why my main criteria:
 * To make it easy environment package dependency checking.
 * To provide easy on demand package installation tool.
 * Being simple and scalable.

# <a name="how-does-it-work"></a> How does it work?

When you are called ```python ./updater check```, the script do following:
* Read all json recipes from ```recipes``` folder. 
* Then execute ```command``` prop value from json object (example ```/usr/bin/php -r 'echo phpversion();'```). Command must return version number of package or module (nothing more!!!).
* Then this value compare with ```required``` prop value and return result.

Also, if you call ```python ./updater install```, after checking, script will try to execute ```installer``` filename from ```recipes``` subdirectory with the same name as recipe filename.

# <a name="why-not"></a> Why not Puppet, Chef, SaltStack or Ansible?

That's a question that's been asked to me, why not simply use Puppet or Chef or SaltStack or Ansible? That tools are perfect. 
I've used Puppet and Chef in the past, it does everything you want it to do, that's a given.
But it remains *master-agent model* and a lot of DevOps knowledge. 

I'm just a programmer!
Sometimes I want simply write rules or *recipes* to check dependencies and install package from "Googling Stackoverflow" (write simple bash files).
Stack updater aims to be as simple as possible by providing simple recipes and Github Gist add-on system.

Also I love Python and it installed out the box on most linux distributions ;)

# <a name="start"></a>Getting started
## <a name="dependencies"></a> Dependencies
* Python (version 2.7 and above)

## <a name="configuration"></a> Configuration
* [Install](#install-recipes) or [create](#customizing) recipes on developer machine
* Copy script with app, log and recipe directory to destination machine
* configure your deploy or provision process to run this script

## <a name="running"></a> Running the application
```python ./updater [-h] {get,install,check} [gist_id]```

## <a name="cli-options"></a> Command line options

Command line option |     Params     | Description
------------------- | -------------- | ------------------------
check               |                | Check application dependencies
install             |                | Trying to install newer package version if needed (by checking)
get                 | Github Gist id | Download new recipe from Gist
--help(-h)          |                | Command line usage

## <a name="install-recipes"></a> Install recipes from [Gist](https://gist.github.com/discover)

 _Not recommended on production!!!_
 
 If the recipe is in a gist file, you can use the command ```python ./updater get GIST_ID```, and it will copy all the files in place. Be sure to check out the gist's README to see if you need to do any extra configuration.

## <a name="save-systemd-command"></a> Save as system command
Try to create symlink to executable file 
Execute from script directory

Note: Script created for all type of OS, but this instructions only for Debian-like system. Such as:
* Ubuntu, Xubuntu, Kubuntu
* Debian
* Linux Mint
* etc

```sh
chmod u+x updater
sudo ln -s updater /usr/bin
```

## <a name="logging"></a> Logging

Log files are in ```log``` directory. Current log in ```updater.log``` file. Note that you can`t see triggered command output (they are all in log file), only script output.
 
# <a name="recipes"></a> Native and Third party recipes

This is a list of user submitted Stack updater recipes. Each one contains a link to how to use it, package list and distro to use.

   Name     |     Packages     |       Distro      |    Author    
----------- | ---------------- | ----------------- | -------------
[Laravel 5.2](https://gist.github.com/levabd/13c3213830cecacbd347)|<ul><li>PHP7</li><li>NGINX</li><li>PHP mongo driver for php-fpm and php-cli</li><li>beanstalkd</li></ul>|Debian-like|[Oleg Levitsky](https://github.com/levabd) and [Max Peshkov](https://github.com/peshkov3)

# <a name="customizing"></a> Customizing

Stack updater can be extensively configured via the recipes in folder recipes.
 * Add new json file like ```recipes/recipe.json.example```. Filename is not important.
 * Add bash executable for packet installation if needed and put it in folder with same name as recipe. 
 * Comparison rules are simple, but if you want they are defined in ```app/helpers/version.py```
 
# <a name="contributing"></a> Contributing
 
 All contributions are more than welcome; [especially new recipes](#recipes)!
 
 The easiest way to share a recipe is to create a gist with the required files. Be sure to include a README with some instructions on how to use it.
 
 The [Laravel 5.2](https://gist.github.com/levabd/13c3213830cecacbd347) recipe is a great example.
 
 When you're ready, add your widget, a package list for it and supported Linux distro to the table above. Please keep the list in alphabetical order.

# <a name="filesystem"></a> Recipes and log filesystem

```python
.
├── updater #entry point
├── recipes
│    ├── recipe.json
│    ├── recipe #same name as recipe linked for
│    │    ├── bash_installer.sh #executable packet installer
│    │    ├── another_bash_installer.sh
│    │    └── ...
│    ├── another_recipe.json
│    └── ...
├── log
│    ├── updater.log #current log
│    ├── updater.log.2016-03-09_21-48-51 # for example
│    └── ...
├── app #app folder from this repo
└── ...
```

# <a name="license"></a> License
Distributed under the [MIT license](MIT-LICENSE)