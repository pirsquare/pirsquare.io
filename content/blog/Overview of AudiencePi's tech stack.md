Title: Overview of AudiencePi's tech stack
Author: Ryan Liao
Date: 24th August 2015
FacebookImage: http://pirsquare.io/images/August-2015/tech-stack-report.png
FacebookDescription: In this post, I will be sharing AudiencePi's tech stack to give others an idea on the fun and challenges in building an adtech product. 

**TL;DR**  
Console (Web UI): Django, jQuery, Handlebars, SASS, Postgres, Celery, Memcached  
LB: Nginx, HAProxy, GCE Load Balancing  
RTB: Golang, Aerospike  
Predictive Modeling: Scikit-Learn  
Data Store: Bigquery, Aerospike, Postgres  
Data Pipeline: Python scripts as cron jobs  
Devops: Ansible  
Monitoring: Stackdriver, Datadog, Librato, Pganalyze  
Logging: Logentries  
DNS: Route53  
CDN: MaxCDN  


*Full content below ...*


AudiencePi will cease operations on 31th August 2015. As such, I would like to take this time to lookback and reflect on AudiencePi's journey. In this post, I will be sharing AudiencePi's tech stack to give others an idea on the fun and challenges in building an adtech product. First, let's understand what AudiencePi does and what are some of our key differentiators.

AudiencePi is a self-serve demand side platform for online display advertising. We provide sophisticated media planning tools to help buyers deliver their campaign's objectives.
 
**Differentiation** 
 
- Self-Serve  
- Inventory Planner for Media Buyers  
- Sprite Ads  
- Efficient Bidder with Configurable Optimization Strategy  
- Powerful Reporting Engine which allows slicing of report views in different aggregations to show trends.  
- Retarget Marketplace  


Some of the technical challenges in building such system includes:  

- Ability to response to majority of bidrequests within 100ms (inclusive of round-trip time)  
- Automatically train and update machine learning models used for predicting bidding price  
- Automate data pipelines to produce training data for machine learning as well as reporting data  
- Supports slicing of reporting data in different dimensions and aggregations  
- Deploying and maintaining large number of servers across different clusters  
- Maintaining budget and ensure that campaign is paced appropriately  
- Easy to use UI since everything is self-serve  

## Acronyms ##
**GCE - Google Compute Engine**  
This is the equivalent of AWS EC2 for Google Cloud.
 
**GCS - Google Cloud Storage**  
This is the equivalent of AWS S3 for Google Cloud.

**RTT - Round Trip Time**  
Time it takes for a signal or packet to be sent to a destination and back again.


## Server Types ##

In total there are 19 different types of servers that we maintain in our system. Below are some of the server types that we use.

**Bidder**  
Written in Golang. Data retrieved in real time are either from:

- Preloaded data in memory
- Aerospike servers

