import time, mmap
from pyaccsharedmemory import accSharedMemory

sm = accSharedMemory()

ema = lambda p,x,a=0.3: x if p is None else a*x + (1-a)*p
last_lap = None
fuel_start = None
fuel_per_lap = None

def get_snapshot():
    snap = sm.read_shared_memory()
    g = p = None
    if snap is None:
        return None, None
    if g is None and hasattr(snap, "gas"): print("broooooo")
    if p is None and hasattr(snap, "brake"):  p = snap.get("brake")

    print(type(snap), g, p, snap)
    return g, p

def field(obj, *names, default=None):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return default

print("Starting… waiting for live data. Make sure ACC is ON TRACK and Shared Memory is ON.", flush=True)

while True:
    g, p = get_snapshot()

    if not g or not p:
        print("[wait] No graphics/physics yet. Are you on track? Shared Memory ON?", flush=True)
        time.sleep(1.0)
        continue

    # lap  = field(g, "completedLaps", "completed_laps", default=None)
    # clt  = field(g, "currentLapTime", "current_lap_time", default=0.0)
    # llt  = field(g, "lastLapTime",    "last_lap_time",    default=0.0)
    # fuel = field(p, "fuel", default=None)
    # wear = field(p, "tyreWear", "tyre_wear", default=None)
    #
    # if lap is None or fuel is None:
    #     print("[wait] Graphics/physics present, but lap/fuel missing. Still loading/menus?", flush=True)
    #     time.sleep(1.0)
    #     continue
    #
    # lap_time = clt if (clt or 0) > 0 else (llt or 0)
    #
    # if last_lap is None:
    #     last_lap = lap
    #     fuel_start = fuel
    #
    # if lap != last_lap:
    #     used = max(0.0, (fuel_start or 0) - (fuel or 0))
    #     fuel_per_lap = ema(fuel_per_lap, used)
    #     fuel_start = fuel
    #     last_lap = lap
    #     if fuel_per_lap is not None:
    #         print(f"[Lap {lap}] Fuel/lap EMA: {fuel_per_lap:.2f} L", flush=True)
    #
    # wear_str = "n/a"
    # if wear is not None:
    #     try:
    #         wear_str = ", ".join(f"{w:.2f}" for w in wear)
    #     except Exception:
    #         wear_str = str(wear)
    #
    # print(f"Fuel {fuel:5.1f} L | LapT {lap_time:7.3f} | Wear {wear_str}", flush=True)
    # time.sleep(0.2)
