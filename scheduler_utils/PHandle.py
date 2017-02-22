from subprocess import check_output, CalledProcessError
import time
import sys
import re

#############################
#                           #
#   Super Process Handle    #
#                           #
#############################
class ProcessHandle(object):
    """
    ProcessHandle is a superclass for what a handle to a process
        should include. Examples of processes are SLURM scripts or
        running straight on the command line.

    Each subclass of ProcessHandle should be able to provide a single
        handle, and describe what kind of handle it is. The subclass
        must also be able to get the output, which will always be a blocking
        call, and tell if the process has finished, which will never be blocking
    """
    def __init__(self, handle, kind):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def get_output(self):
        raise NotImplementedError

    def finished(self):
        raise NotImplementedError


#############################
#                           #
#         SLURMHandle       #
#                           #
#############################
class SLURMHandle(ProcessHandle):
    def __init__(self, handle, out_path = None, err_path = None, kind = 'SLURM'):
        self.handle = handle
        self.out_path = out_path
        self.err_path = err_path
        self.finished()

    def __repr__(self):
        out_str = ''
        out_str += 'SLURMHandle: jobid['+self.handle+'] '
        out_str += 'out_path['+str(self.out_path)+'] '
        out_str += 'err_path['+str(self.err_path)+']\n'
        return out_str

    def get_output(self):
        if self.finished():
            out = None
            err = None
            if self.out_path:
                with open(self.out_path,'r') as out_file:
                    out = out_file.read()

            if self.err_path:
                with open(self.err_path,'r') as err_file:
                    err = err_file.read()

            return out,err

        else:
            time.sleep(60)
            return self.get_output() #<-- was forgetting to return recursive case
                

    def finished(self):
        in_queue = True
        try:
            check_output(['squeue','-j',self.handle])
        except CalledProcessError as e:
            return True

        details = ''
        try:
            details = check_output(['sacct','--format=State','-j',self.handle])
        except CalledProcessError as e:
            return True

        running = 'RUNNING' in details
        finished = 'COMPLETED' in details
        if in_queue or running:
            try:
                details = check_output(['scontrol','show','jobid','-dd',self.handle])
                self.out_path = re.findall(r'StdOut=(.*?)(?:\s+|$)',details)[0]
                self.err_path = re.findall(r'StdErr=(.*?)(?:\s+|$)',details)[0]
                return False
            except CalledProcessError as e:
                return True
            
        elif finished:
            return True
        else:
            sys.stderr.write('ERROR: SLURM process not RUNNING nor COMPLETED\n')
            return True
        

#############################
#                           #
#         PopenHandle       #
#                           #
#############################
class PopenHandle(ProcessHandle):
    def __init__(self, handle, kind = 'Popen'):
        self.handle = handle

    def __repr__(self):
        out_str = 'PopenHandle: handle['+str(self.handle)+']\n'
        return out_str

    def get_output(self):
        out,err = self.handle.communicate()
        return out,err

    def finished(self):
        return self.handle.poll() != None

#############################
#                           #
#            Main           #
#                           #
#############################
if __name__ == '__main__':
    sys.stdout.write('Tests for PHandle coming soon\n')
    sys.exit(0)

