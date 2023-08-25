# Bitbucket + Lambda Boilerplate

This repository is a Bitbucket + Lambda boilerplate for auto-deployment of Python 3 functions on AWS Lambda.

## Deployment

To deploy the function, you need to add your AWS keys to the Bitbucket repository variables:
<pre>
  <code>AWS_ACCESS_KEY_ID: "KEY FROM FROM AWS"</code>
  <code>AWS_SECRET_ACCESS_KEY: "SECRET KEY FROM FROM AWS"</code>
  <code>AWS_DEFAULT_REGION: "AWS REGION eg. us-east-1"</code>
  <code>FUNCTION_NAME: "LAMBDA FUNCTION NAME"</code>
</pre>
Once you have added the keys, the function will be automatically deployed to AWS Lambda on every push to the Bitbucket repository.
