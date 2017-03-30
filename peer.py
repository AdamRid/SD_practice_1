from pyactor.context import set_context, create_host, sleep, serve_forever, interval
from pyactor.exceptions import TimeoutError
import sys


class Peer(object):
    _tell = ['announce_2_tracker', 'init_start', 'stop_interval', 'get_peers']
    _ask = []
    _ref = ['announce_2_tracker', 'get_peers']

    # Inicializador de la/as instancia/as del Peer
    def __init__(self):
        self.tracker = None
        self.torrent_hash = None
        self.interval1 = None
        self.interval2 = None
        self.peersList = None

    def init_start(self, tracker_proxy, torrent):
        self.tracker = tracker_proxy
        self.torrent_hash = torrent
        self.interval1 = interval(self.host, 4, self.proxy, 'announce_2_tracker')
        self.interval2 = interval(self.host, 2, self.proxy, 'get_peers')

    def announce_2_tracker(self):
        if self.tracker and self.torrent_hash:
            tracker.announce(self.torrent_hash, self.proxy)
        print self.id + ' made an announce'

    def stop_interval(self):
        print "stopping interval"
        self.interval1.set()

    def get_peers(self):
        if self.torrent_hash:
            self.peersList = self.tracker.get_peers(self.torrent_hash)
            print self.id + " made an get_peers()"
            print self.peersList

if __name__ == "__main__":
    if len(sys.argv) == 4:
        host_port = sys.argv[1]
        actor_id = sys.argv[2]
        hash = sys.argv[3]

        set_context()
        h = create_host('http://127.0.0.1:' + host_port + '/')
        #print h
        tracker = h.lookup_url('http://127.0.0.1:1277/tracker', 'Tracker', 'tracker')
        p1 = h.spawn(actor_id, Peer)
        #print actor_id
        p1.init_start(tracker, hash)
        serve_forever()
    else:
        print 'Argument\'s number error to execute the peer'

