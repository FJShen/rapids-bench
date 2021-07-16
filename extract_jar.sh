rm -r $2
mkdir $2
jar_location=$(realpath $1)
cd $2
jar -xf $jar_location
echo "$jar_location is extracted"