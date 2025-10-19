init python in JK:
    _constant = True

    class NotificationsClass():
        def __init__(self):
            self.scheduled_notifications = []
            self.active_notification = None
            self.initialized = False

        def show_queued_notifications(self):
            if self.active_notification is None:
                self._show_next_notification()

        def show_queued_notifications_delayed(self):
            if self.active_notification is None and len(self.scheduled_notifications) > 0:
                renpy.invoke_in_thread(self._delayed_show_next_notification)

        def schedule_notification(self, message):
            self.scheduled_notifications.append(message)

            if self.active_notification is None and self.initialized:
                self._show_next_notification()

        def _show_next_notification(self):
            if len(self.scheduled_notifications) > 0:
                self.active_notification = self.scheduled_notifications.pop(0)
                renpy.notify(self.active_notification)
                renpy.invoke_in_thread(self._queue_next_notification)

        def _queue_next_notification(self):
            renpy.time.sleep(3.25)
            self.active_notification = None
            self._show_next_notification()

        def _delayed_show_next_notification(self):
            renpy.time.sleep(5)
            self._show_next_notification()

                