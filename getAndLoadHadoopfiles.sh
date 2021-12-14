#sftp下载的目标表名称，每次创建新任务需配置！！！
remote_tableName=xlb_ms_ner_with_tags_di
#源头表文件格式,每次创建新任务需配置！！！
format=gz
#hadoop加载数据的目标表名称，每次创建新任务需配置！！！
target_tableName=xlb_ms_ner_with_tags_di_pre
#wget从远程下载的各类表的路径，自动生成。
myPath=/home/b_ods_tech_user/wget_files/$remote_tableName/${START_DAY};
#hive目标文件位置，自动生成。
TABLE_DIR=/user/hive/warehouse/ods.db/$target_tableName/dt='${START_DAY}';

echo 'The host is :'&&hostname;
#如果目录存在则清空目录里的文件。
if [ -x $myPath ]; then
    cd $myPath;
    echo 'The Path right now:' && pwd;
    ls -l;
    echo '=====Remove all the files in the target Directory'
    rm -f *.html;
    rm -f *.gz ;   
    rm -f *.snappy;
    ls -l;
    echo '===index and gzip files are cleared in the target Directory!'
else # 不存在目录则新建一个目录，避免wget下载也不存在，hadoop加载文件失败。
    mkdir -p $myPath;
    cd $myPath;
    echo 'Make a new path, The myPath is:' && pwd;
fi;
# wget特性要求回到根目录进行下载。
cd /home/b_ods_tech_user;
echo 'The path right now: ' && pwd;
#wget下载hive压缩gz文件。
echo 'Start1 to wget the files ----> ';
#python程序在2台服务器进行下载，轮询wget，确保获取文件。
wget -c -np -N -r -q http://172.16.11.200/$remote_tableName/${START_DAY}/;
echo 'finished wget 1';
wget_path1=/home/b_ods_tech_user/172.16.11.200/$remote_tableName/${START_DAY};

if [ -x $wget_path1 ]; then
    cd $wget_path1;
    echo \"first wget path:\" && pwd;
    echo \"the target fils1:\"
    ls -l;
    #将wget文件移动到目标文件夹。
    mv *.$format $myPath;
else 
    echo \"The wget_path1 is not exists!\"
fi;

#返回根目录：
cd /home/b_ods_tech_user;
echo 'The path right now: ' && pwd;
#wget下载hive压缩gz文件。
echo 'Start2 to wget the files ----> ';
wget -c -np -N -r -q http://172.16.44.72/$remote_tableName/${START_DAY}/;
echo 'finished wget 2';
wget_path2=/home/b_ods_tech_user/172.16.44.72/$remote_tableName/${START_DAY};

if [ -x $wget_path2 ]; then
    cd $wget_path2;
    echo \"second wget path:\" && pwd;
    echo \"the target fils2:\"
    ls -l;
    #将wget文件移动到目标文件夹。
    mv *.$format $myPath;
else 
    echo \"The wget_path2 is not exists!\"
fi;
#返回目标文件夹
cd \"$myPath\";
pwd;
echo 'The new Downloaded files:';
ls -l;
echo 'Finished wget the files ========> ';
#Hadoop操作将文件put到目标表中。
echo \"Start to hadoop target files===========>\";
hadoop fs -mkdir $TABLE_DIR;
if [ $(ls -l |grep \"^-\" |wc -l) -gt 0 ]; then
    echo 'start to put files!!!';
    hadoop fs -put -f *.$format  $TABLE_DIR;
    echo 'Finished putting the files into hive!'
fi
