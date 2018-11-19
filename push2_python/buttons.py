import mido
from .constants import RGB_COLORS, RGB_DEFAULT_COLOR, ANIMATIONS, ANIMATIONS_DEFAULT, MIDO_CONTROLCHANGE, ACTION_BUTTON_PRESSED, ACTION_BUTTON_RELEASED
from .classes import AbstractPush2Section


class Push2Buttons(AbstractPush2Section):
    """Class to interface with Ableton's Push2 buttons.
    See https://github.com/Ableton/push-interface/blob/master/doc/AbletonPush2MIDIDisplayInterface.asc#Pads
    """

    buttons_map = None
    button_names_index = None
    button_names_list = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons_map = {data['Number']: data for data in self.push.push2_map['Parts']['Buttons']}
        self.button_names_index = {data['Name']: data['Number'] for data in self.push.push2_map['Parts']['Buttons']}
        self.button_names_list = list(self.button_names_index.keys())

    @property
    def available_names(self):
        return self.button_names_list

    def button_name_to_button_n(self, button_name):
        """
        Gets button number from given button name
        See xxx
        """
        return self.button_names_index.get(button_name, None)

    def set_pad_color(self, button_name, color='white', animation='static'):
        """Sets the color of the button with given name.
        See xxx
        """
        button_n = self.button_name_to_button_n(button_name)
        if button_n is not None:
            color = RGB_COLORS.get(color, RGB_DEFAULT_COLOR)
            animation = ANIMATIONS.get(animation, ANIMATIONS_DEFAULT)
            # TODO: test following implementation of set button color
            #msg = mido.Message('control_change', value=button_n, velocity=color, channel=1)
            #self.push.send_midi_to_push(msg)
        
    def on_midi_message(self, message):
        if message.type in [MIDO_CONTROLCHANGE]:
            if message.note in self.buttons_map:  # CC number corresponds to one of the buttons
                button = self.buttons_map[message.note]
                action = ACTION_BUTTON_PRESSED if message.velocity == 127 else ACTION_BUTTON_RELEASED
                self.push.trigger_action(action, button['Name'])