apt-get update
apt-get install wget

#download java
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-i586.tar.gz

#set java home
JAVA_HOME="$INSTALL_HOME/jdk1.7.0_79"
PATH="$PATH:$JAVA_HOME/bin"
export JAVA_HOME PATH

#extract Java
tar -xzvf jdk-7u79-linux-i586.tar.gz

wget https://sourceforge.net/projects/pentaho/files/Data%20Integration/7.0/pdi-ce-7.0.0.0-25.zip/download
