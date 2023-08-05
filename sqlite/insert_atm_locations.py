# insert_atm_locations.py

import sqlite3

def insert_atm_locations():
    conn = sqlite3.connect('data/banking.db')
    cursor = conn.cursor()

    # Sample ATM locations data
    atm_locations_data = [
         (33.7490, -84.3880, 'Peachtree Plaza', '123 Peachtree St NE, Atlanta, GA'),
        (33.7749, -84.2963, 'Centennial Park', '456 Marietta St NW, Atlanta, GA'),
        (33.7537, -84.3880, 'Georgia Aquarium', '789 Luckie St NW, Atlanta, GA'),
        (33.7574, -84.3963, 'CNN Center', '101 Marietta St NW, Atlanta, GA'),
        (33.7550, -84.3880, 'World of Coca-Cola', '888 W Peachtree St NW, Atlanta, GA'),
        (33.7645, -84.4013, 'Mercedes-Benz Stadium', '222 Martin Luther King Jr Dr NW, Atlanta, GA'),
        (33.7513, -84.3911, 'The Tabernacle', '333 Luckie St NW, Atlanta, GA'),
        (33.7683, -84.3933, 'State Farm Arena', '444 Parker St NW, Atlanta, GA'),
        (33.7704, -84.3911, 'Georgia State University', '555 Courtland St NE, Atlanta, GA'),
        (33.7491, -84.3911, 'Underground Atlanta', '666 Upper Alabama St SW, Atlanta, GA'),
        (33.7515, -84.3880, 'Woodruff Park', '777 Peachtree St NE, Atlanta, GA'),
        (33.7727, -84.3845, 'The Varsity', '888 Spring St NW, Atlanta, GA'),
        (33.7531, -84.3880, 'AmericasMart', '999 Peachtree St NE, Atlanta, GA'),
        (33.7625, -84.3943, 'Centennial Olympic Park', '111 Baker St NW, Atlanta, GA'),
        (33.7581, -84.3892, 'Tabernacle', '222 Luckie St NW, Atlanta, GA'),
        (33.7730, -84.3911, 'Rialto Center for the Arts', '333 Auburn Ave NE, Atlanta, GA'),
        (33.7525, -84.3963, 'College Football Hall of Fame', '444 Marietta St NW, Atlanta, GA'),
        (33.7724, -84.3862, 'Hard Rock Cafe', '555 Courtland St NE, Atlanta, GA'),
        (33.7700, -84.3963, 'SkyView Atlanta', '666 West Peachtree St NW, Atlanta, GA'),
        (33.7492, -84.3880, 'Hilton Atlanta', '777 Courtland St NE, Atlanta, GA')
    ]

    # Insert ATM locations into the table
    cursor.executemany('INSERT INTO atm_locations (latitude, longitude, bank_name, address) VALUES (?, ?, ?, ?)',
                       atm_locations_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_atm_locations()
