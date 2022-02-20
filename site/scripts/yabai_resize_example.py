#!/usr/bin/env python3

import json
import subprocess
import sys
import time


###########################################################
# NOTE: Make sure that you manually open as many spaces
# as you want to use via Mission Control: 
#
# https://support.apple.com/en-us/HT204100
#
# For the example, you'll need 3.
###########################################################



def move_things_into_place():

    ###########################################################
    # These lines set things up. You don't need 
    # to mess with them

    am = AppMover()
    am.stage_apps()

    ###########################################################
    # This is the example run of the script. It uses apps
    # that are installed by default so it should run with 
    # no extra fiddling. Any other apps that you have open
    # will end up on the last space you have open. (And
    # remember that you'll need to have at least 3 open
    # for the example to run properly
    ###########################################################

    ##### 
    # Move Safari to space 1 
    am.move_app_to_space('Safari', 1)

    # Move Activity Monitor to the west (left) of Safari
    am.insert_from_anchor('Safari', 'west', 'Activity Monitor')

    # Move Terminal below Activity Monitor 
    am.insert_from_anchor('Activity Monitor', 'south', 'Terminal')

    # Move Dictionary to the west (left) of Dictionary 
    am.insert_from_anchor('Terminal', 'west', 'Dictionary')

    # Stack Console under Safari 
    am.place_app_under_app("Console", "Safari")

    # Expand Activity Monitor (and the apps under it) right
    am.expand_right('Activity Monitor', 200)


    ##### 
    # Move Keychain Access to space 2
    am.move_app_to_space('Keychain Access', 2)

    ##### 
    # Switch focus back to Safari 
    am.focus_app('Safari')



###########################################################
# This is the class that executes your instructions. 
# You don't need to do anything with it unless you 
# want to hack around with it. 
###########################################################


class AppMover():
    def __init__(self):
        self.time_padding = 0.2
        self.yabai_path = '/opt/homebrew/bin/yabai'

    def app_space_id(self, app):
        for window in self.windows():
            if window['app'] == app:
                return window['space']

    def contract_bottom(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize bottom:0:-{amount}".split(' '), check=True)

    def contract_left(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize left:{amount}:0".split(' '), check=True)

    def contract_right(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize right:-{amount}:0".split(' '), check=True)

    def contract_top(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize top:0:{amount}".split(' '), check=True)

    def ensure_app_is_open(self, app):
        print(f"Ensuring {app} is open")
        if self.window_id_for_app(app) == None:
            print(f"Opening {app}")
            subprocess.run(['open', '-a', app])
            for i in range(1,50):
                time.sleep(self.time_padding)
                print('.', end='')
                if self.window_id_for_app(app) != None:
                    print(f"Opened {app}")
                    return True
            print(f"Could not open {app} in a reasonalbe time")
            print("Process halted.")
            sys.exit()

    def expand_bottom(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize bottom:0:{amount}".split(' '), check=True)

    def expand_left(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize left:-{amount}:0".split(' '), check=True)

    def expand_right(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize right:{amount}:0".split(' '), check=True)

    def expand_top(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"{self.yabai_path} -m window --resize top:0:-{amount}".split(' '), check=True)

    def focus_app(self, app):
        print(f"Switching focus to {app}")
        # See if it's already in focus
        for window in self.windows():
            if window['app'] == app and window['has-focus']:
                print(f"{app} already has focus")
                return True
        # otherwise make sure it's open and switch focus to it
        self.ensure_app_is_open(app)
        print(f"Focusing: {app}")
        for window in self.windows():
            if window['app'] == app:
                subprocess.run(f"{self.yabai_path} -m window --focus {window['id']}".split(' '), check=True)
                for i in range(1,14):
                    print(f"Checking focus on: {app}")
                    for check_window in self.windows():
                        if check_window['has-focus'] == True and check_window['app'] == app:
                            print(f"Confirmed {app} is in focus")
                            # need this padding to let the system catch up
                            time.sleep(self.time_padding)
                            return True
                    time.sleep(self.time_padding)
        print(f"Could not focus on {app}")
        print("Process halted")
        sys.exit()

    def insert_from_anchor(self, anchor_app, direction, new_app):
        print(f"Insert from anchor: {anchor_app} - {direction} - {new_app}")
        self.focus_app(anchor_app)
        subprocess.run(f"{self.yabai_path} -m window --insert {direction}".split(' '), check=True)
        self.move_app_to_space(new_app, self.app_space_id(anchor_app))

    def move_app_to_space(self, app, space):
        print(f"Moving: {app} to: {space}")
        if self.app_space_id(app) == space:
            print(f"No need to move. {app} is already on space {space}")
        else:
            # TODO: Make this a recursive function instead of copy paste    
            self.focus_app(app)
            subprocess.run(f"{self.yabai_path} -m window --space {space}".split(' '), check=True)
            print(f"Confirming {app} moved to space {space}")
            for i in range(1, 20):
                if self.app_space_id(app) == space:
                    print(f"- Moved: {app} to: {space}")
                    time.sleep(self.time_padding)
                    return True
                time.sleep(self.time_padding)
                print('.', end='')

            print("- Move didn't work. Trying again")
            self.focus_app(app)
            subprocess.run(f"{self.yabai_path} -m window --space {space}".split(' '), check=True)
            for i in range(1, 30):
                if self.app_space_id(app) == space:
                    print(f"- Moved: {app} to: {space}")
                    time.sleep(self.time_padding)
                    return True
                time.sleep(self.time_padding)
                print('.', end='')

            print("- Move didn't work. Trying again")
            self.focus_app(app)
            subprocess.run(f"{self.yabai_path} -m window --space {space}".split(' '), check=True)
            for i in range(1, 30):
                if self.app_space_id(app) == space:
                    print(f"- Moved: {app} to: {space}")
                    time.sleep(self.time_padding)
                    return True
                time.sleep(self.time_padding)
                print('.', end='')

            print()
            print(f"Failed to move {app} to space {space}")
            print(f"Process halted")
            sys.exit()

    def place_app_under_app(self, lower_app, upper_app):
        print(f"Placing {lower_app} under {upper_app}")
        if self.app_space_id(lower_app) == self.app_space_id(upper_app):
            print(f"Skipping: {lower_app} is already in space {self.app_space_id(lower_app)} with {upper_app}")
            return False
        else:
            self.focus_app(upper_app)
            subprocess.run(f"{self.yabai_path} -m window --insert stack".split(' '), check=True)
            self.focus_app(lower_app)
            self.move_app_to_space(lower_app, self.app_space_id(upper_app))
            print(f"Placed: {lower_app} under {upper_app}")

    def window_id_for_app(self, app):
        for window in self.windows():
            if window['app'] == app:
                print(f"App {app} has ID: {window['id']}")
                return window['id']
        return None

    def spaces(self):
        results = subprocess.run([self.yabai_path, '-m', 'query', '--spaces'], capture_output=True, check=True)
        return json.loads(results.stdout.decode('utf-8'))

    def stage_apps(self):
        staging_space = len(self.spaces())
        for window in self.windows():
            if window['is-floating'] == False:
                self.move_app_to_space(window['app'], staging_space)

    def windows(self):
        results = subprocess.run(f'{self.yabai_path} -m query --windows'.split(' '), capture_output=True)
        return json.loads(results.stdout.decode('utf-8'))


if __name__ == "__main__":
    move_things_into_place()
