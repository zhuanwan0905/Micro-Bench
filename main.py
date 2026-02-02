import machine
import os
import time
import gc
import framebuf
import math

class C3ProBenchmark:
    def __init__(self, width=240, height=240):
        self.width = width
        self.height = height
        self.results = {}
        self.hw_info = {
            "CPU Freq": f"{machine.freq() // 1000000} MHz",
            "Platform": os.uname().machine,
            "Firmware": os.uname().release,
            "Total RAM": f"{gc.mem_free() + gc.mem_alloc() >> 10} KB"
        }
        
        try:
            self.buf = bytearray(self.width * self.height * 2)
            self.fb = framebuf.FrameBuffer(self.buf, self.width, self.height, framebuf.RGB565)
        except MemoryError:
            self.fb = None
            self.hw_info["Graphics"] = "Disabled (Low Memory)"

    def run_all(self):
        print("="*30)
        print("  C3-PRO BENCHMARK START  ")
        print("="*30)
        
        for k, v in self.hw_info.items():
            print(f"{k}: {v}")
        
        self._bench_task("Integer Math", self.test_primes)
        
        self._bench_task("Float Math", self.test_float)
        
        self._bench_task("Memory Bus", self.test_mem)
        
        if self.fb:
            self._bench_task("Graphics Render", self.test_graphics)
        
        self.final_report()

    def _bench_task(self, name, func):
        print(f"Running {name}...", end="")
        start = time.ticks_ms()
        func()
        duration = time.ticks_diff(time.ticks_ms(), start)
        self.results[name] = duration
        print(f" Done ({duration}ms)")

    def test_primes(self):
        limit = 3000
        primes = []
        for num in range(2, limit):
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0: break
            else: primes.append(num)

    def test_float(self):
        x = 0.5
        for i in range(30000):
            x = math.sin(x) * math.cos(i)

    def test_mem(self):
        data = bytearray(10 * 1024)
        for _ in range(300):
            _ = data[:]

    def test_graphics(self):
        for i in range(100):
            self.fb.fill(0)
            self.fb.rect(10, 10, 100, 100, 0xF800, True) 
            self.fb.line(0, 0, 240, 240, 0x07E0) 
            self.fb.text("C3-PRO", 80, 110, 0xFFFF) 

    def final_report(self):
        print("\n" + "="*30)
        print("       FINAL REPORT       ")
        print("="*30)
        total_time = sum(self.results.values())
        score = int(2000000 / total_time) 
        
        for k, v in self.results.items():
            print(f"{k:15}: {v:>6} ms")
        
        print("-" * 30)
        print(f"TOTAL SCORE: {score}")
        print("="*30)

bench = C3ProBenchmark()
bench.run_all()
