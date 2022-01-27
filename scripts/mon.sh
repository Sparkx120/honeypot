le true; do netstat -p --numeric-hosts | grep nyancat | tee -a conn.log; echo "" >> conn.log; sleep 1; done
