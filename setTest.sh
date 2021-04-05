

for i in ./Peer/*messageList.json; do oldfile=$i; rm -v $oldfile; done
for i in ./Peer/chatList.json; do oldfile=$i; rm -v $oldfile; done
for i in ./TestPeer/Peer/*messageList.json; do oldfile=$i; rm -v $oldfile; done
for i in ./TestPeer/Peer/chatList.json; do oldfile=$i; rm -v $oldfile; done

for i in ./Peer/DownloadFile/*; do oldfile=$i; rm -v $oldfile; done
for i in ./TestPeer/Peer/DownloadFile/*; do oldfile=$i; rm -v $oldfile; done
for i in ./TestPeer/Peer/UploadFile/*; do oldfile=$i; rm -v $oldfile; done

cp -r Peer TestPeer/
cp TestPeer/config.json TestPeer/Peer/config.json

