PROVIDER_LIST = [
	{
		"name":"amazonaws s3",
		"cname":["amazonaws.com", "s3"],
		"response":["NoSuchBucket", "The specified bucket does not exist"]
	},
	{
		"name":"heroku", 
		"cname":["herokudns.com"], 
		"response":["There's nothing here, yet.", "herokucdn.com/error-pages/no-such-app.html", "<title>No such app</title>"]
	},
	{
		"name":"amazonaws elastic beanstalk", 
		"cname":["elasticbeanstalk.com"], 
		"response":[]
	}
]