"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

async_utils.py has async.io utilities for the program.
async_utils.py was last updated on 20/04/23 at 20:15 UTC.
"""

def silence_event_loop_closed_exception(func):
    """
    Decorator to silence the exception 'Event loop is closed' 
    when using asyncio on Windows.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise e

    return wrapper
