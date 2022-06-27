while true
do
    if test -f {0}/logs/latest.log
    then
        echo "文件存在，开始监听"
        {
            while inotifywait -e modify {0}/logs/latest.log
            do
                echo "文件写入，wget进行请求"
                wget -qO- http://qqbot.xzy.center/MCServer?uuid={1}&msg=$(tail -1 {0}/logs/latest.log | awk '{print $4  $5  $6  $7  $8  $9  $10  $11}') >> /dev/null
            done
        } || {
            echo "监听执行失败"
        }
    else
        echo "文件不存在，可能是MC正在滚动日志"
    fi
done