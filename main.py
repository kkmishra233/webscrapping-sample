import requests
from bs4 import BeautifulSoup


def get_products_urls(url):
    # Send a GET request to the URL
    response = requests.get(url)

    PRODUCT_URL_list=[]
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        products_list = soup.find('ul', class_='ProductListingResults__productList ProductListingResults__productList--space--top')

        if products_list:
            # Find all li elements within the ul element
            products = products_list.find_all('li',class_="ProductListingResults__productCard")

            # Traverse and print the text content of each li element
            for product in products:
                product_card_div=product.find('div',class_="ProductCard")
                product_link_a=product_card_div.find("a",class_="Link_Huge Link_Huge--secondary")
                PRODUCT_URL=product_link_a["href"]

                PRODUCT_URL_list.append(PRODUCT_URL)
        else:
            print('No products_list found.')
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')
    
    return PRODUCT_URL_list

def get_product_information(url):
    response = requests.get(url)
    information_dict={"Product URL":"",
                          "Product Name":"",
                          "Product Description":"",
                          "Product Price":"",
                          "Overall Ratings":"",
                          "Total no of Reviews/Feedback":"",
                          "Top 50 Review/Feedbacks":{"Review Date":"","Review Country":"","Verified Purchase Flag":"","Review Text":""}
                          }
    information_dict["Product URL"]=url

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_div = soup.find('div', class_='ProductHero').find("div",class_="ProductHero__content")
        
        product_name=product_div.find("div",class_="ProductInformation").find("h1",class_="Text-ds Text-ds--body-1 Text-ds--left").find("span",class_="Text-ds Text-ds--title-5 Text-ds--left").get_text(strip=True)
        information_dict["Product Name"]=product_name
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

    return information_dict

if __name__=="__main__":
    urls= get_products_urls("https://www.ulta.com/brand/dyson")
    for url in urls:
        information=get_product_information(url=url)
        print(information)