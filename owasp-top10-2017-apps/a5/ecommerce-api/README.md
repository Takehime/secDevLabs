# Vulnerable Ecommerce API
> This is a simple Golang web application that contains an example of a Broken Access Control vulnerability.

<img src="images/example-api.png" align="center"/>

## What is Broken Access Control?

Definition from [OWASP](https://www.owasp.org/images/7/72/OWASP_Top_10-2017_%28en%29.pdf.pdf):

Restrictions on what authenticated users are allowed to do are often not properly enforced. Attackers can exploit these flaws to access unauthorized functionality and/or data, such as access other users' accounts, view sensitive files, modify other users’ data, change access rights, etc.

## Requirements

To build this lab you will need [Docker][Docker Install] and [Docker Compose][Docker Compose Install].

## Deploy and Run

After cloning this repository, you can type the following command to start the vulnerable application:

```sh
$ make install
```

## Available routes

* GET /healthcheck
```
$ curl http://localhost:8888/healthcheck
WORKING
```

* POST /register
```
$ curl -s -H "Content-Type: application/json" -d '{"username":"rafael","password":"password"}' http://localhost:8888/register
Register: success!
```

* POST /login
```
$ curl -s -H "Content-Type: application/json" -d '{"username":"rafael","password":"password"}' http://localhost:8888/login
Hello, rafael! This is your userID: 2b53f961-85fe-4988-99b4-c90481ed54ef
```

* GET /ticket/:id
```
$ curl http://localhost:8888/ticket/2b53f961-85fe-4988-99b4-c90481ed54ef
Hey, rafael! This is your ticket: rafael-08e8805f-422b-477b-8565-b0876b89da17
```

## Attack Narrative

(SPOILER) To understand how this vulnerability can be exploited, check this section!

## Mitigating the vulnerability

(SPOILER) To understand how this vulnerability can be mitigated, check this other section!

[Docker Install]:  https://docs.docker.com/install/
[Docker Compose Install]: https://docs.docker.com/compose/install/

## Contributing

Yes, please. :zap:
