import requests
import json
import random
import pandas as pd

NUM_ENTRIES = 1000

def generate_random_locations(num_entries):
    url = f'https://randomuser.me/api/?results={num_entries}&nat=us'
    response = requests.get(url)

    if (response.status_code == 200):
        data = response.json()
        states = []
        cities = []

        for n in range(num_entries):
            cities.append(data["results"][n]["location"]["city"])
            states.append(data["results"][n]["location"]["state"])

        return (states, cities)
    else:
        print(f"Error: {response.status_code}")

def generate_random_bool():
    options = (True, False)
    return random.choice(options)

def generate_random_links_data():
    links = ['link1', 'link2', 'link3', 'link4']
    clicked = []
    converted = []

    for i in range(len(links)):
        cl = generate_random_bool()
        co = False
        if (cl):
            co = generate_random_bool()
        clicked.append(cl)
        converted.append(co)
    
    data = {}
    for i in range(len(links)):
        data.update({links[i]: {'clicked': clicked[i], 'converted': converted[i]}})

    return data

def generate_random_visits(num_entries):

    visits = {}
    states, cities = generate_random_locations(num_entries)
    
    for i in range(num_entries):
        visits[f'visit{i}'] = {'state': states[i],
                       'city': cities[i],
                       'clicked_links': generate_random_links_data()}
    return visits

def getData(num_entries):
    visits = generate_random_visits(num_entries)
    count_clicked = [0] * 4
    count_converted = [0] * 4
    for i in range(num_entries):
        for j in range(4):
            if (visits[f'visit{i}']['clicked_links'][f'link{j+1}']['clicked']):
                count_clicked[j] += 1
            if (visits[f'visit{i}']['clicked_links'][f'link{j+1}']['converted']):
                count_converted[j] += 1
                
    click_through_rate = {
        'ctr_1': count_clicked[0] / num_entries,
        'ctr_2': count_clicked[1] / num_entries,
        'ctr_3': count_clicked[2] / num_entries,
        'ctr_4': count_clicked[3] / num_entries,
        'ctr_total': sum(count_clicked) / num_entries
    }

    conversion_rate = {
        'ctr_1': count_converted[0] / num_entries,
        'ctr_2': count_converted[1] / num_entries,
        'ctr_3': count_converted[2] / num_entries,
        'ctr_4': count_converted[3] / num_entries,
        'ctr_total': sum(count_converted) / num_entries
    }    

    data = {'visits': visits,
            'click_through_rate': click_through_rate,
            'conversion_rate': conversion_rate}
    return data

def getCSV(data):
    states = []
    cities = []
    links_data = [[[], []], [[], []], [[], []], [[], []]]
    for i in range(NUM_ENTRIES):
        states.append(data['visits'][f'visit{i}']['state'])
        cities.append(data['visits'][f'visit{i}']['city'])
        links_data[0][0].append(data['visits'][f'visit{i}']['clicked_links']['link1']['clicked'])
        links_data[0][1].append(data['visits'][f'visit{i}']['clicked_links']['link1']['converted'])
        links_data[1][0].append(data['visits'][f'visit{i}']['clicked_links']['link2']['clicked'])
        links_data[1][1].append(data['visits'][f'visit{i}']['clicked_links']['link2']['converted'])
        links_data[2][0].append(data['visits'][f'visit{i}']['clicked_links']['link3']['clicked'])
        links_data[2][1].append(data['visits'][f'visit{i}']['clicked_links']['link3']['converted'])
        links_data[3][0].append(data['visits'][f'visit{i}']['clicked_links']['link4']['clicked'])
        links_data[3][1].append(data['visits'][f'visit{i}']['clicked_links']['link4']['converted'])
    
    CSVdata = pd.DataFrame({
        'states': states,
        'citites': cities,
        'link1_clicked': links_data[0][0],
        'link1_converted': links_data[0][1],
        'link2_clicked': links_data[1][0],
        'link2_converted': links_data[1][1],
        'link3_clicked': links_data[2][0],
        'link3_converted': links_data[2][1],
        'link4_clicked': links_data[3][0],
        'link4_converted': links_data[3][1],
    })

    csv_filename = 'generateRandomData/output.csv'
    CSVdata.to_csv(csv_filename, index=False)


if __name__ == "__main__":
    data = getData(NUM_ENTRIES)
    with open('generateRandomData/output.json', 'w') as file:
        json.dump(data, file)
    print("done writing json")

    getCSV(data)
    print("done writing csv")
