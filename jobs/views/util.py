from django.core.paginator import Paginator

eu_countries = ["Netherlands", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                    "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                    "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                    "Iceland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Russia", "Serbia", "Slovakia", 
                    "Ukraine", "Slovenia", "Belarus", "Bosnia and Herzegovina", "Moldova", "Montenegro",
                    "San Marino", "Vatican City", "Liechtenstein", "Albania","Kosovo", "Monaco", "North Macedonia", "Andorra"]

categories = ["Software Development", "Data & AI", "Hardware", "Cybersecurity", "IT & Support"]


""" Returns a paginator object for the given jobs """
def get_page_obj(jobs, page_num=1):
    paginator = Paginator(jobs, 15)
    return paginator.get_page(page_num)
