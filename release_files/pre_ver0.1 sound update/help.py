print("welcome to my list thingy")

password = "your mom"
while True:
	guess = input("type in password: ")
	if guess == password:
		break

# here, we are going to make the list
anime_list = [] # this creates an empty list

# next, we are gonna make a loop where we ask the user what it wants to do
while True:
	choice = input("What do you want to do?")

	# now we're gonna make all the different choices
	if choice == "add":
		name = input("Whats the name of the Anime? ")
		# now we're gonna add the name to the list using the "append" method.
		anime_list.append(name)
		# now we just let the user know its added
		print("Anime added!")

	if choice == "see":
		# now we loop through all the items inside the list, and assign the "i" variable to the item
		# the word after for can be whatever you want, its like writing anime = ...
		for anime in anime_list:
			# for every anime in the list, print it out
			print("- ", anime) # now with some styling

	if choice == "quit":
		break

	if choice == "delete":
		# we'll just print all the items in the list again, so the use knows what to delete
		for anime in anime_list:
			# for every anime in the list, print it out
			print("- ", anime) # now with some styling


		# we have to get the "index" if the list item, meaning we have to get its place in the list
		anime = input("What anime do you want to remove? ")

		# we dont need this line
		# anime_to_delete = anime_list.index(anime)

		#now we remove that item from the list
		anime_list.remove(anime)

		print("Removed ", anime, " from the list!")
		#thats it
