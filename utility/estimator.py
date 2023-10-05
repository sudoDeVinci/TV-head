import os, psutil
import gc


gc.collect()

def read_frames(folder, name):
    process = psutil.Process(os.getpid())
    a = process.memory_info().rss

    frames = list()
    
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            with open("/".join([folder, filename]), 'r', encoding = "utf-8") as csvfile:
                next(csvfile)
                
                frame = tuple((int(i), int(a), int(b), int(c)) for i, a, b, c in (line.rstrip('\n').rstrip('\r').split(",") for line in csvfile))
                # frame = tuple((int(i), int(a), int(b), int(c)) for i, a,b,c in frame)
                frames.append(frame)
    

    print(frames[0][0])
    b = process.memory_info().rss  
    print(f"\n-------------\n  {name}\n-------------\n{b-a} bytes\n{((b-a)/1024):.3f} KB\n{((b-a)/1048576):.3f} MB\n")



folder = "upload/render_pico/csvs/blink/"
read_frames(folder, 'Blink')


folder = "upload/render_pico/csvs/big_eye/"
read_frames(folder, 'Big Eye')


print("Done.")