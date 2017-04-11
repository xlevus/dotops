; Example playbook.

(playbook
 (task "zypper"
       :packages ["vim"]
       :state "present"))
