import urllib.request
from bs4 import BeautifulSoup
from PIL import Image
from tkinter import Tk, Label, Button
import requests
import pprint
import secrets
import os

class RarityUnknown(Exception):
    """Raised in this program when an unhandled rarity is encountered"""

pp = pprint.PrettyPrinter(indent=4)
#rng.randrange(n, m)
rng = secrets.SystemRandom()


def stitch_packs(file1, file2, file3, file4, file5, file6, file7, file8, file9):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    image3 = Image.open(file3)
    image4 = Image.open(file4)
    image5 = Image.open(file5)
    image6 = Image.open(file6)
    image7 = Image.open(file7)
    image8 = Image.open(file8)
    image9 = Image.open(file9)

    image1 = image1.resize((476, 695))
    image2 = image2.resize((476, 695))
    image3 = image3.resize((476, 695))
    image4 = image4.resize((476, 695))
    image5 = image5.resize((476, 695))
    image6 = image6.resize((476, 695))
    image7 = image7.resize((476, 695))
    image8 = image8.resize((476, 695))
    image9 = image9.resize((476, 695))

    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size
    (width5, height5) = image5.size
    (width6, height6) = image6.size
    (width7, height7) = image7.size
    (width8, height8) = image8.size
    (width9, height9) = image9.size


    result_width = width1 + width2 + width3
    result_height = height1 + height4 + height7
    result = Image.new('RGB', (result_width, result_height))

    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    result.paste(im=image3, box=(width1 + width2, 0))
    result.paste(im=image4, box=(0, height1))
    result.paste(im=image5, box=(width4, height2))
    result.paste(im=image6, box=(width4 + width5, height3))
    result.paste(im=image7, box=(0, height1 + height4))
    result.paste(im=image8, box=(width7, height2 + height5))
    result.paste(im=image9, box=(width7 + width8, height3 + height6))

    if not os.path.exists("results"):
        os.makedirs("results")

    result.save("results/composite_image.png")

    return "composite_image.png"

def get_card_image(generated_pack):

    for card_count, card_name in enumerate(generated_pack, start=0):

        url = "http://yugioh.wikia.com/wiki/" + card_name
        code = requests.get(url)
        text = code.text
        soup = BeautifulSoup(text, "lxml")
        wiki_images = soup.findAll('img')
        image_url_lowres = wiki_images[21].attrs.get("src")
        image_url = image_url_lowres.split(sep="/scale")[0]
        pp.pprint(image_url)

        urllib.request.urlretrieve(image_url, "file_" + str(card_count) + ".png")

    return 0

def get_names(url):
    #Getting webpage
    code = requests.get(url)
    #I asssume pulling only text out
    text = code.text
    #turning the text into a soup object
    soup = BeautifulSoup(text, "lxml")
    #Finding all strong tags and putting them in a bs4 resultset, which behaves like a list
    all_strong_tags = soup.findAll('strong')
    #seperating each instance of a strong tag into an entry in a list
    strong_tag_list = []

    for t in all_strong_tags:
        strong_tag_list.append(t)

    #Remove 2 junk entries used for other things
    all_strong_tags.pop(0)
    all_strong_tags.pop(0)

    card_name_list = []
    card_rarity_list = []


    #Iterating through all strong tags, to find and link rarities to names
    for tag in all_strong_tags:
        #moving up one level from the strong tag
        current = tag.parent

        #if true, than this element has a rarity above common
        if bool(current.find("img")):
            card_rarity_list.append(current.find("img").get('alt', ''))
            card_name_list.append(tag.text)
            #put current strong_tag name into dictionary with the rare tag name

        #if false than this element has a common rarity
        elif not bool(current.find("img")):
            card_rarity_list.append("Common")
            card_name_list.append(tag.text)
            #put current strong_tag name into dictionary with some kind of indicator of no tag

    """
    Old code, functionality absorbed into above for statement
    
    Remove all tag info, and leave just plaintext strings in the card_names list
    card_names = []
    for number in strong_tag_list:
        card_names.append(number.text)
    """

    #combining list of names with list of rarities
    card_names_and_rarities = [card_name_list, card_rarity_list]
    
    return card_names_and_rarities

