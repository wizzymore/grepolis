from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
from random import randint
from selenium.webdriver.chrome.options import Options


###############
#SETTING UP THINGS
###############
print('################ GREPOLIS  BOT by WiiZZy')
username = input('Utilizator: ')
password = input('Parola: ')
selected_town = input('Numele orasului( 0 pentru a nu selecta un oras ): ')
towns_number = int(input('Numar de orase: '))
world_number = int(input('Lumea numarul: '))



##############
#INITIALIZARI
##############


building_names_romana = ["Senat", "Pestera", "Fabrica de Cherestea", "Cariera de Piatra", "Mina de Argint", "Piata", "Port", "Cazarma", "Zidul Orasului", "Depozit", "Ferma", "Academie", "Templu", "Terme", "Torre"]
building_names = ["main", "hide", "lumber", "stoner", "ironer", "market", "docks", "barraks", "wall", "storage", "farm", "academy", "temple", "terme", "torre"]

matrix_buildings_real = [[0 for i in range(15)] for i in range(towns_number)]

wood = 0
stone = 0
silver = 0
pop = 0

matrix_buildings = [
	[17, 10, 25, 25, 25, 10, 15, 10, 20, 25, 45, 30, 17, 0, 0],

	[17, 10, 20, 20, 21, 10, 15, 10, 20, 25, 45, 30, 17, 0, 0],

	[17, 10, 20, 20, 21, 10, 15, 10, 20, 25, 45, 30, 17, 0, 1],
]


err_senate = False



def rand_time():
	return (0.5 + randint(0, 15)/10)


def get_city_name(br):
	try:
		name = br.find_element_by_css_selector(".town_name").text
		return name
	except:
		print("Numele orasului nu a putut fi gasit.")
		enter_world(br)



def next_town(br):
	try:
		search = br.find_element_by_css_selector(".btn_next_town")
		search.click()
		search = br.find_element_by_css_selector(".btn_jump_to_town")
		search.click()
		print(get_city_name(br))
		print("Orasul a fost schimbat.")
		time.sleep(rand_time())
	except:
		print("Imposibil de schimbat orasul.")
		time.sleep(2)



def find_town(br):
	while(True):
		if(get_city_name(br) == selected_town or selected_town == '0'):
			print("Gasit!")
			break
		else:
			next_town(br)

def enter_world(br):
	try:
		search = br.find_elements_by_css_selector(".world_name")
		a = 0
		for i in search:
			if(a == world_number-1):#NUMERO DEL MONDO CHE COMPARE IN ORDINE NELLA SCHERMATA DOPO LOGIN
				i.click()
			a += 1
	except:
		print("Eroare la pornirea jocului..\nSe reincearca..")
		time.sleep(5)
		enter_world(br)


def login(br):
	try:
		#To fill out a form    ui-button-text
		search = br.find_element_by_name('login[userid]')
		search.send_keys(username)
		search = br.find_element_by_name('login[password]')
		search.send_keys(password)
		search = br.find_element_by_name("login[Login]")
		search.send_keys(Keys.RETURN)
		time.sleep(5)
	except:
		print("Eroare de autentificare..")
		time.sleep(5)
		#login(br)


def bonus_collector(br):
	try:
		search = br.find_element_by_css_selector(".js-tooltip-resources")
		search.click()
		time.sleep(5)
	except:
		print("Bonusul zilnic nu este disponibil.")


def view_town(br):
	try:
		search = br.find_element_by_css_selector(".city_overview div")
		search.click()
		print("Se vizualizeaza orasul")
		time.sleep(2)
	except:
		print("Vizualizarea orasului nu este posibila")

def view_island(br):
	try:
		search = br.find_element_by_css_selector(".island_view div")
		search.click()
		search = br.find_element_by_css_selector(".btn_jump_to_town div")
		search.click()
		print("Se vizualizeaza insula")
	except:
		print("Vizualizarea insulei nu este posibila")
	time.sleep(4)


def get_town_info(br):
	try:
			global wood
			wood = br.find_element_by_css_selector(".ui_resources_bar .wood .amount").text
			global stone
			stone = br.find_element_by_css_selector(".ui_resources_bar .stone .amount").text
			global silver
			silver = br.find_element_by_css_selector(".ui_resources_bar .iron .amount").text
			global pop
			pop = br.find_element_by_css_selector(".ui_resources_bar .population .amount").text
			print("Informatii despre oras:\n Lemn: " + wood + " | Piatra: "  + stone + " | Argint: "  + silver + " | Populatia: "  + pop + " " )
	except:
		print("Imposibil de gasit resursele orasului!")

