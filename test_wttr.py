from pywttr import Wttr
import inspect

print("Wttr dir:", dir(Wttr))
try:
    print("Wttr.weather signature:", inspect.signature(Wttr.weather))
except Exception as e:
    print("Error inspecting signature:", e)

# Try correct invocation
try:
    print("Attempting to instantiate Wttr()...")
    w = Wttr()
    print("Instance created.")
    print("Calling w.weather('Paris')...")
    # Note: 'weather' is async? The dir output showed __enter__/__exit__ so maybe context manager or sync?
    # Inspecting output again: 'session', '_session', 'close'.
    # It might be sync or async. The signature didn't say 'Coroutine'.
    
    # Let's try calling it.
    res = w.weather("Paris")
    print("Result type:", type(res))
    print("Result:", res)
except Exception as e:
    print("Invocation error:", e)
