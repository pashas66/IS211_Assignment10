#IS211_Assignment10
#import the required libraries 

import logging
import sqlite3

def query_db():
#here we are connecting it to the databse in pets.db
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()

    #here we load up the data below by constructing appropriate INSERT commands
    sql_query = """
    SELECT 
    person.first_name AS 'PersonFirst',
    person.last_name AS 'PersonLast',
	person.age AS 'PersonAge', 
	pet.name AS 'PetName',
    pet.breed AS 'PetBreed',
    pet.age AS 'PetAge',
    pet.dead AS 'PetDead',
    person_pet.person_id AS 'PersonID',
    person_pet.pet_id AS 'PetID'
    FROM person_pet
	JOIN person ON person_pet.person_id = person.id
    JOIN pet ON person_pet.pet_id = pet.id;
    """

    cursor.execute(sql_query)
    query_result = cursor.fetchall()
    header = [i[0] for i in cursor.description]

    return [header, query_result]

def value_getter(dict, key, tup):
#this is a simple key getter.

    index = dict[key]

    return tup[index]

def print_person_info(tup_info):
# here we are printing a function that prints the persons name and age.

    (name, age) = tup_info

    print(f"{name}, {age} years old") #Print out data of the person

def print_pet_owner_details(owner, pet_details):
#here we printing a function that prints the owner and the pet details.

    print(f"{owner} {pet_details}")

def print_results(query_result, key_dict):
#here we are printing a function that triggers printing results.

    head = query_result[0]

    person_name = f"{value_getter(key_dict, 'PersonFirst', head)} {value_getter(key_dict, 'PersonLast', head)}"
    person_age = f"{value_getter(key_dict, 'PersonAge', head)}"

    print_person_info((person_name, person_age))

    for pet in query_result:
        #Print out all the data on that person’s pets
        pet_info = f"owned {value_getter(key_dict, 'PetName', pet)}, a {value_getter(key_dict, 'PetBreed', pet)}, that was {value_getter(key_dict, 'PetAge', pet)} years old."
        print_pet_owner_details(person_name, pet_info)
    
def find_person(query_results, keys_dict, user_input):
#here we have a function that loops over the query_results and filters the list with the personId keyed in by the query user. 
    person_id = keys_dict['PersonID']
    filtered_list = filter(lambda x: x[person_id] == user_input, query_results)

    return list(filtered_list)

def get_keys(header_list):
#this is a utility function that creates an index dictionary for key/value lookup.

    config_fields = [
        'PersonFirst',
        'PersonLast',
        'PersonAge',
        'PetName',
        'PetBreed',
        'PetAge',
        'PetDead',
        'PersonID',
        'PetID'
    ]

    return { k:header_list.index(k) for k in config_fields }


def safe_int_checker(int_str):
#this is a function that checks if the string is actually an integer
    try:
        num = int(int_str)
        return (True, num)
    except ValueError:
        return (False, None)

def print_error(num):
#here we have print function that prints out an error when a user keys in a non numerical key. 

    print(f'Sorry the personId of {num} does not exist')
    logging.error(f'Error processing <{num}>')

def main():

    logging.basicConfig(filename='errors.log',
                        level=logging.ERROR, format='%(message)s')
    logging.getLogger('assignment10')

    CLI = True 

    while CLI:
        keyed = input('\nPlease enter a numerical ID\n') #here we ask the user for a person’s ID number
        (is_int, cast_num) = safe_int_checker(keyed)
    #Keep doing this until the user enters in a ­-1, which is an indication to exit the program
        if is_int and cast_num > -1 :
            db_query = query_db()
            [header, db_data] = db_query
            header_index_dict = get_keys(header)
            plucked_values = find_person(db_data, header_index_dict, cast_num)

            print_error(cast_num) if not plucked_values else print_results(plucked_values, header_index_dict)

        elif is_int == False:
            print('It looks like you entered a non-numerical key, please enter in a numerical key')
            logging.error(f'Error processing <{keyed}>')

        else:
            CLI = False
            print('CLI Exiting....')
            SystemExit

if __name__ == '__main__':
    main() #calling the main function

    #end of the code

#Question:
#What is the purpose of the person_pettable?
#the purpose is to use both Person and Pet data as once in a form of dataset to join them by their unique Id,