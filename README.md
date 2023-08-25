# Bitbucket + Lambda Boilerplate

This repository is a Bitbucket + Lambda boilerplate for auto-deployment of Python 3 functions on AWS Lambda.

## Deployment

To deploy the function, you need to add your AWS keys to the Bitbucket repository variables:
<pre>
  <code>AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID</code>
  <code>AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY</code>
  <code>AWS_DEFAULT_REGION: $AWS_REGION</code>
  <code>FUNCTION_NAME: $FUNCTION_NAME</code>
</pre>
Once you have added the keys, the function will be automatically deployed to AWS Lambda on every push to the Bitbucket repository.
