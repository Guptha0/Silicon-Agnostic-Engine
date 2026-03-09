from flask import Flask, render_template, jsonify
import psutil
import platform
import gc 
import os
import time
import subprocess
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telemetry')
def telemetry():
    try:
        battery = psutil.sensors_battery()
        cpu_load = psutil.cpu_percent()
        
        # 1. Energy Economics Math
        watts = 15 + (cpu_load * 0.3) 
        cost_per_hour = (watts / 1000) * 7 
        
        # 2. Battery & OS Data
        bat_percent = battery.percent if battery else 100
        # FIXED: Named it power_status to match the logic below
        power_status = "🔌 PLUGGED IN" if (battery and battery.power_plugged) else "🔋 ON BATTERY"
        operating_system = f"{platform.system()} {platform.release()}"

        # 3. Decision Logic
        if bat_percent < 25 and "BATTERY" in power_status:
            decision = "ECO-PATH: Throttling Logic"
            color = "#ff4757" # Red
        elif cpu_load > 75:
            decision = "THERMAL-PROTECT: Sequential Execution"
            color = "#ffa502" # Orange
        else:
            decision = "OPTIMIZED: Silicon Peak Performance"
            color = "#2ed573" # Green

        return jsonify({
            "cpu_load": cpu_load,
            "ram_usage": psutil.virtual_memory().percent,
            "battery": bat_percent,
            "power": power_status,
            "watts": round(watts, 2),
            "cost": round(cost_per_hour, 4),
            "os_info": operating_system,
            "decision": decision,
            "color": color
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/purge_memory')
def purge_memory():
    initial_mem = psutil.virtual_memory().available
    gc.collect() 
    final_mem = psutil.virtual_memory().available
    saved = (final_mem - initial_mem) // (1024 * 1024)
    return jsonify({"status": "Purged", "saved_mb": max(0, saved)})

@app.route('/stress_test')
def stress_test():
    try:
        start_time = time.time()
        # ECE Logic: Stressing ALU with Floating Point Math
        result = 0
        for i in range(1, 5000000):
            result += math.sqrt(i) * math.sin(i)
            
        duration = round(time.time() - start_time, 4)
        return jsonify({
            "status": "Success",
            "duration": duration,
            "timestamp": time.strftime("%H:%M:%S"),
            "load_score": round(1 / duration, 2) if duration > 0 else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/system_action/reap_heavy')
def reap_heavy():
    reaped = []
    try:
        # DevOps Feature: Process Reaper
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            if proc.info['cpu_percent'] > 20.0:
                reaped.append(proc.info['name'])
        
        msg = f"Reaper Scan: {', '.join(reaped)}" if reaped else "No heavy loads detected"
        return jsonify({"msg": msg})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ping_test')
def ping_test():
    try:
        # DevOps Infrastructure Ping
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", "8.8.8.8"]
        subprocess.check_output(command, timeout=2)
        return jsonify({"latency": "Active", "details": "Link Stable"})
    except:
        return jsonify({"latency": "Offline", "details": "Connection Dropped"})

if __name__ == '__main__':
    # host='0.0.0.0' allows you to view this on your phone via your laptop's IP!
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)