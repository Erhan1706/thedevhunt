from django.core.paginator import Paginator

eu_countries = ["Netherlands", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                    "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                    "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                    "Iceland", "Latvia", "Lithuania", "Luxembourg", "Russia", "Serbia", "Slovakia", 
                    "Ukraine", "Slovenia", "Belarus", "Moldova", "Albania",]

categories = ["Software Development", "Data & AI", "Hardware", "Cybersecurity", "IT & Support"]


""" Returns a paginator object for the given jobs """
def get_page_obj(jobs, page_num=1):
    paginator = Paginator(jobs, 15)
    return paginator.get_page(page_num)
