# Script for creating the zip to be uploaded to lambda
mkdir package
cd package
cp ../../../modules/Table.py .
cp ../../../modules/DiscussionTable.py .
zip -r ../package.zip .
cd ..
zip -g package.zip DiscussionBoard.py