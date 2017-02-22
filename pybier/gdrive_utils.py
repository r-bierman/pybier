#RB: 2/22/17

#Package imports
from PHandle import PopenHandle
from scheduler_utils import build_shell_script, run_SLURM

#General imports
from datetime import datetime
import subprocess
import os
import re

def gdrive_upload(local_dir, gdrive_loc, script_path=None, dry=False, SLURM=True):
    """
    Goal: wrapper to run gdrive sync upload
    Arguments:
        local_dir is the path to the dir to push
        gdrive_loc is the location to push to [e.g. '0B_PjHSg_YHHgSE5oeUtWblBaV1E']

    Returns:
        a process handle p that can be called upon to communicate output and error
        this allows multithreading
    """
    if dry or SLURM == False:
        dry_flag = '--dry-run' if dry else ''
        proc = subprocess.Popen(['gdrive','sync','upload',dry_flag,local_dir,gdrive_loc],
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return PopenHandle(proc)

    else:
        if not script_path:
            script_path = '/home/rbierman/'+datetime.now().strftime('%Y_%m_%d.%H_%M_%S')+'.sh'

        commands = ['gdrive sync upload'+' '+local_dir+' '+gdrive_loc]
        script_path = build_shell_script(script_path, commands)
        handle = run_SLURM(script_path)
        return handle


##########################
#    Main For Testing    #
##########################
if __name__ == '__main__':
    sherlock_dir = '/home/rbierman'
    gdrive_dir = '0B_PjHSg_YHHgSE5oeUtWblBaV1E'

    log_path = '/home/rbierman/gdrive_logs/'
    time_str = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    log_dir = os.path.join(log_path,time_str)
    os.mkdir(log_dir)
    script_path = os.path.join(log_dir,'gdrive_sync.sh')
    

    #################
    #Testing dry run#
    #################
    #p_dry = gdrive_upload(sherlock_dir, gdrive_dir, dry = True)
    #print p_dry
    #print 'It is done running: ',p_dry.finished()
    #dry_out,dry_err = p_dry.get_output()
    #print 'It is done running: ',p_dry.finished()


    ##################
    #Testing full run#
    ##################
    #p = gdrive_upload(sherlock_dir, gdrive_dir, script_path)
    #print p
    #print 'It is done running: ',p.finished()
    #out,err = p.get_output()
    #print 'out:',out
    #print 'err:',err
    #print 'It is done running: ',p.finished()

    #Do a dry run first
    p_dry = gdrive_upload(sherlock_dir, gdrive_dir, dry=True)
    dry_out,dry_err = p_dry.get_output()
    print dry_out

    #Do the full run
    

