
# Locate and Update
```sh
# good old grep
grep -rnwi '<<searchstring>>'
du -ah '<<path>>'

## Find files & apply sed to each file
find . -type f -name "_.sh" -print0 | xargs -0 sed -i "s:foo:bar:g"
find . -type f -name "_.sh" -print0 | xargs -0 sed -i "s:emr_version=\"emr-5.4.0\":emr_version=emr-5.19.0:g"

## soaks up all input and then opens output file. good for in-palace editing or use sed -i.
sed '...' file | grep '...' | sponge file

## capture "ALL" output std and err
dts=$(date +'%Y-%m-%dT%H%M%S')
./shell_script.sh 2>&1 | tee ~/log_dir/${dts}\_shell_script.sh.log

## first_element | sort-desc | pick top-10
cut -f1 -d" " file.txt | sort -n | head -10

## filter delete
ls -d /tmp/_ | grep CQINVENT_MANIFEST_02_19_19.pgp | xargs -d"\n" rm
ll -d /tmp/_ | grep veera | rev |cut -f1 -d" " | rev | grep .pgp | xargs -d"\n" rm
```

# MSCI
```sh
## mount
ip_add=172.27.206.10
sudo mount ${ip_add}:/code/ /home/hadoop/code/

# pull s3 path for all  hive tbl in db: efficient
hive -e "use dds_prod; show tables" | sed -e 's/^/SHOW CREATE TABLE schema_name./' | sed -e 's/$/;/' > show_schema_name.sql
hive -f show_schema_name.sql | grep -E "s3.?://" > s3_paths_schema_name.txt

## inline for
for i in {1..20}; do echo "$i. $(./script.sh)"; done
```

## Zeppelin inc file limit

```sh
cd /etc/zeppelin/conf/
sudo cp zeppelin-site.xml.template zeppelin-site.xml

sudo vim zeppelin-site.xml
# zeppelin.websocket.max.text.message.size and
# zeppelin.interpreter.output.limit:wq
# Default value will be 1024000 (in bytes)

# restart zeppelin
sudo stop zeppelin
sudo start zeppelin

sudo systemctl stop zeppelin
sudo systemctl start zeppelin
```

## GPG

```sh
ll ~/.gnupg/
gpg --list-secret-keys
gpg --armor --export "XXXXXXXX" > pub.key
gpg --armor --export-secret-keys "XXXXXXXX" > sec.key
gpg --import sec.key
```

## JQ

```sh
aws emr list-clusters --active | jq --arg cid "$cl_id" '.Clusters | .[] | select(.Id==$cid)'
```

## pgsql

```sh
sudo apt-get install postgresql postgresql-contrib
dpkg -l | grep postgres
sudo service postgresql start
sudo -u postgres psql
```

## Virtual Env

```sh
## windows venv or
python3 -m venv .env

virtualevn
virtualenv -p python C:\Users\me\virtualEnvs\prjname


## virtual_env
python + tab (list all python)
virtualenv -p python3.7 [directory]
```

## Docker

```sh
sudo systemctl start docker
docker-compose up -d

docker build -t <name> .
docker tag <<name>>:latest <uri>/<name:latest>
aws ecr get-login
docker push <uri>
history

common registry is 000000000000.dkr.ecr.us-east-1.amazonaws.com/<name>
```

## Snowflake service

```sh
service_user_dbtvault t6gmJG]g
```

## windows Spark History Server local activate

```sh
### activate virtual env
# C:\Users\me\virtualEnvs\venv_name\Scripts\activate
cd %SPARK_HOME%
bin\spark-class.cmd org.apache.spark.deploy.history.HistoryServer
```