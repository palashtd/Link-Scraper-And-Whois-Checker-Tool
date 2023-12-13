from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import Link
import whois21
import log21
from django.contrib import messages
from .models import WhosBanner, ScraperBanner

# ------------------Link Scraper------------------------


def scraper(request):
    # Get request from form
    if request.method == "POST":
        try:
            site = request.POST.get('site', '')
            # Filter or condition that URL do not start with these.
            if not site.startswith(('http://', 'https://', 'www',)):
                raise ValueError(
                    "Invalid URL. Please enter a valid URL starting with 'http://' or 'https://' or with 'www'.")
            # Apply link scraping logic
            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string
                if link_text and link_address != None:
                    Link.objects.create(
                        address=link_address, name=link_text)
            return redirect('scraper')
        except (ValueError, TypeError) as e:
            return render(request, 'scraper/link_scraper.html', {'error_message': str(e)})
    else:
        data = Link.objects.all()
        sc_banner = ScraperBanner.objects.all()
    return render(request, 'scraper/link_scraper.html', {'data': data, 'sc_banner': sc_banner})

# -----------------Clear Data----------------


def clear(request):
    link = Link.objects.all()
    link.delete()
    return redirect('scraper')

# -------------------Whois Tool-----------------------------


def domain_info(request):
    # Get data from WhosBanner model.
    ws_banner = WhosBanner.objects.first()
    # Get request from from
    if request.method == 'POST':
        query = request.POST.get('domain_name', '')
        # Preprocess the domain name: strip common prefixes
        # Exclude start with
        prefixes = ['http://', 'https://', 'https://www', 'www.']
        domain_name = query
        for prefix in prefixes:
            if domain_name.startswith(prefix):
                domain_name = domain_name[len(prefix):]
        # Get data from domain
        whois = whois21.WHOIS(domain_name)

        if not whois.success:
            messages.error(request, 'Failed to fetch WHOIS information.')
            return redirect('domain_info')

        creation_date = whois.whois_data.get('CREATION DATE', '')
        registrant_name = whois.whois_data.get('REGISTRANT NAME', '')
        updated_date = whois.whois_data.get('UPDATED DATE', '')
        expiry_date = whois.whois_data.get('REGISTRY EXPIRY DATE', '')
        name_servers = whois.whois_data.get('NAME SERVER', [])

        return render(
            request,
            'whos/who_info.html',
            {
                'creation_date': creation_date,
                'registrant_name': registrant_name,
                'updated_date': updated_date,
                'expiry_date': expiry_date,
                'name_servers': name_servers,
                'whois': whois,
                'ws_banner': ws_banner
            }
        )

    return render(request, 'whos/who_info.html')