def get_sets():
    #boilerplate code to get the database of yu-gi-oh sets of packs from konami's site
    code = requests.get("https://www.db.yugioh-card.com/yugiohdb/card_list.action?request_locale=en")
    text = code.text
    soup = BeautifulSoup(text, "lxml")

    #The way i'm finding the sets gives me one junk entry for every set entry, so I find the number of entries and divide by two to get the true number
    number_of_sets = int((len(soup.findAll('th'))) / 2)
    #List of sets of packs
    all_sets_list = []
    """
    Data structure:
    all_sets_list       [0]         [0]             [0]
                    set select     0 = select       Nothing
                    set select     1 = packs        specific pack
                    set select     2 = ids          specific id
    
    """

    #iterate through the sets and put them in the list
    for element in range(number_of_sets):
        set_data = []
        set_name = []
        pack_name = []
        url_of_packs = []
        #(element * 2) + 1 specifies which element to append, the magic numbers select only the odd numbers which contain actual data
        set_name.append(soup.findAll('th')[(element * 2) + 1].text)

        #find number of strong tags, I need a number because I am manipulating two different things on each loop
        current_set = soup.findAll('th')[(element * 2) + 1].parent.parent.parent.parent
        num_of_packs_in_set = len(current_set.findAll("strong"))


        for pack_index in range(num_of_packs_in_set):
            #Each pack gets appended to the packs list
            pack_name.append(current_set.findAll("strong")[pack_index].text)
            #And then the specific id of the pack gets put into the id_of_packs list
            pack_link = current_set.find_all("input", class_="link_value")[pack_index].get("value")
            pack_id = pack_link.partition("pid=")[2].partition("&rp")[0]
            pack_id = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&pid=" + pack_id + "&rp=99999"
            url_of_packs.append(pack_id)


        set_data.append(set_name)
        set_data.append(pack_name)
        set_data.append(url_of_packs)

        all_sets_list.append(set_data)

    return all_sets_list

def generate_pack(card_list):
    #finding total number of cards in the given pack
    card_num_total = int(len(card_list[0]))

    common_list = []
    rare_list = []
    super_rare_list = []
    ultra_rare_list = []
    secret_rare_list = []

    #going through the pack, and popping element zero of both the name a rarity, and then sorting it into the proper rarity list as just the name
    for card_num in range(card_num_total):
        temp_rarity = card_list[1].pop(0)
        temp_name = card_list[0].pop(0)

        if temp_rarity == "Common" or temp_rarity == "Starfoil":
            common_list.append(temp_name)
        elif temp_rarity == "Rare":
            rare_list.append(temp_name)
        elif temp_rarity == "Super Rare":
            super_rare_list.append(temp_name)
        elif temp_rarity == "Ultra Rare":
            ultra_rare_list.append(temp_name)
        elif temp_rarity == "Secret Rare":
            secret_rare_list.append(temp_name)
        else:
            raise RarityUnknown(temp_rarity, "Unknown rarity encountered in this pack")

    generated_pack = []

    if len(common_list) >= 7 and len(rare_list) >= 1 and len(super_rare_list) >= 1 or len(ultra_rare_list) >= 1 or len(secret_rare_list) >= 1:

        #Packs contain 7 commons, a rare, and a foil
        #The pops ensure that the same card will never be added to any one pack twice. No idea if that is how it actually works
        for common_card_nums in range(7):
            number_of_commons = int(len(common_list)) - 1
            generated_pack.append(common_list.pop(rng.randrange(0, number_of_commons)))

        number_of_rares = int(len(rare_list)) - 1
        generated_pack.append(rare_list.pop(rng.randrange(0, number_of_rares)))

        foil_chance = rng.randrange(0, 100)
        if 1 <= foil_chance <= 8:
            number_of_secret_rares = int(len(secret_rare_list)) - 1
            generated_pack.append(secret_rare_list.pop(rng.randrange(0, number_of_secret_rares)))
        elif 9 <= foil_chance <= 24:
            number_of_ultra_rares = int(len(ultra_rare_list)) - 1
            generated_pack.append(ultra_rare_list.pop(rng.randrange(0, number_of_ultra_rares)))
        elif 25 <= foil_chance <= 100:
            number_of_super_rares = int(len(super_rare_list)) - 1
            generated_pack.append(super_rare_list.pop(rng.randrange(0, number_of_super_rares)))

        #16% for ultra rare, 8% for secret rare, 76% for super rare
        #1-8 for secret rare, 9-24 for ultra rare, 25-100 for super rare

    elif len(common_list) >= 9:
        for common_card_nums in range(9):
            number_of_commons = int(len(common_list)) - 1
            generated_pack.append(common_list.pop(rng.randrange(0, number_of_commons)))

    return generated_pack

