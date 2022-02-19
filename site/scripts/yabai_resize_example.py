#!/usr/bin/env python3

import json
import subprocess
import sys
import time

class AppMover():
    def __init__(self):
        self.time_padding = 0.2

    def app_space_id(self, app):
        for window in self.windows():
            if window['app'] == app:
                return window['space']

    def contract_bottom(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize bottom:0:-{amount}".split(' '), check=True)

    def contract_left(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize left:{amount}:0".split(' '), check=True)

    def contract_right(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize right:-{amount}:0".split(' '), check=True)

    def contract_top(self, app, amount):
        print(f"Contracting left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize top:0:{amount}".split(' '), check=True)

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
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize bottom:0:{amount}".split(' '), check=True)

    def expand_left(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize left:-{amount}:0".split(' '), check=True)

    def expand_right(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize right:{amount}:0".split(' '), check=True)

    def expand_top(self, app, amount):
        print(f"Resizing left: {app} - {amount}")
        self.focus_app(app)
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --resize top:0:-{amount}".split(' '), check=True)

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
                subprocess.run(f"/opt/homebrew/bin/yabai -m window --focus {window['id']}".split(' '), check=True)
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
        subprocess.run(f"/opt/homebrew/bin/yabai -m window --insert {direction}".split(' '), check=True)
        self.move_app_to_space(new_app, self.app_space_id(anchor_app))

    def move_app_to_space(self, app, space):
        print(f"Moving: {app} to: {space}")
        if self.app_space_id(app) == space:
            print(f"No need to move. {app} is already on space {space}")
        else:
            # TODO: Make this a recursive function instead of copy paste    
            self.focus_app(app)
            subprocess.run(f"/opt/homebrew/bin/yabai -m window --space {space}".split(' '), check=True)
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
            subprocess.run(f"/opt/homebrew/bin/yabai -m window --space {space}".split(' '), check=True)
            for i in range(1, 30):
                if self.app_space_id(app) == space:
                    print(f"- Moved: {app} to: {space}")
                    time.sleep(self.time_padding)
                    return True
                time.sleep(self.time_padding)
                print('.', end='')

            print("- Move didn't work. Trying again")
            self.focus_app(app)
            subprocess.run(f"/opt/homebrew/bin/yabai -m window --space {space}".split(' '), check=True)
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
            subprocess.run(f"/opt/homebrew/bin/yabai -m window --insert stack".split(' '), check=True)
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
        results = subprocess.run(['/opt/homebrew/bin/yabai', '-m', 'query', '--spaces'], capture_output=True, check=True)
        return json.loads(results.stdout.decode('utf-8'))

    def stage_apps(self):
        staging_space = len(self.spaces())
        for window in self.windows():
            if window['is-floating'] == False:
                self.move_app_to_space(window['app'], staging_space)

    def windows(self):
        results = subprocess.run('/opt/homebrew/bin/yabai -m query --windows'.split(' '), capture_output=True)
        return json.loads(results.stdout.decode('utf-8'))


if __name__ == "__main__":
    am = AppMover()
    am.time_padding = 0.2

    am.stage_apps()

    am.move_app_to_space('Adobe Photoshop 2022', 2)
    am.move_app_to_space('Code', 5)
    am.move_app_to_space('Discord', 6)
    am.move_app_to_space('Music', 7)
    am.move_app_to_space('1Password 7', 8)
    am.move_app_to_space('Keychain Access', 9)

    am.move_app_to_space('iTerm2', 1)
    am.insert_from_anchor('iTerm2', 'west', 'Google Chrome')
    am.expand_left('iTerm2', 660)
    am.insert_from_anchor('iTerm2', 'north', 'GitHub Desktop')
    am.expand_top('iTerm2', 390)
    am.insert_from_anchor('iTerm2', 'south', 'CodeRunner')
    am.expand_bottom('iTerm2', 130)
    am.insert_from_anchor('CodeRunner', 'east', 'DBeaver Community')
    am.insert_from_anchor('Google Chrome', 'south', 'nvALT')
    am.insert_from_anchor('iTerm2', 'east', 'Sublime Text')
    am.expand_right('iTerm2', 300)
    am.insert_from_anchor('GitHub Desktop', 'east', 'Safari')
    am.expand_right('GitHub Desktop', 140)

    am.place_app_under_app("Soulver 3", "Google Chrome")

    am.focus_app('Music')
    am.focus_app('iTerm2')

