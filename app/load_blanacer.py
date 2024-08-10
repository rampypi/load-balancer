from abc import ABC, abstractmethod
import random
import threading

class ServerStrategy(ABC):
    
    @abstractmethod
    def get_next_server(self):
        raise NotImplementedError
    
class RoundRobin(ServerStrategy):
    def __init__(self):
        self.counter = 1
        self.lock = threading.Lock()
        
    def get_next_server(self, servers):
        if not servers:
            return "No servers available"
        with self.lock:
            server = servers[self.counter % len(servers)]
            self.counter += 1
            return server.name
    
    
class RandomServer(ServerStrategy):
    def __init__(self) -> None:
        self.lock = threading.Lock()

    def get_next_server(self, servers):
        if not servers:
            return "No servers available"
        with self.lock:
            num = random.randint(1, len(servers)-1)
        return servers[(num+1) % len(servers)].name


class Server:
    def __init__(self, urls, name):
        self.name = name
        self.max_url = 10
        self.urls = self.get_unique_first_ten_urls(urls)

  
    def get_unique_first_ten_urls(self, urls):
        result  = []
        for url in urls:
            if url not in result and len(result) < self.max_url:
                result.append(url)
        return result
        
    
    
    
class LoadBalancer:
    
    MAX_SERVER = 10
    
    def __init__(self, stratgey = RoundRobin):
        self.servers = []
        self.strategy = stratgey
        self.lock = threading.Lock()
        
    
    def add_servers(self, server: Server):
        if not server:
            return "Not a Valid server"
            
        with self.lock:
            if len(self.servers) < self.MAX_SERVER:
                self.servers.append(server)
                return "Return Server Added Successfully"
        return "Max Server limit Reached"
    
    def get_next_server(self):
       
        return self.strategy.get_next_server(servers=self.servers)
    
    
        
