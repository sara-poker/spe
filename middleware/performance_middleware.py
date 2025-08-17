import time
import os
import psutil

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.process = psutil.Process(os.getpid())

    def __call__(self, request):
        # ثبت زمان شروع
        start_time = time.time()
        cpu_start = self.process.cpu_times()

        # پردازش درخواست
        response = self.get_response(request)

        # ثبت زمان پایان
        end_time = time.time()
        cpu_end = self.process.cpu_times()

        # محاسبه مصرف CPU و زمان
        elapsed_time = end_time - start_time
        cpu_usage = {
            'user': cpu_end.user - cpu_start.user,
            'system': cpu_end.system - cpu_start.system,
        }

        # نمایش اطلاعات در لاگ یا سرصفحه HTTP
        # print("------------------------------")
        print(f"Request: \"{request.path}\"")
        print(f"Time: \"{elapsed_time:.3f}s\"")
        print(f"CPU: \"{cpu_usage}\"")
        # print("------------------------------")
        response["X-Request-Duration"] = f"{elapsed_time:.3f}s"
        response["X-CPU-Usage"] = str(cpu_usage)

        return response
