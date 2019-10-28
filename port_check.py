#!/usr/bin/python
import socket
import time
from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

ip = "127.0.0.1"
port = 80
retry = 3
delay = 1
timeout = 2

# Check Status definition
STATUS_OK = 0
STATUS_WARNING = 1
STATUS_CRITICAL = 2
STATUS_UNKNOWN = 4

class HelloCheck(AgentCheck):
    def checkHost(self,ip, port):
        ipup = False
        for i in range(retry):
            if self.isOpen(ip, port):
                    ipup = True
                    break
            else:
                    time.sleep(delay)
        return ipup

    def isOpen(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            s.close()

    def check(self, instance):
        check_name = 'custom.host.healthcheck'
        hostname = socket.gethostname()
        tags=['check:health']
        if self.checkHost(ip, port):
            print ip + " is UP"
            self.service_check(check_name, STATUS_OK, tags, None, 'Port 22 accessible')
            self.gauge('custom.host.healthcheck.gauge', 1, tags=tags)
        else:
            print "down"
            self.service_check(check_name, STATUS_CRITICAL, tags, None, 'Port 22 inaccessible')
            self.gauge('custom.host.healthcheck.gauge', 0, tags=tags)
