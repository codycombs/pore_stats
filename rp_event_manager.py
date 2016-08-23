import csv
import copy

class RPEventManager(object):
    def __init__(self):
        self._parameters = []

        self._events = []
        self._selected_events = []
        self._targeted_event = None


    def add_event(self, event):
        self._events.append(event)
        self._selected_events.append(event)
        event._id = len(self._events)
        if self._targeted_event == None:
            self._targeted_event = event

        self.sort_events(self._events)
        self.sort_events(self._selected_events)

        return

    def sort_events(self, events):
        moves = -1
        while moves != 0:
            moves = 0
            for i, event in enumerate(events[:-2]):
                if events[i]._data[0,0] > events[i+1]._data[0,0]:
                    moves+=1
                    temp_event = copy.copy(events[i])
                    events[i] = events[i+1]
                    events[i+1] = temp_event

        return



    def clear_events(self):
        self._events = []
        self._selected_events = []
        self._targeted_event = None

        self._parameters = []

        return

    def set_targeted_event(self, event):
        self._targeted_event = event
        return

    def increment_targeted_event(self):
        targeted_id = self._targeted_event._id

        for i, event in enumerate(self._events):
            if event._id == targeted_id:
                targeted_index = (i + 1)%len(self._events)
                break

        self._targeted_event = self._events[targeted_index]

        return

    def decrement_targeted_event(self):
        targeted_id = self._targeted_event._id
        targeted_index = 0
        for i, event in enumerate(self._events):
            if event._id == targeted_id:
                targeted_index = (i - 1)%len(self._events)
                break

        self._targeted_event = self._events[targeted_index]

        return

    def toggle_selected(self, event):
        event_id = event._id
        if self.is_selected(event) == True:
            self._selected_events = [event for event in self._selected_events if event._id != event_id]
        else:
            self._selected_events.append(event)

        self.sort_events(self._selected_events)

        return

    def select_event(self, event):
        event_id = event._id
        if self.is_selected(event) == False:
            self._selected_events.append(event)
            self.sort_events(self._selected_events)
        return

    def unselect_event(self, event):
        event_id = event._id
        if self.is_selected(event) == True:
            self._selected_events = [event for event in self._selected_events if event._id != event_id]
            self.sort_events(self._selected_events)
        return

    def is_selected(self, event):
        event_id = event._id
        is_selected = False
        if event._id in [event._id for event in self._selected_events]:
            is_selected = True
        else:
            is_selected = False

        return is_selected

    def is_targeted(self, event):
        is_targeted = False
        if self._targeted_event._id == event._id:
            is_targeted = True

        return is_targeted

    def save_events(self, file_path):

        print 'saving events!'

        f = open(file_path, 'w')
        writer = csv.writer(f, delimiter = '\t')

        for i, event in enumerate(self._selected_events):
            header_row = ['event#', i, 'length', event._data.shape[0],\
                'baseline', event._baseline[0], event._baseline[1], event._baseline[2], event._baseline[3]]

            writer.writerow(header_row)

            for row in event._data:
                writer.writerow([row[0], row[1]])

        f.close()

        return