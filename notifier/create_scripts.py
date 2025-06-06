from talkgroups import talkgroups
import os 

for id, name in talkgroups:
    #os.mkdir('/code/log_scripts')
    with open(f'/code/notifier/log_scripts/log_activity_{id}.sh', 'w+') as writer:
        writer.write("#!/bin/bash\n")
 #       writer.write("cd /code/notifier/\n")
        writer.write(f"python /code/notifier/send_skeet.py {id}\n")
    os.chmod(f'/code/notifier/log_scripts/log_activity_{id}.sh', 0o755)