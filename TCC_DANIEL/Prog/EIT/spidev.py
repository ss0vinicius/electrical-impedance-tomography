class SpiDev:
    def open(self, bus, device):
        print(f"Mock SPI open: bus={bus}, device={device}")

    def xfer2(self, data):
        print(f"Mock SPI transfer: data={data}")
        return data

    def close(self):
        print("Mock SPI close")
