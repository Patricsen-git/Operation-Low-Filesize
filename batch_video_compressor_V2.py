import os
import time
from tqdm import tqdm
import datetime
import subprocess

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)


video_files = []

# for file in next(os.walk(os.curdir), (None, None, []))[1]:  # [] if no file:
for file in os.listdir("."):
    if os.path.isfile(os.path.join(".", file)):
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".mp4":   
            # file = os.path.abspath(file)
            video_files.append(file)    
        elif file_extension == ".mkv":
            video_files.append(file)    




# first get all files, then process them 
print("Found the following files: ")
for video in video_files:
    # print every file and ask user
    print(video)




choice = input("Proceeed with compressing? (Y/n)")




if choice in ["n", "N", "No", "no"]:
    import sys
    sys.exit("Aborting.. ")

thumbnail = "temp_thumbnail.png"

crf_value = 17      # 17 is a good compromise between filesize and compression artifacts 
codec = "libx264"   # can select from libx265 or libx264


if "posix" in os.name:
    # linux distribution
    ffmpeg_string = "ffmpeg"
elif "nt" in os.name:
    # windows
    ffmpeg_string = "ffmpeg.exe"
else:
    # mac or whatever / not supported
    print(f"Your operating system {os.name} is not supported. Try Windows or Linux.")







# file reduction sum variable
file_reduction_sum = 0
video_runtime_sum = 0

start_time = time.time()
for index, file in enumerate(tqdm(video_files)):
# for file in tqdm(video_files):
# for index, file in enumerate(video_files):
    # then perform the command
    filename, file_extension = os.path.splitext(file)

    # get video duration
    video_runtime_sum += get_length(file)

    # then do the actual compression
    command = f'{ffmpeg_string} -i "{file}" -y -vf scale=1920:1080 -v quiet -stats -map 0:v -map 0:a -c:a copy -vcodec {codec} -crf {crf_value} "converted_{file}"'

    os.system(command)
    
    #std_out = os.popen(command).read()
    #tqdm.write(std_out)

    # rescale:
    # ffmpeg -i input4kvid.mp4 -vf scale=1920:1080 -c:a copy output1080vid.mp4
    # both in one command (does no harm if footage is already 1080p)
    # ffmpeg -i testfile.mp4 -vf scale=1920:1080 -map 0:v -map 0:a -c:a copy -vcodec libx264 -crf 17 out_1080p.mp4

    # next, rename original file, can be removed after compression  
    os.rename(file, f"orig_{file}")
    os.rename(f"converted_{file}", file)

    # filesize calculation
    file_reduction_factor = os.path.getsize(f"orig_{file}") / os.path.getsize(f"{filename}{file_extension}")
    file_reduction_sum += file_reduction_factor

    # print remaining files
    #print(f"\n File {index+1} out of {len(video_files)} completed. \n {len(video_files)-index-1} remaining. \n")

exec_time = (time.time() - start_time)

print(f'\n Compressed {len(video_files)} files in {str(datetime.timedelta(seconds=round(exec_time, 0)))}. \n Average filesize reduction: {file_reduction_sum/len(video_files):.2f}x. Average processing speed: {video_runtime_sum/exec_time:.2f}x. \n')
# print(f'Average execution time per file: {exec_time/len(video_files)} \n')

