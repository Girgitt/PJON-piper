import os
import subprocess
from Queue import Queue, Empty
from unittest import TestCase
from WatchDog import WatchDog
import time


class TestPjonPiperFunctionally(TestCase):
    def setUp(self):
        try:
            pass
            #os.system("taskkill /im PJON-piper.exe")
        except:
            pass

        import subprocess

        from threading import Timer

        kill = lambda process: process.kill()
        cmd = ['taskkill', '/im', 'PJON-piper.exe']
        ping = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        my_timer = Timer(.1, kill, [ping])

        try:
            my_timer.start()
            stdout, stderr = ping.communicate()
            if stderr:
                print stderr
            if stdout:
                print stdout
        finally:
            my_timer.cancel()

        self._pp_com3_in = Queue()
        self._pp_com3_out = Queue()
        self._pp_com3 = WatchDog(suproc_command='x64/Release/PJON-piper.exe COM3 57600 3',
                                 stdin_queue=self._pp_com3_in,
                                 stdout_queue=self._pp_com3_out,
                                 parent=self,
                                 base_dir=os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2]))
        self._pp_com3.disable_autorestart()
        self._pp_com3.start(blocking=True, blocking_timeout_sec=2)

        self._pp_com4_in = Queue()
        self._pp_com4_out = Queue()
        self._pp_com4 = WatchDog(suproc_command='x64/Release/PJON-piper.exe COM4 57600 4',
                                 stdin_queue=self._pp_com4_in,
                                 stdout_queue=self._pp_com4_out,
                                 parent=self,
                                 base_dir=os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2]))
        self._pp_com3.disable_autorestart()
        self._pp_com4.start(blocking=True, blocking_timeout_sec=2)

    def tearDown(self):
        self._pp_com3.stop()
        self._pp_com4.stop()

    def test_PJON_piper_COM3_should_initialize(self):
        self.assertEqual("PJON instantiation...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening serial...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Setting serial...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening bus...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertRaises(Empty, lambda: self._pp_com3._stdout_queue.get(timeout=0.001))

    def test_PJON_piper_COM4_should_initialize(self):
        self.assertEqual("PJON instantiation...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening serial...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Setting serial...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening bus...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertRaises(Empty, lambda: self._pp_com4._stdout_queue.get(timeout=0.001))

    def test__com3_should_send_to_com4(self):
        self.assertEqual("PJON instantiation...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening serial...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Setting serial...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening bus...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertRaises(Empty, lambda: self._pp_com3._stdout_queue.get(timeout=0.001))
        self.assertEqual("PJON instantiation...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening serial...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Setting serial...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening bus...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertRaises(Empty, lambda: self._pp_com4._stdout_queue.get(timeout=0.001))

        self._pp_com3_in.put("send 4 data=test from 3")
        time.sleep(0.3)
        # node com3 should log what it sent
        self.assertEqual("snd rcv_id=4 data=test from 3", self._pp_com3._stdout_queue.get(timeout=.1))
        # node com4 should log received packet
        com4_rcv_data = self._pp_com4._stdout_queue.get(timeout=.1)
        self.assertTrue(com4_rcv_data.startswith('#RCV snd_id=3'))
        self.assertTrue(com4_rcv_data.endswith('data=test from 3'))
        self.assertRaises(Empty, lambda: self._pp_com4._stdout_queue.get(timeout=0.001))

    def test__com4_should_send_to_com3(self):
        self.assertEqual("PJON instantiation...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening serial...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Setting serial...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening bus...", self._pp_com3._stdout_queue.get(timeout=.1))
        self.assertRaises(Empty, lambda: self._pp_com3._stdout_queue.get(timeout=0.001))
        self.assertEqual("PJON instantiation...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening serial...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Setting serial...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertEqual("Opening bus...", self._pp_com4._stdout_queue.get(timeout=.1))
        self.assertRaises(Empty, lambda: self._pp_com4._stdout_queue.get(timeout=0.001))

        self._pp_com4_in.put("send 3 data=test from 4")
        time.sleep(0.3)
        # node com3 should log what it sent
        self.assertEqual("snd rcv_id=3 data=test from 4", self._pp_com4._stdout_queue.get(timeout=.1))
        # node com4 should log received packet
        com3_rcv_data = self._pp_com3._stdout_queue.get(timeout=.1)
        self.assertTrue(com3_rcv_data.startswith('#RCV snd_id=4'))
        self.assertTrue(com3_rcv_data.endswith('data=test from 4'))
        self.assertRaises(Empty, lambda: self._pp_com3._stdout_queue.get(timeout=0.001))

