# Import necessary modules
import pytest
from brainboost_data_source_search.CompanyDomainSearchEngineService import CompanyDomainSearchEngineService
from brainboost_data_source_search.EmailSearchEngineService import EmailSearchEngineService
import dns.resolver

# Define the fixture to provide instances of CompanyDomainSearchEngineService and EmailSearchEngineService
@pytest.fixture
def search_instance():
    return {
        'companies': CompanyDomainSearchEngineService(),
        'email': EmailSearchEngineService()
    }


def test_get_company_domain_for_company_and_country(search_instance):
    # Define test cases for getting company domains
    test_cases = [
        
        ("Louis Vuitton", "louisvuitton.es","Spain"),
        ("Sony", "sony.jp","Japan"),
        ("Alibaba", "alibaba.cn","China")
    ]

    for company_name, expected_domain,country in test_cases:
        result_domain = search_instance['companies'].search(company_name=company_name,country=country)
        assert result_domain == expected_domain



# Test cases with modified fixture usage
def test_get_company_domain_for_company(search_instance):
    # Define test cases for getting company domains
    test_cases = [
        ("Tesla", "tesla.com"),
        ("Harvard University", "harvarduniversity.com"),
        ("BBC", "bbc.com"),
        ("Greenpeace", "greenpeace.com"),
        ("Louis Vuitton", "louisvuitton.com"),
        ("Sony", "sony.com"),
        ("Alibaba", "alibaba.com"),
        ("Kogan Page","koganpage.com")
    ]

    for company_name, expected_domain in test_cases:
        result_domain = search_instance['companies'].search(company_name=company_name)
        assert result_domain == expected_domain

def test_domain_exists(search_instance):
    # Test domain existence for various domains
    assert search_instance['companies'].domain_exists("google.com") == True
    assert search_instance['companies'].domain_exists("tesla.io") == True
    assert search_instance['companies'].domain_exists("tesla.com") == True
    assert search_instance['companies'].domain_exists("tesla.cum") == False
    assert search_instance['companies'].domain_exists("example.invalid") == False

def test_get_email_enabled(search_instance):
    # Test email availability for domains
    assert search_instance['email'].get_email_enabled("google.com") == True
    assert search_instance['email'].get_email_enabled("tesla.com") == True
    assert search_instance['email'].get_email_enabled("google.cum") == False
    assert search_instance['email'].get_email_enabled("example.invalid") == False

def test_get_domain_extensions(search_instance):
    # Test source domain extension for countries
    assert search_instance['companies'].get_domain_extensions_for_country("United States") == ".com"
    assert search_instance['companies'].get_domain_extensions_for_country("Germany") == ".de"
    assert search_instance['companies'].get_domain_extensions_for_country("Unknown Country") is None
