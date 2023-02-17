import requests
from bs4 import BeautifulSoup
import csv


def main():
    brand = "AUDI"
    year_max = 2023
    year_min = 2000
    km_max = 500000
    km_min = 0
    energy = "ess"
    price_min = 0
    price_max = 300000
    results = []
    for page_num in range(1, 20):
        url = f"https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}&options=&page={page_num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        search_cards = soup.find_all(class_="searchCard")

        for search_card in search_cards:
            price = search_card.find(
                class_="Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
            brand = search_card.find(
                class_="Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2")
            motor = search_card.find(
                class_="Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2")
            year = search_card.find(
                class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")
            km = search_card.find_all(
                class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[1]
            energy = search_card.find_all(
                class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[3]
            price_int = int(price.text.replace(" ", "").replace("€", ""))
            year_int = int(year.text)
            mileage_int = int(km.text.replace("\xa0", "").replace("km", ""))
            model_ = " ".join(brand.text.split()[1])

            results.append(
                [brand.text, model_, motor.text, str(year_int),
                 str(mileage_int), energy.text, str(price_int)])

    with open("audi.csv", "a", newline="") as fd:
        writer = csv.writer(fd, delimiter=",")
        writer.writerow(
            ["Brand", "Model", "Motor", "Year",
             "Km", "Energy", "Price"])
        writer.writerows(results)

if __name__ == "__main__":
    main()