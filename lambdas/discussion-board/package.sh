# pip install --target ./package requests
# cd package
# zip -r ../package.zip .
# cd ..
mkdir package
cd package
cp ../../../modules/Table.py .
cp ../../../modules/DiscussionTable.py .
zip -r ../package.zip .
cd ..
zip -g package.zip DiscussionBoard.py
# zip -g package.zip ../../modules/Table.py
# zip -g package.zip ../../modules/DiscussionTable.py