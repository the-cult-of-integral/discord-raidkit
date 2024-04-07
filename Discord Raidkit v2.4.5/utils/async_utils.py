"""
Discord Raidkit v2.4.5
the-cult-of-integral

Last modified: 2023-04-24 21:08
"""

def silence_event_loop_closed_exception(func):
    """
    Decorator to silence the exception 'Event loop is closed' 
    when using the asyncio module on Windows.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise e

    return wrapper
