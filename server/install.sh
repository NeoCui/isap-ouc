#!/bin/bash
DESTDIR=/usr/share/
SOURDIR=./isapoucserver

ISAPOUC=/usr/share/isapoucserver/isapouc
ISAPOUCD=/usr/share/isapoucserver/isapoucd
GRABNEWS=/usr/share/isapoucserver/grabnews

BIN=/usr/bin

SERVICEFILE=./isapouc
SERVICEDIR=/etc/init.d
SERVICE=isapouc
CHKCONFIG=/sbin/chkconfig
LOG=/var/log/isapouclog.log

echo "复制文件..."
cp -a ${SOURDIR} ${DESTDIR}

echo "创建链接..."
ln -s ${ISAPOUC}  ${BIN}
ln -s ${ISAPOUCD} ${BIN}
ln -s ${GRABNEWS} ${BIN}
touch ${LOG}
chmod 777 ${LOG}
cp ${SERVICEFILE}  ${SERVICEDIR}
cd ${SERVICEDIR}
chmod 777 ${SERVICE}
exec ${CHKCONFIG} --add  ${SERVICE}



