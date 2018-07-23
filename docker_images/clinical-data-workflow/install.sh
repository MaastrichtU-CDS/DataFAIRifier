apt-get update
apt-get install -y wget unzip python python-pip

#download java
wget wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz

#set java home
JAVA_HOME="$INSTALL_HOME/jdk1.8.0_141"
PATH="$PATH:$JAVA_HOME/bin"
export JAVA_HOME PATH

#extract Java
tar -xzvf jdk-8u141-linux-x64.tar.gz

#wget https://sourceforge.net/projects/pentaho/files/Data%20Integration/7.0/pdi-ce-7.0.0.0-25.zip/download

#unzip pentaho
unzip pdi-ce-7.1.0.0-12.zip -d $INSTALL_HOME/pentaho

#unzip d2rq
unzip d2rq-0.8.3-dev.zip -d $INSTALL_HOME
chmod -R 777 $INSTALL_HOME/d2rq-0.8.3-dev

#install cwltool
pip install --upgrade pip
pip install cwltool

#put CWL scripts in correct folder
mkdir /cwl_scripts
mv /curl.cwl.yml /cwl_scripts/curl.cwl.yml
mv /d2r_tool.cwl.yml /cwl_scripts/d2r_tool.cwl.yml
mv /pentaho_tool.cwl.yml /cwl_scripts/pentaho_tool.cwl.yml
mv /workflow.cwl.yml /cwl_scripts/workflow.cwl.yml

#put specific config files (pentaho & CWL settings) in correct folder
mkdir /config
mv /load_csv_to_db.ktr /config/load_csv_to_db.ktr
mv /settings_cwl.yml /config/settings_cwl.yml
mv /registry_mapping.ttl /config/registry_mapping.ttl

#put data (if available) in specific folder
mkdir /data
mv /thunderSubSet.csv /data/thunderSubSet.csv