# Reducing Latency in Crypto Exchange Networks - A Focus on Binance

[toc]

## Teammates 

#### Zhicheng Tang

I am Zhicheng Tang, currently pursuing a Master's degree in Industrial Engineering at the University of Illinois at Urbana-Champaign. My university study covers math, statistics, computer science, economics and finance. I have practical experiences in data analysis, quantitative research, signal generating, machine learning, and arbitrage strategy development. I am proficient in multiple programming languages such as Python, C++, R, SQL and MATLAB. Presently, I am gaining hands-on experiences as a quant developer intern at a California-based hedge fund. Prior to this, I have had the opportunity to work with leading tech companies in China including Huawei, Baidu and Tencent.

Feel free to reach out to me through email aaront596@icloud.com or [LinkedIn](https://www.linkedin.com/in/zhichengtang/)

#### Harsh Agarwal

I am a senior majoring in Computer Science. I am passionate about software development, particularly developing low latency systems for use in finaicial markets. I am well versed with core software development tools including data structures, algorithms, system design, distributed systems, and computer architecture. You can find me here on LinkedIn - https://www.linkedin.com/in/harshagl2002/

#### Shruthik Musukula

I am Shruthik Musukula and I am a current Masters of Computer Science (MCS) student at the University of Illinois at Urbana-Champaign. I am particularly interested in the development of large-scale distributed systems, database systems, and cloud computing infrastructure, much of which is applicable to the high frequency trading world. I am proficient in Python, C/C++, and Java and have core experience working in a research setting as well as in the industry as a Software Engineering Intern at Salesforce, Inc.

Currently, I am looking for winter internship (Jan - May 2024) and new grad opportunities! Feel free to reach out to me at srm14@illinois.edu and connect with me on LinkedIn - https://www.linkedin.com/in/shruthikmusukula/.

#### Yihong Jin

I am Yihong Jin, a Master's student in Computer Engineering at the University of Illinois at Urbana-Champaign. I am interested in software engineering and have experience working in industry as a software development intern at Amazon Web Services.

I am proficient in Java, C/C++, and Go, and I am excited to leverage my skills to create highly available and scalable systems. My interests include infrastructure, distributed system and cloud computing.

Now I am looking for internship opportunities, especially for Software Development Engineer roles. If you would like to discuss any opportunities or have any inquiries, please feel free to reach out to me at yihongj3@illinois.edu.

## Project Overview

In this project, we focus on two key areas: firstly, automating AWS instance management, including initiation, termination, and storage, couldpled with wrapped APIs, latency testing, and analytics scripts. Secondly, we utilize the automated infrastructure to experiment with various hardware configurations, system settings, and AWS features, for example, Linux versions, kernel parameters and instance types. Additionally, we explored the potential benefits of using the new AWS placement group feature to collocated the instances within the same availability zone and region.

## Major Objectives

### Part 1: Automated Management of AWS Instances 

1. Automate the process of launching, terminating and storing instances. 
2. Build Binance API methods including fetching public market information, making orders and canceling orders.
3. Implement a script to run API methods, record and output the latency results.
4. Bootstrap the latency script when launching the instances.

### Part 2: Network Performance/Latency Improvement.

1. *Identify Optimal Hardware Combinations:* Research, evaluate, and test various EC2 network-optimized machine configurations to determine the most effective combination for reducing network latency in crypto exchange systems.
2. *OS Optimization:* Find out the best linux distribution version which provides the lowest network latency.
3. *Other AWS features:* Explore the latency improvements that can be achieved by leveraging the AWS specific features like availability zones and placement groups within the crypto exchange network infrastructure.



## Technologies, Hardware, and Frameworks

Our project is mainly written in Python (specifically compatible with Python v3.8 and above). For numerical anaysis and statistical test, we utilized industry-standard libraries such as Numpy and Pandas. Additionally, we wrapped API with different API libraries like `httpx`, `urllib` and `requests` to compare the difference of latencies.

Given that crypto exchanges are hosted on cloud servers, we decided to rely on AWS as the backbone of our infrastructure. To manage AWS resources effectively, we utilized the AWS SDK for Python (Boto3), streamlining the deployment of our latency reduction solutions. Our key AWS serivices includes EC2 and S3, ensuring real-time evaluation of network performance and data storage. Leveraging AWS's robust services, we amied to create an automated system that finds the combination of paramters to launch the best netowrk performance instances.

## Test Automation

There were two classes we defined, `EC2Manager` and `S3Manager`, to wrap up all the operations we need to automate the latency testing process. Some examples of such operations are launching instances, terminating instances, uploading files to S3 buckets and comparing the current results with the stored results.

Since we needed to launch a large number of instances to test different combinations of parameters, we automated the process of installing required packages and fetching testing scripts from S3 before initialization using a user-data script. After we finalized our tuning, we saved all the kernel configurations using an Amazon Machine Image (AMI) to avoid cumbersome shell scripts.

Each EC2 instance, when being launched, automatically runs the `latency_test_main.py` file to start running our latency testing suite. The script accepts multiple arguments such as testing time, API client, and other information like whether to keep alive and bind a process to a specific core. The script can be run manually on each machine or through the user-data script we created. Finally, the script uploads the latency results to the S3 bucket.

## Instance Search

There are two major goals of the instance search. First is to search for the best combination of parameters. Parameters searching process reads the configuration of the parameters we want to test and generate a combination of them. Then, it will run the latency test script and stop the instance. The second goal of the instance search is to find collocated instances. When starting an instance without specifying cluster placement id, AWS randomly selects an instance within an availability zone to start. Since we have no access to the exchange’s cluster placement id, we could randomly start and terminate instances lots of times, then we keep the instances that perform significantly better than the other instances, which are considered to be collocated. 

Once we find the instances that are collocated with the exchage's servers, everytime we want to launch a new instance, we could easily achieve collocation by implementing the cluster placement group with earlier launched instances.

## System Tuning

There were three major aspects to the system tuning implemented on each AWS instance created as part of a cluster. Each of these system modifications involved core changes to the Linux kernel configuration to decrease latency when tested against our API. 

- We modified `busy_read` and `busy_poll` timeouts on each machine. This controls the number of microseconds to wait for the socket layer to read packets on the device queue and the following wait time for future events. It reduces the latency on the network receive path.
- We configured each machine to not use deeper `C-states` in order to prevent time wasted from switching between sleep and wake states. 
- For multi-core instances, we disabled irqrebalance by default which forces CPUs to handle interrupts evenly, bound all network card interrupts to a specific core and made other cores dedicated to run the actual application. This approach helps in reducing competition for CPU resources, as the cores dedicated to the script won't be frequently interrupted for IRQ processing.

## API Improvement

Besides the above tuning, another notable improvement is the implementation of the keep-alive feature in API connections, for example, the utilization of requests’ session objects. It allows the reuse of TCP connections in subsequent requests to the same host, which reduces the overhead caused by establishing new connections for each request.

## Other AWS Parameters

AWS divides its regions into multiple availability zones (AZ) to ensure robustness. However, the network hops between different Availability Zones will increase. We test multiple availability zones and find out that Binance’s servers are located in Tokyo `zone-a`. The average latency is about 1.6 milliseconds lower than any other zones in the same region.

Another important parameter is the machine type. There are two reasons. The first reason is that AWS built the same types of machines in batches. Thus, the machines with the same type will be collocated with each other. Another more obvious reason is that machines with more CPU and memory capacity have lower latency. For example, C6a.2xlarge is 4 milliseconds faster than t2.micro without any tuning.

## Testing Results

To ensure a convinced comparision, we test the latency for a range of time and compare the difference of the average latencies. However, since we only have one Binance account, we can only test one instance at a time. Otherwise, the instance starts first will have better latency as the following instances API calls queue behind its. Thus, it introduces another uncontrolled factor. The general latency of the Binance API fluctuates because it depends on the market crowdness.

#### API Improvement

Without keeping TCP connections alive, the average latency of is 55.8 milliseconds.  After implementing TCP connections alive, the average latency is reduced to around 10 milliseconds level. This implementation has the most significant improvement, however, it's not part of the system tuning. It's code optimization. The later tuning will be conducted based on this improvement.

#### Availability Zone

This is another easy point to improve our strategy. We ran our latency test scripts for 24 hours on Tokto `zone-a`, `zone-c` and `zone-d` . We got 1.6 milliseconds fatser on `zone-a`. The relative improvement is 16.77%.

#### System Tuning

Due to the limit of time, Busy read, busy poll, ban deep c-states and IRQ allocation tuning has not been tested over 24 hours. Thus, the results have larger variance. However, combing all the tunings together we could have around 1.5 millisecons improvement, which is more significant. The relative improvement is 14.89%.

#### Operating System

Amazon Linux, Red Hat and Debian have relative the same latency, however, they're around 0.3 millisecond faster in average than Ubuntu on t2.micro instance type.

#### Instance Type

Due to the limit of budget, the instances we use for large amount of tests are t2.micro (free) and t2.medium (cheapest multi-core). We also compare the the latency of t2.micro with c6a.2xlarge. They're not in the same performance level, the result is not meaningful.

#### Collocated Instance Search

We ran the instance search script for 24 hours and each instance was ran for 1 hour. However, we didn't get an instance which has a significant lower latency compared with other random initiated instances. With the results of previous tests that lasted over 24 hours, we found that there was a maximum difference in latency of more than 3 milliseconds at different hours of the day. Thus, we need a much loger test time to eliminate this effect. Since we only have one binance account for testing, we plan to run this script for another 1 month and update the results.

## Appendix

- All the tests results will be plcaced in the [Latency-Test-Results](Latency-Test-Results) folder. Part of the above mentioned results, due to time limit, has not been tested for over 24 hours even longer time. It will be gradually updated in the following months.
- The detailed system tuning procedures and references will be placed in [Resources](Resources) folder.
