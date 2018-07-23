#download java
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-i586.tar.gz

#set java home
JAVA_HOME="$INSTALL_HOME/jdk1.7.0_79"
PATH="$PATH:$JAVA_HOME/bin"
export JAVA_HOME PATH

#extract Java
tar -xzvf jdk-7u79-linux-i586.tar.gz

#download CTP
wget --quiet --no-check-certificate http://mirc.rsna.org/download/CTP-installer.jar

#extract CTP jar file
jar xf CTP-installer.jar
rm CTP-installer.jar

#get imageIO library
wget --quiet http://download.java.net/media/jai-imageio/builds/release/1.1/jai_imageio-1_1-lib-linux-i586.tar.gz
tar -xzvf jai_imageio-1_1-lib-linux-i586.tar.gz

rm jai_imageio-1_1-lib-linux-i586.tar.gz

#Add ImageIO libraries to Java
cp jai_imageio-1_1/lib/clibwrapper_jiio.jar $JAVA_HOME/jre/lib/ext
cp jai_imageio-1_1/lib/jai_imageio.jar $JAVA_HOME/jre/lib/ext
cp jai_imageio-1_1/lib/libclib_jiio.so $JAVA_HOME/jre/lib/i386
mkdir $JAVA_HOME/jre/i386
cp jai_imageio-1_1/lib/libclib_jiio.so $JAVA_HOME/jre/i386

rm -rf jai_imageio-1_1