def speed_construction(br):
	try:
		free = br.find_element_by_css_selector(".btn_time_reduction .type_free")
		free.click()
		print("Lista lucrarilor a fost accelerata")
		time.sleep(3)
	except:
		print("Nu se poate accelera lista lucrarilor")

def get_population(br):
	if int(pop) <= 20:
		print("Atentie, populatia are un numar scazut!")
		br.execute_script("BuildingMain.buildBuilding('farm', 20);")

	time.sleep(2)

def coda_edifici(br):
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	try:
		senate = br.find_element_by_xpath("//*[@id='building_main_area_main']")
		senate.click()
		print("Se vizualizeaza senatul.")
		err_senate = False
		time.sleep(2)
	except:
		print("Vizualizarea senatului nu este disponibila.")
		err_senate = True


	if(err_senate==False):
		buildings = br.find_elements_by_css_selector(".white")
		count_buildings = 0
		for build in buildings:
			matrix_buildings_real[n_city][count_buildings] = int(build.text)
			count_buildings += 1

		print (matrix_buildings[n_city])
		print (matrix_buildings_real[n_city])

		for num_building in range(0, 13):
			reale = matrix_buildings_real[n_city][num_building]
			ideale = matrix_buildings[n_city][num_building]
			if(reale < ideale):
				print("Cladirea "+ building_names_romana[num_building] +" subdezvoltata cu %d nivele" % (ideale-reale))
				comando_up = "BuildingMain.buildBuilding('"+building_names[num_building]+"', 50);"
				br.execute_script(comando_up)
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	print("Adaugarea constructiilor finalizata")
	time.sleep(5)

def farmer(br):
	villaggi = br.find_elements_by_xpath("//*[@data-same_island='true']")
	print("Am gasit %d sate." % len(villaggi))
	i = 0
	for villaggio in villaggi:
		print("Actionez in satul: " + str(i + 1))
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		time.sleep(rand_time()+1)
		search = br.find_elements_by_xpath("//*[@data-same_island='true']") #.owned
		a = -1
		for sc in search:
			a += 1
			if(a == i):
				try:
					sc.click()
				except:
					print("Nu se poate deschide panoul satului.")
				time.sleep(rand_time())
				try:
					ele = br.find_element_by_css_selector(".card_click_area")
					ele.click()
				except:
					print("Nu se pot colecta resursele.")
				time.sleep(rand_time())
				webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		i += 1
		time.sleep(rand_time())


def footer(br):
	end = time.time()
	print("Durata: " + str(int(end - start)))

	waiting_time = TEMPO - (int(end - start))*0.80
	if(waiting_time < 5):
			waiting_time = 5

	random_time = rand_time()*3.14+rand_time()*7/5 +rand_time()*19/7+20
	wait_time = int(waiting_time) + int(random_time)
	print("Urmatoarul ciclu in " + str(wait_time) + " secunde")
	y = 0.05
	z = 0
	for i in range(0, wait_time):
		if wait_time - int(wait_time*y) == wait_time - i:
			z+= 1
			y+= 0.05
		percent_done = 100 - int((wait_time - i)/wait_time * 100)
		print("Timp trecut["+ "▇" * z + " " *(20-z) + "] " + str(percent_done) + "%" + " " + str(wait_time - i) + " secunde", end="\r")
		

		time.sleep(1)
	print("-------------------------------------------------------------\n-------------------------------------------------------------\n")












TEMPO = 300    # 5 minute de pauza intre cicluri
#br = webdriver.Chrome()



#options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir=/home/kinder/.config/google-chrome") #Path to your chrome profile
br = webdriver.Chrome(executable_path="chromedriver.exe")




#start it up
print("Se deschide chrome....")
br.get("https://ro.grepolis.com/")
time.sleep(3)


login(br)
enter_world(br)
bonus_collector(br)

while(True):
	try:
		enter_world(br)
		find_town(br)
		start = time.time()
		
		for n_city in range(0, towns_number):


			print("Lucrez in orasul: "+get_city_name(br))

			view_town(br)
			get_town_info(br)
			speed_construction(br)
			get_population(br)
			coda_edifici(br)

			view_island(br)
			farmer(br)

			next_town(br)


		footer(br)
	except:
		print("Eroare bot!!!")
		login(br)
		time.sleep(30)
