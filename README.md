# API-testing
test script and data for MG-RAST API tests

This script harvests example API calls from the MG-RAST
API at http://api.mg-rast.org/1, 
invokes them with curl, and compares the outputs to
previously saved outputs in the data directory. 

```bash
API-testing.py -t   # generates a list of the example API calls
```

This invokation runs tests and puts output in word directoery
genereates files 
```bash
API-testing.py -f -w work
```

```bash
f7f488249d0fbc943fa0c9ca27707a1c.call  # contains the URI
f7f488249d0fbc943fa0c9ca27707a1c.err   # HTTP headers
f7f488249d0fbc943fa0c9ca27707a1c.test  # judgement pass/fail
f7f488249d0fbc943fa0c9ca27707a1c.time  # time to return (s)
f7f488249d0fbc943fa0c9ca27707a1c.out   # output from API server
additionally, if the test fails, the script generates 
f7f488249d0fbc943fa0c9ca27707a1c.out1  and 
f7f488249d0fbc943fa0c9ca27707a1c.out2  
to facilitate debugging the differences.
```


# build & run


```bash
docker build -t mgrast/api-testing .
docker run -ti --rm --name api-testing mgrast/api-testing
```

