; Example recipe.

(setv pip-packages ["pylint" "flake8" "jedi"])

(recipe

 (if False
   (task "Fake"
         :do-not "run"))

 (task "pip"
       :version 2
       :user True
       :packages pip-packages)

 (task "pip"
       :version 3
       :user True
       :packages pip-packages)

 (task "zypper"
       :packages ["emacs"]
       :state "present")

 )
