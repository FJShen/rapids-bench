import os

def main():
    Xcomp = False

    fastdebugJVM = False

    iteration = 10

    result_dir_home = "/home/shen449/intel/vtune/projects/rapids_tpch/"

    vtune_executable = "/opt/intel/oneapi/vtune/2021.5.0/bin64/vtune "

    command_str_common_part = "-collect hotspots "\
    "-knob enable-stack-collection=true -knob enable-characterization-insights=false -target-duration-type=medium "\
    "-data-limit=0 -app-working-dir /home/shen449/rapids-bench --start-paused --app-working-dir=/home/shen449/rapids-bench "\
    "-- /home/shen449/rapids-bench/wrapper.sh benchmark.py --benchmark tpch --template template.txt --input ./tpch-tables/1_none/ "\
    "--input-format parquet --configs cpu --iterations " + str(iteration)

    for i in range(1, 20 + 1):
        proj_identifier = "TPCH_Q"+str(i)+"_IT"+str(iteration)+"_withFrame"
        proj_identifier = (proj_identifier + "_Xcomp") if Xcomp else (proj_identifier + "_noXcomp")
        proj_identifier = (proj_identifier + "_fastdebugJVM") if fastdebugJVM else (proj_identifier + "_defaultJVM")

        result_dir = result_dir_home + proj_identifier

        command_str_unique_part = " " + "--query q" + str(i)
        command_str = vtune_executable + "-result-dir=" + result_dir + " " + command_str_common_part + command_str_unique_part
        print(command_str + "\n")
        #os.system(command_str)


if __name__ == '__main__':
    main()
