# aws-serverless-oxygen-monitor-web-bluetooth

![Amplify App](https://raw.githubusercontent.com/aws-samples/aws-serverless-oxygen-monitor-web-bluetooth/master/imgs/om-app-deployed.png)



This is an example application for interacting with bluetooth pulse oximeters using an AWS Amplify web front-end and AWS Serverless backend. The Amplify front-end uses web bluetooth to interact with the device and make calls to the backend to store a user's oxygen levels and pulse rate in an Amazon DynamoDB table.

The full guide can be found on the AWS Compute Blog
https://aws.amazon.com/blogs/compute/building-a-pulse-oximetry-tracker-using-aws-amplify-and-aws-serverless/

![Application Architecture](https://raw.githubusercontent.com/aws-samples/aws-serverless-oxygen-monitor-web-bluetooth/master/imgs/oxygenMonitorApp.png)

![Levels API](https://raw.githubusercontent.com/aws-samples/aws-serverless-oxygen-monitor-web-bluetooth/master/imgs/levelsAPI.png)

![Access API](https://raw.githubusercontent.com/aws-samples/aws-serverless-oxygen-monitor-web-bluetooth/master/imgs/accessTable.png)
