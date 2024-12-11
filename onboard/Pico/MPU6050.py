from machine import I2C
from time import sleep_ms
from typing import List, Iterable
from math import sqrt


class MPU6050:
    """
    Class for reading gyro rates and acceleration data
    from an MPU-6050 module via I2C.
    """

    def __init__(self, i2c: I2C, address: int = 0x68):
        """
        Creates a new MPU6050 class for reading gyro rates and
        acceleration data.
        :param i2c: A setup I2C module of the machine module.
        :param address: The I2C address of the MPU-6050 (0x68 default).
        """
        self.address = address
        self.i2c = i2c

    def _median(self, lst: List[float]) -> float:
        n = len(lst)
        s = sorted(lst)
        mid = n // 2
        if n % 2 == 0:
            return (s[mid - 1] + s[mid]) / 2
        else:
            return s[mid]

    def _IQR(self, lst: List[float]) -> tuple[float, float, float]:
        n = len(lst)
        s = sorted(lst)
        q1 = self._median(s[:n//2])
        q3 = self._median(s[(n+1)//2:])
        return q1, q3, q3 - q1

    def _filter(self, lst: List[float]) -> tuple[float]:
        # Compute Q1, Q3, and IQR
        q1, q3, iqr = self._IQR(lst)
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Filter the data
        return tuple(x for x in lst if lower_bound <= x <= upper_bound)

    def wake(self) -> None:
        """Wake up the MPU-6050."""
        self.i2c.writeto_mem(self.address, 0x6B, bytes([0x01]))

    def sleep(self) -> None:
        """
        Places MPU-6050 in sleep mode (low power consumption).
        Stops the internal reading of new data. Any calls to get gyro or
        accel data while in sleep mode will remain unchanged -
        the data is not being updated internally within the MPU-6050!
        """
        self.i2c.writeto_mem(self.address, 0x6B, bytes([0x40]))

    def who_am_i(self) -> int:
        """
        Returns the address of the MPU-6050 (ensure it is working).
        """
        return self.i2c.readfrom_mem(self.address, 0x75, 1)[0]

    def read_temperature(self) -> float:
        """
        Reads the temperature, in celsius, of the
        onboard temperature sensor of the MPU-6050.
        """
        data = self.i2c.readfrom_mem(self.address, 0x41, 2)
        raw_temp: float = self._translate_pair(data[0], data[1])
        temp: float = (raw_temp / 340.0) + 36.53
        return temp

    def read_gyro_range(self) -> int:
        """Reads the gyroscope range setting."""
        return self._hex_to_index(self.i2c.readfrom_mem(self.address,
                                                        0x1B, 1)[0])

    def write_gyro_range(self, range: int) -> None:
        """Sets the gyroscope range setting."""
        self.i2c.writeto_mem(self.address, 0x1B,
                             bytes([self._index_to_hex(range)]))

    def sampled_gyro(self, samples: int) -> tuple[float, float, float]:
        x = [0 for i in range(samples)]
        y = [0 for i in range(samples)]
        z = [0 for i in range(samples)]

        for i in range(samples):
            a, b, c = self.read_gyro_data()
            x[i] = a
            y[i] = b
            z[i] = c

        x = self._filter(x)
        y = self._filter(y)
        z = self._filter(z)

        xout = sum(x)/len(x)
        yout = sum(y)/len(y)
        zout = sum(z)/len(z)

        return (xout, yout, zout)

    def read_gyro_data(self) -> tuple[float, float, float]:
        """
        Read the gyroscope data, in a (x, y, z) tuple.
        """

        # set the modified based on the gyro range
        gr: int = self.read_gyro_range()
        modifier: float = None
        if gr == 0:
            modifier = 131.0
        elif gr == 1:
            modifier = 65.5
        elif gr == 2:
            modifier = 32.8
        elif gr == 3:
            modifier = 16.4

        # read data
        data = self.i2c.readfrom_mem(self.address, 0x43, 6)
        x: float = (self._translate_pair(data[0], data[1])) / modifier
        y: float = (self._translate_pair(data[2], data[3])) / modifier
        z: float = (self._translate_pair(data[4], data[5])) / modifier

        return (x, y, z)

    def read_accel_range(self) -> int:
        """Reads the accelerometer range setting."""
        return self._hex_to_index(self.i2c.readfrom_mem(
            self.address, 0x1C, 1)[0])

    def write_accel_range(self, range: int) -> None:
        """Sets the gyro accelerometer setting."""
        self.i2c.writeto_mem(self.address, 0x1C,
                             bytes([self._index_to_hex(range)]))

    def read_accel_data(self) -> tuple[float, float, float]:
        """Read the accelerometer data, in a (x, y, z) tuple."""

        ar: int = self.read_accel_range()
        modifier: float = None
        if ar == 0:
            modifier = 16384.0
        elif ar == 1:
            modifier = 8192.0
        elif ar == 2:
            modifier = 4096.0
        elif ar == 3:
            modifier = 2048.0

        # read data
        data = self.i2c.readfrom_mem(self.address, 0x3B, 6)
        x: float = (self._translate_pair(data[0], data[1])) / modifier
        y: float = (self._translate_pair(data[2], data[3])) / modifier
        z: float = (self._translate_pair(data[4], data[5])) / modifier

        return (x, y, z)

    def read_lpf_range(self) -> int:
        return self.i2c.readfrom_mem(self.address, 0x1A, 1)[0]

    def write_lpf_range(self, range: int) -> None:
        """
        Sets low pass filter range.
        :param range: Low pass range setting, 0-6.
        0 = minimum filter, 6 = maximum filter.
        """

        # check range
        if range < 0 or range > 6:
            raise Exception(f"Range {range} is not a valid filter setting.")

        self.i2c.writeto_mem(self.address, 0x1A, bytes([range]))

    # UTILITY FUNCTIONS BELOW ####
    def _translate_pair(self, high: int, low: int) -> int:
        """
        Converts a byte pair to a usable value. Borrowed from
        https://github.com/m-rtijn/mpu6050/blob/
        0626053a5e1182f4951b78b8326691a9223a5f7d/
        mpu6050/mpu6050.py#L76C39-L76C39.
        """
        value = (high << 8) + low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value

    def _hex_to_index(self, range: int) -> int:
        """
        Converts a hexadecimal range setting to an integer (index), 0-3.
        This is used for both the gyroscope and accelerometer ranges.
        """
        if range == 0x00:
            return 0
        elif range == 0x08:
            return 1
        elif range == 0x10:
            return 2
        elif range == 0x18:
            return 3
        else:
            raise Exception(f"Found unknown gyro range setting {range}")

    def _index_to_hex(self, index: int) -> int:
        """
        Converts an index integer (0-3) to a hexadecimal range setting.
        This is used for both the gyroscope and accelerometer ranges.
        """
        if index == 0:
            return 0x00
        elif index == 1:
            return 0x08
        elif index == 2:
            return 0x10
        elif index == 3:
            return 0x18
        else:
            raise Exception(f"Range index {index} invalid. Must be 0-3.")

    def _mean(self, data: Iterable) -> float:
        return sum(data)/len(data)

    def _ss(self, data: Iterable, c=None):
        if c is None:
            c = self._mean(data)
        total = total2 = 0
        for x in data:
            total += (x - c)**2
            total2 += (x - c)
        total -= total2**2/len(data)
        return total

    def variance(self, data, xbar=None):
        if iter(data) is data:
            data = list(data)
        return self._ss(data, xbar)/(len(data) - 1)

    def stdev(self, data, xbar=None):
        return sqrt(self.variance(data, xbar))
