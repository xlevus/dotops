; Example playbook.

(playbook
 (task "zypper"
       :packages ["emacs"]
       :state "present"))

