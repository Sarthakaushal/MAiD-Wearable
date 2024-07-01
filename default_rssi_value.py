import queue
import time

timeout_seconds = 10

from core import BleScanner
import pandas as pd
if __name__ == '__main__':
    #stores the discovered devices
    buffer = queue.Queue()
    
    scanner = BleScanner(buffer)
    scanner.start()
    
    # time to run the scan for
    TIME_LIMITs = [10,50, 100, 200, 300]
    avg_time = {}
    for time_lim in TIME_LIMITs:
        start_time = time.time()
        time_keeper = {}
        try:
            while time.time()-start_time < time_lim:
                if not buffer.empty():
                    device_address, rssi, name = buffer.get()
                    # print(f"Device Address: {device_address}, RSSI: {rssi}, Name: {name}")
                    obj = time_keeper.get(name, [])
                    obj.append(rssi)
                    time_keeper[name] = obj
                    
        except KeyboardInterrupt:
            print("\nStopping scan...")
            # Stopping the scanner thread (by canceling the event loop)
            scanner.loop.call_soon_threadsafe(scanner.loop.stop)
            break
        print(time_keeper)
        
        for k in time_keeper.keys():
            obj = avg_time.get(time_lim, {})
            obj[k] = sum(time_keeper[k])/len(time_keeper[k])
            obj['time_duration'] = time_lim
            avg_time[time_lim] = obj
        print(avg_time)
    df_comapt_list = [avg_time[k] for k in avg_time.keys()]
    df = pd.DataFrame(df_comapt_list)
    cols = list(df.columns)
    cols.remove('time_duration')
    df.to_csv('output/avg_rssi_vals.csv', columns=['time_duration']+cols,
              index = False)
        