import requests


def ping():
    """A simple health check endpoint to confirm whether the API is up and running."""
    response = requests.get("https://restful-booker.herokuapp.com/ping")
    return response


def get_bookingids(firstname="", lastname="", checkin="", checkout=""):
    """Returns the ids of all the bookings.
    Can take optional query strings to search and return a subset of booking ids """
    varlist = [firstname, lastname, checkin, checkout]
    url = "https://restful-booker.herokuapp.com/booking?"
    for i in varlist:
        print(i)
        if i:
            if i == firstname:
                url = url + "firstname=" + i + "&"
            if i == lastname:
                url = url + "lastname=" + i + "&"
            if i == checkin:
                url = url + "checkin=" + i + "&"
            if i == checkout:
                url = url + "checkout=" + i + "&"
    response = requests.get(url=url.format())
    return response


def get_booking(booking_id):
    """Returns a specific booking based upon the booking id provided"""
    response = requests.get(url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id))
    return response


def create_booking(updates):
    """Creates a new booking in the API"""
    response = requests.post(url="https://restful-booker.herokuapp.com/booking", json=updates
                             )
    return response


def create_token(uname, passw):
    """Creates a new auth token to use for access to the PUT and DELETE /booking"""
    response = requests.post(url="https://restful-booker.herokuapp.com/auth",
                             data={"username": uname, "password": passw})
    return response


def update_booking(booking_id, updates):
    """Updates a current booking with a partial payload"""
    response = requests.put(
        url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id),
        json=updates,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def partial_update(booking_id, updates):
    """Updates a current booking with a partial payload"""
    response = requests.patch(
        url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id),
        json=updates,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def delete_booking(booking_id):
    """Deletes booking with given id"""
    response = requests.delete(
        url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id),
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


