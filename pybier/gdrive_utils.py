#RB: 2/22/17

#Package imports
from PHandle import PopenHandle
from scheduler_utils import build_shell_script, run_SLURM

#General imports
from datetime import datetime
from pkg_resources import resource_filename
import subprocess
import json
import sys
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
    #Build up the command
    cmd = ['gdrive','sync','upload']
    if dry:
        cmd.append('--dry-run')
    cmd += [local_dir,gdrive_loc]

    if not SLURM :
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return PopenHandle(proc)

    else:
        if not script_path:
            script_path = os.path.join(os.getenv('HOME'),datetime.now().strftime('%Y_%m_%d.%H_%M_%S')+'.sh')

        cmd = ' '.join(cmd)
        script_path = build_shell_script(script_path, [cmd]) #<-- needs to be a list of commands
        handle = run_SLURM(script_path)
        return handle


def get_gdrive_loc(gdrive_loc=None, stem=None):
    if gdrive_loc:
        return gdrive_loc

    config_path = resource_filename(__name__,os.path.join('data','gdrive_config.json'))
    gdrive_config = {}
    with open(config_path,'r') as config_f:
        gdrive_config = json.load(config_f)

    parent_gdrive = gdrive_config['parent_gdrive']
    if parent_gdrive == 'None':
        sys.stderr.write('ERROR: No gdrive_loc given and no parent_gdrive set\n')
        sys.exit(1)

    gdrive_loc = gdrive_mkdir(parent_gdrive,stem=stem)
    return gdrive_loc


def gdrive_mkdir(parent_loc, stem=None):
    stem = '' if not stem else stem+'_'
    name = stem+'backup_'+datetime.now().strftime('%Y_%m_%d.%H_%M_%S')
    cmd = ['gdrive','mkdir','--parent',parent_loc,name]
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    phandle = PopenHandle(proc)
    out,err = phandle.get_output()
    gdrive_loc = re.findall(r'Directory (.*?) created',out)
    if len(gdrive_loc) != 1:
        sys.stderr.write('ERROR: failed to make gdrive dir\n')
        sys.exit(1)
 
    return gdrive_loc[0]


   
    

##########################
#    Main For Testing    #
##########################
if __name__ == '__main__':
    #gdrive_mkdir('0B_PjHSg_YHHgVl8tbllncVZsR0U')
    print get_gdrive_loc()

    #sherlock_dir = '/home/rbierman'
    #gdrive_dir = '0B_PjHSg_YHHgSE5oeUtWblBaV1E'

    #log_path = '/home/rbierman/gdrive_logs/'
    #time_str = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    #log_dir = os.path.join(log_path,time_str)
    #os.mkdir(log_dir)
    #script_path = os.path.join(log_dir,'gdrive_sync.sh')
    

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
    #p_dry = gdrive_upload(sherlock_dir, gdrive_dir, dry=True)
    #dry_out,dry_err = p_dry.get_output()
    #print dry_out

    #Do the full run
    

