; Example playbook.

(import [dotops.files [glob]])

(playbook
 ((task (if (= platform "Debian") "apt" "zypper")
        {:packages ["vim"]
         :state "present"})

  (task "stow"
        {:files (glob "files/*")})

