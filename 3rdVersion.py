from ctypes import Structure, sizeof, c_float, c_int32, c_wchar, c_int
import mmap, time, csv
from operator import concat

import csvfile


class SPageFileGraphic(Structure):
    _fields_ = [
        ("currentTime", c_wchar * 15),
        ("lastTime", c_wchar * 15),
        ("bestTime", c_wchar * 15),
        ("split", c_wchar * 15),
        ("completedLaps", c_int),
        ("position", c_int),
        ("iCurrentTime", c_int),
        ("iLastTime", c_int),
        ("iBestTime", c_int),
        ("sessionTimeLeft", c_float),
        ("distanceTraveled", c_float),
        ("currentSectorIndex", c_int),
        ("lastSectorTime", c_int),
        ("numberOfLaps", c_int),
        ("tyreCompound", c_wchar * 33),
        ("penaltyTime", c_float),
        ("flag", c_int),
        ("penalty", c_int),
        ("surfaceGrip", c_float),
    ]

    def toDict(self):
        return {
            "split": self.split,
            "completedLaps": self.completedLaps
        }

    def numLaps(self):
        return self.numberOfLaps

    def currTime(self):
        return self.currentTime


class SPageFilePhysics(Structure):
    _fields_ = [
        ("speedKmh", c_float),
        ("velocity", c_float * 3),
        ("accG", c_float * 3),
        ("wheelSlip", c_float * 4),
        ("wheelLoad", c_float * 4),
        ("wheelsPressure", c_float * 4),
        ("wheelAngularSpeed", c_float * 4),
        ("tyreWear", c_float * 4),
        ("tyreDirtyLevel", c_float * 4),
        ("tyreCoreTemperature", c_float * 4),
        ("numberOfTyresOut", c_int),
        ("pitLimiterOn", c_int),
        ("abs", c_float),
        ("ballast", c_float),
        ("airDensity", c_float),
        ("airTemp", c_float),
        ("roadTemp", c_float),
        ("localAngularVel", c_float * 3),
        ("finalFF", c_float),
        ("performanceMeter", c_float),

        ("engineBrake", c_int),
        ("ersRecoveryLevel", c_int),
        ("ersPowerLevel", c_int),
        ("ersHeatCharging", c_int),
        ("ersIsCharging", c_int),
        ("kersCurrentKJ", c_float),

        ("drsAvailable", c_int),
        ("drsEnabled", c_int),

        ("brakeTemp", c_float * 4),
        ("clutch", c_float),

        ("tyreTempI", c_float * 4),
        ("tyreTempM", c_float * 4),
        ("tyreTempO", c_float * 4),

        ("isAIControlled", c_int),

        ("tyreContactPoint", c_float * 4 * 3),
        ("tyreContactNormal", c_float * 4 * 3),
        ("tyreContactHeading", c_float * 4 * 3),

        ("brakeBias", c_float),

        ("localVelocity", c_float * 3),

        ("P2PActivations", c_int),
        ("P2PStatus", c_int),

        ("currentMaxRpm", c_int),

        ("mz", c_float * 4),
        ("fx", c_float * 4),
        ("fy", c_float * 4),
        ("slipRatio", c_float * 4),
        ("slipAngle", c_float * 4),

        ("tcinAction", c_int),
        ("absInAction", c_int),
        ("suspensionDamage", c_float * 4),
        ("tyreTemp", c_float * 4),
    ]

    def toDict(self):
        return {
            "tyreWear": self.tyreWear[0],
            "tyreTemp": self.tyreTemp[0],
            "tyreDirtyLevel": self.tyreDirtyLevel[0],
            "tyreCoreTemperature": self.tyreCoreTemperature[0],
        }

    def getTyreWear(self):
        return self.tyreWear[0]


def read_physics():
    buf = mmap.mmap(-1, sizeof(SPageFilePhysics), u"Local\\acpmf_physics")
    data = SPageFilePhysics.from_buffer(buf)
    return data.toDict()

def read_graphics():
    buf = mmap.mmap(-1, sizeof(SPageFileGraphic), u"Local\\acpmf_graphics")
    data = SPageFileGraphic.from_buffer(buf)
    return data.toDict()

while True:
    data = []
    graphicsDict = read_graphics()
    physicsDict = read_physics()
    data.append(physicsDict.get('tyreWear'))
    data.append(physicsDict.get('tyreDirtyLevel'))
    data.append(physicsDict.get('tyreCoreTemperature'))
    data.append(physicsDict.get('tyreTempI'))
    data.append(physicsDict.get('tyreTempM'))
    data.append(physicsDict.get('tyreTempO'))

    if data[0] == 0.0:
        continue

    time.sleep(0.5)