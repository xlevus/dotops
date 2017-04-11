; Example playbook.

(setv pip-packages ["pylint" "flake8" "jedi"])

(playbook
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
       :state "present"))
