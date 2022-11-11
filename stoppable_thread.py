from threading import Thread, Event


class StoppableThread(Thread):
    def __init__(self, target=None, name=None, args=(), kwargs=None, daemon=None, cleanup=None):
        super(StoppableThread, self).__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._stop_event = Event()
        self.cleanup = cleanup

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self) -> None:
        while not self.is_stopped():
            self._target(*self._args, **self._kwargs)
        if self.cleanup:
            self.cleanup()
