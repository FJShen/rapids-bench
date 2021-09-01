import os
import subprocess
from datetime import datetime

dry_run = False


def main():
    Xcomp = False

    fastdebugJVM = True

    direct_output = True  #If false, direct stdout and stderr to /dev/null

    query_range = range(1, 22 + 1)

    iteration = 6

    tests = 7  #how many times the application needs to be profiled

    result_dir_home = "/media/10T_external/shen449/intel/vtune/projects/rapids_tpch/"
    #result_dir_home = "/home/shen449/intel/vtune/projects/rapids_tpch/"

    vtune_executable = "/opt/intel/oneapi/vtune/2021.5.0/bin64/vtune "

    command_str_common_part = "-collect hotspots "\
        "-knob sampling-mode=hw -knob sampling-interval=10 -knob enable-stack-collection=true -target-duration-type=medium "\
        "-data-limit=0 -finalization-mode=deferred -app-working-dir /home/shen449/rapids-bench --app-working-dir=/home/shen449/rapids-bench "\
        "-- /home/shen449/rapids-bench/wrapper.sh benchmark.py --benchmark tpch --template template.txt --input ./tpch-tables/1_none/ "\
        "--input-format parquet --configs cpu --gc-between-runs --iterations " + str(iteration)

    dateTimeObj = datetime.now()
    datestamp = [
        dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour,
        dateTimeObj.minute
    ]
    datestamp = "_".join(map(str, datestamp))

    test_id = 1
    for test_id in range(1, tests + 1):
        for i in query_range:
            proj_identifier = "TPCH_Q" + str(i) + "_IT" + str(
                iteration) + "_TEST" + str(test_id) + "_1thrd_gc"
            proj_identifier = (proj_identifier +
                               "_Xcomp") if Xcomp else (proj_identifier +
                                                        "_noXcomp")
            proj_identifier = (proj_identifier +
                               "_fastdebugJVM") if fastdebugJVM else (
                                   proj_identifier + "_defaultJVM")
            proj_identifier = datestamp + "_" + proj_identifier

            result_dir = result_dir_home + proj_identifier

            output_file_name = "output/out_" + proj_identifier + ".txt"

            command_str_unique_part = " " + "--query q" + str(i)
            command_str = vtune_executable + "-result-dir=" + result_dir + " " + command_str_common_part + command_str_unique_part
            #command_str = (command_str + " > " + output_file_name + " 2>&1") if direct_output else (command_str + " > /dev/null" + " 2> " + output_file_name)
            print(command_str + "\n")

            if not dry_run:
                with open(output_file_name, "w") as file:
                    subprocess.run(command_str.split(" "),
                                   stdout=file,
                                   stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main()
