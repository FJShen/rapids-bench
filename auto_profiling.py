import os
import subprocess
from datetime import datetime

dry_run = False

def main():
    Xcomp = False

    fastdebugJVM = True

    direct_output = True #If false, direct stdout and stderr to /dev/null

    iteration = 10

    result_dir_home = "/home/shen449/intel/vtune/projects/rapids_tpch/"

    vtune_executable = "/opt/intel/oneapi/vtune/2021.5.0/bin64/vtune "

    command_str_common_part = "-collect hotspots "\
    "-knob enable-stack-collection=true -knob enable-characterization-insights=false -target-duration-type=medium "\
    "-data-limit=0 -app-working-dir /home/shen449/rapids-bench --start-paused --app-working-dir=/home/shen449/rapids-bench "\
    "-- /home/shen449/rapids-bench/wrapper.sh benchmark.py --benchmark tpch --template template.txt --input ./tpch-tables/1_none/ "\
    "--input-format parquet --configs cpu --iterations " + str(iteration)

    dateTimeObj = datetime.now()
    datestamp = [dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute]
    datestamp = "_".join(map(str, datestamp))

    for i in range(1, 20 + 1):
        proj_identifier = "TPCH_Q"+str(i)+"_IT"+str(iteration)+"_withFrame"
        proj_identifier = (proj_identifier + "_Xcomp") if Xcomp else (proj_identifier + "_noXcomp")
        proj_identifier = (proj_identifier + "_fastdebugJVM") if fastdebugJVM else (proj_identifier + "_defaultJVM")
        proj_identifier = datestamp + "_" + proj_identifier

        result_dir = result_dir_home + proj_identifier

        output_file_name = "out_" + proj_identifier + ".txt"

        command_str_unique_part = " " + "--query q" + str(i)
        command_str = vtune_executable + "-result-dir=" + result_dir + " " + command_str_common_part + command_str_unique_part 
        #command_str = (command_str + " > " + output_file_name + " 2>&1") if direct_output else (command_str + " > /dev/null" + " 2> " + output_file_name)

        with open(output_file_name, "w") as file:
            print(command_str + "\n")
            #os.system(command_str)
            if not dry_run:
                subprocess.run(command_str.split(" "), stdout=file, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main()