'''
sets  = get_sets()

for count, set in enumerate(sets, start = 1):
    print(count, ":", set[0][0])

user_set_selection = int(input("Please select a number of a set."))

for pack_count, pack in enumerate(sets[user_set_selection - 1][1], start = 1):
    print(pack_count, ":", pack)

user_pack_selection = int(input("Please select a number of a pack."))

set_name = sets[user_set_selection - 1][0][0]
pack_name = sets[user_set_selection - 1][1][user_pack_selection - 1]
pack_url = sets[user_set_selection - 1][2][user_pack_selection - 1]

print("Set Name:", set_name)
print("Pack Name:", pack_name)
print("Url:", pack_url)

card_list = get_names(pack_url)

generated_pack = generate_pack(card_list)

pp.pprint(generated_pack)

get_card_image(generated_pack)

print(stitch_packs("file_0.png", "file_1.png", "file_2.png", "file_3.png", "file_4.png", "file_5.png", "file_6.png", "file_7.png", "file_8.png"))
'''

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Yu-gi-oh pack generator")

def greet():
    print("Greetings!")

def func_generate_pack(sets, set_number, pack_number):
    card_list = get_names(sets[set_number][2][pack_number])
    generated_pack = generate_pack(card_list)
    get_card_image(generated_pack)
    stitch_packs("file_0.png", "file_1.png", "file_2.png", "file_3.png", "file_4.png", "file_5.png", "file_6.png", "file_7.png", "file_8.png")

def set_button_clicked(sets, count):
    #return sets[count][0][0]
    return count

def pack_button_clicked(sets, count):
    return count

def delete_buttons(button_list):
    for element in button_list:
        element.destroy()

def pack_selection_gui(sets, count, button_list):
    selected_set = set_button_clicked(sets, count)
    delete_buttons(button_list)

    pack_button_list = []

    button = Button(root, text="Back to main", command=lambda: set_selection_gui(sets, pack_button_list))
    pack_button_list.append(button)
    button.pack()

    for pack_count, pack in enumerate(sets[selected_set][1], start=0):

        button = Button(root, text=pack, command=lambda y=count: selected_pack_gui(sets, count, y, pack_button_list))
        pack_button_list.append(button)
        button.pack()

def selected_pack_gui(sets, set_number, pack_number, button_list):
    delete_buttons(button_list)

    pack_option_button_list = []

    button = Button(root, text="Back to main", command=lambda: set_selection_gui(sets, pack_option_button_list))
    pack_option_button_list.append(button)
    button.pack()
    button = Button(root, text="Generate pack", command=lambda: func_generate_pack(sets, set_number, pack_number))
    pack_option_button_list.append(button)
    button.pack()

def set_selection_gui(sets, button_list):
    delete_buttons(button_list)
    set_button_list = []

    for count, set in enumerate(sets, start=0):
        button = Button(root, text=set[0][0], command=lambda x=count: pack_selection_gui(sets, x, set_button_list))
        set_button_list.append(button)
        button.pack()


sets  = get_sets()
root = Tk()
my_gui = MyFirstGUI(root)

set_selection_gui(sets, [])

root.mainloop()


"""
To do: 
need to figure out how to do the stitching more dynamically, 9 attributs is already too many, structure packs need something more robust for sure

find edge cases in generator function
star pack battle royal, hobby god cards
Fusion enforcers, no commons

Use konami site and figure out how to pick card packs and retain years/pack in the list of links. 
pack selection gui
Then either upload to dropbox or maybe to imgur through their api
"""


#testTEsttestTEST