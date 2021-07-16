import os
from posixpath import split
import subprocess
import argparse


def process_jar_output(jar_output, jar_with_absolute_path, jar_dump_dir):
    debug_info_less_classes = []
    total_class_count=0
    for class_like in jar_output:
        a, b = os.path.splitext(
            class_like)  # "a/b/c/d.class" ==> "a/b/c/d", ".class"
        if b != ".class":
            continue
        else:
            #we have identified a class, we need to inspect whether this class has debug info
            #print(a.replace("/",
            #                "."))  # "com/nvidia/jack" => "com.nvidia.jack"
            total_class_count = total_class_count+1
            javap_process = subprocess.run([
                "javap", "-l", "-classpath", jar_dump_dir,
                a.replace("/", ".")
            ],
                                           capture_output=True)
            javap_output = javap_process.stdout.decode()  # byte => string

            has_line_table = javap_output.find("LineNumberTable")
            if -1 != has_line_table :
                continue

            has_variable_table = javap_output.find("LocalVariableTable")
            if has_variable_table == -1:
                #only record this class when it has neither the local var table nor the line table
                #because some classes only have either one
                debug_info_less_classes.append(class_like)

    if (len(debug_info_less_classes) > 0):
        print(
            jar_with_absolute_path + " has " + str(len(debug_info_less_classes)) +
            " out of "+str(total_class_count)+" classes lacking either a line table or a local var table. They are: \n"
        )
        for x in debug_info_less_classes:
            print("\t" + x)
    else:
        print(jar_with_absolute_path + " is good. Total is " + str(total_class_count)+" classes")


def main():
    parser = argparse.ArgumentParser(
        description=
        'Print the name of all jar files under a directory. Non-recursively.')

    parser.add_argument('path', default='.', help='path to directory')

    args = parser.parse_args()
    dir = os.path.abspath(args.path)  #absolute directory for user-specified path

    for filefullname in os.listdir(dir):
        filename, fileextension = os.path.splitext(
            filefullname)  # "foo.docx" ==> "foo", ".docx"
        if fileextension != ".jar":
            continue
        else:
            #inspect the contents of each jar file
            jar_with_absolute_path = dir + "/" + filefullname

            #use jar command to see contents of the jar file
            jar_process = subprocess.run(
                ["jar", "-tf", jar_with_absolute_path], capture_output=True)

            # byte => string => array[string]
            jar_output = jar_process.stdout.decode().splitlines()

            #extract jar file to current working directory for faster processing
            jar_dump_dir = "jar_dump"
            subprocess.run(["bash", "/home/shen449/rapids-bench/extract_jar.sh", jar_with_absolute_path, jar_dump_dir])

            process_jar_output(jar_output, jar_with_absolute_path, jar_dump_dir)
            print("end of " + filefullname + "\n\n")

            subprocess.run(["rm", "-r", jar_dump_dir])


if __name__ == "__main__":
    main()
