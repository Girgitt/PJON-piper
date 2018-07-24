import gc
import os
import sys
import time
import logging
import win32api
import win32job
import win32con
import threading
import subprocess

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

#os.environ['COMSPEC'] = '%SystemRoot%\system32\cmd.exe'


def nope(*args, **kwargs):
    pass


class WatchDog(threading.Thread):
    TICK_SECONDS = .1
    START_SECONDS_DEFAULT = 2

    def __init__(self, suproc_command, stdin_queue, stdout_queue, parent, base_dir=None, os_env=None):
        threading.Thread.__init__(self)
        self.setDaemon(
            False)  # we want it to survive parent's death so it can detect innactivity and terminate subproccess
        self.setName('esstool-watchdog-thd')
        self._subproc_command = suproc_command
        self._os_env = os_env
        self._birthtime = None
        self._stopped = False
        self._start_failed = False
        self._pipe = None
        self._stdout_queue = stdout_queue
        self._stdin_queue = stdin_queue
        self._parent = parent
        self._autorestart = True
        self._exec_mode_shell = False
        self._exec_mode_shell_execution_completed = False
        if sys.platform == 'win32':
            self._startupinfo = subprocess.STARTUPINFO()
            self._startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._startupinfo.wShowWindow = subprocess.SW_HIDE

        self.log = logging.getLogger(self.name)
        self.log.handlers = []
        self.log.addHandler(logging.NullHandler())
        # self.log.propagate = False
        self.log.setLevel(logging.INFO)
        self.log.debug = nope
        self._base_dir = None
        try:
            if base_dir:
                os.chdir(base_dir)
                self._base_dir = base_dir
                #os.environ["PATH"] += ";"+base_dir
                #os.environ["PATH"] += ";"+"C:\Ovation\shc\config"
        except Exception as e:
            self.log.error("could not change base directory to: %s" % base_dir)

    @property
    def is_suprocess_started(self):
        if self._pipe is None:
            return False
        if self._pipe.poll() is not None:
            return False
        return True

    @property
    def autorestart(self):
        return self._autorestart

    @property
    def shell_execution_completed(self):
        if self._exec_mode_shell:
            if self._exec_mode_shell_execution_completed:
                return True
            return False
        self.log.error("swatchdog not set for single shell execution")
        return False

    def enable_autorestart(self):
        self._autorestart = True

    def disable_autorestart(self):
        self._autorestart = False

    def set_single_shell_cmd_execution_mode(self):
        self.disable_autorestart()
        self._exec_mode_shell = True
        self._exec_mode_shell_execution_completed = False
        self.START_SECONDS_DEFAULT = 0.0001

    def start_subproc(self):
        close_fds = False if sys.platform == 'win32' else True
        if sys.platform == 'win32':
            if self._os_env is None:
                os_env = os.environ
            else:
                os_env = self._os_env
            #self.log.log(1000, "cmd to open in subproc: %s" % self._subproc_command)
            #self.log.log(1000, "cwd: %s" % os.getcwd())
            #self.log.log(1000, "env: %s" % os_env)

            self._pipe = subprocess.Popen(self._subproc_command.strip(), shell=self._exec_mode_shell, close_fds=close_fds,
                                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          bufsize=0, startupinfo=self._startupinfo, env=os_env)
            #self.log.log(1000, "pipe: %s" % self._pipe)
            #self.log.log(1000, "pipe.poll(): %s" % self._pipe.poll())
            #self.log.log(1000, "is_process_started: %s" % self.is_suprocess_started)

        elif sys.platform == 'linux2':
            self._pipe = subprocess.Popen(self._subproc_command, shell=self._exec_mode_shell, close_fds=close_fds,
                                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          bufsize=0, env=os.environ, preexec_fn=os.setpgrp)

        self._birthtime = time.time()

    def poll_on_subproc(self):
        close_fds = False if sys.platform == 'win32' else True
        try:
            while True:
                try:
                    if self._stopped:
                        self.log.debug("poll on subproc: killing within thread run")
                        try:
                            if self._pipe is not None:
                                self._pipe.terminate()
                        except WindowsError:
                            self.log.error("could not kill subprocess; make sure it doesn't remain")
                        self._pipe = None
                        return True
                    else:

                        if self._pipe.poll() is not None:
                            if time.time() - self._birthtime < self.START_SECONDS_DEFAULT:
                                self.log.error('WatchDog(%r) start failed', self.getName())
                                self._stopped = True
                                self._pipe = None
                                self._start_failed = True
                                return False
                            elif not self._stopped:
                                if self._autorestart:
                                    self.log.error('WatchDog(%r) is dead, restarting', self.getName())
                                    self.stop()
                                    if not self.start(blocking=True):
                                        self.log.error("restart failed")
                                else:
                                    self.log.info("command execution completed")
                                    self._exec_mode_shell_execution_completed = True
                                    self.stop(skip_confirmation=True)

                    time.sleep(self.TICK_SECONDS)

                except Exception as e:
                    self.log.exception('WatchDog.run error: %r', e)

        finally:
            try:
                self._pipe.terminate()
            except (AttributeError, OSError):
                pass

    def start(self, blocking=False, blocking_timeout_sec=5):
        self.log.info("start called")
        self._stopped = False
        try:
            self.start_subproc()
        except Exception as e:
            self.log.exception("could not start subprocess: %s" % e.message)
            raise Exception("initialization failure for cmd: %s in base path: %s" % (self._subproc_command.strip(), self._base_dir))

        run_thd = threading.Thread(target=self.poll_on_subproc)
        run_thd.daemon = True
        run_thd.start()

        try:
            stdout_thd = threading.Thread(target=self.attach_queue_to_stdout)
            stdout_thd.daemon = True
            stdout_thd.start()
        except AttributeError:
            self.stop()
            return False

        try:
            stdin_thd = threading.Thread(target=self.attach_queue_to_stdin)
            stdin_thd.daemon = True
            stdin_thd.start()
        except AttributeError:
            self.stop()
            return False

        # stdout_process_thd = threading.Thread(target=self.process_stdout_output)
        # stdout_process_thd.daemon = True
        # stdout_process_thd.start()
        self.log.log(1000, "is subprocess started: %s" % self.is_suprocess_started)
        if blocking:
            start_ts = time.time()
            while not self.is_suprocess_started:
                time.sleep(0.01)
                if time.time() - start_ts > blocking_timeout_sec:
                    self.log.info("not started within confirmation timeout")
                    return False
        return True

    def stop(self, skip_confirmation=False):
        self.log.info("stop called")
        try:
            # self.log.info("PID to kill: %s" % self._pipe.pid)
            self._stopped = True

            if skip_confirmation:
                self.log.debug("no confirmation needed, returning")
                self._pipe.terminate()
                return True

            timeout = self.START_SECONDS_DEFAULT
            while timeout > 0:
                if not self.is_suprocess_started:
                    self.log.info("confirmed quit within quit timeout")
                    time.sleep(0.3)                                         #FIXME temporary fix to avoid exceptions due to threads not finished in time
                    return True
                else:
                    time.sleep(self.TICK_SECONDS)
                    timeout -= self.TICK_SECONDS
            self.log.info("quiting not confirmed within timeout")
            return False

        except AttributeError:
            self.log.exception("could not stop thd")
            return False

    def attach_queue_to_stdout(self):
        start_ts = time.time()
        while time.time() - start_ts < self.START_SECONDS_DEFAULT:
            if self.is_suprocess_started:

                hJob = win32job.CreateJobObject(None, "")
                extended_info = win32job.QueryInformationJobObject(hJob, win32job.JobObjectExtendedLimitInformation)
                extended_info['BasicLimitInformation']['LimitFlags'] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                win32job.SetInformationJobObject(hJob, win32job.JobObjectExtendedLimitInformation, extended_info)

                perms = win32con.PROCESS_TERMINATE | win32con.PROCESS_SET_QUOTA
                hProcess = win32api.OpenProcess(perms, False, self._pipe.pid)
                win32job.AssignProcessToJobObject(hJob, hProcess)

                self.log.debug("attaching queue to stdout")
                while True:
                    try:
                        if self._stopped:
                            break
                        if self._start_failed:
                            break
                        gc.disable()
                        nextline = self._pipe.stdout.readline()
                        if nextline == '':  # and self._pipe.poll() is not None:
                            time.sleep(0.05)
                            continue
                        self.log.debug("got from stdout: %s" % nextline.strip())
                        try:
                            self._stdout_queue.put(nextline.strip())
                        except Exception as e:
                            self.log.exception("could not put result to stdout queue, reason: %s" % e.message)
                        gc.enable()

                    except AttributeError:
                        self.log.exception("stdout queue broken")
                        break
                    finally:
                        gc.enable()
                #if self._pipe:
                #    self._pipe.stdout.close()
            else:
                if not self._stopped:
                    self.log.warning("pipe is None; can't attach queue to stdout")

            time.sleep(0.2)

    def attach_queue_to_stdin(self):
        start_ts = time.time()
        while time.time() - start_ts < self.START_SECONDS_DEFAULT:
            try:
                if self.is_suprocess_started:
                    self.log.debug("attaching queue to stdin")
                    while True:
                        try:
                            if self._stopped:
                                break
                            if self._start_failed:
                                break
                            gc.disable()
                            input_cmd = self._stdin_queue.get(timeout=.1)
                            if input_cmd == '':  # and self._pipe.poll() is not None:
                                continue
                            self.log.debug("writing to stdin: %s" % input_cmd)
                            self._pipe.stdin.write(input_cmd + '\n')
                            self._pipe.stdin.flush()
                            continue
                        except Empty:
                            continue
                        except (IOError, AttributeError):
                            break
                        finally:
                            gc.enable()
                    #if self._pipe:
                    #    self._pipe.stdin.close()
                else:
                    if not self._stopped:
                        self.log.warning("pipe is None; can't attach queue to stdin")

                time.sleep(0.2)
            except KeyboardInterrupt:
                pass
