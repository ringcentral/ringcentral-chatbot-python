
echo 'building'
cd `dirname $0`
cd ../dev/lambda
cp -r ../../ringcentral_bot_framework ./
cp -r ../../requirements.txt ./
../../node_modules/.bin/serverless deploy