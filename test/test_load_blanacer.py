"""

1. Implement a simple load balancer that can handle up to 10 server instances.
2.The load balancer should be able to accept a list of server URLs during initialization.
3. Ensure that duplicates are removed from the list, and if there are more than 10 URLs, only the first 10 are used.
4. The load balancer should support two strategies for distributing requests: round robin and random.
"""


import unittest

from app.load_blanacer import LoadBalancer, RandomServer, RoundRobin, Server

class TestLoadBalancer(unittest.TestCase):
   
    def test_add_single_server_to_load_balancer(self):
       load_balancer =  LoadBalancer()
       server = Server(urls=["url1"], name="Server1")
       load_balancer.add_servers(server)
       self.assertEqual(len(load_balancer.servers), 1)
       
    def test_add_breach_server_limit_load_balancer(self):
        load_balancer =  LoadBalancer()
        server = Server(urls=["url1"], name="Server1")
        for _ in range(110):
            result = load_balancer.add_servers(server)
            
        self.assertEqual(result, "Max Server limit Reached")
        self.assertEqual(len(load_balancer.servers), 10)
        
        
    def test_accept_single_server_with_multiple_urls(self):
        load_balancer =  LoadBalancer()
        server = Server(urls=["url1", "url2", "url3"], name="Server1")
        load_balancer.add_servers(server)
        self.assertEqual(len(load_balancer.servers), 1)
        
    def test_accept_list_of_multiple_server_wit_multiple_urls(self):
        load_balancer =  LoadBalancer()
        for i in range(10):
            server = Server(urls=["url1", "url2", "url3"], name=f"Server {i}")
            load_balancer.add_servers(server)
        
        self.assertEqual(len(load_balancer.servers), 10)
        
    def test_accept_list_of_max_server_wit_multiple_urls(self):
        load_balancer =  LoadBalancer()
        for i in range(100):
            server = Server(urls=["url1", "url2", "url3"], name=f"Server {i}")
            result = load_balancer.add_servers(server)
        
        self.assertEqual(result, "Max Server limit Reached")
        self.assertEqual(len(load_balancer.servers), 10)
        
    def test_accept_one_server_wit_duplicate_urls(self):
        server = Server(urls=["url1", "url1", "url3"], name="Server1")
        self.assertEqual(len(server.urls), 2, "Unique server urls validation Failed")
        
    def test_accept_one_server_wit_hundred_urls(self):
        url_list = [f"url {i}" for i in range(100)]
        server = Server(urls=url_list, name="Server1")
        self.assertEqual(len(server.urls), 10, "Unique server urls validation Failed")
        server_urls = [url for url in server.urls]
        first_ten_url = [f"url {i}" for i in range(10)]
        self.assertEqual(server_urls, first_ten_url, "Not getting first 10 Url")
    
    def test_get_next_instance_round_robin_startegy(self):
        load_balancer =  LoadBalancer(RoundRobin())
        for i in range(10):
            load_balancer.add_servers(Server(urls=["url1", "url2", "url3"], name=f"Server {i}"))
        
        servers = [f"Server {i}" for i in range(10)]
        for i in range(1, 10):
            self.assertEqual(load_balancer.get_next_server(), servers[i % 10])
        

    def test_get_next_instance_random_startegy(self):
        load_balancer =  LoadBalancer(RandomServer())
        for i in range(10):
            load_balancer.add_servers(Server(urls=["url1", "url2", "url3"], name=f"Server {i}"))
        
        self.assertTrue(load_balancer.get_next_server(),  "Random stratgey Fails")
        
        