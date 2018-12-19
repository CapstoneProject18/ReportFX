from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse

from . import views

class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    #=================
    # Test build flow
    #=================
    
    def test_view_url_Step1(self):
        response = self.client.get('/Step1',{'type': 'gaming' , 'price': '1000'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_Step2(self):
        response = self.client.get('/Step2',{'CPU' : '1'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_Step3(self):
        response = self.client.get('/Step3',{'CPU':'1' , 'GPU' : '1'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_Step4(self):
        response = self.client.get('/Step4',{'CPU' : '1' , 'GPU': '1' , 'RAM' : '0'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_Step5(self):
        response = self.client.get('/Step5',{'CPU' : '1' , 'GPU': '1' , 'RAM' : '0', 'STORAGE' : '1'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_Step6(self):
        response = self.client.get('/Step6',{'CPU' : '1' , 'GPU': '1' , 'RAM' : '0', 'STORAGE' : '1' , 'MB' : '2'} )
        self.assertEquals(response.status_code, 200)

    #==================
    # Test CPU details
    #==================
    
    def test_view_url_cpu_details_graph_1(self):
        response = self.client.get('/cpu_details' , {'graph' : '1'} )
        self.assertEquals(response.status_code, 200)
    
    def test_view_url_cpu_details_graph_2(self):
        response = self.client.get('/cpu_details' , {'graph' : '2'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_3(self):
        response = self.client.get('/cpu_details' , {'graph' : '3'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_4(self):
        response = self.client.get('/cpu_details' , {'graph' : '4'} )
        self.assertEquals(response.status_code, 200)
    
    def test_view_url_cpu_details_graph_5(self):
        response = self.client.get('/cpu_details' , {'graph' : '5'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_6(self):
        response = self.client.get('/cpu_details' , {'graph' : '6'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_7(self):
        response = self.client.get('/cpu_details' , {'graph' : '7'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_8(self):
        response = self.client.get('/cpu_details' , {'graph' : '8'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_9(self):
        response = self.client.get('/cpu_details' , {'graph' : '9'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_10(self):
        response = self.client.get('/cpu_details' , {'graph' : '10'} )
        self.assertEquals(response.status_code, 200)

    def test_view_url_cpu_details_graph_11(self):
        response = self.client.get('/cpu_details' , {'graph' : '11'} )
        self.assertEquals(response.status_code, 200)
    
    #==========================
    # Test motherboard details
    #==========================

    def test_view_url_motherboard_details(self):
        '''
        Tests the webpage motherboard_details for all possible graphs
        '''
        for i in range(1, 7):
            self.is_motherboard_details_graph_ok(i)
    
    def is_motherboard_details_graph_ok(self, graph_num):
        '''
        Test the webpage motherboard_details for a specific graph.

        Arguments:
          graph_num: The graph number to test
        '''
        response = self.client.get('/motherboard_details' , {'graph' : str(graph_num)})
        self.assertEquals(response.status_code, 200)
