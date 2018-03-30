部署文档

环境
   Centos
   数据库相应表建立， 帐号密码对应上。

步骤
1  创建目标目录  mkdir /develop/btc2
2  解压文件      tar xvf deploy.tar.gz
3  将解压后的deploy/btc2目录下的文件整体拷贝到 /develop/btc2下
此时进入/develop/btc2下面， ls看到目录如下图
 
4 修改配置文件config.json
{
	"btcserver": "http://192.168.1.128:8332",   
	"btcuser": "dylan",
	"btcpassword": "123456",
	"dbserverip": "192.168.1.144",
	"dbservername": "bitcoin",
	"dbuser": "root",
	"dbpassword": "",
}
5 确认crond服务是启动的
6 执行 sh requirements.centos.sh 确认安装成功
7执行 sh install.sh 
8 检查 /develop/btc2/cron.run.log 文件会被创建，且有日志输出
9检查 /develop/btc2/cron.run.delete.log文件会被创建，且有日志输出
10 执行 query.sql
select tx_height , count(*) from tx_out group by tx_height order by create_time ;
会有数据逐渐入库。

维护
    当前目录下会有json文件不断生成， 因为文件较小，且为了调试， 暂没有删除文件， 可以每个月删除一个月之前的文件。git clean -f
 
    

其他
导出整个数据库结构和数据
mysqldump -h localhost -uroot -p bitcoin > bitcoin.sql