class Tests:
    def test_ping(self):
        """healthcheck test"""
        assert ping().status_code == 201

    def test_get_bookingids(self):
        """get_bookingids test without arguments"""
        assert get_bookingids().status_code == 200

    def test_get_bookingids_fname(self):
        """get_bookingids test with one argument"""
        booking1 = create_booking(updates={'firstname': 'Januszek', 'lastname': 'Kowalski', 'totalprice': 212,
                                           'depositpaid': True,
                                           'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                           'additionalneeds': 'dinner'}).json()['bookingid']
        booking = get_bookingids(firstname="Januszek")
        assert booking.status_code == 200
        assert booking.json()[0]['bookingid'] == booking1
        delete_booking(booking1)

    def test_get_bookingids_fandlname(self):
        """get_bookingids test with two arguments"""
        create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                'depositpaid': True,
                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                'additionalneeds': 'dinner'})
        assert get_bookingids(firstname="Jan", lastname="Kowalski").status_code == 200

    def test_get_bookingids_fname_empty(self):
        """get_bookingids test with empty firstname value"""
        create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                'depositpaid': True,
                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                'additionalneeds': 'dinner'})
        assert get_bookingids(firstname="").status_code == 200

    def test_get_bookingids_checkin(self):
        """get_bookingids test with checkin value greater than in argument"""  # in documentation is greater and equal
        create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                'depositpaid': True,
                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                'additionalneeds': 'dinner'})
        assert get_bookingids(checkin="2021-01-01").status_code == 200

    def test_get_bookingids_checkin_year(self):
        """get_bookingids test with only year in checkin value"""
        create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                'depositpaid': True,
                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                'additionalneeds': 'dinner'})
        assert get_bookingids(checkin="2021").status_code == 200

    def test_get_bookingids_checkin_incorrect(self):
        """get_bookingids test with incorrect checkin value"""
        create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                'depositpaid': True,
                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                'additionalneeds': 'dinner'})
        assert get_bookingids(checkin="20").status_code == 500

    def test_get_bookingids_checkin_empty(self):
        """get_bookingids test with empty checkin value"""
        create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                'depositpaid': True,
                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                'additionalneeds': 'dinner'})
        assert get_bookingids(checkin="").status_code == 200

    def test_get_bookings_id(self):
        """get_booking with correct id value"""
        booking = get_bookingids().json()[0]['bookingid']
        assert get_booking(booking).status_code == 200

    def test_get_bookings_badid(self):
        """get_booking with incorrect id value"""
        assert get_booking(0).status_code == 404

    def test_create_booking_correct_value(self):
        """create_booking with correct values"""
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'})
        assert booking.status_code == 200
        assert booking.json()['booking'] == {'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                             'depositpaid': True,
                                             'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                             'additionalneeds': 'dinner'}

    def test_create_booking_no_additional(self):
        """create_booking with correct values without key 'additionalneeds'"""
        booking = create_booking(updates={'firstname': 'Janusz', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'}})
        assert booking.status_code == 200
        assert booking.json()['booking'] == {'firstname': 'Janusz', 'lastname': 'Kowalski', 'totalprice': 212,
                                             'depositpaid': True,
                                             'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'}}

    def test_create_booking_incorrect_value(self):
        """create_booking with incorrect 'firstname' type"""
        assert create_booking(updates={'firstname': 1, 'lastname': 'Kowalski', 'totalprice': 212,
                                       'depositpaid': True,
                                       'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                       'additionalneeds': 'dinner'}).status_code == 500

    def test_create_booking_empty_value(self):
        """create_booking with incorrect 'firstname' type"""
        assert create_booking(updates={'firstname': None, 'lastname': 'Kowalski', 'totalprice': 212,
                                       'depositpaid': True,
                                       'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                       'additionalneeds': 'dinner'}).status_code == 500

    def test_create_token_correct(self):
        """create_token with correct admin and password values"""
        token = create_token("admin", "password123")
        assert token.status_code == 200

    def test_create_token_incorrect(self):
        """create_token with incorrect admin and password values"""
        token = create_token("admi", "assword123")
        assert token.status_code == 200  # bad creditentials should give 4XX status code
        assert token.json() == {'reason': 'Bad credentials'}

    def test_create_token_empty(self):
        """create_token with empty admin and password values"""
        assert create_token("", "").json() == {'reason': 'Bad credentials'}

    def test_update_booking_correct(self):
        """update_booking with correct values"""
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()['bookingid']
        assert update_booking(booking, updates={'firstname': 'Henry', 'lastname': 'Kowalski', 'totalprice': 212,
                                                'depositpaid': False,
                                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                                'additionalneeds': 'no bed'}).status_code == 200

    def test_update_booking_lack_of_values(self):
        """update_booking with no 'depositpaid' value"""
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()['bookingid']
        assert update_booking(booking, updates={'firstname': 'Henry', 'lastname': 'Kowalski', 'totalprice': 212,
                                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                                'additionalneeds': 'no bed'}).status_code == 400

    def test_update_booking_incorrect_id(self):
        """update_booking with incorrect id"""
        assert update_booking(0, updates={'firstname': 'Henry', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': False,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'no bed'}).status_code == 405

    def test_update_booking_incorrect_values(self):
        """update_booking with incorrect values"""
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()['bookingid']
        assert update_booking(booking, updates={'firstname': True, 'lastname': 123, 'totalprice': 'Ham',
                                                'depositpaid': 'money',
                                                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                                'additionalneeds': 'no bed'}).status_code == 500

    def test_delete_booking(self):
        """delete_booking with correct id"""
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()['bookingid']
        assert delete_booking(booking).status_code == 201

    def test_delete_booking_incorrect_id(self):
        """delete_booking with incorrect id"""
        assert delete_booking(0).status_code == 405

    def test_partial_update_booking_correct(self):
        """partial_update with correct values"""
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()
        assert partial_update(booking['bookingid'], updates={'firstname': 'Jan'}).status_code == 200

    def test_partial_update_booking_incorrect(self):
        """partial_update with incorrect values"""  # bug, it can update with types different than intended
        booking = create_booking(updates={'firstname': 'Jan', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()
        assert partial_update(booking['bookingid'], updates={'firstname': 2, 'depositpaid': 3}).status_code == 200
