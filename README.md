DotOps
======

Devops for your dotfiles (and desktop).

Initially created to answer two questions:
 * Can I create a tool like `stow`.
 * Is there a reason Ansible/Salt really needs to use awful Jinja/YAML? (No.)

Not really fit for actual use yet. It's untested, a bit of a mess, and
doesn't implement many modules.


Goals
-----

* No support for remote hosts. Just local.
* No YAML. Instead, use a language, not markup, to define recipes.
* No 'facts'. It's local-only, and a scripted recipes, you should be able to
  fetch the facts as you need them.
* No package management. CLI and modules should be easily implementable by the
  end user in whichever language they desire. i.e. Search on $PATH.
* sudo, but only when you need it. Users shouldn't need to use sudo when
  they don't need it.
* self-documenting. Users should be able to determine recipe parameters from
  just using the application.
  
  
Installing
----------
```
pip install git+https://github.com/xlevus/dotops
```

Commands
--------
Currently there are two commands:
 * `dotops apply [recipe]`: Runs a recipe
 * `dotops exec [module] [data]`: Runs an individual module.
 
Additional commands can be implemented by placing a `dotops-<command>` 
executable on your $PATH.


Modules
-------
Currently, the following modules are implemented:

 * `pip`: Install packages via pip.
 
Additional modules currently need to be implemented as a python class with a
`main` method that takes kwargs. These can be called by using the full importable
python path. e.g.::

Via command line
```
dotops exec my_module.RubyGem '{"packages":["sass"]}'
```

Via Recipe:
```
(task "my_module.RubyGem"
      :packages ["sass"])
```

In future, modules will be able to be implemented in a fasion similar to commands.

 
Recipes
-------
See `example` directory.

Recipes are written in `hy`, a lisp-like python.


Undecided Implementation Details
--------------------------------

* Can pure-python modules be executed in the same thread, or should they be executed
  in a subprocess like currently?
* How should external modules be named? 
  * `dotops.<module>.module`
  * `<module>.dotops`
* How should modules self-document?
  * Have a `--spec` command flag?
  * Have modules take arguments in a defined format (`--package a --package b --user`)
* Should modules provide a `--check` and `--apply` interface?
  * Can this be used to detect if `sudo` is needed?
