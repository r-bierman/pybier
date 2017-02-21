from PHandle import PopenHandle, SLURMHandle
import subprocess
import sys
import os
import re

def run_SLURM(script_path, out_path=None, err_path=None, queue = 'horence', mem='10000', time='48:00:00'):
    """
    Goal: submit a SLURM job
    Arguments:
        the path to the shell script to be executed is the only required argument
        the out_path and err_path are optional since they can be made from script_path
        there are the standard optional arguments for SLURM

    Returns:
        A SLURMHandle object which can be checked for completion and get input/output
    """
    script_dir = os.path.dirname(script_path)
    base_name = os.path.basename(script_path)
    no_ext = os.path.splitext(base_name)[0]
    if not out_path:
        out_path = os.path.join(script_dir,no_ext+'.out')
    if not err_path:
        err_path = os.path.join(script_dir,no_ext+'.err')

    p = subprocess.Popen(['sbatch','-p',queue,'--mem='+mem,'--time='+time,
                          '-o',out_path,'-e',err_path,script_path],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    job_sub = p.stdout.readline().strip()
    print 'Job sub:',job_sub
    job_num = re.findall('Submitted batch job (.*)',job_sub)[0]
    print 'Job num:',job_num
    handle = SLURMHandle(job_num)
    return handle
    
def build_shell_script(script_path,commands):
    """
    Goal: build a shell script to be submitted to SLURM
    Arguments:
        script_path is the location of where to create the script
        commands is a list of string, where each string will be a new line of the script
            each line is expected to be a full command that can have out/err piped
        out/err_path are optional, will be built similar to script_path if not given

    Returns:
        The script_path that was built
    """
    with open(script_path,'w') as script:
        script.write('#!/bin/bash\n')
        script.write('sleep 60\n')
        for ind,command in enumerate(commands):
            script.write(command+'\n')

    return script_path