AudiencePi's bidder handles parsing and processing of bidrequests recieved from supply partners. Initially we wanted to use Erlang to write the bidder, but we found it easier to build our prototype in Python and later translate it to Golang. Personally, this is also an excuse for me to learn a new programming language =). I like Golang since it is productive for me. The time it takes for me to write testable code in Golang is comparable to the time it takes to write the same thing in Python. This is a huge plus point in a startup enironment, when you need to move fast and at the same time, ensure that your code have sufficient test coverage. Lastly, most supply partners requires us to response within a 100ms window, so [Golang's impressive performance](http://benchmarksgame.alioth.debian.org/u64q/go.html) is also a vital aspect for us! 

One of the challenges in building a bidder is to eke out CPU time for your bidder to evaluate as many creatives as possible within a single bidrequest. As the number of creatives your bidder evaluates increases, so do the total processing time. Currently our bidders have a upper limit of evaluating 120 creatives at one go. There are optimization tricks like making use of indexes to reduce processing time, but we'll leave that on a seperate post.



**MLPipe**  
We run a single instance of MLpipe server to query bigquery and generate training data for machine learning on a daily basis. Training data from bigquery are exported to GCS for further use.

![tech-stack-mlpipe](http://pirsquare.io/images/August-2015/tech-stack-mlpipe.png)



**Trainer**  
Trainer servers download training data from GCS and use Scikit-Learn to build predictive models for all our advertisers campaigns. Trained models are uploaded to GCS for further use. One advantage of decoupling data munging and models building tasks into MLPipe and Trainer servers is that we can easily add new Trainer servers when there's a need to build models for more campaigns.

![tech-stack-trainer](http://pirsquare.io/images/August-2015/tech-stack-trainer.png)

Initially considered using [Graphlab (now called Dato)](https://dato.com/) over Scikit-Learn but licensing costs and increased prediction latency meant that Scikit-Learn is a better option. Other considerations includes Jubatus, MLlib and H2O but since we're not familiar with Java/Scala we're sticking to Scikit-Learn.



**Predictor**  
Predictor servers download trained models from GCS to provide predictive service for our bidders. We use [msgpack-rpc-python](https://github.com/msgpack-rpc/msgpack-rpc-python) library to communicate with bidder servers. That library uses tornado for RPC networking and msgpack for data serialization. Passed data are features used for predictions. Total latency between bidder and predictor communications can be up to 20ms.

To make use of all CPU cores in a single server, we use supervisord to create a number of tornado processes equivalent to number of CPU cores in a server minus one (n-1). For a 16 core server, we will be creating 15 tornado processes. Created tornado processes are mapped to individual TCP port. Requests for bidder servers goes through our TCP Load Balancer (HAProxy) which will than direct traffic to each tornado process in a round robin manner.

![tech-stack-predictor](http://pirsquare.io/images/August-2015/tech-stack-predictor.png)


**Adserver**  
Written in Golang and data are retrieved via aerospike servers. Adserver handles serving of ad impressions. Impressions/Clicks/Conversions are all captured by adserver.



**Pixel**  
Written in Golang and data are retrieved via aerospike servers. Pixel server handles serving of tracking and usersync pixels.



**Feedback**  
Written in Golang and data are retrieved via aerospike servers. Feedback server provides endpoint to collect winning bids from supply partners.



**Filtering**  
Written in Golang and data are retrieved via aerospike servers. Filtering server runs routine background jobs to filter ineligible campaigns. Some campaign eligibility checks like budget, schedule and dayparting doesn't need to be processed in real time. As such, we're offloading such tasks to background filtering jobs so that our bidder have more processing time available.



**Console**  
Django, jQuery, Handlebars, SASS, Postgres, Celery & Memcached is used to build our console. Nothing special since everything used is a cookie cutter for building Django application.



## Hosting ##
We use Google Cloud and Softlayer to host our servers.

Google Cloud is our favorite hosting provider and the benefits of using Google Cloud includes: 

- GCE is [cheaper](http://googlecloudplatform.blogspot.sg/2015/01/understanding-cloud-pricing.html) than other cloud computing solutions like EC2  
- Automatically reduces your server costs instead of requiring you to reserve instances  
- Fast provisioning of servers. Even faster than DigitalOcean.  
- Live migration for maintenance.  
- Prices [follow Moore's Law](https://cloud.google.com/pricing/philosophy/). History of aggressively reduce server costs.  
- Documentations is good. Easy to navigate around their docs. Much better than the ones provided by Softlayer  
- Web UI is straight forward and productive to use. Makes you feel like it's a chore to use Softlayer's UI.  
- Low latency when connecting directly to Doubleclick Ad Exchange.  
- BigQuery is one of the best BigData-As-A-Service solution out in the market right now and having most of your infrastructure on Google Cloud provides deeper integrations to BigQuery.  
- My personal favorite, they have an [API Explorer tool](https://cloud.google.com/bigquery/docs/reference/v2/datasets/get) to test api queries. This is very useful when you are writing client libraries.  


Benefits of Softlayer Bare Metal:

- No bandwidth charges for private networking  
- Servers available in [many regions ](http://www.softlayer.com/data-centers) 
- Access to 24/7 support without paying additional fees  


Initially we wanted to use Google Cloud for all our computing infrastructure but one issue we had is that Google Cloud only allows you to choose from [3 server locations](https://cloud.google.com/compute/docs/zones?hl=en). These locations are namely Iowa for US region, Belgium for Europe region and Taiwan for Asia region. To reduce RTT, we need access to more server locations so that we can place our servers closer to supply partners.


As such, for regions that can't be covered effectively by Google Cloud, we placed independent lb/bidder/adserver/aerospike/pixel/predictor servers on various softlayer regions to:  

- Response to bidrequests  
- Serve ad and pixels  
- Track impressions/clicks/conversions  
- Maintain users cookie pool for that region  


## Datastore ##
**Aerospike**  
Aerospike is our OLTP system. We use Aerospike to store any data that needs to be retrieved within sub-milliseconds and also metadata like:

- Cron job's last ran timestamp
- Predictive model's last trained date
- Report's last ran timestamp

We classify data stored in aerospike into 2 groups, global and region. Global data consists of data like campaign data that needs to exist in all clusters globally. We store these data in `global` namespace. Region data consists of data like user profile data that only needs to exist within a region. We store these data in `region` namespace.


`Global` namespace uses star topology, where writes goes to the primary cluster and data is replicated to all other clusters. Our primary cluster here refers to the cluster where our console stack is located, since this is where all campaign updates are coming from.

![tech-stack-star](http://pirsquare.io/images/August-2015/tech-stack-star.png)

`Region` namespace uses active-active topology setup. Each cluster is paired with another cluster in the same region. For example, in Google Cloud's Europe region, we would pair zone `europe-west1-b` with `europe-west1-c`. Data can be written to any cluster and will be replicated to the paired cluster. Since both clusters are located within the same region, replications for writes/reads is fast. In the event that a cluster goes down, traffic will failover to the other cluster paired to it.

![tech-stack-active](http://pirsquare.io/images/August-2015/tech-stack-active.png)

We use [SSD + RAM](http://www.aerospike.com/docs/operations/plan/capacity/#provision-for-a-flash-ssd-database) setup for aerospike since it is the most cost effective manner to deploy aerospike. Local SSDs from GCE is a [perfect match](http://googlecloudplatform.blogspot.sg/2015/01/Aerospike-demonstrates-RAM-like-performance-with-Local-SSDs.html) for this setup.

Other considerations: Couchbase

> Note: Due to the excess costs in maintaining multiple cluster, our current stack only consists of a single cluster in each region.



**Bigquery**  
Bigquery is our OLAP system and data warehouse. We stream data directly into bigquery and use it as primary storage for our data in its rawest form. Many of our tables in bigquery are in the range of terabytes. When required, we also use bigquery to run ad-hoc queries.

Reporting  
Bigquery is used to aggregate reporting data into hourly/daily precision and later transferred to our console's database (postgres). This step reduces the amount of data our console's database needs to process, making it faster for our console users. Since bigquery doesn't have a direct connector for Postgres, transferring data to Postgres requires multiple steps.

1. Export query results in csv format to GCS
2. Download data from GCS
3. Pipe data to Postgres database with stdin

Training Data (for predictive models)  
For training data, bigquery is used for data munging. We run queries to process data into formats making it easier for scikit-learn to consume the data. Using a distributed data processing engine like bigquery is essential since pandas have memory limitations when your data size gets to the terabytes range.

Other considerations: TreasureData, Vertica



**Postgres**  
Postgres is our console's database. One of the interesting thing our console's database does is to run complex SQL queries to slice report data in different dimensions and aggregations. This allows our advertisers to analyze their campaigns in different ways and identify trends. For example, our advertisers can see how well each domains perform for their campaign on different day of week. 

![tech-stack-report](http://pirsquare.io/images/August-2015/tech-stack-report.png#img-with-border)

If you are using Postgres, you should take a look at [common table expressions (CTE)](http://www.craigkerstiens.com/2013/11/18/best-postgres-feature-youre-not-using/). We use it frequently since it makes our long SQL queries much more readable than before.


## Monitoring ##
Monitoring can be further breakdown into several types. Below we shall further illustrate the types of monitoring we used to keep our system in check.

**Server Monitoring**  
Stackdriver (Google Cloud Monitoring) is our favorite choice for server monitoring. However, since Stackdriver is also limited to cloud servers, we can only use it to monitor all our servers in Google Cloud. For bare metal servers, we monitor it with Datadog.

One of the key things we look for in server monitoring solutions is the capability to monitor linux processes. Both Stackdriver and Datadog provides that capability, but Stackdriver allows you to monitor new process via their web UI while Datadog requires you to specify on your config file the type of process that you want to monitor. Datadog appoarch means that that if you want to monitor a new process (that wasn't monitored previously), you would need to re-deploy and restart datadog agent. When there are many servers to re-deploy the whole process gets painful.

![tech-stack-1](http://pirsquare.io/images/August-2015/tech-stack-1.gif)

Overall, we ranked our favorite server monitoring solutions in the following order:

1. Stackdriver
2. Datadog
3. Sever Density
4. New Relic



**Custom Metrics Monitoring**  
Librato
We use Librato to track over 400+ custom metrics. Some of the metrics that we track includes:

- RTB\_REQ\_RECEIVED
- RTB\_RESPONSE\_SUCCESS
- RTB\_RESPONSE\_ERROR
- RTB\_NOBID\_CPU\_THRESHOLD\_EXCEEDED
- RTB\_NOBID\_INVALID\_IMP\_TYPE
- RTB\_NOBID\_BID\_LESS\_THAN\_MINIMUM\_REQUIRED
- RTB\_NOBID\_BID\_LESS\_THAN\_BIDFLOOR
- RTB\_CREATIVES\_WHITELIST\_FILTERED
- RTB\_CREATIVES\_BLACKLIST\_FILTERED
- RTB\_CREATIVES\_INVENTORY\_FILTERED
- RTB\_PREDICTIONS\_TIMEOUT
- RTB\_PREDICTIONS\_ERROR

These metrics are important to us since it helps us to identify:

- Overview of system
- Hotspots
- Possible Bugs & Errors
- Opportunities for optimization


Logentries  
We use Logentries to monitor errors from server logs using pattern matching. An example would be to search for text `AEROSPIKE_ERR_CLIENT` to identify errors in aerospike connections. When logentries identifies the specified text pattern, it will sent an alert to our monitoring team and notify us the issue.



**Database Monitoring**  
Aerospike Monitoring Console (AMC)  
[AMC](http://www.aerospike.com/docs/amc/) is a web monitoring tool used to monitor aerospike servers. It provides you with an overview of your aerospike servers in near real-time snapshot and allows you to make configurations via the UI interface.


Pganalyze  
We use [Pganalyze](https://pganalyze.com/) to monitor our postgres database. 2 key things that we want to monitor:

- Overview of postgres database
- Slow running queries

Main reason why we use Pganalyze instead of a more comprehensive monitoring tool like New Relic is due to the cost savings. At $149/month/host, the cost of using New Relic to monitor our servers are even more expensive than hosting the server itself. Pganalyze offers a much more attractive pricing plan for us. To use Pganalyze with production plan, it would cost us a flat rate of $99/month.


## Others ##

**Load Balancing**  
For load balancing, we use Nginx, HAProxy and GCE Load Balancing. Nginx is used for HTTP/HTTPS load balancing while HAProxy is used for TCP Load Balancing. Since GCE Load Balancing is [dirt cheap](https://cloud.google.com/compute/docs/load-balancing/#pricing), we place it in front of our nginx/haproxy load balancers to load balance all our load balancers in Google Cloud. This way, we don't have to worry about setting up keepalived and can easily add more load balancing nodes when required.

![tech-stack-lb](http://pirsquare.io/images/August-2015/tech-stack-lb.png)

**Logging**  
Server logs gets written to syslog and than gets forwarded to logentries. We use Logentries for unified log management.


**Devops**  
[Ansible](http://www.ansible.com/), for it's simplicity and easy learning curve, is our choice for configuration management. One of the most worthwhile investment we have made is to ensure as much automation as we can in our delivery pipeline. This is turns out to be immensely useful as things were always moving fast and there were many days where we had to re-deploy our servers multiple times.


**CDN**  
[MaxCDN](https://www.maxcdn.com/). Most bigger players in the adtech use Akamai, but since their rates for smaller clients wasn't so interesting, MaxCDN is a good alternative for us. The good thing about MaxCDN is that unlike some other CDN vendors, they don't charge you on requests made. This works for us since all these request rate charges can easily burst our CDN's budget. MaxCDN also offers one of the lowest rates for dedicated SSL at $99/month with no setup fees.


**DNS**  
[Route53](https://aws.amazon.com/route53/). 


**Password Management**  
[Lastpass](https://lastpass.com/). I highly recommend everyone to use a password management tool. Don't let your login credentials get compromised by [irresponsible sites like Pastamania Delivery](http://pirsquare.io/blog/why-you-shouldnt-order-from-pastamania-delivery.html).



> Note: Some of the names or terms used in this article have been changed for illustration purposes

