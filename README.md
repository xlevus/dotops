DotOps
======

Devops for your dotfiles (and desktop).


Goals
-----

* No support for remote hosts. Just local.
* No YAML. Instead, scripting language to define recipes.
* No 'facts'. It's local-only, and a scripted recipes, you should be able to
  fetch the facts as you need them.
* No package management. CLI and modules should be easily implementable by the
  end user in whichever language they desire. i.e. Search on $PATH.
