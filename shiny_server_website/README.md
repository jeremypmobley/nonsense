
# Hosting a Shiny Server App on an AWS EC2 node

Below are steps to set up an R Shiny Server on an EC2 node.


Steps:  
1) Log into your AWS account.  Go to EC2 Service.  
![alt tag](https://github.com/jeremypmobley/shiny_server_website/blob/master/README_pics/AWS_services.PNG)  

2) Go to Instances -> Launch Instance  
![alt tag](https://github.com/jeremypmobley/shiny_server_website/blob/master/README_pics/Launch_instance.PNG)
 
3) Choose AMI of EC2 node  
![alt tag](https://github.com/jeremypmobley/shiny_server_website/blob/master/README_pics/Choose_AMI.PNG)  

4) Choose an Instance Type  
![alt tag](https://github.com/jeremypmobley/shiny_server_website/blob/master/README_pics/general_purpose_node.PNG)  
 * The default t2 micro should be fine to host a simple shiny server application  
	 * [Costs](https://aws.amazon.com/ec2/pricing/) $0.012 per Hour

5) Configure Instance  
 * Options for termination protection  
 * Options for requesting spot instances (not available for t2.micro)  

6) Add storage, tags - optional

7) Configure Security group

8) Launch

9) Connect


### OK, now we have an EC2 node! Now what?!

Necessary steps to set up R Shiny Server
Download R
Download R Shiny Server
Configure R Shiny Server



### Get static IP address

* Show options for how to assign static IP to EC2 node



### Get domain name



### Tie domain name to IP address
























